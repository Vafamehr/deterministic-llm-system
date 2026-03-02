## Day 35 — Chunk 1 Notes
- Added confirmation-only monotonicity: Step 1 can never upgrade behavior.
- If Step 0 proposed STOP, Step 1 is forced to STOP (no hidden retry path).
- Keeps orchestrator authority intact; Step 1 remains a bounded confirmation pass.

## Day 35 — Chunk 2 Notes
- Step 1 can downgrade RUN_LLM → STOP only when it can cite a concrete constraint in `delta_context.known_constraints`.
- If constraints allow RUN_LLM, Step 1 confirms RUN_LLM immediately (no full re-eval).
- Confirmation logic lives after `_enforce` so envelope constraints are always respected.

## Day 35 — Structural Guarantees
- Step 1 never re-enters Rule 1 (deterministic fallback).
- Step 1 never re-enters Rule 2 (governance-triggered retry).
- Step 1 never evaluates fresh pipeline state.
- Step 1 operates only on frozen `delta_context`.
- The metered window is now monotonic, bounded, and non-iterative.