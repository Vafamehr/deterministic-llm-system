# Disruption Modeling Module Architecture

## Purpose

The disruption modeling module represents **real-world supply chain disruptions** and converts them into operational impacts that the system can use.

Examples:

- supplier delays  
- demand spikes  
- warehouse shutdowns  
- inventory loss  
- transportation disruptions  

---

## One-Line Summary

Converts **business disruption events → operational parameters for simulation**.

---

## Architectural Role

Acts as a **translation layer** between:

business events → operational inputs  

Business terms:

- supplier delay  
- demand surge  
- warehouse outage  

Operational parameters:

- delay days  
- demand multipliers  
- inventory loss  
- capacity reductions  

---

## System Position

Sits between scenario definition and simulation execution.

Flow:

Decision Pipeline  
→ Simulation Engine  
→ (uses disruption inputs)  
→ Scenario Analysis  

It feeds modified inputs into simulation.

---

## Core Concepts

### Disruption Event

Represents the real-world issue.

Attributes:

- type  
- severity  
- duration  
- affected node  

Examples:

- supplier delay at Supplier A  
- warehouse outage at DC-2  

---

### Disruption Impact

Represents operational effects.

Examples:

- supplier_delay_days  
- demand_multiplier  
- inventory_loss_units  
- warehouse_capacity_multiplier  
- transportation_delay_days  

---

### Disruption Scenario

Combination of:

- disruption event  
- operational impact  

Used by simulation to test behavior.

---

## Responsibilities

- define disruption types  
- map events to numeric impacts  
- provide structured inputs for simulation  

Does not execute decisions or simulation.

---

## Design Principles

Deterministic → numeric, repeatable impacts  

Separation → business events separate from system logic  

Extensible → new disruption types without changes to core system  

Modular → independent component  

---

## Project Structure

```text
src/disruption_modeling/
- __init__.py
- schemas.py
- mappings.py
- service.py
```

---

## Relationship

Upstream of simulation  
Used during scenario creation  

---

## Future Extensions

- probabilistic modeling  
- multi-node propagation  
- correlated disruptions  
- historical datasets  
- scenario libraries  

---

## Mental Model

event = what happened  
impact = how system is affected  

---

## Final View

The disruption module is the **bridge between real-world events and operational simulation**, enabling realistic scenario testing without changing core decision logic.