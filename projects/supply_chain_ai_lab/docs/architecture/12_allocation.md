# Allocation Module Architecture

## Purpose

The allocation module determines how **limited inventory is distributed across multiple locations**.

It is used when total supply cannot satisfy total demand.

Examples:

- distributing scarce inventory across stores  
- allocating stock during disruptions  
- prioritizing locations under shortage  
- balancing service levels  

---

## One-Line Summary

Converts **limited supply → allocation plan across locations**.

---

## Architectural Role

Introduces **network-level decision making**.

Earlier modules focus on local logic:

- forecasting → demand  
- inventory → stock state  
- replenishment → reorder  

Allocation answers:

👉 when supply is limited, who gets how much?

---

## System Position

Allocation is used after inventory visibility, typically under shortage scenarios.

Flow:

Forecast  
→ Inventory  
→ Replenishment  
→ Disruption / Shortage  
→ Allocation  
→ Scenario Analysis  

It complements replenishment rather than replacing it.

---

## Core Concepts

### Location Demand

Demand requirement per location.

Examples:

- Store A: 80  
- Store B: 60  
- Store C: 50  

---

### Allocation Request

Defines the allocation problem:

- SKU  
- total available inventory  
- list of location demands  

---

### Location Allocation

Assigned inventory for one location.

Examples:

- Store A: 42  
- Store B: 32  
- Store C: 26  

---

### Allocation Result

Complete allocation plan across all locations.

---

## Current Policy

Proportional allocation.

Logic:

- if supply ≥ demand → full allocation  
- if supply < demand → allocate proportionally  

This is:

- simple  
- deterministic  
- interpretable  

---

## Why It Matters

Real systems frequently face shortages due to:

- supplier delays  
- demand spikes  
- transportation issues  
- production limits  
- inventory loss  

Allocation provides a **rational and explainable way to distribute scarce inventory**.

---

## Design Principles

Deterministic → same inputs produce same outputs  

Simple baseline → proportional allocation  

Modular → independent service  

Extensible → supports future policies  

---

## Project Structure

```text
src/allocation/
- __init__.py
- schemas.py
- policy.py
- service.py
- smoke_test.py
```

---

## Relationship to Other Modules

Uses inputs from:

- demand (forecast or scenario)  
- inventory availability  

Feeds into:

- scenario analysis  
- service level evaluation  
- decision reasoning  

---

## Future Extensions

- priority-based allocation  
- minimum service level rules  
- regional weighting  
- customer prioritization  
- warehouse constraints  
- cost-aware policies  

---

## Mental Model

demand = who needs inventory  
supply = what we have  
allocation = how we distribute it  

---

## Final View

The allocation module is the system’s **network decision layer**, distributing limited inventory across locations in a consistent and explainable way.