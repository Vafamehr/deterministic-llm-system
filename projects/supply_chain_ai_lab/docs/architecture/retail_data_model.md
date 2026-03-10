# Retail Data Model

This document defines the **core data structure used throughout the Supply Chain AI Lab**.

The entire system is built around the fundamental supply chain key:

```
SKU × Location × Time
```

This structure allows the system to consistently represent:

- demand
- inventory
- shipments
- supply chain decisions

All analytical modules in the system operate on data organized using these dimensions.

---

# Core Data Dimensions

## SKU (Product)

A SKU represents a **unique product** sold by the retailer.

Examples:

- Coke 12oz can
- Nike Air Max size 10
- iPhone 14 128GB

Typical SKU attributes may include:

- product category
- brand
- unit price
- cost
- shelf life

These attributes may later be used as **features for forecasting or optimization models**.

---

## Location

A location represents a **physical place where inventory exists**.

Two primary location types are modeled.

### Store

A retail store where customers purchase products.

Stores typically have:

- customer demand
- limited shelf capacity
- local demand patterns

---

### Warehouse / Distribution Center

Warehouses supply multiple stores.

Their role is to:

- store larger quantities of inventory
- replenish stores
- redistribute inventory across the network

---

## Time

Retail supply chains operate over discrete time periods.

Common time resolutions include:

- daily periods
- weekly periods

Weekly aggregation is frequently used for demand forecasting.

Example:

| week | start_date |
|-----|-----|
| 2024-W01 | 2024-01-01 |

---

# Core Data Tables

The supply chain system uses several core datasets built on the **SKU × Location × Time** structure.

---

## Sales Table

Records customer purchases and is the **primary source of demand data**.

Example schema:

| sku | store | week | units_sold |
|----|----|----|----|
| milk | store_01 | week_10 | 54 |

This table is the main input to the **demand forecasting module**.

---

## Inventory Table

Tracks the amount of inventory available at each location.

Example schema:

| sku | location | week | inventory_on_hand |
|----|----|----|----|
| milk | store_01 | week_10 | 32 |

Inventory levels are required for:

- replenishment decisions
- simulation models
- allocation logic

---

## Shipment Table

Records the movement of inventory between locations.

Example schema:

| sku | from_location | to_location | week | units |
|----|----|----|----|----|
| milk | warehouse_01 | store_01 | week_10 | 100 |

Shipment data is used to track supply flows through the network.

---

## Lead Time Table

Defines how long it takes for shipments to arrive.

Example schema:

| supplier | sku | lead_time_days |
|----|----|----|
| supplier_A | milk | 3 |

Lead times influence:

- replenishment timing
- safety stock calculations
- simulation behavior

---

## Promotion Table

Records promotional events that temporarily affect demand.

Example schema:

| sku | store | week | promotion_type |
|----|----|----|----|
| milk | store_01 | week_10 | discount |

Promotions are important features for forecasting models.

---

# Relationship to the Forecasting Module

The demand forecasting module converts raw sales data into structured forecasting inputs.

Example transformation:

```
Sales Table
      ↓
Demand Records
      ↓
Item–Location Time Series
      ↓
Feature Engineering
      ↓
Training / Prediction Feature Tables
```

This transformation is implemented inside:

```
src/demand_forecasting/
```

---

# Why This Data Model Matters

This data model allows the system to support multiple supply chain analytics capabilities using a shared structure.

These include:

- demand forecasting
- inventory simulation
- replenishment optimization
- allocation and transfers
- disruption analysis

Because every module uses the same **SKU × Location × Time** foundation, the system can combine:

- machine learning
- simulation
- optimization
- LLM reasoning