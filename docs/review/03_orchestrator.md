# Orchestrator

This section explains how the orchestrator controls system execution and routes requests across deterministic logic, capabilities, and reasoning layers.

See diagram:

[Orchestrator Control Flow](./diagrams/orchestrator_control.md)

The **Orchestrator** is the control center of the system.

It manages execution flow and ensures that the system follows a **deterministic-first policy**.

The orchestrator performs several key responsibilities.

---

## Execution Planning

When a request arrives, the orchestrator creates an **execution plan** that determines how the system should attempt to resolve the request.

The plan defines the sequence of capabilities the system may use.

---

## Capability Routing

The orchestrator determines which capability should run next:

- deterministic logic
- tool execution
- retrieval
- optional LLM reasoning

This routing ensures the system expands capability **only when necessary**.

---

## Bounded Execution

The orchestrator enforces **bounded execution**.

Components cannot run arbitrarily or call other capabilities without approval.

This prevents uncontrolled agent behavior.

---

## Trace Collection

Each stage produces **trace artifacts**.

The orchestrator aggregates these traces so the system can be inspected and debugged.

---

## Candidate Result Production

Once a stage produces a candidate answer, the orchestrator passes the result to the **governance layer** for validation.

---

## Kitchen Analogy

| System Component | Kitchen Role |
|---|---|
Orchestrator | Head chef |
Execution plan | Cooking steps |
Capability routing | Choosing which station cooks |
Bounded execution | No chef improvises outside the recipe |
Trace artifacts | Order ticket history |