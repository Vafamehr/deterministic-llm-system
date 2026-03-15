# Supply Chain AI Lab: System Architecture

## Purpose

This document describes the **overall architecture of the Supply Chain AI Lab**.

The project simulates how a real **AI-driven retail supply chain decision platform** can be structured.

The system combines:

- demand forecasting
- inventory state evaluation
- replenishment policies
- scenario simulation
- supply disruption modeling
- constrained inventory allocation
- network monitoring
- LLM reasoning

This file provides a **top-level architectural overview**, while detailed explanations are documented in the other architecture files.

---

# System Philosophy

The Supply Chain AI Lab follows a **deterministic-first architecture**.

Operational decisions are produced by structured models and policies.  
LLMs are used only for reasoning, explanation, and interpretation.

This approach ensures the system remains:

• transparent  
• modular  
• interpretable  
• reproducible  

The architecture mirrors how modern retail supply chain platforms combine **machine learning, planning logic, and decision monitoring**.

---

# High-Level Architecture Layers

The system is organized into several conceptual layers.

## Domain Layer

Defines the core supply chain concepts used throughout the system.

Examples include:

- SKU
- location
- demand
- inventory
- replenishment policy

---

## Data & Forecasting Layer

Transforms raw retail demand observations into predictive signals.

Key responsibilities include:

- representing retail demand data
- segmenting demand into item–location time series
- generating time-series features
- producing demand forecasts

---

## Operational Decision Layer

Transforms forecasts and inventory state into operational supply chain actions.

This layer includes:

- inventory evaluation
- replenishment policy decisions

---

## Scenario & Risk Layer

Evaluates how supply chain policies behave under uncertainty.

This layer introduces:

- simulation experiments
- disruption scenarios
- supply risk modeling

---

## Network Decision Layer

Handles decisions that occur across the supply chain network.

Examples include:

- inventory allocation
- balancing supply across locations

---

## Monitoring Layer

Tracks the health of the supply chain system.

Typical monitoring metrics include:

- fill rate
- service level
- stockout risk
- forecast accuracy
- inventory turnover

---

## Reasoning Layer

The final layer uses LLMs to interpret system outputs.

Examples include:

- explaining supply chain decisions
- summarizing scenario outcomes
- identifying operational risks

---

# Core Decision Pipeline

At the heart of the system is the **supply chain decision pipeline**.


Demand Forecasting
↓
Inventory State Evaluation
↓
Replenishment Policy
↓
Simulation Engine
↓
Supply Disruption Modeling
↓
Inventory Allocation
↓
Network Metrics / Monitoring
↓
LLM Decision Copilot


Each stage enriches the system's ability to make and interpret operational decisions.

---

# Detailed System Flow

The system can also be viewed as a flow of information and decisions.


Retail Data Sources
(sales, inventory, shipments, promotions)
│
▼
Retail Data Model
(SKU × Location × Time)
│
▼
Demand Forecasting
(predict future demand)
│
▼
Inventory State
(current stock health)
│
▼
Replenishment Policy
(ordering decisions)
│
▼
Simulation Engine
(scenario experimentation)
│
▼
Supply Disruption Modeling
(lead time / supply risk)
│
▼
Allocation Engine
(network inventory balancing)
│
▼
Network Metrics
(system monitoring)
│
▼
LLM Decision Copilot
(reasoning and explanation)


This structure allows the platform to combine:

- machine learning
- supply chain planning logic
- scenario simulation
- network monitoring
- LLM reasoning

within a unified decision system.

---

# Architectural Principles

## Modular Design

Each module has a clearly defined responsibility and can evolve independently.

---

## Deterministic Decision Core

Operational decisions come from structured models and policies.  
LLMs interpret decisions rather than generating them.

---

## Scenario-Driven Evaluation

Simulation allows supply chain policies to be evaluated under uncertain conditions.

---

## Clean Dependency Direction

Dependencies flow in a strict direction.


simulation_engine
↓
decision_coordinator
↓
tools
↓
domain modules


Lower-level modules never depend on higher orchestration layers.

---

# Architecture Documents

This document serves as the **entry point for the architecture documentation**.

Supporting architecture documents include:

- **domain_scope.md** — business problems addressed by the system
- **mental_model.md** — conceptual intuition behind the supply chain system
- **retail_data_model.md** — retail data representation
- **module_map.md** — overview of system modules
- **demand_forecasting_module.md** — forecasting architecture
- **simulation_engine.md** — scenario simulation architecture

Together these documents describe the structure of the Supply Chain AI Lab.

---

# Mental Model

The system answers four fundamental operational questions:

1. What demand should we expect?
2. What inventory risk do we face?
3. What decisions should we take?
4. What happens if conditions change?

---

# Mental Hook

A modern supply chain AI platform follows this logic:

Predict demand  
→ Evaluate inventory health  
→ Decide replenishment actions  
→ Stress test decisions with simulation  
→ Manage supply disruptions  
→ Allocate constrained inventory  
→ Monitor network performance  
→ Explain outcomes with LLM reasoning