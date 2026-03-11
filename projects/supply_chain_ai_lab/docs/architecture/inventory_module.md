# Inventory Module

This document describes the role, scope, and structure of the inventory module in the Supply Chain AI Lab.

The inventory module is the second core operational module after demand forecasting.

Its purpose is to represent the current stock state of the system in a form that later decision layers can use.

Conceptually, the system backbone becomes:

forecast → inventory state → replenishment decision

---

## Module Purpose

The inventory module answers questions such as:

- how much stock is currently available
- how much stock is already on order
- how much inventory is effectively usable
- how many days of supply remain
- whether a SKU-location is healthy or at risk

This module does not yet decide what to order.

Its job is to describe the current operational inventory state.

---

## Why Inventory Comes Before Replenishment

Replenishment decisions depend on inventory state.

Before deciding whether to reorder, the system must know:

- current on-hand stock
- incoming stock
- demand expectations
- lead time exposure
- stockout risk

This makes inventory the bridge between:

- demand forecasting
- replenishment logic

---

## Initial Scope

The first version of the inventory module should remain minimal and structured.

Initial responsibilities:

- represent inventory for one SKU at one location
- compute inventory position
- compute days of supply
- flag basic stock risk conditions

The first version does not need:

- network-wide optimization
- simulation-heavy behavior
- transfer logic
- supplier-level complexity

Those can be added later without changing the basic module boundary.

---

## Core Inventory Concepts in the Module

The initial module will focus on a few core operational quantities.

### On Hand

Physical inventory currently available at the location.

### On Order

Inventory already ordered but not yet received.

### Reserved

Inventory that is present but already committed and therefore not freely available.

### Inventory Position

A core planning quantity defined as:

inventory_position = on_hand + on_order - reserved

This is more useful than on-hand inventory alone because it reflects the effective supply pipeline.

### Days of Supply

A simple forward-looking inventory metric:

days_of_supply = on_hand / expected demand rate

In later versions, expected demand rate can come from the forecasting module.

### Stockout Risk

A simple risk signal indicating whether inventory is likely to be exhausted before replenishment arrives.

---

## Initial External Service Boundary

The inventory module should eventually expose a small stable service boundary to the rest of the system.

Examples of future service calls:

- get_inventory_state(...)
- get_inventory_position(...)
- get_days_of_supply(...)
- assess_stockout_risk(...)

These service functions should hide the internal calculation details from other modules.

This follows the same design principle used in demand forecasting:

outside systems depend on stable service contracts, not internal implementation details.

---

## Initial Data Grain

The inventory module should operate at the same operational grain used by forecasting:

SKU × Location

This keeps the supply chain modules aligned.

Forecasting predicts demand at SKU-location level.

Inventory should represent stock at the same level.

This alignment is critical because later replenishment logic will combine:

- forecasted demand
- current inventory state
- lead time assumptions

for the same SKU-location unit.

---

## Likely Internal Structure

The inventory module will likely evolve into a structure such as:

src/inventory/
- __init__.py
- schemas.py
- metrics.py
- service.py

Possible responsibilities:

- schemas.py → inventory dataclasses
- metrics.py → inventory calculations
- service.py → external callable interface

This structure mirrors the modular style already established in demand forecasting.

---

## Relationship to Other Modules

The inventory module sits downstream of forecasting and upstream of replenishment.

Conceptual flow:

demand forecasting
→ expected demand
→ inventory state evaluation
→ replenishment decision

Later it will also support:

- allocation and transfers
- disruption response
- agent reasoning
- explanation layers

---

## Design Principle

The first version of the inventory module should be:

- simple
- explicit
- stable
- easy to extend

The goal is not to build a full enterprise inventory platform immediately.

The goal is to create a clean operational state module that later decisions and agents can use reliably.