# Forecasting — Knowledge

Forecasting is about estimating future demand.

It does not make decisions.
It produces inputs for decisions.

---

# Core Question

What will demand look like in the near future?

Everything else follows from this.

---

# Why Forecasting Exists

Supply chains operate with delay.

- orders take time
- shipments take time
- inventory cannot react instantly

So decisions must be made **before demand happens**.

Forecasting provides that forward-looking signal.

---

# What a Forecast Actually Is

A forecast is not truth.

It is a **best estimate under uncertainty**.

It typically outputs:

- expected demand (mean)
- sometimes uncertainty (variance, intervals)

Mental hook:

Forecast = signal, not guarantee.

---

# Level of Forecasting

Most practical forecasting happens at:

SKU × Location × Time

Example:

- SKU: Coke 12oz
- Location: Store 101
- Time: next 7 days

This granularity matters because:

- demand varies by location
- promotions affect specific stores
- inventory decisions happen locally

---

# Forecast Horizon

The horizon defines how far ahead we predict.

Common choices:

- short-term (1–7 days)
- medium-term (1–4 weeks)

Longer horizon = more uncertainty  
Shorter horizon = more accuracy

Tradeoff:

Long horizon helps planning  
Short horizon helps execution

---

# What Drives Demand Patterns

Forecasting relies on patterns in historical data.

Common signals:

- trend (growth or decline)
- seasonality (weekly, monthly)
- promotions
- randomness (noise)

The model’s job is to extract these patterns.

---

# What Models Actually Do

Models do not “understand” demand.

They:

- learn patterns from past data
- project those patterns forward

Common approaches:

- simple averages (baseline)
- tree-based models
- time-series models

The choice matters less than:

- data quality
- feature design
- stability

---

# Forecast Accuracy Is Not Enough

A common mistake is focusing only on accuracy metrics.

But in supply chains:

- slightly wrong but stable forecasts are often better
- highly volatile forecasts can break decisions

Why:

Decisions depend on consistency, not just precision.

---

# Forecast vs Actual Gap

Forecast error is unavoidable.

So the system must handle:

- under-forecast (stockouts)
- over-forecast (excess inventory)

This is why forecasting alone is not enough.

Inventory and replenishment absorb the error.

---

# Forecast Is an Input, Not a Decision

Forecasting answers:

What will happen?

It does NOT answer:

What should we do?

That is handled by:

- inventory evaluation
- replenishment logic

Mixing these leads to confusion.

---

# How Forecast Flows in the System

Demand History (DataFrame)  
→ Model  
→ Predicted Demand  

Then:

Predicted Demand  
→ Inventory Module  
→ Replenishment Decisions  

Forecast feeds the system.
It does not control it.

---

# Tradeoffs in Forecasting

## Granularity vs Stability

Fine granularity:

- more precise
- more noise

Aggregated level:

- more stable
- less specific

---

## Complexity vs Robustness

Complex models:

- can capture more patterns
- harder to maintain

Simple models:

- easier to trust
- often good enough

---

## Responsiveness vs Smoothness

Fast-changing forecasts:

- react quickly
- can be noisy

Smooth forecasts:

- stable
- may lag behind changes

---

# Mental Model

Think of forecasting as:

Looking forward with imperfect visibility.

You are not predicting the future.
You are estimating it well enough to act.

---

# Common Mistakes

- treating forecasts as exact numbers  
- overfitting models to past data  
- ignoring uncertainty  
- using forecasting to directly make decisions  

---

# One-Line Summary

Forecasting estimates future demand under uncertainty and provides the signal that drives inventory and replenishment decisions, but it is not itself a decision system.