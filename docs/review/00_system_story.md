# System Story

This section introduces the high-level idea behind the deterministic-first LLM system.

See diagram:

[Deterministic-First LLM System Overview](./diagrams/system_story.md)

This repository demonstrates a **deterministic-first architecture for building reliable LLM systems**.

Instead of treating the language model as the central controller, the system attempts to solve requests using **deterministic logic and structured tools first**. Only when those mechanisms cannot complete the task does the system invoke **LLM reasoning as a bounded capability**.

This design prioritizes **reliability, observability, and control**, which are critical requirements for production AI systems.

---

### The “Kitchen Line” Analogy (used consistently throughout docs)

- **Orchestrator = head chef**  
  Reads the ticket and decides which stations run and in what order.

- **Deterministic layer = standard recipes**  
  Validation, parsing, rules, and known computations that produce predictable results.

- **Tools / Retrieval = pantry runner + recipe book lookup**  
  External capabilities that return structured data the kitchen can use.

- **LLM = creative sous-chef**  
  Used only when earlier stations cannot fully resolve the request.

- **Governance = expo / pass**  
  Final quality check before the dish leaves the kitchen.

- **Trace = ticket history**  
  A record of every step taken during execution for debugging and observability.

---

### What happens on each request

1. The **Orchestrator** receives the user request and determines the execution path.

2. The system first attempts to resolve the request using the **Deterministic Layer**.

3. If deterministic logic cannot complete the task, the orchestrator identifies the missing capability and either:
   - calls a **Tool** (via registry + envelope), or
   - performs **Retrieval** (bounded query returning relevant context).

4. Deterministic reasoning runs again using the returned structured inputs.

5. If the request is still unresolved and policy allows it, the system invokes **LLM reasoning**.

6. A **Governance Gate** evaluates the candidate answer for risk, ambiguity, and policy constraints.

7. The system returns the **Final Output** and records **Trace Artifacts** across all stages for observability.

---

### Why this design

- **Reliability first**  
  Deterministic logic is predictable, testable, and easy to debug.

- **Bounded capability expansion**  
  Tools and retrieval introduce new capabilities in a controlled way.

- **LLM is not the controller**  
  The model assists reasoning but does not control the system.

- **Explainability and observability**  
  Trace artifacts make the system transparent and debuggable.