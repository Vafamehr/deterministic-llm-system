# Agent Control

This section explains how agent reasoning is bounded and controlled so that the system remains predictable and safe.

See diagram:

[Bounded Agent Control](./diagrams/agent_control.md)

The system includes an **agent reasoning capability**, but it is intentionally **bounded and controlled**.

The goal is to allow flexible reasoning when necessary while ensuring that the agent cannot take uncontrolled actions within the system.

---

## Decision Window

The orchestrator defines a **decision window** that determines when agent reasoning is permitted.

The agent is only invoked **after deterministic logic, tools, and retrieval have already been attempted**.

This ensures that the system always prioritizes structured and predictable mechanisms before allowing model-driven reasoning.

The orchestrator remains the **primary controller of execution**.

---

## Controlled Reasoning

When the decision window opens, the agent analyzes the current system state and produces a **structured decision or recommendation**.

The agent does **not execute system operations directly**.

Instead, the agent’s output is fed back into the **deterministic layer**, where the system continues execution using standard pipeline rules.

This design ensures that:

- all actions still pass through deterministic execution paths
- the orchestrator maintains full control of system flow
- reasoning remains observable and traceable

---

## Preventing Uncontrolled Behavior

Bounding the agent prevents several common issues in LLM-based systems:

- uncontrolled tool loops
- unpredictable execution paths
- difficult debugging
- hidden or opaque reasoning chains

By restricting the agent to a defined execution boundary, the system remains:

- stable
- observable
- easier to reason about and maintain

---

## Kitchen Analogy

| System Component | Kitchen Role |
|---|---|
Agent reasoning | Creative chef |
Decision window | Allowed cooking step |
Orchestrator | Head chef controlling the kitchen |
Deterministic layer | Standard recipes |