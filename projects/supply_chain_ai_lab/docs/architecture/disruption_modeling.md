# Disruption Modeling Module

## Purpose

The disruption modeling module represents operational disruptions that occur in real-world supply chains.

Examples include:

* supplier shipment delays
* sudden demand spikes
* warehouse shutdowns
* inventory loss events
* transportation disruptions

These disruptions can significantly impact inventory availability, replenishment timing, and service levels across the network.

The purpose of this module is to **represent disruption events and translate them into operational impacts** that the simulation engine can apply deterministically.

---

## Architectural Role

The disruption modeling module acts as a **translation layer between business events and operational parameters**.

Real-world disruptions are expressed in business terms such as:

* supplier delay
* demand surge
* warehouse outage

However, the operational planning system works with numeric parameters such as:

* supplier delay days
* demand multipliers
* inventory loss
* warehouse capacity reductions

The disruption module converts disruptions into these operational effects.

---

## System Position

Within the overall system architecture, disruption modeling sits between scenario definition and simulation execution.

Supply Chain Decision Flow:

Forecast Demand
↓
Evaluate Inventory State
↓
Generate Replenishment Decision
↓
Decision Coordinator
↓
Simulation Engine
↓
Scenario Analysis

Disruption modeling feeds into the simulation engine by modifying operational inputs under hypothetical conditions.

---

## Core Concepts

### Disruption Event

Represents the real-world disruption.

Attributes include:

* disruption type
* severity
* duration
* affected node

Examples:

* supplier delay affecting Supplier A
* warehouse outage affecting DC-2
* transportation delay affecting a shipping lane

---

### Disruption Impact

Represents the operational consequences of the disruption.

These impacts are numeric parameters the planning system can apply during simulation.

Examples:

* supplier_delay_days
* demand_multiplier
* inventory_loss_units
* warehouse_capacity_multiplier
* transportation_delay_days

---

### Disruption Scenario

A disruption scenario combines:

* the disruption event
* the resulting operational impact

This allows simulation to test how planning decisions behave under different disruption conditions.

---

## Design Principles

The disruption modeling module follows several design principles:

Deterministic behavior
All impacts are expressed as numeric parameters that downstream modules apply deterministically.

Separation of concerns
Business disruption descriptions are separated from operational simulation logic.

Extensibility
The disruption model allows new disruption types to be added without modifying the core simulation engine.

Modularity
The module operates independently and integrates with the simulation engine through clearly defined interfaces.

---

## Future Extensions

Future versions of this module may include:

* probabilistic disruption modeling
* multi-node disruption propagation
* correlated disruptions
* historical disruption datasets
* scenario libraries for planning exercises

These extensions would allow the system to simulate more complex supply chain risks while maintaining deterministic planning logic.
