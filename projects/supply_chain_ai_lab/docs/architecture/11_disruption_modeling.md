# Disruption Modeling

## Purpose

Represents real-world supply chain disruptions and converts them into inputs that the system can use.

---

## One-Line Summary

Transforms business events into numeric parameters for simulation.

---

## Role in System

Used during scenario setup before simulation runs.

Flow:

Disruption Modeling → Simulation → Coordinator → Modules

It does not execute the pipeline.
It prepares inputs for it.

---

## Core Mapping

event → impact

Examples:

* supplier delay → increased lead time
* demand spike → demand multiplier
* inventory loss → reduced available stock

---

## Components

### Disruption Event

Describes what happened.

* type
* severity
* duration
* affected node

---

### Disruption Impact

Defines how the system is affected.

* demand multiplier
* lead time adjustment
* inventory loss
* capacity change

---

### Disruption Scenario

Combines:

* event
* impact

This is what simulation consumes.

---

## Responsibilities

* define disruption types
* map events to operational impacts
* generate structured inputs for simulation

---

## What It Does Not Do

* does not run simulation
* does not execute decisions
* does not modify pipeline logic

---

## Project Structure

```text
src/disruption_modeling/
- schemas.py
- service.py
- mappings.py
```

---

## Dependency Direction

disruption → simulation → coordinator → modules

---

## Design Rules

* deterministic
* modular
* extensible
* separate from core logic

---

## Mental Model

event = what happened
impact = how the system reacts

---

## One-Line Summary

A translation layer that converts real-world disruptions into simulation-ready inputs.
