# Scenario Analysis Module

## Purpose

The Scenario Analysis module converts raw simulation outputs into structured comparisons that planners and analysts can interpret.

While the Simulation Engine executes different hypothetical worlds, the Scenario Analysis module explains **how those worlds differ from the baseline system behavior**.

This module answers questions such as:

- How does demand shock affect reorder quantities?
- How sensitive is the system to supplier delays?
- Which scenarios produce the largest operational impact?

It therefore acts as the **interpretation layer between simulation and decision insight**.

---

## Position in the System

The Scenario Analysis module sits immediately after the Simulation Engine.

Operational flow:

Demand Forecasting  
↓  
Inventory State  
↓  
Replenishment Policy  
↓  
Decision Coordinator  
↓  
Simulation Engine  
↓  
Scenario Analysis

The Simulation Engine generates multiple scenario outcomes.

Scenario Analysis converts those outcomes into **structured comparison outputs**.

---

## Input

The module receives a `SimulationResult`.

This object contains:

- baseline system input
- baseline decision result
- a list of scenario results

Each scenario result includes:

- the scenario definition
- the simulated system input
- the decision result produced by the pipeline

---

## Core Responsibilities

The Scenario Analysis module performs four core tasks.

### 1. Identify the Baseline

The baseline decision output acts as the reference point for comparison.

All scenario outcomes are evaluated relative to the baseline.

---

### 2. Extract Operational Decisions

For each scenario, the module extracts the operational decisions produced by the pipeline.

Example fields extracted:

- reorder decision
- recommended order quantity

These values come from the replenishment result inside the decision coordinator output.

---

### 3. Compute Scenario Deltas

The module computes how each scenario differs from the baseline.

For the current implementation:

Delta vs baseline =  
scenario recommended units − baseline recommended units

This provides a direct measure of disruption impact.

---

### 4. Produce Structured Comparison Output

The module returns a `ScenarioAnalysisResult` which contains a list of structured comparison rows.

Each row contains:

- scenario name
- reorder decision
- recommended units
- delta vs baseline

Example output:

| Scenario | Reorder | Units | Delta vs Baseline |
|--------|--------|--------|--------|
| baseline | True | 75 | 0 |
| demand_spike | True | 110 | +35 |
| supplier_delay | True | 140 | +65 |

This structure allows downstream systems to easily consume scenario insights.

---

## Design Principles

The module follows several design principles used across the Supply Chain AI Lab.

### Deterministic Logic

Scenario analysis performs deterministic comparisons and does not introduce additional modeling.

---

### No Mutation

The module does not modify simulation results.  
It only reads them and produces derived comparison objects.

---

### Separation of Concerns

Simulation and interpretation are intentionally separated.

Simulation Engine  
→ generates alternative system states.

Scenario Analysis  
→ interprets the consequences of those states.

---

### Minimal Dependencies

The module only depends on:

- simulation_engine.schemas
- scenario_analysis.schemas

This keeps the module lightweight and reusable.

---

## Future Extensions

The current version compares only reorder decisions and order quantities.

Future versions may extend the analysis to include:

- service level impact
- stockout risk
- inventory holding cost
- days of supply
- disruption severity classification

These extensions would allow the module to support richer planning insights.

---

## Role in the Future AI Layer

The Scenario Analysis module will eventually feed a reasoning layer powered by LLMs.

Example future capabilities:

- explain why a disruption changes decisions
- summarize scenario risks
- recommend policy adjustments

Because Scenario Analysis produces structured comparison outputs, it provides an ideal input format for such reasoning systems.

---

## Summary

The Scenario Analysis module transforms simulation outputs into actionable planning insights.

It bridges the gap between **scenario execution** and **decision interpretation**, making it possible to understand how supply chain policies behave under disruption.