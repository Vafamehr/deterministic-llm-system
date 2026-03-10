# Retail Supply Chain — Core Concepts

This document summarizes the **most important concepts in retail supply chains**.

It serves as a **review sheet for interviews and system design discussions**.

---

# The Retail Supply Chain Flow

A typical retail supply chain has three main stages:

1. **Supplier → Distribution Center (DC)**
2. **Distribution Center → Store**
3. **Store → Customer**

Products move through this network while demand information flows in the opposite direction.

Customer purchases generate signals that propagate upstream through the supply chain.

---

# Key Entities in Retail Supply Chains

## SKU (Stock Keeping Unit)

A SKU represents a unique product.

Examples:

- Coke 12oz can
- Nike Air Max size 10
- iPhone 14 128GB Black

Each SKU has its own:

- demand pattern
- lead time
- inventory policy

---

## Store

A retail location where customers buy products.

Stores have:

- demand patterns
- limited shelf space
- inventory constraints

Demand is typically modeled at the **SKU × store × time level**.

---

## Distribution Center (Warehouse)

A warehouse that supplies multiple stores.

Functions include:

- storing inventory
- replenishing stores
- consolidating shipments
- balancing inventory across the network

---

# Core Supply Chain Problems

## Demand Forecasting

Demand forecasting predicts how much of each SKU will be sold in the future.

Typical forecasting horizon:

- daily
- weekly

Forecasts drive almost all other decisions.

Examples:

- how much inventory to order
- how much inventory to allocate
- how much safety stock is needed

---

## Inventory Management

Inventory management determines:

- how much stock to keep
- when to reorder products
- how to balance service level and cost

Key trade-off:

**High inventory → high holding cost**

**Low inventory → stockouts and lost sales**

---

## Replenishment

Replenishment determines:

**when and how much inventory should be ordered.**

Typical approaches:

- reorder point policies
- periodic review systems
- optimization-based replenishment

---

## Allocation

Allocation determines how inventory should be distributed across stores.

Examples:

- how many units of a new product each store receives
- how to distribute limited inventory during shortages

Allocation is important when:

- demand differs across locations
- inventory supply is limited

---

## Transfers

Inventory transfers move products between locations.

Examples:

- store-to-store transfers
- warehouse-to-warehouse transfers

Transfers help reduce stockouts and balance inventory across the network.

---

## Disruptions

Disruptions occur when supply chain operations deviate from plan.

Examples:

- supplier delays
- transportation failures
- sudden demand spikes
- weather events

Disruption management involves detecting problems and adjusting decisions.

---

# Key Metrics

Retail supply chains are typically evaluated using metrics such as:

## Service Level

The probability that demand can be fulfilled without stockouts.

Higher service levels require more inventory.

---

## Stockout Rate

The fraction of demand that cannot be fulfilled due to lack of inventory.

Stockouts reduce revenue and customer satisfaction.

---

## Inventory Turnover

Measures how quickly inventory is sold and replaced.

Higher turnover indicates more efficient inventory usage.

---

## Holding Cost

Cost of storing inventory over time.

Includes:

- storage costs
- capital costs
- risk of obsolescence

---

# Why These Concepts Matter for Data Science

Most supply chain data science work revolves around:

- predicting demand
- modeling uncertainty
- optimizing inventory decisions
- detecting disruptions
- evaluating policies using simulation

Understanding these concepts is essential for building realistic supply chain AI systems.


