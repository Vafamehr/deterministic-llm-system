# Scenario Analysis

## Purpose

Converts simulation outputs into comparable, decision-facing results.

---

## One-Line Summary

Compares scenario outcomes against baseline using a small set of operational signals.

---

## Role in System

The scenario analysis layer sits immediately after simulation.

Flow:

Simulation → Scenario Analysis

Simulation generates outcomes.
Scenario analysis turns those outcomes into interpretable comparisons.

---

## Inputs

Receives:

* baseline result
* list of scenario results

Each result already contains the outputs of the coordinator-driven pipeline.

---

## Core Outputs

For each scenario, the module exposes:

* reorder
* recommended units
* delta vs baseline
* days of supply
* stockout risk
* inventory pressure

---

## Key Computation

Delta vs baseline is computed as:

scenario units − baseline units

This shows how much more or less inventory is needed relative to normal conditions.

---

## Signals

### Days of Supply

How long current inventory can support expected demand.

### Stockout Risk

Categorical risk signal derived from inventory state.

### Inventory Pressure

A simplified interpretation layer built on top of coverage and risk signals.

It helps distinguish:

* understock pressure
* overstock pressure
* relatively balanced conditions

---

## What It Does Not Do

* does not run scenarios
* does not modify inputs
* does not make new decisions
* does not introduce new business logic

Its job is interpretation.

---

## Project Structure

```text
src/scenario_analysis/
- schemas.py
- service.py
- smoke_test.py
```

---

## Design Rules

* deterministic
* read-only
* lightweight
* downstream of simulation

---

## Role for the LLM Layer

This module provides the structured signals used later for explanation and comparison.

---

## Mental Model

simulation = generate outcomes
analysis = compare outcomes

---

## One-Line Summary

A lightweight interpretation layer that turns simulation results into baseline-relative comparisons.
