import json
from pathlib import Path
import subprocess
# from Day 20
from delay_risk.validation.validate import validate_inputs

# “Bring me the relevant facts and documents.” siple alternatice for RAG

explain = """ 

What Each File Represents
metrics.json

This stands in for structured retrieval:

database rows

API results

warehouse metrics

telemetry

Think: SQL query result.

policy.md

This stands in for unstructured retrieval:

SOP documents

PDFs

manuals

internal wiki pages

"""






def load_metrics(path: str) -> dict:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Metrics file not found at {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data

def load_policy(path: str) -> str:

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Policy file not found at {path}")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return text


def build_decision_packet(metrics: dict, policy: str) -> str:
    packet = f"""
Decision Packet:

Operational Signals:
- Region: {metrics['region']}
- Time Window: {metrics['time_window']}
- Port: {metrics['port']}
- Average Delay (hours): {metrics['avg_delay_hours']}
- Days Above Threshold: {metrics['days_above_threshold']}
- Week-over-Week Change (%): {metrics['wow_change_pct']}
- Primary Cause Code: {metrics['primary_cause_code']}

Policy Context:
{policy}
"""

    return packet.strip()



def analyze_with_llm(decision_packet: str) -> str:
    prompt = f"""
You are a supply chain risk analyst.

Using the information below, determine whether escalation is required.

Return ONLY valid JSON in this schema:

{{
  "escalate": true/false,
  "risk_level": "LOW|MEDIUM|HIGH",
  "primary_cause": "string",
  "reasoning": "short explanation",
  "confidence": 0-1
}}

Decision Context:
{decision_packet}
"""

    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()














if __name__ == "__main__":
    metrics = load_metrics("data/metrics.json") # data from relation DB (RAG)
    policy = load_policy("data/policy.md") # Data from Non relational DB (also RAG)

    decision_packet = build_decision_packet(metrics, policy) # Data Interface → prepares evidence

    # print(decision_packet)

    ####### Finally Send the Decision Packet to the LLM + Force Structured Output


    print("Sending to LLM...\n")

    analysis = analyze_with_llm(decision_packet)

    print("LLM Response:\n")
    print(analysis)

