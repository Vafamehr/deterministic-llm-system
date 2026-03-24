# System Output Contract

## Overview

The Supply Chain AI Lab produces structured, deterministic outputs that represent inventory decisions and risk signals under different scenarios.

The system is designed to move from raw computation to interpretable operational signals.

Each scenario produces a consistent set of outputs that can be compared against a baseline.

---

## Output Structure

For each scenario, the system outputs a row containing:

- scenario_name
- reorder
- recommended_units
- days_of_supply
- stockout_risk
- delta_vs_baseline
- inventory_pressure

These outputs are generated after the full pipeline execution:
Forecast → Inventory → Replenishment → Simulation → Scenario Analysis

---

## Signal Definitions

### Reorder

Indicates whether the system recommends placing a replenishment order.

- True → reorder is required
- False → no action needed

This is the primary decision output of the system.

---

### Recommended Units

The number of units the system recommends ordering.

- Derived from inventory position, demand, and target levels
- Reflects how much inventory is needed to restore balance

---

### Days of Supply (DOS)

Represents how long current inventory can satisfy expected demand.

- Lower values → higher urgency
- Higher values → safer inventory position

This is a key operational metric used across supply chain systems.

---

### Stockout Risk

Categorical indicator of inventory risk.

- LOW → sufficient coverage
- MEDIUM → potential risk under variation
- HIGH → likely stockout without intervention

This signal provides a quick view of inventory vulnerability.

---

### Delta vs Baseline

Measures how much a scenario deviates from normal conditions.

- Positive → more units required than baseline
- Negative → fewer units required than baseline

This enables direct comparison across scenarios.

---

### Inventory Pressure

Derived interpretation signal based on days of supply.

- HIGH → urgent action required (low coverage)
- MEDIUM → moderate risk
- LOW → stable inventory condition

This compresses multiple signals into a human-readable indicator of urgency.

---

## Scenario Comparison

The system always includes a baseline scenario, which represents normal operating conditions.

All other scenarios are compared against this baseline.

This allows the system to answer questions such as:

- How much more inventory is needed under disruption?
- How does risk change under demand spikes?
- Which scenarios create the highest operational pressure?

---

## Design Principles

- Deterministic: All outputs are generated through transparent, rule-based logic
- Interpretable: Signals are designed to be understandable by humans
- Structured: Outputs follow a consistent schema across all scenarios
- Layered: Computation and interpretation are separated

---

## Role in System Architecture

This output contract represents the final structured state of the system.

It is used for:

- decision support
- scenario comparison
- downstream interpretation
- future LLM-based explanation (V3)

The LLM layer will consume these structured outputs but will not modify or replace the underlying decision logic.