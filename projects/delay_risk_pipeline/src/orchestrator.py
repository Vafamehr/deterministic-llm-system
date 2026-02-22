from __future__ import annotations

from typing import Dict, List, Tuple

from router.dispatch import choose_branch
from router.strategy import Strategy

from decision_engine import assess_risk_from_packets
from llm_reasoner import build_prompt, call_llm_with_retry


def run_pipeline(fact_packets: List[str]) -> Dict:
    """
    Public entrypoint for the system.
    Keep this name stable; internals can evolve.
    """
    return run_full_assessment(fact_packets)


# ------------------------------------------------------------
# Internal helpers (keep orchestrator composable)
# ------------------------------------------------------------

def _run_deterministic(fact_packets: List[str]) -> Dict:
    return assess_risk_from_packets(fact_packets)


def _run_llm(fact_packets: List[str]) -> Dict:
    prompt = build_prompt(fact_packets)
    return call_llm_with_retry(prompt)


def _cross_check(deterministic_result: Dict, llm_result: Dict) -> Tuple[List[Dict], float, str]:
    """
    Compare deterministic vs LLM project risks.
    Returns: (inconsistencies, consistency_ratio, confidence)
    """
    deterministic_projects = {
        item["fact_packet"]: item["risk_level"]
        for item in deterministic_result.get("assessments", [])
    }

    inconsistencies: List[Dict] = []

    for proj in llm_result.get("projects", []):
        project_id = proj.get("project_id")
        if not project_id:
            continue

        for packet, det_risk in deterministic_projects.items():
            if f"Project: {project_id}" in packet:
                if proj.get("risk") != det_risk:
                    inconsistencies.append(
                        {
                            "project_id": project_id,
                            "deterministic_risk": det_risk,
                            "llm_risk": proj.get("risk"),
                        }
                    )

    total = len(llm_result.get("projects", []))
    consistency_ratio = 1.0 if total == 0 else 1 - (len(inconsistencies) / total)

    confidence = "HIGH"
    if consistency_ratio < 1.0:
        confidence = "MEDIUM"
    if consistency_ratio < 0.5:
        confidence = "LOW"

    return inconsistencies, consistency_ratio, confidence


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def run_full_assessment(fact_packets: List[str]) -> Dict:
    # Deterministic, safe routing input (temporary until user_query is wired in)
    routing_input = " ".join(fact_packets[:3])

    try:
        strategy = choose_branch(routing_input)
    except Exception:
        strategy = Strategy.GENERAL

    # --- ANALYTICS ONLY ---
    if strategy == Strategy.ANALYTICS:
        deterministic_result = _run_deterministic(fact_packets)
        return {
            "deterministic_layer": deterministic_result,
            "llm_layer": None,
            "inconsistencies": [],
            "confidence": "HIGH",
            "consistency_ratio": 1.0,
            "strategy": strategy.value,
        }

    # --- HYBRID (POLICY / SUMMARY / GENERAL) ---
    deterministic_result = _run_deterministic(fact_packets)
    llm_result = _run_llm(fact_packets)

    inconsistencies, consistency_ratio, confidence = _cross_check(deterministic_result, llm_result)

    return {
        "deterministic_layer": deterministic_result,
        "llm_layer": llm_result,
        "inconsistencies": inconsistencies,
        "confidence": confidence,
        "consistency_ratio": consistency_ratio,
        "strategy": strategy.value,
    }