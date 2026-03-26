# System Walkthrough

## What the system does

This is a deterministic supply chain decision system.

Given demand and inventory state, it:
- produces replenishment decisions
- evaluates those decisions under different scenarios
- summarizes risk using simple signals

Forecasting is only an input.

---

## End-to-end flow

Forecast → Inventory → Replenishment → Coordinator → Simulation → Scenario Analysis

---

## Inputs

- historical demand
- current inventory (on hand, on order, reserved)
- lead time
- safety stock / configuration

---

## Outputs

- reorder (True / False)
- recommended_units
- days_of_supply (DOS)
- stockout_risk
- delta_vs_baseline
- inventory_pressure (understock / overstock)

---

## Module roles

### Forecast
Produces expected demand (signal only).

### Inventory
Converts inventory into:
- inventory_position
- days_of_supply
- stockout risk

### Replenishment
Core decision logic:
- reorder or not
- how much to order

### Coordinator
Runs modules in sequence.  
No business logic inside.

### Simulation
Applies input changes:
- demand shifts
- lead time changes
- inventory shocks

Then re-runs the same pipeline.

### Scenario Analysis
Turns raw outputs into comparable signals:
- delta vs baseline
- DOS
- risk level
- inventory pressure

---

## Numerical example (baseline)

Assume:
- inventory = 100
- demand = 20/day
- lead time = 3 days
- safety stock = 40

### Inventory

DOS = 100 / 20 = 5 days

---

### Replenishment

Lead time demand = 20 × 3 = 60  
Reorder point = 60 + 40 = 100  

Inventory = 100 → reorder = True  

Recommended units = 100 − 100 = 0

Interpretation:
System is exactly at the boundary.

---

## Scenario behavior

### Demand spike

Demand = 30/day

- DOS = 100 / 30 ≈ 3.3
- lead time demand = 90
- reorder point = 130
- recommended_units = 30

Driver: faster consumption

---

### Supplier delay

Lead time = 5 days

- DOS = 5 (unchanged)
- lead time demand = 100
- reorder point = 140
- recommended_units = 40

Driver: longer exposure window

---

### Key difference

- demand spike → rate risk
- delay → time risk

---

## Scenario analysis signals

### Delta vs baseline
Extra units needed compared to normal case.

---

### Days of Supply (DOS)
How long inventory lasts without replenishment.

---

### Stockout risk
Simple thresholds on DOS:
- <2 → HIGH
- 2–4 → MEDIUM
- ≥4 → LOW

---

### Inventory pressure

Combines:
- delta
- DOS
- risk

Also captures:
- understock pressure (risk of running out)
- overstock pressure (excess coverage)

---

## Example summary

| Scenario        | Units | Delta | DOS | Risk   | Pressure |
|----------------|------|------|-----|--------|----------|
| baseline       | 100  | 0    | 5   | LOW    | LOW      |
| demand_spike   | 130  | +30  | 3.3 | MEDIUM | HIGH     |
| supplier_delay | 140  | +40  | 5   | LOW    | HIGH     |

---

## Implementation map

### Core modules
- demand_forecasting/
- inventory/
- replenishment/
- decision_coordinator/

### Scenario layer
- simulation_engine/
- scenario_analysis/

### Extensions
- allocation/
- disruption_modeling/
- network_monitoring/

### Execution
- system_runner/
- input_builder/
- sample_data/

---

## One-line summary

A deterministic system that turns demand and inventory into replenishment decisions, then tests and explains those decisions under changing conditions.