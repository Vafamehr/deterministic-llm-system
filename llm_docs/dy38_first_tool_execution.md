## Day 38 — Chunk 1 Notes
- Implemented first concrete tool (`get_current_time`).
- Tool is deterministic and side-effect free.
- Purpose is validating tool runner + envelope wiring before introducing retrieval.
- Keeps debugging surface minimal before adding RAG complexity.

## Day 38 — Chunk 2 Notes
- Added a tool registry (`TOOL_REGISTRY`) mapping tool name → callable.
- Added a manual sanity test to execute one tool via `ToolRunner` under `ToolEnvelope`.
- Validated allow-list + max_calls behavior before wiring tools into the orchestrator.

## Day 38 — Chunk 3 Notes
- Added minimal orchestrator tool hook.
- Tool execution is optional and plan-driven.
- Agent remains unaware of tools.
- Tool execution logged in trace.
- Envelope enforces single-call boundary.