# Retail Domain Scope

## Domain Focus

Supply Chain AI Lab will initially focus on a **retail supply chain** setting.

The system will model a business environment with:

- products (SKUs)
- stores
- warehouses or distribution centers
- customer demand over time
- replenishment decisions
- inventory movement across locations
- disruptions affecting supply or demand

## Core Business Problems

The initial lab will focus on these must-know retail supply chain problems:

- demand forecasting
- inventory and replenishment
- allocation and transfers
- disruption intelligence
- assortment optimization
- recommendation-based decision support

## Main Entities

The core entities in the system will include:

- `sku`
- `store`
- `warehouse`
- `calendar_week`
- `sales`
- `inventory_position`
- `shipment`
- `lead_time`
- `promotion`
- `stockout_event`

## Decision Context

The system should support decisions such as:

- how much demand is expected next week
- which SKUs are at risk of stockout
- when and how much to replenish
- where inventory should be transferred
- how disruptions affect service levels
- what actions should be recommended under different scenarios

## Why Retail First

Retail is the best initial scope because it provides:

- realistic and common supply chain use cases
- strong alignment with data science interview topics
- natural integration of ML, simulation, optimization, and LLM reasoning
- a modular path for expansion later