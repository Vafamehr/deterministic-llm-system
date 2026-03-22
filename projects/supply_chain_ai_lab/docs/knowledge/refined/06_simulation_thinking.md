# Simulation Thinking

Simulation is how you test decisions before reality tests them.

It answers: what happens if conditions change?

---

# Core Question

If we run this policy under different scenarios, what will happen?

---

# Why Simulation Exists

Forecasts are uncertain.  
Supply is uncertain.  

You cannot rely on one expected scenario.

Simulation allows you to:

- stress test decisions
- explore edge cases
- understand system behavior

---

# What Simulation Actually Is

Simulation is repeated execution of the same pipeline under different inputs.

You keep the logic fixed.
You change the conditions.

Examples:

- demand +20%
- demand drops suddenly
- lead time increases
- inventory shock

---

# What Changes in Simulation

You vary inputs like:

- demand patterns
- lead times
- supply availability
- initial inventory

The system itself does not change.

---

# Why Determinism Matters

Simulation only works if the system is stable.

If logic is inconsistent:
- results are not comparable
- insights are unreliable

Deterministic system → meaningful comparison.

---

# Output of Simulation

You don’t just look at decisions.

You evaluate outcomes:

- stockouts
- service level
- inventory levels
- cost impact

Simulation is about **system behavior over time**, not one decision.

---

# Scenario Thinking

Each simulation run represents a scenario.

Examples:

- normal demand
- peak season
- disruption scenario
- supply delay scenario

You compare outcomes across scenarios.

---

# Policy Testing

Simulation is used to test policies, not just predictions.

Examples:

- different safety stock levels
- different reorder points
- different review frequencies

You ask:

Which policy performs better under uncertainty?

---

# Tradeoffs in Simulation

## Realism vs Simplicity

Highly realistic:
- harder to build
- harder to interpret

Simple:
- easier to understand
- may miss edge cases

---

## Coverage vs Speed

More scenarios:
- better insight
- more computation

Fewer scenarios:
- faster
- less robust conclusions

---

# Common Mistakes

- changing logic between runs  
- focusing on one scenario only  
- evaluating only averages  
- ignoring worst-case outcomes  

---

# Mental Model

Simulation is a sandbox.

You safely break the system in theory,
so it doesn’t break in reality.

---

# One-Line Summary

Simulation evaluates how a fixed decision system behaves under different scenarios, allowing you to test policies and understand tradeoffs before real-world execution.