# Day 31 — Trace-Aware Agent (Context, Not Autonomy)

## Goal
Make the agent **state-aware** by passing a structured summary of `DecisionTrace` into `AgentController.decide()`.

This is the bridge from a stateless decision module to an agent capable of safe multi-step behavior later.
Today we add **awareness only** — no new autonomy or loops.

---

## What Changed

### 1) Trace Summary Helper
A lightweight summarizer converts the full `DecisionTrace` into a small `trace_context` payload.

Key fields:
- `steps_run`: ordered list of trace step names
- `had_early_exit`: whether early-exit occurred
- `llm_attempted`: whether LLM has already run (normal or follow-up)
- `governance_checks`: count of governance evaluations
- `last_step`: most recent trace step

Design intent:
- Keep agent input bounded and stable
- Avoid feeding full trace into decision logic
- Provide enough history to prevent redundant actions

---

### 2) Orchestrator Passes `trace_context` into Agent Decision
Before the agent decides, orchestrator builds:

- `trace_context = _summarize_trace_for_agent(trace)`

Then passes it into:

- `agent.decide(..., trace_context=trace_context)`

---

### 3) AgentController Signature Updated
`AgentController.decide()` now accepts an optional parameter:

- `trace_context: Optional[Dict[str, Any]] = None`

The agent remains bounded by `max_steps`.

---

## Behavior Policy (Day 31)
No behavior expansion. The agent remains conservative.

Primary use today:
- Use `llm_attempted` to avoid redundant LLM follow-up requests.

Example:
- If deterministic fails and LLM has not yet been attempted → request `RUN_LLM`
- If LLM already ran → `STOP`

---

## What Did NOT Change (On Purpose)
- No multi-step loop
- No retries beyond the existing one-step follow-up hook
- No new stage execution logic
- No output schema changes
- No refactor of governance/execution separation

---

## Why This Matters
This creates a stable interface for future work:

- Day 32+: bounded multi-step behavior driven by trace history
- Decision trace becomes the state carrier for LangGraph-style transitions
- Enables “I already tried this” reasoning safely, without open loops

State awareness before autonomy is the correct order.

---

## Test Checklist
- Pipeline runs successfully
- Agent receives `trace_context` (optional debug print if needed)
- No behavior regressions in outputs
- No duplicate follow-up LLM requests when `llm_attempted` is true

---

## Outcome
The system is now:

Execution → Trace Recorded → Trace Summarized → Agent Reads Context → Decision

A state-aware decision engine that remains strictly bounded.