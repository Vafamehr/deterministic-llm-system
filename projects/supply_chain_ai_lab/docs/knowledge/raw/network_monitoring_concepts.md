# Supply Chain Network Monitoring — Core Concepts

## What Is a Supply Chain Control Tower

A supply chain control tower is a centralized monitoring system that provides visibility into supply chain operations.

It allows planners and operators to monitor:

* inventory levels
* demand signals
* disruptions
* logistics flows
* service risks

Control towers aggregate data from multiple systems and provide alerts when problems occur.

---

## Why Monitoring Is Important

Even well-designed planning systems can encounter unexpected issues.

Common operational risks include:

* inventory shortages
* demand spikes
* supplier delays
* transportation disruptions
* warehouse bottlenecks

Monitoring systems help organizations detect these problems early.

Early detection allows planners to intervene before service levels are affected.

---

## Days of Supply

Days of supply is one of the most common inventory monitoring metrics.

It estimates how long current inventory will last given expected demand.

Formula:

```
days_of_supply = on_hand_inventory / daily_demand
```

Example:

Inventory on hand: 100 units
Daily demand: 20 units

Days of supply:

```
100 / 20 = 5 days
```

This means the location will run out of inventory in approximately five days if no replenishment occurs.

---

## Stockout Risk Signals

A stockout risk occurs when days of supply falls below a defined threshold.

Example thresholds:

* 3 days for fast-moving items
* 7 days for slower items

These thresholds help planners identify locations that require immediate attention.

---

## Network-Level Monitoring

In large supply chains, companies must monitor inventory across:

* hundreds of stores
* multiple warehouses
* multiple SKUs
* multiple suppliers

Monitoring systems aggregate this information to identify patterns and risks across the entire network.

---

## Role in Supply Chain Planning Systems

Monitoring systems do not replace planning systems.

Instead, they complement them.

Planning systems answer:

* how much should we order?
* where should inventory be allocated?

Monitoring systems answer:

* where are we at risk right now?
* where should planners intervene?

Together, these systems support proactive supply chain management.

---

## Monitoring in the Supply Chain AI Lab

In this project, the network monitoring module simulates a simplified control tower.

It scans inventory conditions across multiple locations and flags stockout risks based on days of supply.

This adds a **network visibility layer** to the supply chain planning platform.
