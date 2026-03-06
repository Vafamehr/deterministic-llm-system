### Day 39 — Chunk 1: Retrieval tool interface

- Introduced a typed retrieval tool contract:
  - `RetrievalQuery` (query, top_k, optional namespace)
  - `RetrievedChunk` (id, text, source, score, meta)
  - `RetrievalResult` (chunks, sources, meta)
- Purpose: make RAG retrieval a deterministic tool (envelope-bounded + trace-logged) owned by the orchestrator, not the agent.

### Day 39 — Chunk 2: Retrieval payload adapters

- Added strict adapters:
  - `retrieval_tool_input(payload)` validates + converts ToolRequest payload → `RetrievalQuery`.
  - `retrieval_tool_output(result)` converts `RetrievalResult` → JSON-serializable dict for ToolResult.data.
- Purpose: keep retrieval deterministic, predictable, and compatible with the existing generic ToolRunner interface without refactoring the architecture.


### Day 39 — Chunk 3: Deterministic Retrieval Executor

- Implemented `execute_retrieval(query: RetrievalQuery)`.
- Pure deterministic function.
- Converts raw index hits → structured `RetrievedChunk`.
- Returns `RetrievalResult` with:
  - chunks
  - sources
  - metadata
- No LLM usage.
- No agent decision.
- Retrieval is now a deterministic tool-layer capability.



### Day 39 — Chunk 4: Wrap retrieval as a registered ToolSpec (no refactor)

- Kept existing `src/tools/retrieval.py` implementation (types + adapters + deterministic executor).
- Added a thin Tool wrapper:
  - Tool name: `rag.retrieve`
  - Runner: ToolRequest.payload → `RetrievalQuery` → deterministic `execute_retrieval` → ToolResult.data
  - Returns `SUCCESS` or `ERROR` ToolResult (no LLM, no loops).
- Registered `RETRIEVAL_TOOL` in `src/tools/registry.py`.

Result: retrieval is now a first-class deterministic tool runnable via ToolRunner + ToolEnvelope, orchestrator-owned (agent never selects tools).