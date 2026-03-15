# Retail Domain Scope

## Domain Focus

The Supply Chain AI Lab focuses on a **retail supply chain decision system**.

The lab models a simplified but realistic retail environment that includes:

- products (SKUs)
- stores where demand occurs
- warehouses or distribution centers that supply stores
- customer demand evolving over time
- inventory stored at multiple locations
- replenishment decisions that restock inventory
- supply chain disruptions that affect supply or demand

The system is designed to simulate how modern supply chain AI platforms support operational decision making.

---

# Core Business Problems

The lab focuses on the **most fundamental operational problems in retail supply chains**.

These problems correspond directly to the modules implemented in the system.

Primary operational problems include:

- demand forecasting
- inventory state evaluation
- replenishment planning
- supply chain scenario simulation
- supply disruption modeling
- constrained inventory allocation
- network performance monitoring
- decision interpretation using LLM reasoning

These represent the **minimum set of problems required to model a realistic supply chain decision platform**.

---

# Core Entities

The core entities in the system represent objects commonly used in supply chain analytics.

Examples include:

- `sku` — a unique product
- `store` — a retail location where customers purchase products
- `warehouse` — a distribution node supplying stores
- `calendar_week` or `date` — time dimension for demand and supply events
- `sales` — observed customer demand
- `inventory_position` — current available inventory
- `shipment` — inventory movement between locations
- `lead_time` — time required for replenishment
- `promotion` — marketing activity affecting demand
- `stockout_event` — failure to meet demand due to insufficient inventory

These entities form the **foundation of the system data model**.

---

# Decision Context

The system is designed to support common supply chain operational decisions.

Examples include:

- how much demand should be expected in the next planning period
- which SKUs and locations are at risk of stockout
- when and how much inventory should be replenished
- how inventory should be distributed across locations when supply is limited
- how disruptions affect inventory risk and service levels
- how the system should respond under different scenarios

These decisions are supported through a combination of:

- machine learning predictions
- deterministic supply chain policies
- scenario simulation
- decision monitoring
- LLM reasoning support

---

# Retail Supply Chain Decision Layers

Retail supply chains can be understood through several interacting decision layers.

## Demand Layer

This layer answers the question:

"What demand should we expect?"

Typical problems include:

- demand forecasting
- promotion impact modeling
- seasonality detection
- demand anomaly detection

Machine learning is heavily used in this layer.

---

## Inventory Layer

This layer answers:

"What inventory do we currently have and how risky is our position?"

Typical problems include:

- inventory position evaluation
- stockout risk estimation
- safety stock planning

---

## Operational Decision Layer

This layer answers:

"What operational actions should we take?"

Typical problems include:

- replenishment planning
- ordering decisions
- inventory balancing

---

## Scenario and Risk Layer

This layer answers:

"What happens if conditions change?"

Examples include:

- demand spikes
- supplier delays
- logistics disruptions
- inventory shocks

Simulation and disruption modeling are used in this layer.

---

# Why Retail Is the Initial Domain

Retail is an ideal starting domain for the lab because it provides:

- realistic supply chain decision problems
- strong alignment with machine learning and data science interview topics
- clear integration of forecasting, inventory logic, and simulation
- natural expansion into LLM-powered decision support

Retail supply chains also illustrate how **machine learning, operational policies, and simulation interact in real business environments**.

---

# Mental Hook

Retail supply chains revolve around three core questions:

What demand should we expect?  
What inventory risk do we face?  
What actions should we take?

The Supply Chain AI Lab extends this with a fourth question:

What happens if conditions change?