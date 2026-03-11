# Demand Forecasting Module Architecture

The demand forecasting module is organized as a layered system where each layer has a clear responsibility.

This structure keeps the forecasting pipeline modular, testable, and easy to extend with new models.

Mental structure of the module:

schemas → data → features → model → evaluate → service

Each layer performs a specific role in the forecasting pipeline.

---

## Schemas Layer

The `schemas` module defines the core data structures used throughout the forecasting system.

Key objects:

- `DemandRecord`
- `DemandDataset`
- `ForecastFeatureRow`
- `ForecastPredictionRow`
- `ForecastEvaluationResult`

These dataclasses define the **system contracts**.

They ensure that each stage of the pipeline receives well-defined inputs and produces predictable outputs.

This prevents raw dictionaries or unstructured DataFrames from flowing through the system.

---

## Data Layer

The `data` module organizes raw demand records into usable time series.

Main responsibilities:

- sorting demand records chronologically
- grouping records into `(sku_id, location_id)` series
- generating historical slices for evaluation
- performing train/test splits for forecasting experiments

Example flow:

DemandDataset  
→ split_into_series  
→ {(sku_id, location_id): List[DemandRecord]}

This segmentation step is critical because forecasting features must be computed **within each series independently**.

---

## Feature Engineering Layer

The `features` module converts demand history into model-ready feature rows.

Typical feature types:

- lag features (lag_1, lag_2, etc.)
- rolling statistics (rolling_mean_k)

Example pipeline:

DemandRecord series  
→ build_feature_rows_for_series  
→ ForecastFeatureRow objects

Feature rows contain:

- identifiers (`sku_id`, `location_id`)
- timestamp
- engineered features
- target demand value

These rows are then converted into a tabular dataset for machine learning.

---

## Model Layer

The `model` module contains forecasting models and training logic.

Implemented models include:

- naive forecast baseline
- linear regression
- tree-based models such as XGBoost

Model responsibilities:

- train forecasting models
- generate predictions from feature inputs

Example flow:

Feature rows  
→ feature_rows_to_dataframe  
→ train_linear_regression_model  
→ predict_with_model

This layer is intentionally modular so additional forecasting models can be added later.

---

## Evaluation Layer

The `evaluate` module measures forecasting performance.

Key responsibilities:

- compute forecast error metrics
- evaluate forecasts on a single series
- evaluate forecasts across many series
- support rolling backtesting
- support train/test horizon evaluation

Primary metric used in the current system:

**Mean Absolute Error (MAE)**

Evaluation can operate at several levels:

- single time series
- dataset-level aggregation
- train/test forecasting experiments

---

## Service Layer

The `service` module provides the **external interface** for the forecasting system.

Other modules in the Supply Chain AI Lab should interact with forecasting only through these service functions.

Examples:

- `get_next_step_forecast`
- `get_forecast_horizon`

Example usage:

series → model → next step forecast

or

series → model → multi-step horizon forecast

The service layer hides the internal feature engineering and model details from the rest of the system.

---

## Recursive Multi-Step Forecasting

The module supports multi-step forecasting through **recursive prediction**.

Process:

1. predict the next demand value
2. append the predicted value to the series
3. recompute features
4. predict the next step again

Example flow:

history  
↓  
predict t+1  
↓  
append prediction  
↓  
predict t+2  
↓  
repeat until horizon reached

This approach allows simple one-step models to generate forecasts for longer horizons.

---

## Full Forecasting Pipeline

The complete demand forecasting pipeline in this project follows the structure below:

DemandDataset  
↓  
split_into_series  
↓  
feature generation  
↓  
training table  
↓  
model training  
↓  
prediction rows  
↓  
forecast generation  
↓  
evaluation  

This modular pipeline makes the forecasting system:

- easier to debug
- easier to extend with new models
- easier to explain in interviews
- closer to real production forecasting architectures