# Agent Control

The system includes an **agent reasoning capability**, but it is intentionally **bounded and controlled**.

The goal is to allow flexible reasoning while preventing the agent from taking uncontrolled actions in the system.

---

## Decision Window

The orchestrator defines a **decision window** that determines when the agent is allowed to reason.

This means the agent is only invoked **after deterministic logic, tools, and retrieval have already been attempted**.

The orchestrator remains the primary controller of the system.

---

## Controlled Reasoning

When reasoning is allowed, the agent analyzes the current system state and produces a **structured decision**.

The agent does not execute system operations directly.

Instead, its reasoning feeds back into the deterministic layer where the system continues the pipeline.

This ensures that the system remains predictable and that all actions still pass through deterministic execution paths.

---

## Preventing Uncontrolled Behavior

Bounding the agent prevents several common issues in LLM-based systems:

- uncontrolled tool loops
- unpredictable system behavior
- difficult debugging
- hidden reasoning paths

By keeping the agent within a defined execution boundary, the system remains **stable, observable, and easier to reason about**.

---

## Kitchen Analogy

| System Component | Kitchen Role |
|---|---|
Agent reasoning | Creative chef |
Decision window | Allowed cooking step |
Orchestrator | Head chef controlling the kitchen |
Deterministic layer | Standard recipes |