# Network Monitoring

## Purpose

Provides network-level visibility into inventory health.

---

## One-Line Summary

Aggregates inventory signals into risk indicators.

---

## Role in System

Monitoring runs after decisions.

- it does not influence execution  
- it does not modify inputs  
- it only observes system state  

---

## Inputs

- inventory signals  
- expected demand  

---

## Outputs

- days of supply  
- stockout risk  
- flagged SKU-location pairs  

---

## Core Logic

Days of supply:

on_hand ÷ expected demand  

Stockout risk:

triggered when days of supply < threshold  

---

## Service Interface

- compute_days_of_supply  
- detect_stockout_risk  
- build_network_report  

---

## What It Does Not Do

- no forecasting  
- no replenishment  
- no allocation  
- no orchestration  

---

## Key Rule

Monitoring observes outcomes.  
It does not make decisions.

---

## Mental Model

inventory = local state  
monitoring = system visibility  

---

## One-Line Summary

A diagnostic layer that surfaces inventory risk across the network.

---

## STATUS AFTER THIS STEP

Core pipeline ✔  
Simulation / analysis / disruption ✔  
Modules ✔  
Allocation / monitoring ✔  

---