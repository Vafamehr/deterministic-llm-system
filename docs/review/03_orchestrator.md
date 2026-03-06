# Orchestrator

This section explains how the orchestrator controls system execution and routes requests across deterministic logic, capability expansion, and reasoning layers.

See diagram:

[Orchestrator Control Flow](./diagrams/orchestrator_control.md)

The **Orchestrator** is the control center of the system.

It manages execution flow and ensures that every request follows the system's **deterministic-first policy**.

Rather than allowing components to call each other freely, the orchestrator coordinates the entire execution pipeline.

---

## Execution Planning

When a request arrives, the orchestrator creates an **execution plan** that defines how the system should attempt to resolve the request.

The execution plan determines:

- which stage runs first
- what capability may be invoked next
- when the pipeline should escalate to more advanced reasoning

This planning step ensures the system follows a **controlled sequence of operations** rather than ad-hoc execution.

---

## Capability Routing

During execution, the orchestrator decides which capability should run next.

Possible routing options include:

- deterministic logic
- tool execution
- retrieval
- optional LLM reasoning

This routing ensures the system expands its capability **only when earlier stages cannot resolve the request**.

---

## Bounded Execution

The orchestrator enforces **bounded execution rules**.

Individual components cannot independently trigger other capabilities or expand execution without orchestrator approval.

This prevents uncontrolled agent behavior and keeps the system predictable.

---

## Trace Collection

Each stage produces **trace artifacts** describing what occurred during execution.

The orchestrator aggregates these traces so the system can be:

- inspected
- debugged
- explained

Trace data provides visibility into the full execution path.

---

## Candidate Result Production

When a stage produces a candidate answer, the orchestrator forwards the result to the **governance layer**.

Governance then evaluates whether the result should be returned to the user.

---

## Kitchen Analogy

| System Component | Kitchen Role |
|---|---|
Orchestrator | Head chef |
Execution plan | Cooking steps |
Capability routing | Choosing which station cooks |
Bounded execution | No chef improvises outside the recipe |
Trace artifacts | Order ticket history |