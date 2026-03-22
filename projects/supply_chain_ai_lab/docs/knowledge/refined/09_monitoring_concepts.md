# Monitoring Concepts

Monitoring tells you if the system is behaving as expected.

It closes the loop between decision and outcome.

---

# Core Question

Is the system working, or drifting?

---

# Why Monitoring Exists

Decisions are made based on assumptions:

- forecast accuracy
- lead time stability
- demand patterns

Reality changes.

Monitoring detects when those assumptions break.

---

# What Gets Monitored

## Forecast vs Actual

- how accurate predictions are
- where errors occur

---

## Inventory Health

- stock levels
- days of supply
- stockout frequency

---

## Replenishment Behavior

- order frequency
- order size
- late or missed orders

---

## System Outcomes

- service level
- lost sales
- inventory cost

---

# Monitoring vs Evaluation

Evaluation:
- offline
- before deployment

Monitoring:
- continuous
- during operation

---

# Leading vs Lagging Signals

## Leading Signals

- forecast error increasing
- demand variability rising
- lead time changes

These warn early.

---

## Lagging Signals

- stockouts
- lost sales
- excess inventory

These show the result.

---

# Why Leading Signals Matter

By the time lagging signals appear, damage is already done.

Monitoring should detect problems early enough to react.

---

# Threshold-Based Alerts

Most systems use thresholds.

Examples:

- forecast error > X%
- stockout rate > Y%
- inventory below Z days

Thresholds trigger investigation or action.

---

# Drift

Drift is gradual change over time.

Examples:

- demand pattern shifts
- seasonality changes
- supplier performance degrades

Monitoring detects drift before it becomes failure.

---

# Feedback Loop

Monitoring feeds back into the system.

- adjust forecasts
- tune replenishment policies
- update safety stock

Without feedback, the system becomes outdated.

---

# Tradeoffs

## Sensitivity vs Stability

Sensitive monitoring:
- detects issues early
- more false alarms

Stable monitoring:
- fewer false alarms
- slower detection

---

## Simple Metrics vs Deep Analysis

Simple:
- easy to track
- limited insight

Complex:
- more insight
- harder to maintain

---

# Common Mistakes

- focusing only on lagging metrics  
- ignoring drift  
- setting thresholds too tight or too loose  
- monitoring without action  

---

# Mental Model

Monitoring is the system’s dashboard.

It tells you if you are on track or drifting off course.

---

# One-Line Summary

Monitoring tracks system performance and detects deviations from expected behavior, enabling early intervention and continuous improvement.