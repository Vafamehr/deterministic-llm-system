# Replenishment Module

## Purpose

Converts inventory state and expected demand into an ordering decision.

---

## One-Line Summary

Transforms inventory signals and demand into reorder decisions and quantities.

---

## Role in System

Replenishment is called by the coordinator after inventory evaluation.

* it makes decisions based on inputs
* it does not interact with forecasting directly
* it does not control execution

All outputs return to the coordinator.

---

## Inputs

* inventory position
* expected demand
* lead time
* safety stock

---

## Outputs

* reorder decision
* recommended order quantity

---

## Core Calculations

Lead time demand:

expected demand × lead time

Reorder point:

lead time demand + safety stock

Reorder condition:

inventory position < reorder point

Order quantity:

max(0, reorder point − inventory position)

---

## Service Interface

* get_reorder_point
* should_reorder
* get_order_quantity
* get_replenishment_recommendation

---

## What It Does Not Do

* no forecasting
* no inventory state computation
* no orchestration

---

## Key Rule

Replenishment decides actions based on inputs.
It does not compute demand or inventory state.

---

## One-Line Summary

A decision module that converts inventory state and demand into concrete ordering actions.
