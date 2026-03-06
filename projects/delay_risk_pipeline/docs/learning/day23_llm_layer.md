# Day 23 — Chunk 1 — LLM Reasoning Layer

Mental Line:
LLM sits on top of deterministic signals. It does reasoning, not computation.

Added:
- llm_reasoner.py
    - build_prompt()
    - call_llm()
    - parse_llm_output()

Design Principles:
- LLM receives only fact_packets
- Strict JSON output required
- No raw data access
- No numeric computation delegated to model

System Evolution:

Fact Packets
   ↓
LLM Prompt Builder
   ↓
LLM Call (Ollama)
   ↓
JSON Parse
   ↓
Structured Decision


# Day 23 — Chunk 2 — Schema Validation

Mental Line:
Never trust LLM output blindly. Validate structure explicitly.

Added:
- REQUIRED_KEYS = {"overall_risk", "reasoning"}
- validate_decision_schema()

Validation Rules:
- Keys must exist
- overall_risk ∈ {LOW, MEDIUM, HIGH}
- reasoning must be string

System Evolution:

LLM
   ↓
JSON Extraction
   ↓
JSON Parse
   ↓
Schema Validation
   ↓
Safe Structured Output

# Day 23 — Chunk 3 — Orchestrator Layer

Mental Line:
Connect deterministic signals and LLM reasoning into one controlled flow.

Added:
- orchestrator.py
- run_full_assessment()

Flow:
Fact Packets
   ↓
Deterministic Assessment
   ↓
LLM Reasoning
   ↓
JSON Extraction
   ↓
Schema Validation
   ↓
Combined Output

Purpose:
Central control point for future agent behavior.


# Day 23 — Chunk 4 — Retry Guard

Mental Line:
Never let a single malformed LLM response crash the system.

Added:
- call_llm_with_retry(prompt, max_retries=1)

Behavior:
- Call LLM
- Attempt parse + schema validation
- If failure → retry once
- If still failure → raise error

System Evolution:

LLM
   ↓
Extract JSON
   ↓
Validate Schema
   ↓
Retry if needed
   ↓
Safe Structured Output
