# Supply Chain AI Lab — System Overview

## What this is

A supply chain decision system that takes demand and inventory state, produces replenishment decisions, and evaluates how those decisions behave under different scenarios.

---

## Core Pipeline

Forecast → Inventory → Replenishment → Decision Coordinator

- Forecast → estimates demand
- Inventory → translates stock into risk signals (days of supply, stockout risk)
- Replenishment → decides whether to reorder and how much
- Coordinator → runs the flow end-to-end

---

## Key Components

### Simulation Engine
Runs the same pipeline under different conditions (demand spikes, lead time delays, inventory shocks).

### Scenario Analysis
Compares baseline vs scenarios using:
- delta vs baseline
- days of supply (DOS)
- stockout risk
- inventory pressure (understock / overstock)

### Disruption Modeling
Defines structured disruption events that feed into simulation.

### Allocation
Distributes limited inventory across locations.

### Monitoring
Tracks risk signals across the system.

### LLM Explanation Layer (V3)
Explains outcomes using structured outputs.  
Does not make decisions.

### Decision Intelligence (V4)
Adds interpretation of risk and trade-offs (for example, understock vs overstock).

---

## Design Principles

- deterministic logic first
- clear module boundaries
- simulation for validation
- simple, interpretable signals
- LLM used only for explanation

---

## Why this matters

- produces decisions, not just predictions
- shows how decisions behave under stress
- keeps logic transparent and explainable