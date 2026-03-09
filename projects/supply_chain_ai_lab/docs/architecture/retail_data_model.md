# Retail Data Model

This document defines the core data structure used throughout the Supply Chain AI Lab.

The entire system is built around the concept:

**SKU × Location × Time**

This structure allows the system to represent demand, inventory, and supply chain decisions consistently.

---

# Core Data Dimensions

## SKU (Product)

A SKU represents a unique product sold by the retailer.

Examples:

- Coke 12oz can
- Nike Air Max size 10
- iPhone 14 128GB

Each SKU has attributes such as:

- category
- brand
- unit price
- cost
- shelf life

---

## Location

A location represents where inventory is stored or sold.

Two common location types exist:

### Store

A retail store where customers purchase products.

Stores have:

- customer demand
- limited shelf capacity
- local demand patterns

---

### Warehouse / Distribution Center

A warehouse that supplies multiple stores.

Warehouses:

- store larger inventory
- replenish stores
- balance supply across locations

---

## Time

Retail supply chains typically model time using:

- daily periods
- weekly periods

Weekly aggregation is often used for forecasting.

Example:

| week | start_date |
|----|----|
| 2024-W01 | 2024-01-01 |

---

# Core Data Tables

## Sales Table

Records customer purchases.

Example schema:

| sku | store | week | units_sold |
|----|----|----|----|
| milk | store_01 | week_10 | 54 |

This table is the primary source for **demand forecasting**.

---

## Inventory Table

Tracks inventory levels.

Example schema:

| sku | location | week | inventory_on_hand |
|----|----|----|----|
| milk | store_01 | week_10 | 32 |

---

## Shipment Table

Records inventory movement.

Example schema:

| sku | from_location | to_location | week | units |
|----|----|----|----|----|
| milk | warehouse_01 | store_01 | week_10 | 100 |

---

## Lead Time Table

Defines how long it takes for shipments to arrive.

Example:

| supplier | sku | lead_time_days |
|----|----|----|
| supplier_A | milk | 3 |

---

## Promotion Table

Records promotional events that affect demand.

Example:

| sku | store | week | promotion_type |
|----|----|----|----|
| milk | store_01 | week_10 | discount |

Promotions often increase demand temporarily.

---

# Why This Data Model Matters

This data model supports:

- demand forecasting models
- inventory simulation
- replenishment decisions
- allocation algorithms
- disruption analysis

By using a consistent structure, the system can combine:

- machine learning
- simulation
- optimization
- LLM reasoning