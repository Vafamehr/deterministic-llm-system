# Allocation Tradeoffs

Allocation decides who gets limited inventory.

It only matters when supply is not enough for everyone.

---

# Core Question

Given limited inventory, where should it go?

---

# When Allocation Happens

Allocation is needed when:

- demand > available supply
- multiple locations compete for inventory

If supply is sufficient, allocation is trivial.

If not, tradeoffs begin.

---

# Why Allocation Is Hard

You cannot satisfy all demand.

So every decision:

- helps some locations
- hurts others

There is no perfect solution.
Only tradeoffs.

---

# Common Objectives

Different systems prioritize different goals.

## Maximize Sales

Send inventory where demand is highest.

---

## Maximize Service Level

Spread inventory to avoid stockouts everywhere.

---

## Prioritize Key Locations

Flagship stores or strategic regions get priority.

---

## Fairness

Distribute inventory evenly across locations.

---

# Core Tradeoff

Concentration vs Distribution

## Concentration

- send more inventory to high-demand locations
- maximize total sales
- increase risk of stockouts elsewhere

---

## Distribution

- spread inventory across locations
- reduce extreme stockouts
- may reduce total sales

---

# Demand vs Supply View

Allocation sits between:

Demand signals:
- forecasted demand per location

Supply constraints:
- limited inventory available

The goal is to match them as best as possible.

---

# Static vs Dynamic Allocation

## Static

- one-time allocation decision
- based on initial forecast

---

## Dynamic

- adjust allocation over time
- respond to new demand signals

Tradeoff:

Dynamic is better, but more complex.

---

# Role of Forecasting

Allocation depends heavily on forecast quality.

Bad forecast:
- wrong locations get inventory

Good forecast:
- allocation is more effective

---

# Role of Inventory State

Allocation must consider:

- current inventory per location
- incoming shipments
- existing imbalances

It is not just about demand.

---

# Tradeoffs

## Efficiency vs Fairness

Max efficiency:
- concentrate inventory

Max fairness:
- spread inventory

---

## Simplicity vs Optimality

Simple rules:
- easier to implement
- less optimal

Complex optimization:
- better results
- harder to maintain

---

# Common Mistakes

- ignoring existing inventory differences  
- relying only on forecast  
- over-optimizing for one metric  
- treating allocation as static  

---

# Mental Model

Allocation is dividing a limited pie.

More for one slice means less for another.

---

# One-Line Summary

Allocation manages limited inventory by balancing competing demand across locations, trading off efficiency, fairness, and risk under supply constraints.