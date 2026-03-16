# Network Monitoring Module

## Purpose

The network monitoring module provides a high-level view of supply chain health across multiple locations.

It acts as a **control tower layer**, scanning inventory conditions across the network and identifying locations at risk of stockouts.

The module helps planners answer questions such as:

* Which locations are running low on inventory?
* Which SKUs are most at risk of stockout?
* Where should planners intervene first?

Instead of computing decisions, this module **observes the network and reports risk signals**.

---

## Architectural Role

The network monitoring module is a **diagnostic layer** that sits on top of the operational decision pipeline.

Earlier modules compute operational decisions:

* forecasting predicts demand
* inventory evaluates stock state
* replenishment recommends reorder quantities
* allocation distributes limited inventory

The monitoring module aggregates these states and produces **network-level alerts**.

It does not modify decisions; it provides visibility.

---

## System Position

Within the overall system architecture, network monitoring sits at the final stage of the planning pipeline.

Planning Flow:

Forecast Demand
↓
Evaluate Inventory State
↓
Generate Replenishment Decision
↓
Simulate Disruptions
↓
Allocate Inventory
↓
Monitor Network Health

This design mirrors real-world supply chain planning systems, where monitoring layers provide dashboards and alerts for planners.

---

## Core Concepts

### Network Inventory Record

Represents the inventory state for a specific SKU at a specific location within the network.

Attributes include:

* SKU identifier
* location identifier
* on-hand inventory
* expected daily demand

This object provides the necessary information to evaluate stockout risk.

---

### Days of Supply

Days of supply estimates how long the current inventory will last given expected demand.

Formula:

```
days_of_supply = on_hand / expected_daily_demand
```

This metric is widely used in supply chain planning.

---

### Stockout Risk

A stockout risk occurs when the estimated days of supply falls below a defined threshold.

Example:

If the threshold is 3 days, any location with fewer than 3 days of supply is flagged as a risk.

---

### Network Health Report

The network health report aggregates all detected stockout risks across the network.

It represents the monitoring output of the system and highlights locations requiring attention.

---

## Design Principles

The network monitoring module follows several design principles:

Deterministic logic
Stockout risk signals are computed using simple deterministic formulas.

Separation of concerns
Monitoring logic is separated from operational planning modules.

Network-level visibility
The module focuses on summarizing risk across the entire supply chain network.

Extensibility
Future versions can support more advanced monitoring metrics.

---

## Future Extensions

Possible extensions of the monitoring module include:

* SKU-level risk ranking
* disruption impact monitoring
* network imbalance detection
* service level monitoring
* control tower dashboards
* automated alerting systems

These features would bring the system closer to real-world supply chain control tower platforms.
