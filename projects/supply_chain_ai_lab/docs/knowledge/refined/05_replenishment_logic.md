    # Replenishment Logic

Replenishment turns risk into action.

It decides when to order and how much.

---

# Core Question

Do we need to reorder, and if yes, how much?

---

# Where It Fits

Forecast → expected demand  
Inventory → risk level  
Replenishment → action  

Replenishment is the execution step.

---

# Why Replenishment Exists

Inventory only tells you the situation.

Replenishment changes it.

Without replenishment:
- inventory only decreases
- stockouts are inevitable

---

# Basic Idea

Order inventory before you run out.

But not too early.
And not too much.

---

# Reorder Point Logic

A common rule:

Reorder Point = Lead Time Demand + Safety Stock

Meaning:

Order when inventory drops below what you need during lead time, plus a buffer.

---

# Lead Time Demand

This is expected demand during the time it takes to receive new stock.

If lead time = 7 days  
and demand = 10 units/day  

Lead Time Demand = 70 units

---

# Safety Stock

Extra buffer to protect against:

- forecast error
- supply delays

Without it, small errors cause stockouts.

---

# Order Quantity

Once you decide to reorder, you must decide how much.

Common approaches:

- fixed quantity
- order up to a target level
- demand-based calculation

---

# Order-Up-To Logic

A simple approach:

Target Level = Lead Time Demand + Safety Stock + Review Demand

Order Quantity = Target Level − Inventory Position

This ensures you refill to a safe level.

---

# Inventory Position Matters

Always use:

Inventory Position = On-hand + On-order − Committed

Not just on-hand.

Otherwise, you will over-order or under-order.

---

# Timing Matters

Two common approaches:

## Continuous Review

- check inventory all the time
- reorder immediately when threshold is hit

## Periodic Review

- check inventory at fixed intervals
- reorder at review points

Tradeoff:

Continuous = responsive  
Periodic = simpler, cheaper operationally  

---

# Replenishment Is Policy, Not Optimization

In most real systems:

- rules are simple
- policies are stable
- behavior is predictable

Overly complex optimization can make systems fragile.

---

# Tradeoffs

## Larger Orders

- fewer orders
- higher holding cost

---

## Smaller Orders

- lower inventory
- higher ordering frequency

---

## High Safety Stock

- fewer stockouts
- more cost

---

## Low Safety Stock

- cheaper
- riskier

---

# Common Mistakes

- ignoring lead time  
- using on-hand instead of inventory position  
- overreacting to short-term demand spikes  
- constantly changing policies  

---

# Mental Model

Replenishment is like refilling a tank.

You don’t wait until empty.
You refill when you reach a threshold.

---

# One-Line Summary

Replenishment converts inventory risk into action by triggering orders based on lead time demand and safety stock, ensuring the system maintains service while controlling cost.