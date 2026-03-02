## Day 37 — Chunk 1 Notes
- Introduced tool data contracts (ToolSpec, ToolRequest, ToolResult).
- Tools are defined declaratively.
- ToolRequest is created by orchestrator, not agent.
- ToolResult separates success vs failure explicitly.
- No execution logic added yet.

## Day 37 — Chunk 2 Notes (Tool Envelope)

* Introduced `ToolEnvelope` to control **which tools may execute** during a pipeline run.
* The envelope is created by the orchestrator and never modified by the agent.
* Enforces:

  * explicit allow-list of tools (`allowed_tools`)
  * a strict execution cap (`max_calls`) to prevent loops or retries.
* Tracks usage internally while exposing a read-only view (`calls_made`) via `@property`.
* This mirrors `ExecutionEnvelope`, but governs **side effects instead of decisions**.
* Ensures tools remain deterministic infrastructure, not agent-driven behavior.

## Day 37 — Chunk 3 Notes (Tool Runner)
- Added `ToolRunner`: deterministic executor that runs orchestrator-specified tools only.
- Enforces `ToolEnvelope`:
  - allow-list (`allows`)
  - max tool calls (`record_call`)
- Returns a structured `ToolResult` (success/data/error).
- Agent never selects tools; this preserves deterministic-first authority.