# Decision Intelligence Layer (V4)

## Purpose

The Decision Intelligence Layer (V4) sits **after Scenario Analysis** and provides a structured, deterministic interpretation of the system state.

It does NOT:
- perform optimization
- make execution decisions
- replace replenishment logic
- use LLMs

It ONLY:
- classifies inventory condition
- identifies dominant risk
- explains the situation in simple deterministic terms

---

## Position in Architecture

Pipeline flow:

Forecast → Inventory → Replenishment → Decision Coordinator  
→ Simulation Engine → Scenario Analysis  
→ **Decision Intelligence (V4)** ← NEW  
→ LLM Explanation Layer (optional)

---

## Why This Layer Exists

Upstream outputs are correct but fragmented:

Example signals:
- days_of_supply = 0.75
- stockout_risk = HIGH
- inventory_pressure = HIGH
- overstock_risk = LOW

These require interpretation.

V4 converts them into a **single business-readable state**.

---

## Core Output Schema

Each scenario (or baseline) produces:

- `inventory_state`
- `key_risk`
- `reasoning_summary`

### InventoryState
- UNDERSTOCK
- BALANCED
- OVERSTOCK

### KeyRisk
- SHORTAGE_RISK
- EXCESS_RISK
- HIDDEN_RISK
- STABLE

### reasoning_summary
Short deterministic explanation of the state.

---

## Example

Input signals:

- days_of_supply = 0.75
- stockout_risk = HIGH
- inventory_pressure = HIGH
- overstock_risk = LOW

Output:

- inventory_state = UNDERSTOCK
- key_risk = SHORTAGE_RISK
- reasoning_summary = "Low days of supply and high stockout risk indicate an understock condition."

---

## Design Principles

- Deterministic rule-based logic
- No ML / no RL / no heuristics explosion
- Minimal schema (3 fields only)
- One output per scenario row
- Strict separation from upstream modules

---

## Responsibility Boundaries

| Layer | Responsibility |
|------|---------------|
| Inventory | Raw metrics (DoS, inventory position) |
| Scenario Analysis | Interpreted signals (pressure, overstock risk) |
| **Decision Intelligence** | State classification + reasoning |
| LLM Layer | Natural language explanation |

---

## Key Insight

V4 transforms:

**Signals → Meaning**

This is the first layer that behaves like a business analyst rather than a calculator.


## Decision Logic (V4 Classification Rules)

The Decision Intelligence Layer applies a simple priority-based classification over interpreted signals.

### Rule Order (highest priority first)

1. **Overstock dominates**
   - Condition: `overstock_risk == HIGH`
   - Output:
     - inventory_state = OVERSTOCK
     - key_risk = EXCESS_RISK

2. **Understock dominates**
   - Condition: `inventory_pressure == HIGH`
   - Output:
     - inventory_state = UNDERSTOCK
     - key_risk = SHORTAGE_RISK

3. **Hidden risk**
   - Condition:
     - inventory_pressure != HIGH
     - overstock_risk != HIGH
     - stockout_risk == HIGH
   - Output:
     - inventory_state = BALANCED
     - key_risk = HIDDEN_RISK

4. **Stable (fallback)**
   - All other cases
   - Output:
     - inventory_state = BALANCED
     - key_risk = STABLE

---

## Key Design Choice

This layer does NOT enumerate all signal combinations.

Instead, it uses **priority-based classification**:
- dominant condition determines the outcome
- avoids combinatorial explosion
- keeps logic simple and interpretable

---

## Interpretation Behavior

- `UNDERSTOCK` captures urgent shortage situations (low DoS)
- `OVERSTOCK` captures excess inventory situations (high DoS)
- `HIDDEN_RISK` captures non-obvious risk (moderate DoS but elevated stockout risk)
- `STABLE` captures normal operating conditions

---

## Important Constraint

This layer:
- consumes only interpreted signals (not raw metrics)
- does not modify upstream logic
- produces one classification per scenario row


## Integration into Existing Flow

V4 is attached after Scenario Analysis.

Integration pattern:

1. Scenario Analysis computes interpreted signals:
   - days_of_supply
   - stockout_risk
   - inventory_pressure
   - overstock_risk

2. V4 consumes those signals through:
   - `classify_decision_intelligence(...)`

3. The resulting structured output is stored on each `ScenarioComparisonRow` as:
   - `decision_intelligence`

This keeps V4:
- downstream from raw metric computation
- separate from replenishment logic
- reusable for printing and future LLM grounding

---

## Current V4 Output Shape

Each scenario row now contains:

- scenario_name
- reorder
- recommended_units
- delta_vs_baseline
- days_of_supply
- stockout_risk
- inventory_pressure
- overstock_risk
- decision_intelligence

Where `decision_intelligence` contains:

- inventory_state
- key_risk
- reasoning_summary

---

## Example

Scenario row:

- days_of_supply = 0.75
- stockout_risk = HIGH
- inventory_pressure = HIGH
- overstock_risk = LOW

V4 result:

- inventory_state = UNDERSTOCK
- key_risk = SHORTAGE_RISK
- reasoning_summary = "Low days of supply and high replenishment urgency indicate an understock condition."

---

## Result

The system now supports a deterministic business-reasoning layer between Scenario Analysis and the optional LLM explanation layer.