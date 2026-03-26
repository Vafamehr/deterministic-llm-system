# Simulation Engine

## Purpose

Runs the same decision pipeline under different input conditions.

---

## One-Line Summary

Executes the coordinator-driven pipeline multiple times with modified inputs.

---

## Role in System

The simulation engine sits above the core pipeline.

Flow:

Simulation → Coordinator → Tools → Domain Modules

It does not replace or change the pipeline.
It reuses the same logic under different scenarios.

---

## Responsibilities

* define scenarios
* apply input changes
* run the pipeline
* collect results

---

## Execution Logic

For each scenario:

1. start from baseline input
2. apply scenario modifications
3. run the coordinator
4. capture outputs
5. store scenario result

Typical modifications include:

* demand multiplier
* lead time multiplier
* inventory shock

---

## What It Does Not Do

* does not implement forecasting
* does not implement inventory logic
* does not implement replenishment logic
* does not introduce new business rules

Its job is execution, not decision-making.

---

## Outputs

Each scenario run returns structured outputs such as:

* scenario name
* decision output
* inventory signals
* replenishment result

These outputs are then passed to scenario analysis.

---

## Project Structure

```text
src/simulation_engine/
- schemas.py
- service.py
- smoke_test.py
```

---

## Dependency Direction

simulation_engine
↓
decision_coordinator
↓
tools
↓
domain modules

Lower layers must not depend on simulation.

---

## Design Rules

* reuse the exact same pipeline
* keep simulation non-intrusive
* modify inputs only
* keep core logic unchanged

---

## Mental Model

single run = one decision path
simulation = many decision paths under different conditions

---

## One-Line Summary

A thin execution layer that stress-tests the same deterministic pipeline under different scenarios.
