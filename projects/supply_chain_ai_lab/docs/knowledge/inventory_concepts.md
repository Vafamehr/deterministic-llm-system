# Inventory Concepts

This document explains the operational and modeling concepts used in the inventory module of the Supply Chain AI Lab.

These notes are intended for:

* supply chain understanding
* interview preparation
* quick concept review
* connecting forecasting outputs to operational decisions

## Why Inventory Matters in Supply Chains

Demand forecasting predicts future demand, but forecasting alone does not operate the supply chain.

Supply chain decisions depend on understanding the **current inventory state**.

Inventory answers questions such as:

* how much stock is currently available
* how much stock is already on the way
* how long stock will last
* whether a stockout is likely
* whether new orders should be placed

This makes inventory the bridge between:

```
demand forecasting → replenishment decisions
```

## Inventory Grain

Inventory is tracked at the same operational level used by demand forecasting:

**SKU × Location**

Example:

| sku_id  | location_id | on_hand |
| ------- | ----------- | ------- |
| milk_1L | store_102   | 120     |

This alignment is critical because later decisions will combine:

* forecasted demand
* inventory state
* replenishment policies

for the same SKU-location unit.

## On-Hand Inventory

On-hand inventory represents the physical stock currently available at a location.

Example:

```
on_hand = 120 units
```

This is the stock that can immediately satisfy customer demand.

On-hand inventory changes due to:

* sales
* replenishment deliveries
* inventory adjustments
* transfers between locations

## On-Order Inventory

On-order inventory represents items that have already been ordered but have not yet arrived.

Example:

```
on_order = 80 units
```

This inventory exists in the **supply pipeline**.

It will increase on-hand inventory when the shipment arrives.

## Reserved Inventory

Reserved inventory represents stock that is already committed and cannot be used freely.

Examples include:

* online orders already allocated
* safety buffers held for high-priority demand
* inventory reserved for transfers

Example:

```
reserved = 10 units
```

Reserved inventory reduces the stock that is effectively available.

## Inventory Position

Inventory position is a core supply chain planning metric.

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

Why this matters:

Inventory position reflects the **total effective supply pipeline**.

Planners use inventory position rather than raw on-hand stock when deciding whether to reorder.

## Days of Supply

Days of supply estimates how long current inventory will last given expected demand.

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

## Stockout Risk

A stockout occurs when demand exceeds available inventory.

Stockout risk can be estimated by comparing:

* days of supply
* supplier lead time

If inventory will run out before new supply arrives, the system flags risk.

Rule used in this project:

```
if days_of_supply < lead_time_days:
    stockout_risk = True
```

Example:

```
days_of_supply = 6
lead_time = 7

6 < 7 → stockout risk
```

Meaning the system is likely to run out of stock before replenishment arrives.

## Lead Time

Lead time represents the delay between placing an order and receiving inventory.

Example:

```
order placed → supplier processes → shipment → store receives
```

If this process takes seven days:

```
lead_time = 7 days
```

Lead time is a critical factor in replenishment decisions.

## Relationship to Demand Forecasting

Inventory metrics depend heavily on demand forecasts.

Forecasting predicts:

```
expected demand
```

Inventory metrics combine this with current stock levels to determine:

* how long inventory will last
* whether replenishment is required
* how urgent the situation is

## Operational Mental Model

The system pipeline now looks like this:

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

Inventory therefore acts as the **state layer** of the supply chain system.

## Why Inventory Modules Are Separate

In real supply chain systems, inventory state is managed independently from forecasting models.

Reasons:

* inventory changes continuously due to sales and shipments
* forecasts may update less frequently
* operational systems require fast inventory queries

Separating inventory state from forecasting models keeps the system:

* modular
* scalable
* easier to maintain

## Why This Module Is Important for Later Work

The inventory module will support many later components of the Supply Chain AI Lab.

Future modules that will use inventory data include:

* replenishment optimization
* inventory allocation across stores
* supplier risk simulations
* disruption response agents
* explanation layers for decision support

Because of this, the inventory module is designed as a clean and extensible system component.
