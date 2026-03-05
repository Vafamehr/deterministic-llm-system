# Request Execution Pipeline

This section describes how a user request flows through the system from intake to final output.

See diagram:

[Request Execution Pipeline](./diagrams/pipeline.md)

The system processes every request through a **deterministic-first execution pipeline** controlled by the orchestrator.

The goal is to **use reliable logic first**, then expand capability only when necessary.

---

## Pipeline Stages

### 1. Request Intake
The **Orchestrator** receives the user request and determines the execution path.

### 2. Deterministic Attempt
The system first attempts to resolve the request using deterministic logic such as:
- validation
- rules
- known transformations

If a valid answer is produced, the system proceeds to governance.

### 3. Capability Expansion

If deterministic logic cannot resolve the request, the orchestrator identifies the missing capability.

Two options are available:

**Tool Execution**
- The system calls structured tools through a registry.
- Tools return structured results.

**Retrieval**
- The system retrieves contextual knowledge.
- Retrieved chunks are returned to the deterministic layer.

### 4. Optional LLM Reasoning

If deterministic logic combined with tools or retrieval still cannot resolve the request, the system may allow **LLM reasoning**.

LLM reasoning is therefore a **secondary capability**, not the primary engine.

### 5. Governance

The candidate result passes through a governance check that may evaluate:

- safety
- ambiguity
- missing evidence

### 6. Final Output

If governance approves the result, the system returns the final answer.

### 7. Observability

Every stage produces **trace artifacts** so the system can be inspected and debugged.

---

## Kitchen Analogy

| Pipeline Stage | Kitchen Equivalent |
|---|---|
User Request | Order ticket |
Orchestrator | Head chef |
Deterministic Logic | Standard recipe |
Tool Execution | Pantry runner |
Retrieval | Recipe book |
LLM Reasoning | Creative chef |
Governance | Quality check |
Trace | Ticket history |