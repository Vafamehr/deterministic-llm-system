# Day 30 — Decision Trace (Making the System Explain Its Decisions)

## Goal
Introduce a structured **Decision Trace** so the system records *why it behaved the way it did*.

Before Day 30, the pipeline executed correctly but had no memory of reasoning.
Now we capture execution outcomes, governance interpretation, and agent decisions
as an append-only record.

This enables:
- Explainability
- Auditability
- Future multi-step bounded agents
- Transition toward graph-based execution (LangGraph-style later)

---

## Key Idea: Trace ≠ Logging

Logs answer:
"What happened technically?"

DecisionTrace answers:
"Why did the system choose this path?"

Trace is structured reasoning, not debug output.

---

## Architecture Change (Minimal)

No refactors.
No signature changes.
No new control flow.

We simply:
1. Created a `DecisionTrace` object inside `run_full_assessment`.
2. Added trace events at real execution boundaries.
3. Returned the trace alongside the normal JSON output.

---

## New Module

`decision_trace.py`

Defines:
- `TraceEvent`
- `DecisionTrace`

Responsibilities:
- Append-only reasoning history
- JSON-serializable output
- Decoupled from execution logic

---

## Where Trace Events Are Added

Trace is initialized at the top of:

`run_full_assessment(...)`

Events are recorded only at true decision boundaries:

### After Deterministic Stage
Captures status + latency.

### After LLM Stage (if executed)
Captures model execution outcome.

### After Cross-Check Stage (if executed)
Captures agreement / inconsistency signals.

### After Governance Evaluation
Captures:
- degradation_mode
- hard_stop
- escalation reasons

### After Agent Decision
Captures:
- chosen action
- reasoning text
- step index

### During Follow-Up Execution (if triggered)
Records re-run and governance re-evaluation.

### During Early Exit
Records why LLM + cross-check were intentionally skipped.

---

## Important Fix — Early Exit Contract

Originally early-exit returned a smaller schema.
We updated it to return the SAME structure as the normal path.

Early-exit is now:
A different execution path,
not a different API.

---

## Final Output Now Includes

`"decision_trace": [...]`

Example:

```json
{
  "step": "governance",
  "status": "pass",
  "reason": "Failure policy evaluated",
  "data_snapshot": {
    "degradation_mode": "NONE"
  }
}
```

---

## What Day 30 Achieved

We moved from:
Pipeline execution

to:
Inspectable decision system.

The system now remembers:
- What it did
- Why it did it
- What influenced the decision

This trace becomes the state backbone for future agent iterations.

---

## Validation Check

Run:

```python
result = run_pipeline(packets)
print(result["decision_trace"])
```

Both normal runs and early-exit runs must produce trace events.

---

## Why This Matters for the Big Picture

Supply chain systems must justify:
- Why an escalation happened
- Why a lane was skipped
- Why a retry occurred

DecisionTrace enables explainable automation — not black-box AI.

---

## Sets Up Day 31

Next:
The agent will read this trace before deciding,
allowing bounded multi-step reasoning.

This is the bridge toward:
Stateful agents → tool orchestration → graph execution.