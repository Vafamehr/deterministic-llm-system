# Supply Chain Decision Pipeline — Architecture

This system is a modular, deterministic supply chain decision pipeline that separates data processing, tool execution, and orchestration.

## High-Level Flow (text diagram)

Historical Demand (CSV/DataFrame)
→ Feature Engineering + Model Training
→ Forecast Tool Input
→ Forecast Tool
→ Forecast Context
→ Derived Demand Signal
→ Inventory Status Tool
→ Replenishment Tool
→ Decision Coordinator
→ Final Result + Execution Trace

## Layered Architecture

### 1. Data / ML Layer (DataFrame World)

Handles raw data and modeling.

Components:
- synthetic_demand_history.csv
- load_demand_history
- DemandRecord
- feature engineering
- model training (LinearRegression, etc.)

Responsibilities:
- prepare historical demand
- train forecasting models
- build forecast inputs

Key idea: flexible, data-focused layer.

---

### 2. Tool Layer (Typed Contracts)

Defines structured interfaces using dataclasses.

Components:
- ForecastToolInput
- InventoryStatusToolInput
- ReplenishmentToolInput

Responsibilities:
- enforce structure
- isolate logic
- allow independent testing

Key idea: modular, replaceable components.

---

### 3. Coordination Layer (Execution Orchestration)

Controls execution flow and aggregates results.

Components:
- DecisionCoordinatorInput
- run_supply_chain_decision(...)
- execution trace

Responsibilities:
- run tools in order
- collect outputs
- produce final result
- log execution steps

Key idea: control plane of the system.

---

## Data Representation Separation

Two worlds exist intentionally:

DataFrame World:
- used for ML, transformations, training
- flexible and exploratory

Dataclass World:
- used for tool inputs/outputs
- strict and stable

Why:
DataFrames are good for computation.
Dataclasses are good for system boundaries.

---

## Why Tools Instead of Direct Function Calls

Instead of calling functions directly, each step uses structured tool inputs and outputs.

Benefits:
- clear boundaries between components
- easier debugging
- easier testing
- supports future simulation and agents

---

## Why the Coordinator Exists

The coordinator:
- controls execution order
- keeps pipeline consistent
- collects outputs
- logs execution trace

Without it:
- system becomes tightly coupled
- harder to extend and debug

---

## Current System Behavior

The pipeline:
1. loads demand history
2. trains a forecasting model
3. builds forecast input
4. derives demand signal from same SKU-location history
5. evaluates inventory
6. generates replenishment decision
7. returns outputs and trace

---

## Design Philosophy

- deterministic-first
- modular design
- explicit data flow
- interview-friendly structure

---

## Future Direction

- forecast → decision dependency wiring
- simulation loops
- scenario analysis
- policy layers
- multi-node networks
- agent-based orchestration

---

## One-Line Summary

A modular, deterministic supply chain decision system that separates ML, business logic, and orchestration using typed contracts.