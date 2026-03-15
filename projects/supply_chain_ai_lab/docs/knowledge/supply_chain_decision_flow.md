# Supply Chain Decision Flow

## Purpose

This document explains the **core operational decision flow** used in the Supply Chain AI Lab.

The goal is to show **how a supply chain system converts demand signals into operational actions**.

In practical supply chain systems, forecasting, inventory monitoring, and replenishment must work together to produce decisions.

At the highest level, the system follows a simple pipeline:

Demand History
↓
Forecast Demand
↓
Evaluate Inventory State
↓
Assess Risk
↓
Generate Replenishment Recommendation

This flow represents the **minimum operational backbone of a modern supply chain decision system**.

---

# Mental Model of the System

A useful mental hook for remembering the entire system is:

Forecast
↓
Inventory
↓
Replenishment

Or in operational language:

Predict demand
↓
Measure supply
↓
Restore balance

Mental Hook:

A supply chain constantly asks one question:

**Will we run out before the next delivery arrives?**

---

# Why This Decision Flow Matters

Forecasting alone does not create business value.

Forecasts become useful only when they are combined with **inventory visibility and replenishment logic**.

A real supply chain system must continuously answer questions such as:

* What demand should we expect?
* Do we currently have enough inventory?
* How long will current stock last?
* Are we at risk of running out?
* Should we place a new order?
* If we order, how much should we order?

The decision flow connects these questions into a **structured operational process**.

---

# Step 1 — Forecast Demand

The first step estimates **future demand**.

Demand forecasting uses historical demand observations for a specific product at a specific location and produces an estimate of future demand.

Typical forecasting inputs include:

* historical demand observations
* lag features (recent demand values)
* rolling statistics (moving averages or trends)
* calendar signals (seasonality or holidays)

Forecasting produces an **expected demand estimate** that drives downstream decisions.

Example forecast output:

| sku     | location  | expected_daily_demand |
| ------- | --------- | --------------------- |
| milk_1L | store_102 | 20                    |

Without forecasting, inventory decisions would rely only on past demand rather than expected future demand.

Mental Hook:

Forecasting answers the question:

**How fast will inventory be consumed?**

---

# Step 2 — Evaluate Inventory State

After estimating expected demand, the system evaluates the **current supply state**.

Inventory state uses operational data such as:

* on-hand inventory
* on-order inventory
* reserved inventory

From these inputs the system calculates several key metrics.

---

## Inventory Position

Inventory Position represents the **true available supply pipeline**.

Formula:

Inventory Position
= On Hand + On Order − Reserved

Example:

| Metric   | Value |
| -------- | ----- |
| On-hand  | 100   |
| On-order | 40    |
| Reserved | 10    |

Inventory Position = 130

Inventory position is used instead of raw on-hand inventory because it reflects **all available supply including incoming shipments**.

Mental Hook:

Inventory Position answers:

**How much supply is actually available?**

---

## Days of Supply

Days of Supply estimates **how long the current inventory will last**.

Formula:

Days of Supply = Inventory Position ÷ Expected Daily Demand

Example:

Inventory Position = 130
Expected Daily Demand = 20

Days of Supply ≈ 6.5 days

This metric gives planners a quick estimate of how long inventory will last if demand continues at the expected rate.

Mental Hook:

Days of Supply answers:

**How many days before we run out?**

---

## Stockout Risk

Stockout risk identifies whether the system may run out of inventory before new supply arrives.

The simplest signal compares:

Days of Supply
vs
Lead Time

Rule:

If

Days of Supply < Lead Time

Then stockout risk exists.

Example:

Days of Supply = 6
Lead Time = 7

Since 6 < 7 → a stockout risk is detected.

Mental Hook:

Stockout risk occurs when **inventory will run out before the next delivery arrives**.

---

# Step 3 — Generate Replenishment Recommendation

The final step determines whether the system should **place a new order**.

Replenishment decisions depend on three inputs:

* expected demand
* inventory position
* supplier lead time

A common replenishment strategy uses a **reorder point**.

---

## Reorder Point

The reorder point represents the inventory threshold below which a new order should be placed.

Formula:

Reorder Point = Lead Time Demand + Safety Stock

Example:

Expected Daily Demand = 20
Lead Time = 7 days

Lead Time Demand = 140

Safety Stock = 40

Reorder Point = 180

Interpretation:

When inventory falls below 180 units, the system recommends placing a new order.

Mental Hook:

The reorder point is the **inventory alarm level**.

---

## Reorder Decision

The system compares the inventory position to the reorder point.

Decision rule:

If Inventory Position < Reorder Point
→ place order

Example:

Inventory Position = 150
Reorder Point = 180

150 < 180 → reorder is triggered.

Mental Hook:

Replenishment begins when **supply falls below the safe threshold**.

---

## Order Quantity

Once a reorder is triggered, the system determines **how much to order**.

In this project a simplified gap-based policy is used.

Formula:

Order Quantity = Reorder Point − Inventory Position

Example:

Reorder Point = 180
Inventory Position = 150

Order Quantity = 30

This restores inventory back to the reorder threshold.

Mental Hook:

Order quantity fills the **inventory gap**.

---

# The Complete Decision Pipeline

Combining the steps produces the full operational decision flow:

Demand History
↓
Forecast Expected Demand
↓
Compute Inventory Position
↓
Calculate Days of Supply
↓
Assess Stockout Risk
↓
Compute Reorder Point
↓
Generate Replenishment Recommendation

This pipeline represents a **minimal but realistic supply chain decision loop**.

Mental Hook:

Forecast → Inventory → Replenish

---

# Relationship to the Project Modules

The Supply Chain AI Lab implements this decision flow through three core modules.

## Demand Forecasting Module

Responsible for predicting future demand for each SKU-location series.

Output:

Expected demand estimates.

---

## Inventory Module

Responsible for computing operational inventory metrics including:

* inventory position
* days of supply
* stockout risk

This module represents the **state layer of the supply chain system**.

---

## Replenishment Module

Responsible for generating supply decisions including:

* reorder point
* reorder decision
* recommended order quantity

This module converts system signals into **operational supply actions**.

---

# Role of the Tool Interface Layer

The Tool Interface Layer exposes the decision pipeline to higher-level system components.

Instead of calling modules directly, system components interact through tools such as:

* forecast tool
* inventory status tool
* replenishment recommendation tool

Example tool execution flow:

Tool Runner
↓
Forecast Tool
↓
Inventory Tool
↓
Replenishment Tool

This architecture allows higher-level systems such as:

* scenario simulators
* decision coordinators
* disruption analyzers
* LLM-based agents

to execute the supply chain pipeline safely.

Mental Hook:

Tools provide a **controlled interface to operational logic**.

---

# Practical Analogy

A useful analogy is a **restaurant kitchen**.

Forecasting estimates how many customers will arrive.

Inventory checks how many ingredients are currently available.

Replenishment determines whether more ingredients must be ordered from suppliers.

Just as a restaurant must anticipate demand and maintain ingredients, a supply chain must continuously:

forecast demand
monitor inventory
replenish supply

---

# Key Concepts to Remember

Forecast
An estimate of future demand derived from historical data.

Inventory Position
The true available supply once on-order and reserved inventory are considered.

Days of Supply
An estimate of how long current inventory will last given expected demand.

Reorder Point
The inventory threshold below which a new order should be placed.

Safety Stock
Extra inventory held to protect against uncertainty in demand and supply.

---

# Summary

The supply chain decision flow connects three fundamental activities:

forecasting demand
evaluating inventory
making replenishment decisions

Together these steps create a **continuous operational loop** that allows organizations to maintain product availability while controlling inventory levels.

The Supply Chain AI Lab implements this loop as the **foundation for future simulation engines, disruption analysis systems, and LLM-driven decision support**.
