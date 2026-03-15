# Supply Chain AI Lab — Module Map

This document defines the major modules of the **Supply Chain AI Lab**.

The lab is designed as a **modular retail supply chain AI system**, where each module solves a specific business problem while sharing common data, simulation, and reasoning layers.

The system evolves from a deterministic operational backbone toward an explainable AI decision platform.

---

# Foundational Operational Modules

These modules form the **core operational decision backbone** of the supply chain system.

## 1. Demand Forecasting

Purpose:

Predict future demand at the **SKU × location × time** level.

Why it matters:

Demand forecasting generates the future signal that drives downstream supply chain planning decisions.

Typical outputs:

- demand forecasts
- forecast accuracy metrics
- demand trend summaries
- demand volatility indicators

Mental Hook:

Forecasting answers the question:  
**What demand should we expect?**

---

## 2. Inventory State

Purpose:

Represent the **current health of inventory across the network**.

Why it matters:

Before any planning decisions can be made, the system must understand the current inventory situation.

Typical outputs:

- inventory position
- days of supply
- stockout risk indicators
- service level estimates

Mental Hook:

Inventory answers the question:  
**What is our current supply risk?**

---

## 3. Replenishment Policy

Purpose:

Determine **when and how much inventory should be replenished**.

Why it matters:

Replenishment converts demand expectations and inventory state into operational ordering decisions.

Typical outputs:

- reorder point calculations
- recommended order quantities
- safety stock estimates
- replenishment alerts

Mental Hook:

Replenishment answers the question:  
**What action should we take now?**

---

# Scenario and Risk Modules

These modules evaluate how the system behaves under uncertainty.

## 4. Simulation Engine

Purpose:

Run supply chain scenarios by executing the decision pipeline under different conditions.

Examples:

- demand spikes
- promotion events
- supplier delays
- inventory shocks

Typical outputs:

- scenario comparisons
- stockout risk outcomes
- replenishment impacts
- service level changes

Mental Hook:

Simulation answers the question:  
**What happens if conditions change?**

---

## 5. Disruption / Lead Time Risk

Purpose:

Model supply chain disruptions and lead time uncertainty.

Examples:

- supplier delays
- transportation disruptions
- port congestion
- manufacturing interruptions

Typical outputs:

- disruption alerts
- lead time risk indicators
- supply reliability summaries

Mental Hook:

Disruption modeling tests whether the system is **resilient to supply uncertainty**.

---

# Network Decision Modules

These modules operate across the **entire supply chain network** rather than individual SKU-location pairs.

## 6. Allocation / Inventory Distribution

Purpose:

Determine how limited inventory should be **distributed across locations** when supply is constrained.

Why it matters:

Demand often exceeds available inventory, requiring prioritization decisions.

Typical outputs:

- inventory allocation plans
- shortage balancing decisions
- location priority rules

Mental Hook:

Allocation answers the question:  
**Who receives scarce inventory first?**

---

## 7. Network Metrics / Control Tower

Purpose:

Monitor overall supply chain performance and operational health.

Typical metrics include:

- fill rate
- service level
- stockout rate
- forecast accuracy
- inventory turnover

Typical outputs:

- system health dashboards
- operational alerts
- network performance summaries

Mental Hook:

The control tower answers the question:  
**How healthy is the supply chain network?**

---

# LLM Reasoning Layer

## 8. Supply Chain Decision Copilot

Purpose:

Use LLM reasoning to interpret deterministic system outputs and assist planners.

The LLM does not replace planning logic.  
It provides **explanations, summaries, and insights**.

Examples:

- explaining forecast changes
- summarizing disruption causes
- comparing scenario outcomes
- generating operational narratives

Typical outputs:

- operational summaries
- scenario explanations
- decision-support narratives

Mental Hook:

The LLM layer answers the question:  
**Why did the system make this decision?**

---

# Optional Advanced Extensions

These modules extend the platform but are not required for the core system.

## Assortment Optimization

Purpose:

Determine which products should be stocked at each store.

Mental Hook:

Right product in the right store.

---

## Substitution Recommendation

Purpose:

Recommend alternative products when items are unavailable.

Mental Hook:

What should replace an out-of-stock item?

---

## Promotion Optimization

Purpose:

Determine which products should be promoted and when.

Mental Hook:

Promotions intentionally shape demand.

---

## Pricing Optimization

Purpose:

Adjust prices to balance demand and inventory.

Mental Hook:

Price influences demand behavior.

---

## Supplier Intelligence

Purpose:

Evaluate supplier reliability and risk exposure.

Mental Hook:

Not all suppliers perform equally.

---

# Shared System Layers

All modules rely on shared infrastructure components.

Shared layers include:

- retail data model
- feature pipelines
- deterministic decision logic
- simulation engine
- evaluation framework
- LLM reasoning layer

These layers ensure that modules interact with the same underlying data and decision structures.

---

# Recommended Build Order

The recommended implementation order for the Supply Chain AI Lab is:

1. demand forecasting  
2. inventory state  
3. replenishment policy  
4. simulation engine  
5. disruption / lead time risk  
6. allocation / inventory distribution  
7. network metrics / control tower  
8. LLM decision copilot  

This sequence builds a **realistic supply chain decision backbone before adding LLM reasoning**.