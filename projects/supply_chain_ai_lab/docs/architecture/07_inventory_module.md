# Inventory Module Architecture

## Purpose

The inventory module represents the **current operational stock state** of the system.

It is the second core module in the decision backbone:

forecast → inventory state → replenishment decision

Its role is not to decide what to order.  
Its role is to describe inventory in a form that downstream modules can use.

---

## One-Line Summary

The inventory module converts raw stock information into a **usable operational inventory state** for downstream decision-making.

---

## Module Role

The inventory module answers questions such as:

- how much stock is currently available
- how much stock is already on order
- how much inventory is effectively usable
- how many days of supply remain
- whether a SKU-location is healthy or at risk

It sits between:

- forecasting
- replenishment

This makes it the **bridge between expected demand and operational action**.

---

## Why Inventory Comes Before Replenishment

Replenishment depends on inventory state.

Before the system can decide whether to reorder, it must understand:

- current on-hand stock
- incoming stock
- reserved stock
- expected demand
- stockout exposure

Without this layer, replenishment logic would act on incomplete context.

---

## Initial Scope

The first version should stay intentionally narrow.

Responsibilities:

- represent inventory for one SKU at one location
- compute inventory position
- compute days of supply
- flag basic stock risk

Out of scope for now:

- network-wide optimization
- transfer logic
- supplier-level complexity
- simulation-heavy behavior

These can be added later without changing the module boundary.

---

## Core Concepts

### On Hand
Physical inventory currently available at the location.

### On Order
Inventory already ordered but not yet received.

### Reserved
Inventory that exists physically but is already committed.

### Inventory Position
A planning metric defined as:

inventory_position = on_hand + on_order - reserved

This is more useful than on-hand alone because it reflects usable and incoming supply.

### Days of Supply
A forward-looking coverage metric:

days_of_supply = on_hand / expected demand rate

Later versions can use forecast-derived demand as the demand rate.

### Stockout Risk
A basic signal indicating whether inventory may run out before replenishment arrives.

---

## Data Grain

The inventory module operates at the same grain as forecasting:

SKU × Location

This alignment is critical because downstream replenishment combines:

- forecasted demand
- inventory state
- lead time assumptions

for the same operational unit.

---

## External Service Boundary

The module should expose a small, stable service interface.

Examples:

- `get_inventory_state(...)`
- `get_inventory_position(...)`
- `get_days_of_supply(...)`
- `assess_stockout_risk(...)`

Other modules should depend on these service functions, not on internal calculations.

This preserves modularity and clean system boundaries.

---

## Internal Structure

```text
src/inventory/
- __init__.py
- schemas.py
- metrics.py
- service.py
```

Responsibilities:

- `schemas.py` → inventory dataclasses
- `metrics.py` → inventory calculations
- `service.py` → external interface

This keeps the module simple, explicit, and extensible.

---

## Relationship to Other Modules

The inventory module sits downstream of forecasting and upstream of replenishment.

Conceptual flow:

forecasting  
→ expected demand  
→ inventory evaluation  
→ replenishment decision  

Later it can also support:

- allocation
- transfers
- disruption handling
- agent reasoning
- explanation layers

---

## Design Principle

The inventory module should be:

- simple
- explicit
- stable
- easy to extend

The goal is not to build a full inventory platform immediately.

The goal is to build a clean operational state module that later decisions can rely on.

---

## Mental Model

forecast tells us what demand is coming  
inventory tells us how exposed we are  
replenishment decides what to do  

---

## Final View

The inventory module is the system’s **state interpreter**.

It converts raw stock quantities into operational signals that make replenishment and later decision layers possible.