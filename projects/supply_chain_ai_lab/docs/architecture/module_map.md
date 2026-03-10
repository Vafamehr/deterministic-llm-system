# Supply Chain AI Lab — Module Map

This document defines the major modules of the Supply Chain AI Lab.

The lab is designed as a modular retail supply chain AI system, where each module solves a specific business problem while sharing common data, simulation, and reasoning layers.

---

# Foundational Modules

These modules form the backbone of the lab.

## 1. Demand Forecasting

Purpose:

Predict future demand at the **SKU × store × time** level.

Why it matters:

Demand forecasting is the foundation of most downstream supply chain decisions.

Typical outputs:

- next-week demand forecast
- forecast uncertainty
- demand trend summaries

---

## 2. Inventory and Replenishment

Purpose:

Determine when and how much inventory should be replenished.

Why it matters:

This module converts demand expectations into operational inventory decisions.

Typical outputs:

- reorder recommendations
- safety stock logic
- stockout risk indicators

---

## 3. Inventory Simulation

Purpose:

Simulate how inventory evolves over time under demand, lead times, and replenishment rules.

Why it matters:

Simulation allows the system to test policies and understand consequences before real deployment.

Typical outputs:

- inventory trajectories
- stockout events
- service level estimates
- cost metrics

---

# Network Decision Modules

These modules operate across multiple locations in the retail network.

## 4. Allocation and Transfers

Purpose:

Decide how limited inventory should be distributed across stores or moved between locations.

Why it matters:

Demand differs across locations, and supply is often constrained.

Typical outputs:

- allocation plans
- transfer recommendations
- shortage balancing decisions

---

## 5. Disruption Intelligence

Purpose:

Detect and analyze disruptions that affect normal supply chain operations.

Examples:

- supplier delays
- transportation interruptions
- demand spikes
- inventory imbalances

Typical outputs:

- disruption alerts
- impact summaries
- scenario-based action suggestions

---

# Advanced Business Modules

These modules expand the system into richer retail decision problems.

## 6. Assortment Optimization

Purpose:

Decide which products should be stocked at which stores.

Why it matters:

Not every store should carry every SKU.

Typical outputs:

- assortment recommendations
- low-performing SKU flags
- store-specific product mix suggestions

---

## 7. Recommendation-Based Decision Support

Purpose:

Use AI and LLM-based reasoning to support decisions made by planners or operators.

Examples:

- explain forecast changes
- summarize disruption causes
- compare policy outcomes
- recommend next actions

Typical outputs:

- business summaries
- scenario comparisons
- decision-support narratives

---

# Shared System Layers

All modules should rely on shared infrastructure.

## Shared Layers

- retail data model
- feature pipelines
- simulation engine
- evaluation framework
- deterministic decision logic
- LLM reasoning layer
- bounded agent orchestration

---

# Recommended Build Order

The recommended implementation order is:

1. demand forecasting
2. inventory simulation
3. inventory and replenishment
4. allocation and transfers
5. disruption intelligence
6. assortment optimization
7. recommendation-based decision support

This order ensures that later modules build on strong foundations.