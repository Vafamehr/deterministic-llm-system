# Inventory Reasoning

Inventory is the system’s buffer against uncertainty.

It absorbs forecast error, delays, and variability.

---

# Core Question

Do we have enough stock to meet expected demand?

---

# Why Inventory Exists

Supply chains cannot react instantly.

- demand is uncertain
- supply has lead time

Inventory exists to bridge that gap.

Without inventory:
- every delay becomes a stockout
- every forecast error becomes visible

---

# Inventory Is a Tradeoff

Holding inventory is not free.

Two opposing forces:

High inventory:
- fewer stockouts
- higher holding cost

Low inventory:
- lower cost
- higher stockout risk

Mental hook:

Inventory balances **availability vs cost**.

---

# What “Enough Inventory” Means

Inventory is not judged in isolation.

It is always compared against demand.

Key idea:

Inventory must cover **expected demand over time**.

---

# Days of Supply (DOS)

A simple way to reason about inventory:

Days of Supply = Inventory / Daily Demand

Example:

- inventory = 120 units
- demand = 10 units/day
- DOS = 12 days

---

# Why DOS Matters

It converts stock into time.

That makes it easier to compare against:

- lead time
- planning horizon

Mental hook:

Inventory is not units.
Inventory is **time coverage**.

---

# Lead Time Matters

Lead time = time between ordering and receiving stock.

If lead time is 7 days:

You need enough inventory to survive those 7 days.

---

# Inventory Risk

Risk comes from mismatch:

- demand is higher than expected
- supply arrives late
- forecast is wrong

Inventory reasoning is about detecting that risk early.

---

# Safety Stock

Safety stock is extra inventory held to absorb uncertainty.

It protects against:

- demand variability
- supply delays

Mental hook:

Safety stock = buffer for mistakes.

---

# Inventory Position vs On-Hand

Important distinction:

On-hand:
- physical stock available now

Inventory position:
- on-hand + on-order − committed

Decisions are made on **position**, not just on-hand.

---

# What the Inventory Module Does

It evaluates:

- current inventory position
- expected demand
- coverage (DOS)
- risk level

Output is not just a number.

It is a judgment:

- LOW risk
- MEDIUM risk
- HIGH risk

---

# Inventory Is Not a Decision

Inventory reasoning does not decide actions.

It answers:

Are we safe or at risk?

The action (reorder or not) comes next.

---

# Where It Fits in the System

Forecast → expected demand  
Inventory module → evaluates coverage  
Replenishment → decides action  

Inventory sits in the middle.

It translates forecast into risk.

---

# Tradeoffs in Inventory Thinking

## More Safety Stock

- reduces stockouts
- increases cost

---

## Less Safety Stock

- reduces cost
- increases risk

---

## Faster Replenishment

- less inventory needed
- depends on supply reliability

---

# Common Mistakes

- looking only at on-hand inventory  
- ignoring lead time  
- ignoring variability  
- treating inventory as static  

---

# Mental Model

Think of inventory as a **shock absorber**.

Forecast is never perfect.
Inventory absorbs the error.

---

# One-Line Summary

Inventory reasoning evaluates whether current stock can cover expected demand over time, balancing service level and cost while absorbing uncertainty in the system.