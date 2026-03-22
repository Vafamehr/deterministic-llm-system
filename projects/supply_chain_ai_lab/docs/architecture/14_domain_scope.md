# Retail Domain Scope

## Purpose

Defines the **business context** for the Supply Chain AI Lab.

The system models a **retail supply chain decision environment** where data, decisions, and disruptions interact.

---

## One-Line Summary

A simplified retail system modeling **demand → inventory → decisions → risk → outcomes**.

---

## Domain Scope

The system represents a retail environment with:

- products (SKUs)  
- stores (demand points)  
- warehouses / distribution centers  
- time-evolving customer demand  
- multi-location inventory  
- replenishment flows  
- supply chain disruptions  

---

## Core Business Problems

The system focuses on essential supply chain problems:

- demand forecasting  
- inventory evaluation  
- replenishment planning  
- scenario simulation  
- disruption modeling  
- inventory allocation  
- network monitoring  
- decision interpretation  

These form a **complete decision loop**.

---

## Core Entities

Key objects in the system:

- sku → product  
- store → demand location  
- warehouse → supply node  
- date / week → time dimension  
- sales → observed demand  
- inventory_position → available inventory  
- shipment → inventory movement  
- lead_time → replenishment delay  
- promotion → demand driver  
- stockout_event → unmet demand  

---

## Decision Context

The system supports decisions such as:

- expected demand  
- stockout risk  
- replenishment timing and quantity  
- inventory distribution across locations  
- response to disruptions  
- behavior under different scenarios  

These decisions combine:

- machine learning  
- deterministic policies  
- simulation  
- monitoring  
- reasoning  

---

## Decision Layers

### Demand Layer

What demand should we expect?

- forecasting  
- seasonality  
- promotions  
- anomaly detection  

---

### Inventory Layer

What is our inventory state?

- inventory position  
- stockout risk  
- safety stock  

---

### Operational Layer

What actions should we take?

- replenishment  
- ordering  
- inventory balancing  

---

### Scenario & Risk Layer

What happens if conditions change?

- demand spikes  
- supplier delays  
- disruptions  
- inventory shocks  

---

## Why Retail

Retail provides:

- realistic decision problems  
- strong ML relevance  
- clear module interactions  
- natural extension to AI systems  

---

## Mental Model

demand → what is coming  
inventory → what we have  
decision → what we do  
simulation → what could happen  

---

## Final View

The retail domain defines the **problem space**, grounding the system in real-world supply chain decisions and enabling meaningful modeling, simulation, and analysis.