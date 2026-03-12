# Replenishment Module

This document describes the role, scope, and structure of the replenishment module in the Supply Chain AI Lab.

The replenishment module is the next core operational module after demand forecasting and inventory.

Its purpose is to turn inventory state and expected demand into a simple ordering decision.

Conceptually, the system backbone becomes:

forecast → inventory state → replenishment decision

---

# Module Purpose

The replenishment module answers questions such as:

- should we reorder now
- how much should we order
- what inventory threshold should trigger replenishment
- how much buffer is needed to protect against uncertainty

This module is the first true **decision layer** in the operational supply chain system.

---

# Why Replenishment Comes After Inventory

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

inventory state → operational action

---

# Initial Scope

The first version of the replenishment module remains intentionally minimal.

Initial responsibilities:

- compute reorder point
- decide whether reorder is needed
- compute a simple order quantity
- return a structured replenishment recommendation

The first version does **not** include:

- supplier capacity constraints
- MOQ logic
- truckload optimization
- multi-echelon replenishment
- dynamic policy optimization

These can be added later without breaking the module boundary.

---

# Core Replenishment Concepts

## Lead Time Demand

Expected demand that will occur during replenishment lead time.

Formula:

lead_time_demand = expected_daily_demand × lead_time_days

Example:

1 kg per day demand  
7 day lead time

Lead time demand = 7 kg

---

## Safety Stock

Extra inventory buffer used to protect against uncertainty.

Safety stock protects against:

- demand variability
- delivery delays
- forecast error

---

## Inventory Position

Inventory position represents the **true available supply**.

In real supply chain systems:

inventory_position = on_hand + on_order − backorders

This value is used instead of on-hand inventory because it reflects inventory that has already been ordered but not yet received.

---

## Reorder Point

A threshold that triggers replenishment.

Formula:

reorder_point = lead_time_demand + safety_stock

Example:

lead_time_demand = 7  
safety_stock = 3

reorder_point = 10

When inventory position drops below this level, a reorder should be triggered.

---

## Reorder Decision

Replenishment is triggered when:

inventory_position < reorder_point

---

## Order Quantity

The initial policy used in this project calculates the **gap to the reorder point**.

order_quantity = max(0, reorder_point − inventory_position)

This means the system orders enough inventory to restore the inventory position back to the reorder threshold.

More advanced systems often use **order-up-to policies**, which replenish inventory to a higher target level.

---

# Initial External Service Boundary

The replenishment module exposes a stable service interface to the rest of the system.

Example service calls:

get_reorder_point(...)

should_reorder(...)

get_order_quantity(...)

get_replenishment_recommendation(...)

These service functions hide the internal calculation logic from other modules.

This follows the design principle used throughout the system:

outside systems depend on **stable service contracts**, not internal implementation details.

---

# Initial Data Grain

The replenishment module operates at the same operational grain used by forecasting and inventory:

SKU × Location

This alignment ensures consistent system behavior:

Forecasting predicts demand at SKU-location level.

Inventory tracks stock at SKU-location level.

Replenishment produces decisions at the same level.

---

# Internal Module Structure

src/replenishment/

__init__.py  
schemas.py  
metrics.py  
service.py  
smoke_test.py

Responsibilities:

schemas.py → replenishment dataclasses  
metrics.py → reorder calculations and decision logic  
service.py → external callable interface  
smoke_test.py → quick functional test of the module

---

# Relationship to Other Modules

The replenishment module sits downstream of forecasting and inventory.

Conceptual system flow:

demand forecasting → expected demand → inventory state → replenishment recommendation

Later the module will also support:

- allocation decisions
- inventory transfers
- disruption response
- simulation scenarios
- agent reasoning
- explanation layers

---

# Design Principle

The first version of the replenishment module should be:

- simple
- explicit
- stable
- easy to extend

The goal is not to build a full enterprise replenishment platform immediately.

The goal is to create a clean decision module that later policies, simulations, and AI agents can use reliably.