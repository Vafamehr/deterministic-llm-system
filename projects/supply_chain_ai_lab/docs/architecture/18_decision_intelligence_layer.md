# Decision Intelligence Layer

## Purpose

Classifies system outputs into a simple, interpretable state.

---

## One-Line Summary

Transforms signals into business-readable classification.

---

## Role in System

Position:

Scenario Analysis → Decision Intelligence → LLM

---

## Inputs

- days_of_supply  
- stockout_risk  
- inventory_pressure  
- overstock_risk  

---

## Outputs

- inventory_state  
- key_risk  
- reasoning_summary  

---

## Classification Logic

Priority order:

1. overstock → OVERSTOCK / EXCESS_RISK  
2. understock → UNDERSTOCK / SHORTAGE_RISK  
3. hidden risk → BALANCED / HIDDEN_RISK  
4. fallback → BALANCED / STABLE  

---

## Design Rules

- deterministic  
- rule-based  
- minimal schema  
- no ML  
- no decision-making  

---

## Role

Transforms signals into meaning.

---

## One-Line Summary

A deterministic interpretation layer that converts signals into a clear business state.
