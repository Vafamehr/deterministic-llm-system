from typing import Dict, List


def assess_risk_from_packets(fact_packets: List[str]) -> Dict:
    """
    Deterministic reasoning stub.
    No LLM yet.
    Looks at delay_rate or volatility hints inside text.
    """

    results = []

    for packet in fact_packets:
        risk_flag = "LOW"

        if "volatility" in packet.lower():
            # naive rule for now
            if "0.7" in packet or "0.8" in packet or "0.9" in packet:
                risk_flag = "HIGH"
            else:
                risk_flag = "MEDIUM"

        results.append({
            "fact_packet": packet,
            "risk_level": risk_flag
        })

    return {
        "num_projects": len(results),
        "assessments": results
    }
