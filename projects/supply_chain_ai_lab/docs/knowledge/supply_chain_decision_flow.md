# Supply Chain Decision Flow

## Purpose

This document explains the core decision logic that drives the Supply Chain AI Lab.  
The goal is to understand how a supply chain system moves from **observed demand signals** to **operational replenishment decisions**.

At a high level, the system follows a simple decision pipeline:

Forecast Demand  
↓  
Evaluate Inventory State  
↓  
Generate Replenishment Recommendation

This pipeline represents the minimal operational backbone of a supply chain decision system.

---

## Why This Flow Matters

Forecasting alone does not create business value.  
Value appears when forecasts are combined with inventory visibility and replenishment logic.

A practical supply chain system must answer questions such as:

- What demand should we expect?
- Do we have enough inventory?
- How long will current stock last?
- Are we at risk of running out?
- Should we reorder?
- If we reorder, how much should we order?

The decision flow connects these questions into one operational sequence.

---

## Step 1 — Forecast Demand

The first step is estimating future demand.

Forecasting uses historical demand records for a specific SKU at a specific location and produces an estimate of future demand over a defined horizon.

Typical forecasting inputs include:

- historical demand observations
- lag features (recent demand values)
- rolling statistics (moving averages or trends)

Forecasting outputs an expected demand value that becomes an input to downstream decisions.

Without this step, inventory decisions would be based only on past observations rather than expected future demand.

---

## Step 2 — Evaluate Inventory State

Once expected demand is known, the system evaluates the current inventory position.

Inventory state is determined using operational data such as:

- on-hand inventory
- on-order inventory
- reserved inventory

From these values, the system computes metrics such as:

Inventory Position  
On-hand + On-order − Reserved

Days of Supply  
Inventory Position ÷ Expected Daily Demand

Stockout Risk  
A signal indicating whether the current inventory is likely to run out before new supply arrives.

These metrics provide visibility into the current operational situation.

---

## Step 3 — Generate Replenishment Recommendation

The final step is deciding whether replenishment should occur.

This decision is based on three main inputs:

- expected demand
- current inventory position
- supply lead time

A common replenishment rule uses a **reorder point**.

Reorder Point = Expected Demand During Lead Time + Safety Stock

If inventory position falls below the reorder point, the system recommends placing a new order.

The replenishment output typically includes:

- reorder point
- reorder decision (true or false)
- recommended order quantity

This recommendation becomes the operational output of the system.

---

## The Complete Decision Pipeline

Combining the steps produces the full decision flow:

Demand History  
↓  
Forecast Expected Demand  
↓  
Compute Inventory Metrics  
↓  
Assess Stock Risk  
↓  
Compute Reorder Point  
↓  
Generate Replenishment Recommendation

This flow represents a minimal but realistic supply chain decision loop.

---

## Relationship to the Current Project Modules

The Supply Chain AI Lab implements this decision flow using three modules:

Demand Forecasting Module  
Estimates expected demand for a SKU-location series.

Inventory Module  
Computes inventory metrics and stock risk signals.

Replenishment Module  
Generates reorder decisions and order quantities.

These modules form the operational backbone of the system.

---

## Role of the Tool Layer

The Tool Interface Layer exposes this decision pipeline to higher-level system components.

Instead of calling modules directly, future components interact through tools such as:

- forecast tool
- inventory status tool
- replenishment recommendation tool

This allows scenario engines, coordinators, or agents to execute the decision pipeline in a controlled and modular way.

---

## Mental Model

A useful mental model is a professional kitchen.

Forecasting acts like estimating how many customers will arrive.  
Inventory evaluation checks the ingredients currently available.  
Replenishment decisions determine whether new ingredients must be ordered.

Just as a restaurant must anticipate demand and manage ingredients carefully, a supply chain must continuously forecast demand, monitor inventory, and replenish stock.

---

## Key Concepts to Remember

Forecast  
An estimate of future demand based on historical data.

Inventory Position  
The true available supply once on-order and reserved stock are considered.

Days of Supply  
How long current inventory will last given expected demand.

Reorder Point  
The threshold below which a replenishment order should be placed.

Safety Stock  
Extra inventory held to protect against uncertainty in demand or supply.

---

## Summary

The supply chain decision flow connects three fundamental activities:

forecasting demand  
evaluating inventory  
making replenishment decisions

Together these steps create a continuous operational loop that allows organizations to maintain product availability while controlling inventory levels.

The Supply Chain AI Lab implements this loop as the foundation for future simulation, disruption analysis, and agent-driven decision systems.