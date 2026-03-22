# Simulation Engine Architecture

## Purpose

The Simulation Engine is a **scenario execution layer** that evaluates how the supply chain system behaves under different conditions.

Instead of running the decision pipeline once, it runs it multiple times with controlled input changes.

This enables testing situations such as:

- demand spikes
- supplier delays
- promotions
- inventory disruptions

---

## One-Line Summary

The Simulation Engine runs the **same decision pipeline under different scenarios to evaluate policy behavior**.

---

## Position in System

The Simulation Engine sits above the existing pipeline.

System flow:

Simulation Engine  
→ Decision Coordinator  
→ Tool Runner  
→ Domain Modules  

It does not replace or modify the pipeline.

It **reuses the exact same system logic**.

---

## Core Principle

The Simulation Engine does not implement forecasting or replenishment.

It only:

- modifies inputs  
- runs the pipeline  
- collects outputs  

This ensures:

- consistency  
- realism  
- no duplicated logic  

---

## Responsibilities

The engine performs four steps:

1. define scenarios  
2. modify inputs  
3. execute decision pipeline  
4. collect results  

---

## Scenario Examples

Baseline  
No changes  

Demand spike  
Increase demand  

Supplier delay  
Increase lead time  

Promotion  
Temporary demand boost  

Inventory shock  
Reduce available inventory  

---

## Scenario Execution Flow

For each scenario:

1. start with base inputs  

2. apply modifications  

   examples:  
   - demand × multiplier  
   - lead time increase  
   - inventory reduction  

3. call Decision Coordinator  

4. capture outputs  

5. store results  

---

## Output Structure

Each scenario produces structured results:

- scenario_name  
- forecast summary  
- inventory risk indicators  
- replenishment decision  
- service level estimate  

These allow direct comparison across scenarios.

---

## Comparison Purpose

Simulation enables questions like:

- which scenario increases stockout risk  
- which scenario triggers large orders  
- which scenario breaks policy  

This turns the system into a **decision experimentation platform**.

---

## Project Structure

```text
src/simulation_engine/
- __init__.py
- schemas.py
- scenarios.py
- service.py
- smoke_test.py
```

---

## File Responsibilities

schemas → scenario inputs and outputs  
scenarios → input modification rules  
service → scenario execution engine  
smoke_test → validation  

---

## Dependency Direction

simulation_engine  
↓  
decision_coordinator  
↓  
tools  
↓  
domain modules  

Lower layers must never depend on simulation.

---

## Design Principle

The Simulation Engine should be:

- non-intrusive  
- reusable  
- consistent with pipeline  
- easy to extend  

It must not introduce new business logic.

---

## Mental Model

pipeline = single decision  

simulation = multiple decisions under different worlds  

---

## Final View

The Simulation Engine is a **policy testing layer** that evaluates how decisions change when the environment changes.