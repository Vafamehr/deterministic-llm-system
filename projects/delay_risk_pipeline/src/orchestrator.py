from typing import List, Dict

from decision_engine import assess_risk_from_packets
from llm_reasoner import build_prompt, call_llm_with_retry


def run_pipeline(fact_packets: List[str]) -> Dict:
    """
    Public entrypoint for the system.
    Keep this name stable; internals can evolve.
    """
    return run_full_assessment(fact_packets)


def run_full_assessment(fact_packets: List[str]) -> Dict:
    deterministic_result = assess_risk_from_packets(fact_packets)

    prompt = build_prompt(fact_packets)
    llm_result = call_llm_with_retry(prompt)

    # Cross-check deterministic vs LLM outputs
    deterministic_projects = {
        item["fact_packet"]: item["risk_level"]
        for item in deterministic_result["assessments"]
    }

    inconsistencies = []
    for proj in llm_result.get("projects", []):
        project_id = proj.get("project_id")

        for packet, det_risk in deterministic_projects.items():
            if project_id and f"Project: {project_id}" in packet:
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

    return {
        "deterministic_layer": deterministic_result,
        "llm_layer": llm_result,
        "inconsistencies": inconsistencies,
        "confidence": confidence,
        "consistency_ratio": consistency_ratio,
    }