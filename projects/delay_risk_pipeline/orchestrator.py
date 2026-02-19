from typing import List, Dict

from decision_engine import assess_risk_from_packets
from llm_reasoner import (
    build_prompt,
    # call_llm,
    # parse_llm_output,
    # validate_decision_schema,
    call_llm_with_retry
)


# def run_full_assessment(fact_packets: List[str]) -> Dict:
#     """
#     Orchestrates:
#     1) Deterministic signal assessment
#     2) LLM reasoning
#     3) Schema validation
#     """

#     deterministic_result = assess_risk_from_packets(fact_packets)

#     prompt = build_prompt(fact_packets)
#     raw = call_llm(prompt)
#     parsed = parse_llm_output(raw)
#     validated = validate_decision_schema(parsed)

#     return {
#         "deterministic_layer": deterministic_result,
#         "llm_layer": validated,
#     }



# def run_full_assessment(fact_packets: List[str]) -> Dict:

#     deterministic_result = assess_risk_from_packets(fact_packets)

#     prompt = build_prompt(fact_packets)
#     llm_result = call_llm_with_retry(prompt)

#     return {
#         "deterministic_layer": deterministic_result,
#         "llm_layer": llm_result,
#     }


def run_full_assessment(fact_packets: List[str]) -> Dict:

    deterministic_result = assess_risk_from_packets(fact_packets)

    prompt = build_prompt(fact_packets)
    llm_result = call_llm_with_retry(prompt)


    # Cross-check
    deterministic_projects = {
        item["fact_packet"]: item["risk_level"]
        for item in deterministic_result["assessments"]
    }

    inconsistencies = []

    for proj in llm_result["projects"]:
        project_id = proj["project_id"]

        # Find matching packet
        for packet, det_risk in deterministic_projects.items():
            if f"Project: {project_id}" in packet:
                if proj["risk"] != det_risk:
                    inconsistencies.append({
                        "project_id": project_id,
                        "deterministic_risk": det_risk,
                        "llm_risk": proj["risk"],
                    })

    # return {
    #     "deterministic_layer": deterministic_result,
    #     "llm_layer": llm_result,
    #     "inconsistencies": inconsistencies,
    # }
    consistency_ratio = 1.0
    total = len(llm_result["projects"])

    if total > 0:
        consistency_ratio = 1 - (len(inconsistencies) / total)

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


