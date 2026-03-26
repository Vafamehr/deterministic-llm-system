# Supply Chain AI Lab

A modular supply chain decision system that simulates demand, evaluates inventory, generates replenishment decisions, and analyzes risk under different scenarios.

---

## Overview

This project implements a deterministic supply chain pipeline with layered extensions for simulation, scenario analysis, and interpretation.

Core flow:

Forecast → Inventory → Replenishment → Decision Coordinator  
→ Simulation → Scenario Analysis → Decision Intelligence → LLM Explanation

The system reflects how real supply chain decisions are produced, evaluated, and interpreted in practice.

---

## What the System Does

For a given SKU and location, the system:

- predicts demand using a forecasting model  
- evaluates inventory position and coverage  
- determines reorder decisions and quantities  
- simulates alternative scenarios (e.g., demand spikes, supplier delays)  
- compares outcomes against a baseline  
- classifies inventory state and dominant risk  
- generates explanations grounded in structured outputs  

---

## Architecture

### Decision Backbone

- Forecasting  
- Inventory  
- Replenishment  
- Decision Coordinator  

### Simulation & Scenario Layer

- Simulation Engine  
- Scenario Analysis  
- Disruption Modeling  

### Network Extensions

- Allocation  
- Monitoring  

### Intelligence Layer

- System Output Contract  
- Decision Intelligence (deterministic classification)  
- LLM Explanation Layer (optional, non-decision-making)  

---

## Design Principles

- Deterministic-first: all decisions are rule-based and reproducible  
- Modular: each component has a clear and isolated responsibility  
- Simulation-driven: decisions are evaluated under multiple scenarios  
- Layered design: computation, interpretation, and explanation are separated  
- Bounded LLM usage: explanations only, never decision-making  

---

## Example Output

Each scenario produces structured signals:

- reorder  
- recommended_units  
- days_of_supply  
- stockout_risk  
- delta_vs_baseline  
- inventory_pressure  

These are further interpreted into:

- inventory_state (UNDERSTOCK / BALANCED / OVERSTOCK)  
- key_risk (SHORTAGE / EXCESS / HIDDEN / STABLE)  

---

## How to Run

```bash
cd src
python run_system.py