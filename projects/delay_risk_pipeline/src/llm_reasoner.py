import json
import subprocess
from typing import List, Dict,Any



MODEL_NAME = "llama3"  # adjust if needed


# def build_prompt(fact_packets: List[str]) -> str:
#     joined_packets = "\n\n".join(fact_packets)

#     return f"""
# You are a supply chain risk analyst.

# Below are structured project summaries.

# {joined_packets}

# Return a JSON object with:
# - overall_risk (LOW / MEDIUM / HIGH)
# - reasoning (short explanation)

# Respond with valid JSON only.
# """




def build_prompt(fact_packets: List[str]) -> str:
    joined = "\n\n".join(fact_packets)

    return f"""
You are a supply chain risk analyst.

You will receive project fact packets.
Return ONLY valid JSON. No backticks. No extra text.

JSON schema:
{{
  "overall_risk": "LOW|MEDIUM|HIGH",
  "projects": [
    {{"project_id": "string", "risk": "LOW|MEDIUM|HIGH", "reason": "string"}}
  ],
  "next_actions": ["string"]
}}

Rules:
- Include one entry in "projects" per project present in the fact packets.
- project_id must match exactly what appears after "Project:".
- Keep reasons short (1 sentence max).

Fact packets:
{joined}
""".strip()




def call_llm(prompt: str) -> str:
    result = subprocess.run(
        ["ollama", "run", MODEL_NAME],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.decode()



def call_llm_with_retry(prompt: str, max_retries: int = 1) -> Dict:
    """
    Calls LLM and retries once if parsing fails.
    """
    for attempt in range(max_retries + 1):
        raw = call_llm(prompt)
        try:
            parsed = parse_llm_output(raw)
            validated = validate_decision_schema(parsed)
            return validated
        except Exception as e:
            if attempt == max_retries:
                raise e
    raise RuntimeError("Unexpected retry failure.")



# def parse_llm_output(text: str) -> Dict:
#     try:
#         return json.loads(text.strip())
#     except json.JSONDecodeError:
#         raise ValueError("LLM returned invalid JSON.")



def parse_llm_output(text: str) -> Dict:
    """
    Parse JSON even if the model wraps it with extra text.
    Extract first {...} block via brace matching.
    """
    s = text.strip()

    start = s.find("{")
    if start == -1:
        raise ValueError(f"LLM returned no JSON object. Raw:\n{s[:500]}")

    depth = 0
    for i in range(start, len(s)):
        ch = s[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                candidate = s[start : i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON extracted: {e}\nExtracted:\n{candidate}")

    raise ValueError("JSON braces did not close. Model output was truncated or malformed.")


# REQUIRED_KEYS = {"overall_risk", "reasoning"}


# def validate_decision_schema(result: Dict) -> Dict:
#     missing = REQUIRED_KEYS - set(result.keys())
#     if missing:
#         raise ValueError(f"Missing required keys: {missing}")

#     if result["overall_risk"] not in {"LOW", "MEDIUM", "HIGH"}:
#         raise ValueError("Invalid overall_risk value.")

#     if not isinstance(result["reasoning"], str):
#         raise ValueError("Reasoning must be a string.")

#     return result



def validate_decision_schema(result: Dict[str, Any]) -> Dict[str, Any]:
    required_top = {"overall_risk", "projects", "next_actions"}
    missing = required_top - set(result.keys())
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    if result["overall_risk"] not in {"LOW", "MEDIUM", "HIGH"}:
        raise ValueError("Invalid overall_risk value.")

    projects = result["projects"]
    if not isinstance(projects, list) or len(projects) == 0:
        raise ValueError("projects must be a non-empty list.")

    for p in projects:
        if not isinstance(p, dict):
            raise ValueError("Each project entry must be an object.")
        for k in ("project_id", "risk", "reason"):
            if k not in p:
                raise ValueError(f"Project entry missing key: {k}")
        if p["risk"] not in {"LOW", "MEDIUM", "HIGH"}:
            raise ValueError("Invalid project risk value.")
        if not isinstance(p["reason"], str):
            raise ValueError("Project reason must be a string.")

    actions = result["next_actions"]
    if not isinstance(actions, list):
        raise ValueError("next_actions must be a list.")
    for a in actions:
        if not isinstance(a, str):
            raise ValueError("Each next_action must be a string.")

    return result
