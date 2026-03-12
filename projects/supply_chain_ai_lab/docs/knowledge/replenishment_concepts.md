# Replenishment Concepts

This document explains the core concepts behind replenishment decisions in retail supply chains.

Replenishment answers two fundamental operational questions:

1. **When should we place an order?**
2. **How much should we order?**

The module implemented in this project models a simplified **reorder point policy**, one of the most common replenishment strategies in retail and manufacturing.

---

# Core Concepts

## Demand Rate

Demand rate represents the expected sales per unit of time.

Example:

- 1 kg of honey sold per day
- expected_daily_demand = 1

Demand rate is usually estimated from **demand forecasting models**.

---

# Lead Time

Lead time is the time between placing an order and receiving the goods.

Example:

- supplier delivery time = 7 days
- lead_time_days = 7

During this period, inventory continues to be consumed.

---

# Lead Time Demand

Lead time demand represents how much product will be sold while waiting for the next delivery.

Formula:

Lead Time Demand = Expected Daily Demand × Lead Time

Example:

Expected daily demand = 1 kg  
Lead time = 7 days

Lead Time Demand = 7 kg

This means that after placing an order, approximately **7 kg will be sold before the new inventory arrives**.

---

# Safety Stock

Safety stock is additional inventory held to protect against uncertainty.

Uncertainty can come from:

- demand fluctuations
- delivery delays
- forecast errors
- supplier disruptions

Example:

Safety stock = 3 kg

This buffer ensures the store does not run out of product during unexpected demand spikes.

---

# Reorder Point

The reorder point determines **when an order should be placed**.

Formula:

Reorder Point = Lead Time Demand + Safety Stock

Example:

Lead time demand = 7 kg  
Safety stock = 3 kg

Reorder point = 10 kg

Interpretation:

When inventory position drops to **10 kg**, the system should place an order.

During the lead time:

10 kg − 7 kg demand = 3 kg remaining

This preserves the safety stock.

---

# Inventory Position

Inventory position represents the **true available supply**.

In real retail systems:

Inventory Position =
On Hand Inventory
+ On Order Inventory
− Backorders

Example:

On hand inventory = 8 kg  
On order inventory = 5 kg  
Backorders = 1 kg

Inventory position = 12 kg

Inventory position is used instead of on-hand inventory because it accounts for **incoming inventory already ordered**.

---

# Reorder Decision

The reorder decision compares inventory position with the reorder point.

Decision rule:

Reorder if:

Inventory Position < Reorder Point

Example:

Inventory position = 8 kg  
Reorder point = 10 kg

Since 8 < 10 → reorder is triggered.

---

# Order Quantity

Once a reorder is triggered, the system must decide how much to order.

There are several replenishment policies used in practice:

Common policies include:

- Order-up-to level
- Economic Order Quantity (EOQ)
- Fixed batch sizes
- Min/Max inventory policies

---

# Gap-Based Order Policy (Used in This Project)

The simplified policy used in this module calculates the **gap to the reorder point**.

Order Quantity = max(0, Reorder Point − Inventory Position)

Example:

Reorder point = 10 kg  
Inventory position = 8 kg

Gap = 2 kg

Order quantity = 2 kg

This means the system orders enough inventory to restore the inventory position back to the reorder threshold.

---

# Alternative Policy: Order-Up-To Level

Many real supply chains use an **order-up-to policy** instead.

Example:

Target inventory level = 25 kg  
Current inventory position = 8 kg

Order quantity = 25 − 8 = 17 kg

This approach reduces ordering frequency by replenishing to a higher inventory level.

---

# Practical Interpretation

Replenishment systems continuously monitor inventory and answer two questions:

**When should we reorder?**

When inventory position falls below the reorder point.

**How much should we order?**

Enough to restore inventory according to the chosen replenishment policy.

---

# Role in the Supply Chain AI Lab

In this project:

Demand Forecasting → predicts expected demand

Inventory Module → tracks inventory position

Replenishment Module → decides when and how much to reorder

The replenishment service exposes a clean interface that can later be used by an AI agent:

get_replenishment_recommendation(...)

This allows future LLM-based agents to reason about supply chain decisions while relying on deterministic operational tools.