# Replenishment Module

This document describes the role, scope, and structure of the replenishment module in the Supply Chain AI Lab.

The replenishment module is the next core operational module after demand forecasting and inventory.

Its purpose is to turn inventory state and expected demand into a simple ordering decision.

Conceptually, the system backbone becomes:

forecast → inventory state → replenishment decision

---

## Module Purpose

The replenishment module answers questions such as:

- should we reorder now
- how much should we order
- what inventory threshold should trigger replenishment
- how much buffer is needed to protect against uncertainty

This module is the first true decision layer in the operational supply chain system.

---

## Why Replenishment Comes After Inventory

Replenishment depends on both:

- expected demand
- current inventory state

Before deciding whether to place an order, the system must know:

- current on-hand inventory
- inventory already on order
- inventory position
- expected demand during lead time
- safety buffer requirements

This makes replenishment the bridge between:

- inventory state
- operational action

---

## Initial Scope

The first version of the replenishment module should remain minimal and structured.

Initial responsibilities:

- compute reorder point
- decide whether reorder is needed
- compute a simple order quantity
- return a structured replenishment recommendation

The first version does not need:

- supplier capacity constraints
- MOQ logic
- truckload optimization
- multi-echelon replenishment
- dynamic policy optimization

These can be added later without breaking the module boundary.

---

## Core Replenishment Concepts in the Module

The initial module will focus on a few core planning quantities.

### Lead Time Demand

Expected demand that will occur during replenishment lead time.

Example:

expected_daily_demand × lead_time_days

### Safety Stock

Extra inventory buffer used to protect against uncertainty.

### Reorder Point

A threshold that triggers replenishment.

Basic idea:

reorder_point = lead_time_demand + safety_stock

### Reorder Decision

If current inventory position falls below the reorder point, replenishment is needed.

### Order Quantity

A simple first policy can order enough inventory to restore stock to a target level.

---

## Initial External Service Boundary

The replenishment module should expose a small stable service boundary to the rest of the system.

Examples of future service calls:

- get_reorder_point(...)
- should_reorder(...)
- get_order_quantity(...)
- get_replenishment_recommendation(...)

These service functions should hide the internal calculation details from other modules.

This follows the same design principle already used in demand forecasting and inventory:

outside systems depend on stable service contracts, not internal implementation details.

---

## Initial Data Grain

The replenishment module should operate at the same operational grain used by forecasting and inventory:

SKU × Location

This keeps the supply chain modules aligned.

Forecasting predicts demand at SKU-location level.

Inventory tracks stock at SKU-location level.

Replenishment should produce decisions at the same level.

---

## Likely Internal Structure

The replenishment module will likely evolve into a structure such as:

src/replenishment/
- __init__.py
- schemas.py
- metrics.py
- service.py

Possible responsibilities:

- schemas.py → replenishment dataclasses
- metrics.py → reorder logic and calculations
- service.py → external callable interface

This structure mirrors the modular style already established in forecasting and inventory.

---

## Relationship to Other Modules

The replenishment module sits downstream of forecasting and inventory.

Conceptual flow:

demand forecasting
→ expected demand
→ inventory state
→ replenishment recommendation

Later it will also support:

- allocation and transfers
- disruption response
- simulation scenarios
- agent reasoning
- explanation layers

---

## Design Principle

The first version of the replenishment module should be:

- simple
- explicit
- stable
- easy to extend

The goal is not to build a full enterprise replenishment platform immediately.

The goal is to create a clean decision module that later policies, simulations, and agents can use reliably.