# Inventory Concepts

This document explains the **core operational concepts behind inventory management** in the Supply Chain AI Lab.

These notes serve four purposes:

* building intuition about how inventory systems work
* connecting forecasting outputs to operational decisions
* preparing for supply chain data science interviews
* supporting later modules such as replenishment, allocation, and simulation

Inventory management is the **operational bridge between forecasting and action** in supply chain systems.

---

# Mental Model of Inventory in the Supply Chain

A useful mental model is:

```
Forecast → Inventory State → Inventory Metrics → Replenishment Decisions
```

Explanation:

| Layer             | Role                                    |
| ----------------- | --------------------------------------- |
| Forecast          | predicts future demand                  |
| Inventory State   | tracks current stock and pipeline       |
| Inventory Metrics | evaluate risk and coverage              |
| Replenishment     | determines when and how much to reorder |

Mental Hook:

Inventory is the **state layer** of the supply chain system.

Forecasts predict the future, but **inventory determines what we can actually sell.**

---

# Why Inventory Matters in Supply Chains

Demand forecasting predicts future demand, but forecasting alone does not operate the supply chain.

Operational decisions require knowing the **current inventory state**.

Inventory answers questions such as:

* how much stock is currently available
* how much stock is already on the way
* how long stock will last
* whether a stockout is likely
* whether new orders should be placed

Inventory therefore connects:

```
demand forecasting → operational decisions
```

Mental Hook:

Forecasting predicts **what customers want**.
Inventory determines **whether we can serve them**.

---

# Inventory Grain

Inventory is tracked at the same operational level used by forecasting:

**SKU × Location**

Example:

| sku_id  | location_id | on_hand |
| ------- | ----------- | ------- |
| milk_1L | store_102   | 120     |

This alignment is critical because replenishment decisions combine:

* forecasted demand
* inventory state
* replenishment rules

for the same SKU-location pair.

Mental Hook:

Inventory should be tracked at the **decision grain**.

---

# On-Hand Inventory

On-hand inventory represents the **physical stock currently available at a location**.

Example:

```
on_hand = 120 units
```

This is the inventory that can immediately satisfy customer demand.

On-hand inventory changes due to:

* customer sales
* replenishment deliveries
* store transfers
* adjustments or shrinkage

Mental Hook:

On-hand inventory is **what is physically on the shelf or in the warehouse right now**.

---

# On-Order Inventory

On-order inventory represents items that have already been ordered but have not yet arrived.

Example:

```
on_order = 80 units
```

This inventory is part of the **supply pipeline**.

When shipments arrive, on-order inventory becomes on-hand inventory.

Mental Hook:

On-order inventory represents **inventory in transit through the supply chain**.

---

# Reserved Inventory

Reserved inventory represents stock that is **committed and cannot be freely used**.

Examples include:

* online orders already allocated
* inventory set aside for priority customers
* stock reserved for store transfers
* safety allocations for important products

Example:

```
reserved = 10 units
```

Reserved inventory reduces what is truly available for new demand.

Mental Hook:

Reserved inventory is **already spoken for**.

---

# Inventory Position

Inventory position is one of the most important planning metrics.

Formula:

```
inventory_position = on_hand + on_order - reserved
```

Example:

```
on_hand = 120
on_order = 80
reserved = 10

inventory_position = 120 + 80 - 10 = 190
```

Why planners use inventory position:

* it captures the full supply pipeline
* it reflects all committed inventory
* it supports reorder decisions

Mental Hook:

Inventory position represents the **true supply available to meet future demand**.

---

# Days of Supply

Days of supply estimates **how long inventory will last**.

Formula:

```
days_of_supply = on_hand / expected_daily_demand
```

Example:

```
on_hand = 120
expected_daily_demand = 20

days_of_supply = 6
```

Interpretation:

If demand continues at the current rate, inventory will last **six days**.

Mental Hook:

Days of supply answers:

**“How long until we run out?”**

---

# Stockout Risk

A stockout occurs when customer demand exceeds available inventory.

One simple risk signal compares:

* days of supply
* supplier lead time

Rule used in this project:

```
if days_of_supply < lead_time_days:
    stockout_risk = True
```

Example:

```
days_of_supply = 6
lead_time = 7
```

Since 6 < 7:

```
stockout risk = True
```

This means the store may run out of stock before replenishment arrives.

Mental Hook:

If inventory runs out **before the next delivery**, a stockout is likely.

---

# Lead Time

Lead time represents the delay between placing an order and receiving inventory.

Example process:

```
order placed
→ supplier processes order
→ shipment travels
→ store receives inventory
```

If this takes seven days:

```
lead_time = 7 days
```

Lead time strongly influences:

* reorder timing
* safety stock
* stockout risk

Mental Hook:

Lead time is the **delay between decision and supply arrival**.

---

# Relationship to Demand Forecasting

Inventory metrics depend on demand forecasts.

Forecasting estimates:

```
expected demand
```

Inventory systems combine this with current stock levels to determine:

* how long inventory will last
* whether replenishment is needed
* how urgent the situation is

Mental Hook:

Forecasts predict **demand pressure**.
Inventory measures **supply capacity**.

---

# Operational Supply Chain Pipeline

The system pipeline now looks like:

```
Demand Forecasting
        ↓
Expected Demand
        ↓
Inventory State
        ↓
Inventory Metrics
        ↓
Replenishment Decisions
```

Inventory is the **operational state layer** between prediction and action.

Mental Hook:

Forecasts estimate demand.
Inventory reveals risk.
Replenishment responds.

---

# Why Inventory Systems Are Separate from Forecasting

In real supply chain systems, inventory state is managed independently from forecasting models.

Reasons:

* inventory changes continuously due to sales
* shipments update inventory frequently
* forecasts update less frequently
* operational systems need fast queries

Separating these components makes the architecture:

* modular
* scalable
* easier to maintain

Mental Hook:

Forecasting predicts the future.
Inventory tracks the **present state of supply**.

---

# Why This Module Matters for the Full System

The inventory module becomes a core input for many later components.

Future modules that rely on inventory include:

* replenishment optimization
* inventory allocation across stores
* supplier risk simulations
* disruption detection
* LLM-based decision explanations

Because of this, the inventory module is designed as a **clean, reusable subsystem**.

Mental Hook:

Inventory is the **foundation of operational supply chain decisions**.
