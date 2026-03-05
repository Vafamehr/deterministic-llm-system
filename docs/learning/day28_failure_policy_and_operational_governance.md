# Day 28 — Chunk 1
## Introducing Failure Policy Layer

### Purpose
Translate stage outcomes into system-level behavior.

### New Component
FailurePolicy evaluator:
evaluate_failure_policy(det_res, llm_res, cc_res)

### Returns
{
  "needs_review": bool,
  "degradation_mode": str,
  "escalation_reasons": List[str]
}

### Initial Policy Rules
- Deterministic FAILED → TOTAL_FAILURE
- LLM FAILED → DETERMINISTIC_ONLY
- Cross-check FAILED → NO_CROSS_CHECK
- All SUCCESS → NONE

### Why This Matters
Moves system from reactive error handling
to structured operational governance.


## Chunk 2 — Implement Failure Policy

Created: src/failure_policy.py

evaluate_failure_policy(det_res, llm_res, cc_res)

Policy logic:
- Deterministic FAILED → TOTAL_FAILURE
- LLM FAILED → DETERMINISTIC_ONLY
- Cross-check FAILED → NO_CROSS_CHECK
- All SUCCESS → NONE

This layer translates stage-level failures
into system-level operational behavior.

## Chunk 3 — Expose Failure Policy in Output

Integrated evaluate_failure_policy() into run_full_assessment.

Added new top-level output field:
governance: {
  needs_review,
  degradation_mode,
  escalation_reasons
}

This makes the system operationally interpretable:
it can communicate when output is degraded and why.


## Chunk 4 — Confidence Alignment

Problem: governance and business-layer confidence can disagree.

Fix:
- If governance.needs_review == True, confidence cannot be HIGH.
- Apply a minimal helper to downgrade HIGH → MEDIUM under review.

This prevents contradictory outputs and improves production credibility.

## Chunk 5 — Type-Safe DegradationMode

Added DegradationMode Enum to prevent typo bugs in governance outputs.

- Created src/degradation_mode.py
- failure_policy now returns DegradationMode values internally
- orchestrator converts governance["degradation_mode"] to a JSON-friendly string via .value



## Summary of what we have built so far:

system now:

Plans execution (ExecutionPlan abstraction)

Executes stages independently

Captures latency + error metadata

Prevents cascade failures

Self-describes degradation

Flags when human review is needed

Aligns business confidence with operational risk

Produces structured, inspectable output.