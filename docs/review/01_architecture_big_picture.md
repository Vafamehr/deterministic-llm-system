# Architecture Big Picture

This system follows a **layered architecture** designed to keep LLM reasoning controlled and observable.

The architecture separates the system into five conceptual layers:

### Control Layer
The **Orchestrator** manages system flow.  
It decides which components run and in what order.

### Deterministic Layer
This layer performs reliable operations such as:
- validation
- rule execution
- known logic
- structured reasoning

It is the **default path for solving requests**.

### Capability Layer
If deterministic logic cannot resolve a request, the orchestrator can expand capability using:

- **Tools** – structured external operations
- **Retrieval** – access to contextual knowledge
- **LLM reasoning** – optional reasoning layer

### Safety Layer
The **Governance** layer verifies that results meet safety or quality expectations before returning the answer.

### Observability
Every stage produces **trace artifacts** so the system can be inspected, debugged, and explained.

---

## Kitchen Analogy

The system can be understood like a professional kitchen:

| System Component | Kitchen Role |
|---|---|
Orchestrator | Head chef directing the line |
Deterministic | Standard recipes |
Tools | Pantry runner |
Retrieval | Recipe book lookup |
LLM | Creative sous-chef |
Governance | Quality check at the pass |
Trace | Order ticket history |

This analogy helps explain the system consistently during technical discussions or interviews.