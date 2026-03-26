# Decision Coordinator

## Purpose

Orchestrates the core decision pipeline by connecting forecasting, inventory, and replenishment into a single flow.

---

## One-Line Summary

Coordinates module execution to produce a complete decision output.

---

## Role in System

The coordinator is the central execution layer of the system.

It does not compute logic itself.  
It calls modules in sequence and passes outputs between them.

Flow:

forecast → inventory → replenishment

---

## Responsibilities

- call forecasting service  
- pass expected demand to inventory  
- compute inventory state  
- pass signals to replenishment  
- return structured decision output  

---

## Execution Flow

1. Forecast Module  
   → produces expected demand  

2. Inventory Module  
   → computes inventory position  
   → computes days of supply  
   → assesses stockout risk  

3. Replenishment Module  
   → computes reorder point  
   → determines reorder decision  
   → computes order quantity  

---

## Inputs

- forecast input  
- inventory record  
- replenishment parameters  

---

## Outputs

- reorder decision  
- recommended units  
- inventory signals  

---

## Design Rules

- no business logic  
- no calculations  
- no state mutation  
- only orchestration  

---

## Why It Exists

Without a coordinator:

- modules are disconnected  
- execution flow is unclear  
- system cannot scale  

---

## Mental Model

modules = tools  
coordinator = conductor  

---

## One-Line Summary

A pure orchestration layer that connects modules into a working decision system.