# Retail Data Model

This document defines the **core data structure used throughout the Supply Chain AI Lab**.

The entire system is built around the fundamental supply chain key:

SKU × Location × Time

This structure allows the system to consistently represent:

- demand
- inventory
- shipments
- supply chain decisions
- disruption scenarios

All analytical modules in the system operate on data organized using these three dimensions.

---

# Core Data Dimensions

## SKU (Product)

A SKU represents a **unique product** sold by the retailer.

Examples include:

- Coke 12oz can
- Nike Air Max size 10
- iPhone 14 128GB

Typical SKU attributes may include:

- product category
- brand
- unit price
- cost
- shelf life
- supplier

These attributes may later be used as **features for forecasting models or optimization decisions**.

Mental Hook

SKU represents **what product we are managing in the supply chain**.

---

## Location

A location represents a **physical node in the supply chain network where inventory exists**.

Two primary location types are modeled.

### Store

A retail store where customers purchase products.

Stores typically have:

- customer demand
- limited shelf capacity
- localized demand patterns

Mental Hook

Stores are **demand points in the network**.

---

### Warehouse / Distribution Center

Warehouses supply inventory to multiple stores.

Their responsibilities include:

- storing larger quantities of inventory
- replenishing stores
- redistributing inventory across the network

Mental Hook

Warehouses act as **inventory buffers and distribution hubs**.

---

## Time

Retail supply chains operate over discrete time periods.

Common time resolutions include:

- daily periods
- weekly periods

Weekly aggregation is often used for forecasting and planning.

Example:

| week | start_date |
|-----|-----|
| 2024-W01 | 2024-01-01 |

Mental Hook

Time allows the system to track **how demand and inventory evolve over time**.

---

# Core Data Tables

The supply chain system uses several datasets built on the **SKU × Location × Time** structure.

---

## Sales Table

Records customer purchases and serves as the **primary source of demand data**.

Example schema:

| sku | store | week | units_sold |
|----|----|----|----|
| milk | store_01 | week_10 | 54 |

This table feeds the **demand forecasting module**.

Mental Hook

Sales data represents **real customer demand signals**.

---

## Inventory Table

Tracks how much inventory is currently available at each location.

Example schema:

| sku | location | week | inventory_on_hand |
|----|----|----|----|
| milk | store_01 | week_10 | 32 |

Inventory data supports:

- replenishment decisions
- stockout risk analysis
- simulation models
- allocation logic

Mental Hook

Inventory data describes **the current supply position**.

---

## Shipment Table

Records movements of inventory between supply chain locations.

Example schema:

| sku | from_location | to_location | week | units |
|----|----|----|----|----|
| milk | warehouse_01 | store_01 | week_10 | 100 |

Shipment data helps track **inventory flow across the network**.

Mental Hook

Shipments represent **how inventory moves through the supply chain**.

---

## Lead Time Table

Defines how long it takes for replenishment shipments to arrive.

Example schema:

| supplier | sku | lead_time_days |
|----|----|----|
| supplier_A | milk | 3 |

Lead times influence:

- reorder points
- safety stock calculations
- disruption scenarios
- simulation outcomes

Mental Hook

Lead time determines **how quickly supply can respond to demand**.

---

## Promotion Table

Records marketing events that influence demand.

Example schema:

| sku | store | week | promotion_type |
|----|----|----|----|
| milk | store_01 | week_10 | discount |

Promotions are important inputs for forecasting models because they often create **temporary demand spikes**.

Mental Hook

Promotions represent **intentional demand shocks**.

---

# Relationship to the Forecasting Module

The demand forecasting module converts raw sales data into structured forecasting inputs.

Transformation pipeline:

Sales Table  
↓  
Demand Records  
↓  
Item–Location Time Series  
↓  
Feature Engineering  
↓  
Training / Prediction Feature Tables

This pipeline is implemented in:

src/demand_forecasting/

Key components include:

- schemas.py for structured data interfaces
- data.py for time-series segmentation
- features.py for feature engineering
- service.py for the forecasting interface

---

# Relationship to Other Modules

Because all data follows the **SKU × Location × Time structure**, the same model supports multiple modules.

Demand forecasting uses the sales table.

Inventory evaluation uses the inventory table.

Replenishment policies combine:

- forecast demand
- inventory position
- lead time information

Simulation scenarios modify:

- demand
- inventory
- lead time assumptions

Allocation modules distribute inventory across locations.

This shared structure allows the system to combine:

- machine learning
- inventory logic
- scenario simulation
- supply chain planning
- LLM reasoning

within one consistent data framework.

---

# Mental Model

The data model describes three things:

What product is involved  
Where it exists in the network  
When the event occurs

Mental Hook

Every supply chain decision ultimately depends on:

SKU × Location × Time