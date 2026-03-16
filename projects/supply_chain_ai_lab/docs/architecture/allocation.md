# Allocation Module

## Purpose

The allocation module determines how limited inventory should be distributed across multiple locations.

This module becomes necessary when available inventory is not sufficient to satisfy total demand across the network.

Examples include:

* distributing scarce inventory across stores
* allocating limited stock during a supply disruption
* prioritizing inventory across competing locations
* balancing service levels under constrained supply

The purpose of this module is to convert a limited supply situation into a clear allocation plan for each location.

---

## Architectural Role

The allocation module introduces multi-location decision making into the Supply Chain AI Lab.

Earlier modules focus mainly on local planning logic:

* demand forecasting estimates expected demand
* inventory evaluates stock position
* replenishment recommends reorder quantities

The allocation module extends this logic to network-level tradeoffs.

It answers a different kind of question:

If supply is limited, who should receive how much inventory?

This makes the system significantly more realistic because real supply chains often face constrained inventory and must make explicit allocation decisions.

---

## System Position

Within the broader system, allocation sits after inventory visibility and can be used during shortage or disruption scenarios.

A simplified planning flow becomes:

Forecast Demand
↓
Evaluate Inventory State
↓
Generate Replenishment Decision
↓
Simulate Disruptions / Shortages
↓
Allocate Limited Inventory Across Locations
↓
Analyze Service Impact

This means allocation is not replacing replenishment.
Instead, it complements replenishment when supply cannot fully satisfy demand.

---

## Core Concepts

### Location Demand

Represents the demand requirement for a location.

Examples:

* Store A needs 80 units
* Store B needs 60 units
* Store C needs 50 units

This is the input demand signal for allocation.

---

### Allocation Request

Represents the allocation problem to solve.

It includes:

* SKU identifier
* available inventory
* location-level demand list

This object defines the constrained supply decision context.

---

### Location Allocation

Represents the inventory assigned to one location.

Examples:

* Store A receives 42 units
* Store B receives 32 units
* Store C receives 26 units

This is the decision output for a single location.

---

### Allocation Result

Represents the complete allocation plan across all locations.

It contains the per-location allocation outputs for the requested SKU.

---

## Current Allocation Policy

The first implementation uses a proportional allocation policy.

Logic:

* if inventory is sufficient, all locations receive full demand
* if inventory is insufficient, each location receives inventory proportional to its share of total demand

This policy is simple, deterministic, and easy to explain.

It also provides a strong baseline for future extensions.

---

## Why This Module Matters

In real supply chains, shortage is common.

Causes include:

* supplier delays
* transportation problems
* unexpected demand spikes
* production constraints
* inventory loss

When shortages occur, supply chain systems must decide how to distribute limited inventory across locations in a rational and explainable way.

That is exactly the role of the allocation module.

---

## Design Principles

The allocation module follows these design principles:

Deterministic behavior
The same inputs always produce the same allocation outputs.

Simple baseline logic
The first version uses proportional allocation for clarity and interpretability.

Modularity
Allocation is implemented as an independent service and can later support multiple allocation strategies.

Extensibility
Future policies can be added without breaking the current architecture.

---

## Future Extensions

Future versions of the allocation module may include:

* priority-based allocation
* minimum service level rules
* region-weighted allocation
* strategic customer prioritization
* warehouse-to-store allocation constraints
* cost-aware allocation policies

These extensions would allow the system to represent more realistic operational tradeoffs across the supply chain network.
