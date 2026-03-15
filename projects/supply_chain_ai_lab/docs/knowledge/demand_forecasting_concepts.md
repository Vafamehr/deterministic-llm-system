# Demand Forecasting Concepts

This document contains the **core conceptual foundation of the demand forecasting module** used in the Supply Chain AI Lab.

It serves three purposes:

* understanding how the forecasting pipeline works
* reviewing forecasting concepts for supply chain roles
* building strong mental models for interview discussions

The goal is not only to implement forecasting, but to **understand how forecasting systems operate in real supply chain environments**.

---

# Mental Model of the Forecasting Pipeline

A useful mental hook for the entire forecasting system is:

table → records → series → features → model → forecast → evaluate

Explanation:

| Stage    | Meaning                             |
| -------- | ----------------------------------- |
| table    | raw retail sales data               |
| records  | structured demand objects           |
| series   | item-location time series           |
| features | engineered signals from past demand |
| model    | forecasting algorithm               |
| forecast | predicted future demand             |
| evaluate | measurement of forecast accuracy    |

This mental line captures the **entire lifecycle of retail demand forecasting systems**.

---

# Base Demand Record

The smallest useful unit of demand history is a **DemandRecord**.

Minimum fields:

* sku_id
* location_id
* date
* demand

Why these matter:

| Field       | Meaning                           |
| ----------- | --------------------------------- |
| sku_id      | identifies the product            |
| location_id | identifies the store or warehouse |
| date        | defines the time index            |
| demand      | the value we want to predict      |

Example:

| sku_id  | location_id | date       | demand |
| ------- | ----------- | ---------- | ------ |
| milk_1L | store_102   | 2024-01-01 | 42     |

Mental Hook:
A demand record is the **atomic unit of demand history**.

---

# Demand Dataset

A forecasting system operates on many demand records.

Conceptually:

DemandRecord = one row
DemandDataset = collection of rows

Advantages of this design:

* clean module boundaries
* explicit data contracts
* easier testing
* prevents uncontrolled DataFrame usage

Mental Hook:
The dataset is the **full history**, not the forecasting unit yet.

---

# Forecasting Grain

Forecasting grain defines **what exactly we predict**.

Most retail systems forecast at:

SKU × Location × Time

Example forecast:

| sku     | store     | week    | forecast_demand |
| ------- | --------- | ------- | --------------- |
| milk_1L | store_102 | week_12 | 47              |

Why this grain matters:

* inventory decisions occur at item-location level
* replenishment requires item-location forecasts
* forecasts can be aggregated later
* aggregated demand loses important information

Mental Hook:
Forecasting should happen at the **decision grain**.

---

# Demand Series

A demand series is the **history of demand for one SKU at one location**.

Example:

| date       | demand |
| ---------- | ------ |
| 2024-01-01 | 42     |
| 2024-01-08 | 39     |
| 2024-01-15 | 45     |
| 2024-01-22 | 41     |

Example scale:

500 SKUs × 50 stores = **25,000 demand series**

Mental Hook:
One series = **one SKU at one location over time**.

---

# Series Segmentation

Retail demand tables contain mixed rows.

Segmentation converts the table into individual series.

Process:

1. read demand table
2. convert rows to DemandRecord
3. group by (sku_id, location_id)
4. sort by date
5. output one time series per group

Mental Hook:

table → series

---

# Forecast Horizon

Forecast horizon defines **how far into the future predictions extend**.

Examples:

| Horizon | Example    |
| ------- | ---------- |
| 1-step  | tomorrow   |
| 7-step  | next week  |
| 4-step  | next month |

The project begins with **1-step forecasting**:

predict demand(t+1)

Mental Hook:
Start with **one-step correctness** before multi-step forecasting.

---

# Naive Forecast Baseline

Naive forecast rule:

next demand = last observed demand

Example:

| date | demand |
| ---- | ------ |
| 1    | 10     |
| 2    | 12     |
| 3    | 14     |

Forecast = **14**

Why baselines matter:

* establishes a minimum benchmark
* detects broken pipelines
* prevents misleading model claims

Mental Hook:
If your complex model cannot beat naive, something is wrong.

---

# Forecast Error Metric — MAE

MAE = Mean Absolute Error

MAE = mean(|actual − predicted|)

Example:

| actual | predicted | error |
| ------ | --------- | ----- |
| 50     | 45        | 5     |
| 30     | 37        | 7     |

Mental Hook:
MAE answers: **On average, how wrong are we?**

---

# Lag Features

Lag features represent **previous demand values used as predictors**.

Example:

| date | demand |
| ---- | ------ |
| 1    | 42     |
| 2    | 39     |
| 3    | 45     |

Lag features:

lag_1 = demand(t−1)
lag_2 = demand(t−2)

Mental Hook:
Lags allow the model to **see the recent past**.

---

# Rolling Window Features

Rolling features summarize **recent demand behavior**.

Example:

rolling_mean_3 = average(last 3 observations)

Rolling features capture:

* short-term trends
* demand smoothing
* volatility signals

Mental Hook:
Rolling windows capture **patterns, not single points**.

---

# Feature Leakage

Feature leakage occurs when a model accidentally uses **future information**.

Incorrect:

rolling_mean = mean(demand_t, demand_t−1, demand_t−2)

Correct:

rolling_mean = mean(demand_t−1, demand_t−2, demand_t−3)

Rule:

Features must use **only past information**.

Mental Hook:
If the model sees the future, the evaluation is fake.

---

# Feature Row Construction

A **feature row** represents one forecastable moment.

Example:

| sku  | store  | date       | lag_1 | lag_2 | rolling_mean | target |
| ---- | ------ | ---------- | ----- | ----- | ------------ | ------ |
| SKU1 | STORE1 | 2024-01-04 | 13    | 11    | 12           | 15     |

Mental Hook:
Feature rows convert time series into **machine learning rows**.

---

# Multi-Series Forecasting Pipeline

Real systems forecast thousands of series simultaneously.

Pipeline:

DemandDataset
→ series segmentation
→ feature generation per series
→ combine rows
→ model training

Mental Hook:
Retail forecasting = **many parallel time series problems**.

---

# Recursive Multi-Step Forecasting

To forecast multiple periods ahead:

1. predict t+1
2. append prediction
3. recompute features
4. predict t+2

Example:

[10,12,11,15]
→ predict 16
→ predict 17

Mental Hook:
Recursive forecasting lets a **1-step model walk into the future**.

---

# Model Progression

Typical forecasting system evolution:

naive forecast
→ linear regression
→ tree-based models (XGBoost)

Why tree models help:

* capture nonlinear relationships
* combine lag signals
* learn complex demand behavior

Mental Hook:
Tree models become the **strong ML baseline**.

---

# Why This Architecture Matters

The forecasting system is designed to be:

* modular
* scalable
* safe from leakage
* explainable

These properties make the system easier to:

* extend
* test
* debug
* explain in interviews

Final Mental Hook:

Demand forecasting is not just a model.
It is a **pipeline that converts raw sales history into future demand signals for supply chain decisions**.
