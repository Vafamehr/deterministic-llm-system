# Inventory Allocation — Core Concepts

## Why Allocation Exists

In real supply chains, available inventory is often **insufficient to meet total demand across all locations**.

This can happen due to:

* supplier delays
* production constraints
* transportation disruptions
* unexpected demand spikes
* inventory loss or shrinkage

When supply is limited, companies must decide **how to distribute available inventory across locations**.

This decision process is called **inventory allocation**.

---

## The Allocation Problem

The allocation problem occurs when:

```
Total Demand > Available Inventory
```

Example:

Available inventory: 100 units

Demand:

Store A → 80
Store B → 60
Store C → 50

Total demand = 190 units.

Since only 100 units are available, the system must determine **how to distribute inventory fairly or strategically across locations**.

---

## Objectives of Allocation

Different organizations optimize different objectives when allocating inventory.

Common goals include:

* maximizing service level
* protecting high-priority locations
* minimizing lost sales
* maintaining regional balance
* protecting strategic customers

The allocation policy determines how these goals are implemented.

---

## Common Allocation Policies

### Proportional Allocation

Inventory is distributed based on each location’s share of total demand.

Example:

```
allocation_ratio = available_inventory / total_demand
```

Each location receives:

```
location_demand × allocation_ratio
```

This approach is simple and fair.

It is commonly used as a **baseline allocation strategy**.

---

### Priority-Based Allocation

Some locations are more important than others.

Examples:

* flagship stores
* high-revenue regions
* strategic partners

In this approach, higher-priority locations receive inventory first.

Lower-priority locations receive remaining inventory.

---

### Minimum Service Level Allocation

Some companies enforce minimum service levels.

Example:

* each store must receive at least 40% of demand

After minimum levels are satisfied, remaining inventory is distributed across locations.

---

### Strategic Allocation

In advanced systems, allocation may incorporate:

* store profitability
* customer importance
* expected lost sales
* inventory holding costs

These approaches require more complex optimization models.

---

## Allocation in Supply Chain Planning Systems

Allocation decisions are typically triggered when:

* supply shortages occur
* production capacity is constrained
* supplier shipments are delayed
* distribution centers receive less inventory than expected

Allocation ensures that **limited supply is distributed rationally across the network**.

Without allocation logic, shortages could lead to unfair or inefficient distribution.

---

## Allocation in the Supply Chain AI Lab

In this project, the allocation module introduces **network-level decision making**.

Earlier modules focus on:

* forecasting demand
* evaluating inventory
* recommending replenishment

The allocation module extends this pipeline to handle **constrained supply situations across multiple locations**.

This makes the system closer to real-world supply chain planning platforms.

---

## Why Allocation Is Important

Allocation is one of the most practical decisions in supply chain operations.

It directly affects:

* store stockouts
* customer satisfaction
* lost sales
* regional performance
* operational fairness

A well-designed allocation strategy helps organizations maintain service levels even when supply disruptions occur.
