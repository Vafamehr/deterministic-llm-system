# Decision Pipeline — Core Concepts

This document explains the key ideas behind the supply chain decision pipeline and why it is designed this way.

## Deterministic-First Design

The system follows a deterministic-first approach.

This means:
- the flow of execution is fixed and predictable
- each step produces consistent outputs for the same inputs
- there is no hidden or implicit behavior

Why this matters:
- easier debugging
- easier testing
- easier to explain in interviews
- strong foundation before adding complexity like agents or RL

In simple terms:
First make it correct and stable, then make it smart.

---

## Forecasting System vs Decision System

These are two different responsibilities.

### Forecasting System

Purpose:
Predict future demand.

What it does:
- uses historical data
- applies ML models
- outputs future demand estimates

Example:
"SKU A will sell ~30 units per day over the next 3 days"

---

### Decision System

Purpose:
Decide what actions to take.

What it does:
- uses demand signals (from forecast or history)
- evaluates inventory
- decides whether to reorder and how much

Example:
"Inventory is sufficient, no reorder needed"

---

Key distinction:

Forecasting answers:
What will happen?

Decision system answers:
What should we do?

---

## Why Tools Instead of Direct Function Calls

The system uses tool-style inputs and outputs instead of direct function calls.

Instead of:
- tightly connected functions calling each other

We use:
- structured inputs (dataclasses)
- structured outputs
- isolated components (tools)

Why this matters:

- each component is independent
- easier to test each tool separately
- easier to replace parts (e.g., swap model)
- clearer data flow

This design mimics real production systems, not scripts.

---

## Role of the Coordinator

The coordinator is the orchestrator of the system.

It:
- runs tools in a defined order
- passes inputs to each tool
- collects outputs
- produces a final result
- records execution trace

Without a coordinator:
- logic becomes scattered
- harder to track execution
- harder to extend system

The coordinator makes the system structured and controllable.

---

## Why This Design Supports Simulation

Because everything is modular and deterministic:

- you can run the same pipeline with different inputs
- you can simulate different demand scenarios
- you can test policies (e.g., reorder thresholds)

This allows:
"What happens if demand increases by 20%?"
"What happens if lead time doubles?"

---

## Why This Design Supports Agents (Future)

Since each tool has clear contracts:

- an agent can decide which tool to call
- an agent can change execution order
- an agent can reason about outputs

The current system is fixed (deterministic),
but the structure is ready for dynamic decision-making later.

---

## Why This Design Supports Explainability

Every step is explicit:

- forecast is visible
- inventory calculation is visible
- replenishment logic is visible
- execution trace is recorded

This allows:
- clear reasoning for decisions
- easy debugging
- strong business trust

---

## Mental Model (Simple)

Think of the system as:

Data → Prediction → Evaluation → Decision → Output

Each step is separate, structured, and traceable.

---

## One-Line Summary

A deterministic, modular decision system that separates prediction, evaluation, and action using clear contracts, enabling simulation, explainability, and future agent-based extensions.