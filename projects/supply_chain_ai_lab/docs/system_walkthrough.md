# Step 1 — Big Picture System Understanding

## What This System Is

This is **not a forecasting system**.

This is a **deterministic supply chain decision system**.

The goal is:
- Given demand expectations and current inventory state, produce operational decisions (reorder or not, how much), and evaluate those decisions under different scenarios.

Forecasting is only an input — not the final objective.

---

## System Flow (Core Backbone)
Forecast → Inventory → Replenishment → Coordinator → Simulation → Scenario Analysis

This flow represents the full decision pipeline.

---

## Inputs to the System

The system operates using:

- historical demand data
- current inventory state
- lead time information
- configuration parameters (thresholds, safety logic)

---

## Outputs of the System

The system produces **action-oriented outputs**, not just predictions:

- reorder decision (True / False)
- recommended_units
- days_of_supply (DOS)
- stockout_risk
- scenario comparisons (baseline vs alternatives)
- delta_vs_baseline
- inventory_pressure

---

## Layer Responsibilities

### 1. Forecast Module
- Predicts future demand
- Output is expected demand (not a decision)

### 2. Inventory Module
- Combines demand and inventory state
- Computes coverage metrics (e.g., days of supply)

### 3. Replenishment Module (Decision Layer)
- Produces actual decisions:
  - whether to reorder
  - how many units to order
- This is where business logic for action lives

### 4. Coordinator (Orchestration Layer)
- Controls execution flow across modules
- Calls modules in sequence
- Does NOT contain business logic

### 5. Simulation Layer
- Modifies inputs (e.g., demand spike, lead time delay)
- Re-runs the same deterministic pipeline
- Does NOT change decision logic

### 6. Scenario Analysis Layer
- Interprets outputs across scenarios
- Computes:
  - delta vs baseline
  - risk levels
  - inventory pressure

---

## Key Architectural Principle

Separation of concerns:

- **Modules = business logic**
- **Coordinator = orchestration only**

If decision logic leaks into the coordinator:
- system becomes a "god object"
- module boundaries break
- testing and extension become difficult

---

## One-Sentence Summary (Interview Ready)

This is a deterministic supply chain decision system that uses demand forecasts and inventory state to generate replenishment decisions and evaluates those decisions under different scenarios through simulation and analysis.


# Step 2 — Numerical Walkthrough (Baseline Only)

## Setup

We consider a simple case with:

- 1 SKU
- 1 Location

### Given:

- Current Inventory = 100 units
- Predicted Daily Demand = 20 units/day
- Lead Time = 3 days
- Safety Stock = 40 units

---

## Step 1 — Forecast Output

Forecast module provides:

Expected demand = 20 units/day

This is an input to downstream modules, not a decision.

---

## Step 2 — Inventory Evaluation

### Days of Supply (DOS)

DOS = Inventory / Daily Demand  
    = 100 / 20 = 5 days

Interpretation:
If no replenishment occurs, inventory will last 5 days.

---

## Step 3 — Replenishment Decision

### Demand during lead time

Lead time demand = 20 × 3 = 60 units

### Reorder point

Reorder point = Lead time demand + Safety stock  
              = 60 + 40 = 100 units

### Decision rule

If Inventory ≤ Reorder Point → reorder

Since:

Inventory = 100  
Reorder Point = 100  

→ reorder = TRUE

---

### Recommended units

Recommended Units = Reorder Point − Inventory  
                  = 100 − 100 = 0

Interpretation:
We are exactly at the safety threshold. No additional units are needed, but the system flags that we are at risk boundary.

---

## Timeline Interpretation

The reorder decision is forward-looking:

- At time of decision, inventory must cover demand during lead time
- During lead time (3 days), demand will consume inventory
- Safety stock ensures a buffer after lead time

Example:

Start: 100  
Demand over 3 days: −60  
Ending inventory: 40 (safety stock)

---

## Role of Safety Stock

Safety stock protects against:

- demand variability
- lead time delays

It ensures that even if actual conditions deviate from expected values, the system avoids stockout.

Without safety stock:

- Reorder point = 60
- System operates with no buffer
- Any deviation causes stockout

---

## Key Insight

This is a **reorder point policy**:

- ensures service level
- prevents stockout
- does not optimize long-term inventory

More advanced systems may use:
- order-up-to policies
- EOQ models
- dynamic optimization


# Step 3 — Scenario-Based Behavior

## Baseline (Reference)

- Inventory = 100
- Demand = 20/day
- Lead Time = 3 days
- Safety Stock = 40

Baseline Output:
- reorder = True
- recommended_units = 0
- days_of_supply = 5

---

## Scenario 1 — Demand Spike

### Change
Demand increases from 20 → 30 units/day

---

### Inventory Impact

DOS = 100 / 30 ≈ 3.33 days

Interpretation:
Inventory depletes faster.

---

### Replenishment Logic

Lead time demand = 30 × 3 = 90  
Reorder point = 90 + 40 = 130  

Inventory = 100 < 130 → reorder = True  

Recommended units = 130 − 100 = 30

---

### Interpretation

- Higher demand increases depletion speed
- System reacts by increasing reorder quantity
- Risk comes from faster consumption

---

## Scenario 2 — Supplier Delay

### Change
Lead time increases from 3 → 5 days

---

### Inventory Impact

DOS = 100 / 20 = 5 days (unchanged)

---

### Replenishment Logic

Lead time demand = 20 × 5 = 100  
Reorder point = 100 + 40 = 140  

Inventory = 100 < 140 → reorder = True  

Recommended units = 140 − 100 = 40

---

### Interpretation

- Demand is stable, but exposure window increases
- System must survive longer without replenishment
- Risk comes from extended time under uncertainty

---

## Key Insight

- Demand spike = **rate risk** (faster depletion)
- Lead time delay = **time risk** (longer exposure)

Lead time delay is often more dangerous because it compounds uncertainty over a longer period.

---

## Role of Simulation

Simulation does NOT change business logic.

It only changes inputs such as:
- demand
- lead time
- inventory conditions

The same deterministic pipeline is re-executed under different conditions.

---

## Why This Matters

This layer transforms the system from:

“single decision engine”

into:

“decision system under uncertainty”

It allows evaluation of:
- robustness
- sensitivity to disruptions
- operational risk

# Step 4 — Scenario Analysis Layer

## Purpose

The scenario analysis layer converts raw outputs from the simulation into interpretable signals.

Without this layer, the system only produces numbers.
With this layer, the system provides decision intelligence.

---

## Why It Is Needed

Reorder decisions alone are not sufficient.

Example:

- baseline: reorder = True
- demand spike: reorder = True
- supplier delay: reorder = True

This does not tell us:
- which scenario is worse
- how severe the situation is
- how long inventory will last

---

## Core Metrics

### 1. Delta vs Baseline

delta = scenario_units − baseline_units

Meaning:
Additional inventory required under stress compared to normal conditions.

---

### 2. Days of Supply (DOS)

DOS = inventory / daily demand

Meaning:
How long the system can sustain demand without replenishment.

---

### 3. Stockout Risk

Derived from DOS:

- DOS < 2 → HIGH
- 2 ≤ DOS < 4 → MEDIUM
- DOS ≥ 4 → LOW

Meaning:
Likelihood of stockout under current conditions.

---

### 4. Inventory Pressure

Interpretation layer combining:

- delta
- DOS
- risk level

Meaning:
How stressed the system is relative to baseline.

---

## Example Summary

| Scenario | Units | Delta | DOS | Risk | Pressure |
|--------|------|------|-----|------|---------|
| baseline | 100 | 0 | 5 | LOW | LOW |
| demand_spike | 130 | +30 | 3.3 | MEDIUM | HIGH |
| supplier_delay | 140 | +40 | 5 | LOW | HIGH |

---

## Key Insights

- Reorder flag alone is insufficient
- Delta measures magnitude of change
- DOS measures survivability over time
- Both are required to understand risk

---

## Role in System

- Simulation → generates alternative outcomes
- Scenario Analysis → interprets those outcomes

This separation ensures:
- clean architecture
- modular design
- extensibility

---

## Strategic Value

This layer transforms the system from:

“decision calculator”

into:

“decision intelligence system”

It enables:
- risk-aware planning
- scenario comparison
- future integration with LLM-based reasoning systems


# Step 5 — Full System Meaning & Interview Framing

## What This Project Really Is

This is not a forecasting project.

This is a **deterministic supply chain decision system** that:

- uses demand forecasts as inputs
- evaluates inventory state
- produces replenishment decisions
- tests those decisions under uncertainty
- interprets outcomes into actionable insights

---

## End-to-End Flow

Forecast → Inventory → Replenishment → Coordinator → Simulation → Scenario Analysis


---

## What Makes This System Different

### 1. Decision-Centric Design

- Forecasting is not the goal
- The system produces **actions**, not predictions
- Core output:
  - reorder decision
  - recommended units

---

### 2. Deterministic Core

- All business logic is deterministic
- No black-box decision-making
- Fully explainable pipeline

---

### 3. Strict Separation of Concerns

- Forecast → demand estimation
- Inventory → state evaluation
- Replenishment → decision logic
- Coordinator → orchestration only
- Simulation → input variation
- Scenario Analysis → interpretation

This keeps the system:
- modular
- testable
- extensible

---

### 4. Simulation Layer

- Introduces uncertainty:
  - demand spikes
  - supplier delays
- Does not change logic
- Re-runs same decision pipeline

---

### 5. Scenario Analysis Layer

- Converts outputs into:
  - delta vs baseline
  - days of supply
  - stockout risk
  - inventory pressure

This enables:
- comparison across scenarios
- understanding severity
- decision prioritization

---

## Why This Is More Than Forecasting

A forecasting system answers:
> “What will demand be?”

This system answers:
> “What should we do, and how robust is that decision under uncertainty?”

---

## Why Simulation + Analysis Matter

Without simulation:
- only one scenario (baseline)
- no understanding of risk

Without analysis:
- only raw numbers
- no interpretation

Together they provide:
- robustness evaluation
- sensitivity analysis
- operational insight

---

## Example Interpretation (Simple)

- baseline → stable
- demand spike → faster depletion
- supplier delay → longer exposure

System shows:
- how much more inventory is needed (delta)
- how long we can survive (DOS)
- how severe the situation is (risk, pressure)

---

## Architectural Strength

- deterministic-first design
- clear module boundaries
- no logic duplication
- scalable for future extensions

---

## Foundation for V3 (LLM Layer)

This system is intentionally built as a **strong deterministic backbone**.

Future LLM layer will:

- explain decisions
- summarize scenarios
- assist in planning
- provide human-readable reasoning

But:

- LLM will NOT replace decision logic
- LLM will sit on top of structured outputs

---

## One-Sentence Interview Summary

This is a deterministic supply chain decision system that uses demand forecasts and inventory state to generate replenishment decisions, evaluates them under multiple scenarios, and translates results into interpretable risk signals for better operational planning.


# High-Level Implementation Map

## Overview

The system is a **deterministic supply chain decision platform** composed of:

- core decision modules
- orchestration layer
- scenario simulation and analysis layers
- extension modules
- system execution layer

The design emphasizes:
- modularity
- separation of concerns
- extensibility

---

## 1. Core Decision Modules

### demand_forecasting/
- prepares and processes demand data
- generates expected demand signals

Role:
> provides demand inputs for downstream decisions

---

### inventory/
- represents current inventory state
- computes coverage metrics (e.g., days of supply)

Role:
> evaluates current inventory position and survivability

---

### replenishment/
- decision-making module
- determines:
  - whether to reorder
  - how much to order

Role:
> core action engine of the system

---

## 2. Tool / Interface Layer

### tools/
- standardizes interfaces for domain modules
- wraps module inputs/outputs into structured contracts

Role:
> provides a clean interface between modules and orchestration

---

## 3. Orchestration Layer

### decision_coordinator/
- executes deterministic pipeline:
  forecast → inventory → replenishment
- controls sequencing of module calls
- collects outputs

Role:
> orchestrates execution without owning business logic

---

## 4. Scenario Execution Layer

### simulation_engine/
- applies scenario-based input modifications
- reruns the full decision pipeline under different conditions

Typical modifications:
- demand changes
- lead time changes
- inventory changes

Role:
> evaluates system behavior under uncertainty

---

## 5. Result Interpretation Layer

### scenario_analysis/
- compares scenario outputs against baseline
- produces interpretable metrics:
  - delta vs baseline
  - days of supply
  - stockout risk
  - inventory pressure

Role:
> converts outputs into decision intelligence

---

## 6. Extension Modules

### allocation/
- distributes inventory across locations
- handles multi-location supply scenarios

Role:
> determines where inventory should go

---

### disruption_modeling/
- defines structured disruption scenarios
- represents events such as:
  - supplier delays
  - demand spikes
  - inventory loss

Role:
> formalizes disruption inputs for simulation

---

### network_monitoring/
- tracks system behavior over time
- supports alerts and KPI monitoring

Role:
> provides operational visibility

---

## 7. System Execution Layer

### system_runner/
- main entry point for running the system
- selects execution mode:
  - simulation
  - disruption
  - allocation
- assembles inputs and executes full pipeline
- prints final results

Role:
> orchestrates end-to-end execution

---

## 8. Input Construction Layer

### system_runner/input_builder.py
- builds structured inputs for:
  - decision pipeline
  - simulation scenarios
  - allocation requests

Role:
> prepares consistent inputs for system execution

---

## 9. Data / Sample Layer

### sample_data/
- provides synthetic or sample datasets
- supports testing and development

Role:
> enables reproducible system runs without external data dependencies

---

## Core System Backbone
Forecast → Inventory → Replenishment → Coordinator
↓
Simulation → Scenario Analysis


---

## Summary

### Core (decision-making)
- demand_forecasting
- inventory
- replenishment
- decision_coordinator

### Scenario evaluation
- simulation_engine
- scenario_analysis

### Extensions
- allocation
- disruption_modeling
- network_monitoring

### Execution
- system_runner
- input_builder
- sample_data

---

## Key Insight

The system is structured to:

- produce decisions (not just predictions)
- evaluate decisions under uncertainty
- interpret results into actionable insights
- support future extensions and LLM integration
