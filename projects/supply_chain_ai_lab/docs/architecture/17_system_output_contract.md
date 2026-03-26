## Purpose

Defines the structured outputs produced by the system.

---

## One-Line Summary

A consistent schema for decision and risk signals.

---

## Output Fields

- scenario_name  
- reorder  
- recommended_units  
- days_of_supply  
- stockout_risk  
- delta_vs_baseline  
- inventory_pressure  

---

## Signal Meaning

Reorder → decision flag  

Recommended Units → order quantity  

Days of Supply → inventory coverage  

Stockout Risk → categorical risk  

Delta vs Baseline → change vs normal  

Inventory Pressure → urgency signal  

---

## Design Rules

- deterministic  
- structured  
- comparable across scenarios  
- independent of LLM  

---

## Role in System

Used by:

- scenario comparison  
- monitoring  
- decision intelligence  
- LLM explanation  

---

## One-Line Summary

A structured output layer that standardizes decision and risk signals.

---
