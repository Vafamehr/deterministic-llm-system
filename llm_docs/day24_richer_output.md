# Day 24 — Chunk 1 — Rich Output Contract

Mental Line:
We force the model to produce per-project structured decisions, not vague summaries.

Changes:
- Prompt now requires JSON with:
  - overall_risk
  - projects[{project_id, risk, reason}]
  - next_actions[]

Validation:
- Enforce top-level keys
- Enforce per-project object fields and allowed values
- Enforce next_actions list of strings

Why:
Richer structured output becomes a stable interface for later agent actions.



# Day 24 — Chunk 2 — LLM vs Deterministic Cross-Check

Mental Line:
LLM reasoning must not silently contradict deterministic signals.

Added:
- Compare LLM per-project risk vs deterministic risk
- Produce `inconsistencies` list

Why:
Production systems must detect model drift or hallucinated escalation.

System Evolution:

Deterministic Layer
         ↓
LLM Layer
         ↓
Cross-Check
         ↓
Structured Output + Inconsistency Flags



# Day 24 — Chunk 3 — Confidence Layer

Mental Line:
Trust is measured, not assumed.

Added:
- consistency_ratio = 1 - (# inconsistencies / total projects)
- confidence label:
    HIGH (no mismatches)
    MEDIUM (some mismatches)
    LOW (many mismatches)

Why:
LLM systems need measurable trust signals.
This is foundation for gating and escalation policies.


