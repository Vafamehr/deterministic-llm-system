# V4 Decision Intelligence — Example Output

## Scenario Analysis + V4


=== SCENARIO ANALYSIS + V4 ===

baseline reorder=True units=96.57 delta=0.00 dos=0.75 risk=HIGH pressure=HIGH overstock=LOW state=UNDERSTOCK key_risk=SHORTAGE_RISK
demand_spike reorder=True units=126.45 delta=29.87 dos=0.58 risk=HIGH pressure=HIGH overstock=LOW state=UNDERSTOCK key_risk=SHORTAGE_RISK
supplier_delay reorder=True units=129.76 delta=33.19 dos=0.75 risk=HIGH pressure=HIGH overstock=LOW state=UNDERSTOCK key_risk=SHORTAGE_RISK
---

## Interpretation

- All scenarios indicate **UNDERSTOCK** conditions
- High inventory pressure and low days of supply drive **SHORTAGE_RISK**
- Supplier delay increases required replenishment units, but does not change the fundamental state

---

## Purpose

This example demonstrates:

- deterministic pipeline execution
- scenario-based comparison
- V4 decision intelligence classification layer

This output is fully reproducible using the simulation mode in `run_system.py`.