# System Story

This section introduces the high-level idea behind the deterministic-first LLM system.

See diagram:

[Deterministic-First LLM System Overview](./diagrams/system_story.md)

This repository implements a **deterministic-first LLM system**. The core idea is simple: **solve with reliable logic first**, then use an LLM only as a **secondary** layer when deterministic methods cannot complete the job.

### The “Kitchen Line” Analogy (used consistently throughout docs)
- **Orchestrator = head chef**: reads the ticket and decides the sequence of stations.
- **Deterministic layer = standard recipes**: validation, parsing, rules, and known computations.
- **Tools/Retrieval = pantry runner + recipe book lookup**: bounded calls return structured results.
- **LLM = creative sous-chef**: allowed only if earlier stations cannot resolve the request.
- **Governance = expo / pass**: quality and risk check before serving.
- **Trace = ticket history**: timestamps + outcomes at every station for observability.

### What happens on each request
1. The **Orchestrator** receives the user request and chooses the pipeline route.
2. The system attempts a **Deterministic** solution (the default path).
3. If unresolved, the orchestrator identifies the missing capability:
   - call a **Tool** (via registry + envelope), or
   - run **Retrieval** (bounded query → context chunks).
4. The system re-runs deterministic reasoning using returned tool data or retrieved context.
5. If still unresolved (and allowed), the system runs **LLM reasoning** as a secondary layer.
6. A **Governance Gate** validates the candidate answer (risk, ambiguity, evidence).
7. The system returns the **Final Output** and emits **Trace Artifacts** across all steps.

### Why this design
- **Reliability first**: deterministic logic is predictable and testable.
- **Bounded capability expansion**: tools/retrieval are structured and controlled.
- **LLM is not the controller**: it reasons only when necessary.
- **Explainability**: traces make the system debuggable and interview-ready.