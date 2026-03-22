# Network Monitoring Module Architecture

## Purpose

The network monitoring module provides a **network-wide view of supply chain health**.

It acts as a **control tower layer**, identifying locations and SKUs at risk.

---

## One-Line Summary

Aggregates **inventory signals → network-level risk alerts**.

---

## Architectural Role

The monitoring module is a **diagnostic layer**.

Other modules compute decisions:

- forecasting → demand  
- inventory → stock state  
- replenishment → orders  
- allocation → distribution  

Monitoring:

👉 observes outcomes and flags risks  

It does not change decisions.

---

## System Position

Final stage in planning flow:

Forecast  
→ Inventory  
→ Replenishment  
→ Simulation  
→ Allocation  
→ Monitoring  

Provides visibility after decisions are made.

---

## Core Concepts

### Network Inventory Record

Represents inventory at:

SKU × Location  

Attributes:

- sku_id  
- location_id  
- on_hand  
- expected_daily_demand  

---

### Days of Supply

```
days_of_supply = on_hand / expected_daily_demand
```

Measures how long inventory will last.

---

### Stockout Risk

Triggered when:

days_of_supply < threshold  

Example:

threshold = 3 days → flag risk  

---

### Network Health Report

Aggregated view of all risks across the network.

Highlights:

- critical locations  
- high-risk SKUs  

---

## Responsibilities

- compute days of supply  
- detect stockout risks  
- aggregate network signals  
- produce structured report  

---

## Design Principles

Deterministic → simple formulas  

Separation → monitoring ≠ decision logic  

Network focus → cross-location visibility  

Extensible → supports richer metrics later  

---

## Project Structure

```text
src/network_monitoring/
- __init__.py
- schemas.py
- metrics.py ### TODO: for future
- service.py
- smoke_test.py
```

---

## Relationship

Uses outputs from:

- inventory  
- forecast  

Feeds into:

- dashboards  
- alerts  
- analysis layers  

---

## Future Extensions

- SKU risk ranking  
- disruption monitoring  
- imbalance detection  
- service level tracking  
- alerting systems  

---

## Mental Model

inventory = local state  
monitoring = network visibility  

---

## Final View

The network monitoring module is the system’s **control tower**, providing visibility into supply chain health and highlighting where intervention is needed.