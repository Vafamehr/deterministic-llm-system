# Replenishment Module Architecture

## Purpose

The replenishment module converts **inventory state and expected demand into an ordering decision**.

It is the first true **decision layer** in the system:

forecast → inventory state → replenishment decision

---

## One-Line Summary

The replenishment module transforms **inventory state + expected demand → reorder decision and quantity**.

---

## Module Role

The replenishment module answers:

- should we reorder
- how much should we order
- when should replenishment be triggered
- how much buffer is needed

It sits between:

- inventory (state)
- operational action (ordering)

---

## Why Replenishment Comes After Inventory

Replenishment depends on both:

- expected demand
- inventory state

Before making a decision, the system must know:

- on-hand inventory
- on-order inventory
- inventory position
- demand during lead time
- buffer requirements

Inventory provides the **state**, replenishment provides the **action**.

---

## Initial Scope

Keep the first version minimal and clear.

Responsibilities:

- compute reorder point
- determine reorder condition
- compute order quantity
- return structured recommendation

Out of scope:

- supplier constraints
- MOQ logic
- truckload optimization
- multi-echelon systems
- dynamic policies

---

## Core Concepts

### Lead Time Demand

Demand expected during replenishment lead time:

lead_time_demand = expected_daily_demand × lead_time_days

---

### Safety Stock

Buffer to protect against:

- demand variability
- forecast error
- delays

---

### Inventory Position

Represents true available supply:

inventory_position = on_hand + on_order − reserved

Used instead of on-hand because it reflects pipeline supply.

---

### Reorder Point

Threshold that triggers replenishment:

reorder_point = lead_time_demand + safety_stock

---

### Reorder Decision

Trigger condition:

inventory_position < reorder_point

---

### Order Quantity

Simple gap-based policy:

order_quantity = max(0, reorder_point − inventory_position)

This restores inventory to the reorder threshold.

---

## External Service Boundary

Expose stable service functions:

- `get_reorder_point(...)`
- `should_reorder(...)`
- `get_order_quantity(...)`
- `get_replenishment_recommendation(...)`

Other modules should depend only on these interfaces.

---

## Data Grain

Operates at:

SKU × Location

Aligned with:

- forecasting
- inventory

This ensures consistent decision-making across modules.

---

## Internal Structure

```text
src/replenishment/
- __init__.py
- schemas.py
- metrics.py
- service.py
- smoke_test.py
```

Responsibilities:

- schemas → data contracts
- metrics → calculations and logic
- service → external interface
- smoke_test → validation

---

## Relationship to Other Modules

Position in system:

forecasting  
→ expected demand  
→ inventory state  
→ replenishment decision  

Supports later:

- allocation
- transfers
- disruption handling
- simulation
- reasoning

---

## Design Principle

The module should be:

- simple
- explicit
- stable
- extensible

Focus on clarity over completeness.

---

## Mental Model

forecast → what demand is coming  
inventory → what we have  
replenishment → what we should do  

---

## Final View

The replenishment module is the system’s **action engine**.

It converts inventory state and demand expectations into concrete ordering decisions.