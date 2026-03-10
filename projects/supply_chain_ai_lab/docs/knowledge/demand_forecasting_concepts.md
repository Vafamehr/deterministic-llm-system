# Demand Forecasting Concepts

This document contains key concepts, design decisions, and mental models related to the demand forecasting module of the Supply Chain AI Lab.

These notes are intended for:
- system understanding
- interview preparation
- quick concept review

## Base Demand Record

The minimum useful demand history record contains:

- `sku_id`
- `location_id`
- `date`
- `demand`

Why these four fields matter:

- `sku_id` identifies the product
- `location_id` identifies where demand happened
- `date` anchors the time series
- `demand` is the target variable to forecast

This is the atomic unit of retail demand history.

## Demand Dataset

While `DemandRecord` represents a single observation, forecasting systems operate on collections of records.

`DemandDataset` represents the full demand history used by the forecasting module.

Structure:

- `DemandDataset`
  - contains a list of `DemandRecord`
  - represents the dataset used for forecasting

Conceptually:

DemandRecord → one row of demand history  
DemandDataset → the collection of many records

This separation helps keep module interfaces clean and prevents raw lists or ad-hoc structures from flowing through the system.

## Forecasting Grain

Forecasting grain defines the level at which demand predictions are produced.

In retail supply chains, the most common grain is:

**SKU × Location × Time**

This means each forecast corresponds to the demand of a specific product at a specific location during a specific time period.

Example:

- SKU: milk_1L
- Location: store_102
- Date: 2024-03-01

Reasons this grain is widely used:

- inventory decisions occur at item-location level
- replenishment systems require item-location forecasts
- forecasts can be aggregated later (region, category, network)
- starting from aggregated demand loses important information

## Time Series Ordering

Demand forecasting depends on correctly ordered historical data.

A forecasting pipeline should not assume raw records arrive in the correct order.

For item-location demand forecasting, records should be sorted by:

- `sku_id`
- `location_id`
- `date`

Why this matters:

- forecasting uses past observations to predict future demand
- lag and rolling features depend on chronological order
- evaluation and backtesting break if time order is wrong
- unordered records can create misleading results without obvious errors

## Demand Series

A demand series represents the demand history of a single SKU at a single location over time.

Example:

SKU: milk_1L  
Location: store_102

Date        Demand
2024-01-01     42
2024-01-08     39
2024-01-15     45
2024-01-22     41

In a retail network, the full demand dataset usually contains many such series.

Example:

- 500 SKUs
- 50 stores

This produces up to:

500 × 50 = 25,000 demand series

Forecasting systems typically train or generate forecasts for each series independently.

## Why Start with Dataclasses Instead of Pandas

The forecasting module starts with `dataclass` structures rather than raw Pandas DataFrames.

Why this is useful:

- dataclasses make required fields explicit
- they create stable input/output contracts
- they improve readability of the system design
- they make testing easier
- they prevent loose, ambiguous DataFrame-based interfaces

In this design:

- dataclasses define the system boundary
- Pandas can still be used later as an internal processing tool

This is a cleaner architecture than letting raw DataFrames flow through every part of the module.

## Splitting the Dataset into Demand Series

A full demand dataset is not yet the direct forecasting unit.

Forecasting usually operates on **item-location demand series**.

This means the dataset must be split into groups where each group contains the demand history of:

- one `sku_id`
- at one `location_id`
- across time

Conceptually:

- `DemandDataset` = all rows
- one demand series = one SKU-location history
- forecasting system = many parallel demand series

This step is important because:

- features are created per series
- forecasts are produced per series
- evaluation is often done per series before aggregation


## Forecast Horizon

Forecast horizon defines how far into the future the model is trying to predict.

Examples:

- 1 day ahead
- 1 week ahead
- 4 weeks ahead

The initial forecasting setup in the Supply Chain AI Lab uses:

**1-step-ahead forecasting**

This means the model predicts the next time period for each item-location demand series.

Why start with 1-step-ahead forecasting:

- it is the simplest correct forecasting setup
- it is easy to evaluate
- it creates a strong baseline
- it can later be extended to multi-step forecasting


## Naive Forecast Baseline

Before training any forecasting model, it is important to define a simple baseline forecast.

One common baseline is the **naive forecast**.

Rule:

next demand = last observed demand

Example:

Date        Demand  
2024-01-01     42  
2024-01-08     39  
2024-01-15     45  

Naive forecast for the next period:

45

Why this baseline is important:

- it provides a simple benchmark
- many forecasting models fail to outperform naive forecasts
- it helps detect modeling mistakes early
- it is widely used in forecasting competitions and research

## Why Baselines Matter

A forecasting model should never be evaluated in isolation.

It should first be compared against a simple baseline forecast.

The first baseline used in this project is:

**naive forecast = last observed demand**

Why baselines matter:

- they provide a minimum performance bar
- they prevent misleading claims about model quality
- they help detect broken modeling pipelines
- they make evaluation more credible in real projects and interviews

## Mean Absolute Error (MAE)

MAE stands for **Mean Absolute Error**.

It measures the average size of forecast errors using absolute differences between actual and predicted values.

Formula idea:

- error for one prediction = `abs(actual - predicted)`
- MAE = average of those absolute errors

Example:

- actual = 50, predicted = 45 → error = 5
- actual = 30, predicted = 37 → error = 7

MAE is useful because:

- it is easy to interpret
- it stays in the same unit as demand
- it is a strong first metric for forecast evaluation
- it is easy to explain in interviews and business settings

## Lag Features

Lag features are one of the most common features used in time series forecasting.

A lag feature represents past demand values used as predictors.

Example demand history:

Date        Demand  
2024-01-01     42  
2024-01-08     39  
2024-01-15     45  

Possible lag features:

- lag_1 = demand in previous period
- lag_2 = demand two periods ago
- lag_3 = demand three periods ago

Example feature row:

Date        Demand   lag_1   lag_2  
2024-01-15     45      39      42

Lag features help models capture short-term demand patterns and momentum.

## Rolling Window Features

Rolling window features summarize recent demand behavior.

A rolling feature is calculated using the most recent observations within a fixed window.

Example demand history:

Date        Demand  
2024-01-01     42  
2024-01-08     39  
2024-01-15     45  
2024-01-22     41  

Example rolling mean with window size = 3

For 2024-01-22:

rolling_mean_3 = mean(45, 39, 42)

Rolling window features help capture short-term trends and smooth noisy demand patterns.

# Series Segmentation

In retail forecasting, the raw demand table usually contains rows for many SKUs and many stores.

Example mental line:

table → records → series → features → model

## Why segmentation is needed

A single retail table is not one time series.

Instead, it contains many independent item-location histories, such as:

- SKU A at Store 1
- SKU A at Store 2
- SKU B at Store 1

Each `(sku, store)` pair represents its own demand series.

## What series segmentation does

Series segmentation converts a large table of demand rows into many smaller time-ordered series.

Typical process:

1. read the demand table
2. convert rows into `DemandRecord` objects
3. group records by `(sku, store)`
4. sort each group by date
5. output one `List[DemandRecord]` per group

## Why it matters

Lag features and rolling statistics must be computed only within the correct series.

If segmentation is not done correctly, demand values from different SKUs or stores can leak together, producing invalid forecasting features.


# Series-to-Feature Pipeline

After raw demand data is segmented into item-location series, the forecasting system processes each series independently.

Mental line:

table → records → series → features → model

## Why this step matters

A retail dataset may contain thousands of `(sku, location)` combinations.

The system cannot treat the full table as one time series.

Instead, it must:

1. split the dataset into series
2. process each series independently
3. generate feature rows for each series
4. combine all generated rows into one modeling dataset

## Operational idea

For each `(sku, location)` series:

- sort records by date
- compute lag features
- compute rolling features
- create one feature row per forecastable time point

Then all feature rows are combined into one feature table for modeling.

## Why this is important

This is the step that turns a forecasting concept into a scalable system.

Instead of manually engineering one series, the pipeline can generate training data across many products and locations automatically.

# Feature Row Construction

Feature helper functions such as lags and rolling averages are not the final modeling dataset.

A forecasting model trains on feature rows.

## What is a feature row?

A feature row represents one forecastable time point for one item-location series.

Example:

- sku_id = SKU1
- location_id = STORE1
- date = 2024-01-04
- lag_1 = 13
- lag_2 = 11
- rolling_mean_3 = 12.0
- target = 15

## Why this step matters

The forecasting pipeline must convert each ordered demand series into a set of modeling rows.

Each row contains:

- identifiers
- engineered features from past observations
- the target demand value to learn

## Operational logic

For each series:

1. move through time in chronological order
2. compute features only from prior demand
3. create one row per valid date
4. skip dates that do not have enough history

This is the step that transforms time-series history into a model-ready training table.

# Multi-Series Feature Pipeline

A retail forecasting system must process many item-location series, not just one.

Mental line:

table → records → series → features → model

## Why this step exists

The raw demand dataset contains mixed rows across many SKUs and locations.

The forecasting pipeline must:

1. split the full dataset into item-location series
2. build feature rows for each series independently
3. combine all resulting rows into one training dataset

## Operational flow

DemandDataset
→ split into `(sku_id, location_id)` series
→ build feature rows for each series
→ merge all rows into one feature table

## Why this matters

This is the scaling step.

Instead of manually testing one series, the system can now generate model-ready training rows across the full business dataset automatically.


# From Feature Rows to ML Training Table

The forecasting pipeline first creates model-ready feature rows as Python dataclass objects.

Example flow:

raw table → records → series → feature rows → DataFrame → model

## What is the feature table?

The feature table is the tabular dataset used for machine learning training.

Each row represents one forecastable time point for one item-location series.

Example columns:

- sku_id
- location_id
- date
- lag_1
- lag_2
- rolling_mean_3
- target

## Why convert to a DataFrame?

Machine learning libraries expect tabular input.

A pandas DataFrame makes it easy to:

- inspect the training data
- filter columns
- define X and y
- train forecasting models

## Typical training setup

- X = feature columns such as lag_1, lag_2, rolling_mean_3
- y = target column

This is the final bridge between feature engineering and model training.