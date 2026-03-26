# Allocation Module

## Purpose

Distributes limited inventory across multiple locations.

---

## One-Line Summary

Converts limited supply into an allocation plan.

---

## Role in System

Allocation is used when supply is insufficient.

- it operates at network level  
- it does not belong to the core pipeline  
- it is triggered under shortage scenarios  

---

## Inputs

- total available inventory  
- demand per location  

---

## Outputs

- allocation per location  

---

## Core Logic

If supply ≥ demand → full allocation  

If supply < demand → proportional allocation  

---

## Service Interface

- build_allocation_request  
- run_allocation  

---

## What It Does Not Do

- no forecasting  
- no inventory computation  
- no replenishment decisions  
- no orchestration  

---

## Key Rule

Allocation distributes supply.  
It does not generate or modify supply.

---

## Mental Model

demand = need  
supply = available  
allocation = distribution  

---

## One-Line Summary

A network-level module that distributes limited inventory across locations.
