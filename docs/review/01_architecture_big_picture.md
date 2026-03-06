# Architecture Overview

This section explains the major components of the system and how responsibilities are separated across architectural layers.

See diagram:

[LLM System Architecture Overview](./diagrams/architecture_big_picture.md)

This system follows a **layered architecture designed to keep LLM reasoning controlled, bounded, and observable**.

Instead of allowing a language model to directly control execution, the architecture separates responsibilities across layers that manage **control, reasoning, capability expansion, safety, and observability**.

This design allows the system to remain **predictable and debuggable**, while still benefiting from LLM reasoning when deterministic logic is insufficient.

---

## Architectural Layers

The system is organized into five conceptual layers.

### Control Layer

The **Orchestrator** acts as the central controller of the system.

Its responsibilities include:

- receiving the user request
- selecting the execution path
- deciding when to invoke tools, retrieval, or LLM reasoning
- coordinating execution across system components

The orchestrator ensures that the system behaves like a **pipeline**, not an autonomous agent.

---

### Deterministic Layer

The deterministic layer performs reliable, predictable computation.

Typical responsibilities include:

- validation
- rule execution
- known transformations
- structured reasoning
- data parsing

This layer is the **default and preferred path for resolving requests** because deterministic logic is easier to test, explain, and maintain.

---

### Capability Layer

When deterministic logic cannot resolve a request, the system can expand its capabilities through controlled mechanisms.

These include:

- **Tools**  
  Structured external operations that return well-defined outputs.

- **Retrieval**  
  Querying a knowledge source to obtain relevant contextual information.

- **LLM Reasoning**  
  A bounded reasoning layer used when deterministic approaches and structured capabilities cannot complete the task.

The orchestrator decides which capability to invoke based on the missing requirement.

---

### Safety Layer

Before returning a result to the user, the system passes the candidate output through the **Governance Layer**.

This layer performs checks such as:

- risk assessment
- ambiguity detection
- policy validation
- answer completeness

The governance step ensures that outputs meet safety and quality expectations.

---

### Observability Layer

Every stage of execution produces **trace artifacts**.

Trace data captures:

- which components executed
- decision points
- execution outcomes
- timestamps and latency

These artifacts allow the system to be **debugged, inspected, and explained**, which is critical for operating LLM systems in production environments.

---

## Kitchen Analogy

The architecture can also be understood using a professional kitchen analogy.

| System Component | Kitchen Role |
|---|---|
Orchestrator | Head chef directing the line |
Deterministic | Standard recipes |
Tools | Pantry runner |
Retrieval | Recipe book lookup |
LLM | Creative sous-chef |
Governance | Quality check at the pass |
Trace | Order ticket history |

This analogy helps explain how the system operates during technical discussions and interviews.