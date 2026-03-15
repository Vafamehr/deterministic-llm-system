# Retail Supply Chain — Core Concepts

This document summarizes the **most important concepts in retail supply chains**.

It is designed as a **mental reference sheet for system design discussions, interviews, and architecture reasoning**.

The Supply Chain AI Lab models these concepts through modules such as forecasting, inventory evaluation, replenishment policies, simulation, disruption modeling, allocation decisions, and monitoring.

---

# The Retail Supply Chain Flow

A typical retail supply chain has three operational stages:

Supplier → Distribution Center → Store → Customer

Products move **downstream** through this network while demand information flows **upstream**.

Customer purchases generate signals that propagate upstream through the supply chain, influencing forecasting, replenishment, and inventory planning decisions.

Mental Hook:

Products flow **downstream**, information flows **upstream**.

---

# Core Supply Chain Dimensions

Most supply chain systems organize data around three fundamental dimensions:

SKU × Location × Time

These dimensions describe:

- what product is involved
- where it exists in the network
- when an event occurs

Mental Hook:

Every supply chain decision ultimately depends on **SKU × Location × Time**.

---

# Key Entities in Retail Supply Chains

## SKU (Stock Keeping Unit)

A SKU represents a **unique product** sold by the retailer.

Examples include:

- Coke 12oz can  
- Nike Air Max size 10  
- iPhone 14 128GB Black  

Each SKU has its own:

- demand pattern
- lead time
- replenishment policy
- inventory dynamics

Mental Hook:

A SKU represents **what product is being managed**.

---

## Store

A store is a retail location where customers purchase products.

Stores have:

- customer demand
- limited shelf space
- local demand patterns
- store-specific promotions

Demand is typically modeled at the **SKU × store × time level**.

Mental Hook:

Stores represent **demand points in the network**.

---

## Distribution Center (Warehouse)

A distribution center supplies inventory to multiple stores.

Key responsibilities include:

- storing inventory
- replenishing stores
- consolidating shipments
- redistributing inventory across the network

Distribution centers act as **buffers that absorb supply and demand variability**.

Mental Hook:

Warehouses act as **inventory buffers and distribution hubs**.

---

# Core Supply Chain Decision Problems

Modern supply chain planning systems must solve several core problems.

---

## Demand Forecasting

Demand forecasting predicts how much of each SKU will be sold in the future.

Typical forecasting horizons include:

- daily
- weekly
- multi-week planning horizons

Forecasts drive almost all downstream decisions such as:

- replenishment orders
- safety stock levels
- allocation planning

Mental Hook:

Forecasting answers the question:

What demand should we expect?

---

## Inventory Management

Inventory management determines:

- how much stock should be held
- how inventory risk should be monitored
- how service levels should be protected

A fundamental trade-off exists:

High inventory → higher holding cost

Low inventory → higher risk of stockouts

Mental Hook:

Inventory management balances **availability and cost**.

---

## Replenishment

Replenishment determines **when and how much inventory should be ordered**.

Common replenishment policies include:

- reorder point policies
- order-up-to policies
- periodic review systems

A common formula used in practice:

Reorder Point = Lead Time Demand + Safety Stock

Mental Hook:

Replenishment converts **forecast signals into operational actions**.

---

## Allocation

Allocation determines how inventory should be distributed across locations when supply is limited.

Examples include:

- allocating a new product launch across stores
- distributing limited inventory during shortages

Allocation is important when:

- demand differs across locations
- inventory supply is constrained

Mental Hook:

Allocation answers the question:

Who receives limited inventory first?

---

## Transfers

Transfers move inventory between locations within the network.

Examples include:

- store-to-store transfers
- warehouse-to-warehouse transfers

Transfers help balance inventory and reduce stockouts.

Mental Hook:

Transfers rebalance **inventory across the network**.

---

## Supply Disruptions

Disruptions occur when supply chain operations deviate from plan.

Examples include:

- supplier delays
- transportation interruptions
- demand spikes
- extreme weather events

Disruption management involves detecting problems and adjusting decisions.

Mental Hook:

Disruptions test the **resilience of the supply chain**.

---

# Scenario Simulation

Because supply chains operate under uncertainty, planners often test policies through simulation.

Simulation explores hypothetical situations such as:

- demand spikes
- supplier delays
- inventory shocks
- promotion events

Simulation allows planners to test whether policies remain effective under changing conditions.

Mental Hook:

Simulation answers the question:

What happens if conditions change?

---

# Key Supply Chain Metrics

Supply chains are evaluated using several core performance metrics.

---

## Service Level

Service level measures the probability that demand can be fulfilled without stockouts.

Higher service levels typically require more inventory.

Mental Hook:

Service level measures **customer fulfillment reliability**.

---

## Stockout Rate

Stockout rate measures the fraction of demand that cannot be fulfilled due to insufficient inventory.

Stockouts reduce revenue and customer satisfaction.

Mental Hook:

Stockouts represent **lost sales opportunities**.

---

## Inventory Turnover

Inventory turnover measures how quickly inventory is sold and replaced.

Higher turnover indicates more efficient inventory usage.

Mental Hook:

Inventory turnover measures **inventory efficiency**.

---

## Holding Cost

Holding cost represents the cost of storing inventory over time.

Typical components include:

- storage cost
- capital cost
- risk of obsolescence
- insurance

Mental Hook:

Holding cost represents **the price of carrying inventory**.

---

# Why These Concepts Matter for Data Science

Most supply chain data science work revolves around:

- predicting demand
- modeling uncertainty
- optimizing inventory decisions
- detecting disruptions
- evaluating policies through simulation

Understanding these concepts allows data scientists to build **realistic decision systems rather than isolated models**.

Mental Hook:

Supply chain data science combines **prediction, decision policies, and operational monitoring**.