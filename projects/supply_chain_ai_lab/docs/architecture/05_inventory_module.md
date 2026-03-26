# Inventory Module

## Purpose

Represents current inventory state and converts it into operational signals.

---

## One-Line Summary

Transforms raw stock data into usable inventory signals.

---

## Role in System

Inventory is called by the coordinator after demand is computed.

* it does not make decisions
* it does not interact with forecasting directly
* it only evaluates inventory state

All outputs return to the coordinator.

---

## Inputs

* on-hand inventory
* on-order inventory
* reserved inventory
* expected demand

---

## Outputs

* inventory position
* days of supply
* stockout risk

---

## Core Calculations

Inventory position:

on_hand + on_order − reserved

Days of supply:

on_hand ÷ expected demand

---

## Service Interface

* get_inventory_position
* get_days_of_supply
* assess_stockout_risk

---

## What It Does Not Do

* no forecasting
* no replenishment decisions
* no orchestration

---

## Key Rule

Inventory evaluates state only.
It does not decide actions.

---

## One-Line Summary

A state evaluation module that converts inventory data into signals used for decision-making.
