# Day 32 — Governance-Aware Bounded Follow-Up

## Goal
Make the agent’s follow-up decision depend on **governance + trace history**, not only deterministic failure.

## Changes
- `AgentController.decide(...)` now accepts `governance_context`
- Added policy:
  - If `hard_stop` → STOP
  - If deterministic failed and LLM not attempted → RUN_LLM
  - If governance `needs_review` and LLM not attempted → RUN_LLM
  - Otherwise STOP
- Still bounded by `max_steps`

## Why
This aligns the follow-up hook with the governance layer and prevents redundant LLM requests.
It’s a controlled step toward multi-step bounded agents.