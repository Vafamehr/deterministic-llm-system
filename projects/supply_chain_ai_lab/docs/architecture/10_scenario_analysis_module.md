# Scenario Analysis Module Architecture

## Purpose

The Scenario Analysis module converts **simulation outputs into structured, interpretable comparisons**.

While the Simulation Engine generates different possible worlds, this module explains **how those worlds differ from baseline behavior**.

---

## One-Line Summary

Transforms **simulation results → comparable insights relative to baseline**.

---

## Position in System

Forecast → Inventory → Replenishment → Coordinator → Simulation → Scenario Analysis  

Simulation generates outcomes.  
Scenario Analysis interprets them.

---

## Input

Receives a `SimulationResult`:

- baseline input  
- baseline decision output  
- list of scenario results  

Each scenario includes:

- scenario definition  
- modified inputs  
- resulting decision output  

---

## Core Responsibilities

### 1. Identify Baseline

Baseline decision output is the reference point.

---

### 2. Extract Decisions

From each scenario:

- reorder decision  
- recommended order quantity  

---

### 3. Compute Deltas

delta = scenario_units − baseline_units  

Measures impact relative to baseline.

---

### 4. Produce Structured Output

Returns `ScenarioAnalysisResult` with rows:

- scenario name  
- reorder decision  
- recommended units  
- delta vs baseline  

Example:

| Scenario | Reorder | Units | Delta |
|----------|--------|-------|--------|
| baseline | True   | 75    | 0      |
| demand_spike | True | 110 | +35 |
| supplier_delay | True | 140 | +65 |

---

## Design Principles

Deterministic → no new modeling  
No mutation → read-only  
Separation → simulation ≠ analysis  
Minimal dependencies → lightweight module  

---

## Project Structure

```text
src/scenario_analysis/
- __init__.py
- schemas.py
- service.py
- smoke_test.py
```

---

## Relationship

Downstream of simulation  
Upstream of reporting and reasoning  

---

## Future Extensions

- service level  
- stockout risk  
- inventory cost  
- days of supply  
- disruption severity  

---

## Role in AI Layer

Provides structured inputs for:

- explanations  
- summaries  
- recommendations  

---

## Mental Model

simulation = generate outcomes  
analysis = compare outcomes  

---

## Final View

The Scenario Analysis module is the **interpretation layer**, turning scenario results into clear, comparable insights.