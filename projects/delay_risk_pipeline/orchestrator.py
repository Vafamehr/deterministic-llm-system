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



def run_full_assessment(fact_packets: List[str]) -> Dict:

    deterministic_result = assess_risk_from_packets(fact_packets)

    prompt = build_prompt(fact_packets)
    llm_result = call_llm_with_retry(prompt)

    return {
        "deterministic_layer": deterministic_result,
        "llm_layer": llm_result,
    }

