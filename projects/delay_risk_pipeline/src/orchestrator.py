from __future__ import annotations

from typing import Dict, List, Tuple

from router.dispatch import choose_branch
from router.strategy import Strategy

from decision_engine import assess_risk_from_packets
from llm_reasoner import build_prompt, call_llm_with_retry
from execution_plan import ExecutionPlan
import time


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

# def run_full_assessment(fact_packets: List[str]) -> Dict:
#     # Deterministic, safe routing input (temporary until user_query is wired in)
#     routing_input = " ".join(fact_packets[:3])

#     try:
#         strategy = choose_branch(routing_input)
#     except Exception:
#         strategy = Strategy.GENERAL

#     # --- ANALYTICS ONLY ---
#     if strategy == Strategy.ANALYTICS:
#         deterministic_result = _run_deterministic(fact_packets)
#         return {
#             "deterministic_layer": deterministic_result,
#             "llm_layer": None,
#             "inconsistencies": [],
#             "confidence": "HIGH",
#             "consistency_ratio": 1.0,
#             "strategy": strategy.value,
#         }

#     # --- HYBRID (POLICY / SUMMARY / GENERAL) ---
#     deterministic_result = _run_deterministic(fact_packets)
#     llm_result = _run_llm(fact_packets)

#     inconsistencies, consistency_ratio, confidence = _cross_check(deterministic_result, llm_result)

#     return {
#         "deterministic_layer": deterministic_result,
#         "llm_layer": llm_result,
#         "inconsistencies": inconsistencies,
#         "confidence": confidence,
#         "consistency_ratio": consistency_ratio,
#         "strategy": strategy.value,
#     }

def _build_execution_plan(strategy: Strategy) -> ExecutionPlan:
    if strategy == Strategy.ANALYTICS:
        return ExecutionPlan(
            run_deterministic=True,
            run_llm=False,
            run_cross_check=False,
        )

    if strategy == Strategy.SUMMARY:
        return ExecutionPlan(
            run_deterministic=False,
            run_llm=True,
            run_cross_check=False,
        )

    if strategy == Strategy.POLICY:
        return ExecutionPlan(
            run_deterministic=True,
            run_llm=True,
            run_cross_check=True,
        )

    # GENERAL fallback
    return ExecutionPlan(
        run_deterministic=True,
        run_llm=True,
        run_cross_check=True,
    )

def run_full_assessment(fact_packets: List[str]) -> Dict:
    # Deterministic, safe routing input (temporary until user_query is wired in)
    routing_input = " ".join(fact_packets[:3])

    try:
        strategy = choose_branch(routing_input)
    except Exception:
        strategy = Strategy.GENERAL

    # # --- ANALYTICS: deterministic only ---
    # if strategy == Strategy.ANALYTICS:
    #     deterministic_result = _run_deterministic(fact_packets)
    #     return {
    #         "deterministic_layer": deterministic_result,
    #         "llm_layer": None,
    #         "inconsistencies": [],
    #         "confidence": "HIGH",
    #         "consistency_ratio": 1.0,
    #         "strategy": strategy.value,
    #     }

    # # --- SUMMARY: LLM only ---
    # if strategy == Strategy.SUMMARY:
    #     llm_result = _run_llm(fact_packets)
    #     return {
    #         "deterministic_layer": None,
    #         "llm_layer": llm_result,
    #         "inconsistencies": [],
    #         "confidence": "MEDIUM",
    #         "consistency_ratio": None,
    #         "strategy": strategy.value,
    #     }

    # # --- POLICY: hybrid with governance ---
    # if strategy == Strategy.POLICY:
    #     deterministic_result = _run_deterministic(fact_packets)
    #     llm_result = _run_llm(fact_packets)

    #     inconsistencies, consistency_ratio, confidence = _cross_check(
    #         deterministic_result, llm_result
    #     )

    #     return {
    #         "deterministic_layer": deterministic_result,
    #         "llm_layer": llm_result,
    #         "inconsistencies": inconsistencies,
    #         "confidence": confidence,
    #         "consistency_ratio": consistency_ratio,
    #         "strategy": strategy.value,
    #     }

    # # --- GENERAL: safe hybrid default ---
    # deterministic_result = _run_deterministic(fact_packets)
    # llm_result = _run_llm(fact_packets)

    # inconsistencies, consistency_ratio, confidence = _cross_check(
    #     deterministic_result, llm_result
    # )

    # return {
    #     "deterministic_layer": deterministic_result,
    #     "llm_layer": llm_result,
    #     "inconsistencies": inconsistencies,
    #     "confidence": confidence,
    #     "consistency_ratio": consistency_ratio,
    #     "strategy": strategy.value,
    # }


    plan = _build_execution_plan(strategy)

    deterministic_result = None
    llm_result = None
    inconsistencies = []
    consistency_ratio = None
    confidence = None

# --- Execute Plan ---
    # if plan.run_deterministic:
    #     deterministic_result = _run_deterministic(fact_packets)

    # Even mofre pro style to measure the run time. 
    deterministic_ms = None
    llm_ms = None

    start_total = time.perf_counter()

    if plan.run_deterministic:
        start = time.perf_counter()
        deterministic_result = _run_deterministic(fact_packets)
        deterministic_ms = (time.perf_counter() - start) * 1000

##### later we added following. More pro. If no need to LLM not even call him save tome and money


    # --- Early Exit Optimization ---
    if (
        plan.run_llm
        and deterministic_result
        and all(
            item["risk_level"] == "LOW"
            for item in deterministic_result.get("assessments", [])
        )
    ):
        # Skip LLM — deterministic result sufficient
        llm_result = None
        confidence = "HIGH"
        consistency_ratio = 1.0

        total_ms = (time.perf_counter() - start_total) * 1000

        return {
            "strategy": strategy.value,
            "execution_plan": {
                "run_deterministic": plan.run_deterministic,
                "run_llm": False,  # skipped
                "run_cross_check": False,
            },
            "deterministic_layer": deterministic_result,
            "llm_layer": None,
            "inconsistencies": [],
            "confidence": confidence,
            "consistency_ratio": consistency_ratio,
            "metrics": {
                "deterministic_ms": deterministic_ms,
                "llm_ms": None,
                "total_ms": total_ms,
            },
        }



    if plan.run_llm:
        start = time.perf_counter()
        llm_result = _run_llm(fact_packets)
        llm_ms = (time.perf_counter() - start) * 1000

    total_ms = (time.perf_counter() - start_total) * 1000

    if plan.run_llm:
        llm_result = _run_llm(fact_packets)

    if plan.run_cross_check and deterministic_result and llm_result:
        inconsistencies, consistency_ratio, confidence = _cross_check(
            deterministic_result, llm_result
        )
    elif plan.run_deterministic and not plan.run_llm:
        confidence = "HIGH"
    elif plan.run_llm and not plan.run_cross_check:
        confidence = "MEDIUM"

    # return {
    #     "deterministic_layer": deterministic_result,
    #     "llm_layer": llm_result,
    #     "inconsistencies": inconsistencies,
    #     "confidence": confidence,
    #     "consistency_ratio": consistency_ratio,
    #     "strategy": strategy.value,
    # }
##################################################
    ### This is better! why we will understand what plan was chosen:
    # by seeing the final output ------------> Better monitoring human involvement"
    return {
    "strategy": strategy.value,
    "execution_plan": {
        "run_deterministic": plan.run_deterministic,
        "run_llm": plan.run_llm,
        "run_cross_check": plan.run_cross_check,
    },
    "deterministic_layer": deterministic_result,
    "llm_layer": llm_result,
    "inconsistencies": inconsistencies,
    "confidence": confidence,
    "consistency_ratio": consistency_ratio,

    "metrics": {
    "deterministic_ms": deterministic_ms,
    "llm_ms": llm_ms,
    "total_ms": total_ms,
}
}