# Demand Forecasting Module

Location:

```
projects/supply_chain_ai_lab/src/demand_forecasting/
```

This module implements the **demand forecasting subsystem** of the Supply Chain AI Lab.

Its purpose is to transform raw demand history into **model-ready training data and prediction inputs**, which will later support:

- inventory planning
- replenishment decisions
- allocation and transfers
- simulation experiments
- LLM-based decision support

The module is designed to resemble how a forecasting component would be structured in a real supply chain analytics system.

---

# Forecasting Pipeline

The forecasting module converts raw demand observations into structured inputs for machine learning models.

```
DemandDataset
      ↓
split_into_series
      ↓
Item–Location Time Series
      ↓
Feature Engineering
      ↓
Training Feature Table
      ↓
Prediction Feature Table
```

Two outputs are produced:

- **training feature tables** used to train forecasting models
- **prediction feature tables** used for model inference

---

# Core Concepts

### Demand Record

A **DemandRecord** represents one observation of demand.

Example fields:

- sku_id
- location_id
- date
- demand

Each record represents one row in a retail demand dataset.

---

### Demand Series

Forecasting operates on **time series**, not raw tables.

A demand series represents the demand history for one item at one location.

Example:

```
(SKU1, STORE1)

Jan 1 → 10  
Jan 2 → 12  
Jan 3 → 14  
Jan 4 → 16
```

Series are created by grouping records by:

```
(sku_id, location_id)
```

---

### Feature Generation

Demand forecasting models require **signals derived from past demand**.

Common features include:

- lag features  
- rolling averages  
- calendar indicators (future)  
- product/store attributes (future)

Example features:

| lag_1 | lag_2 | rolling_mean_3 |
|------|------|------|

These features allow the model to learn patterns in demand history.

---

# Module Files

### `__init__.py`

Marks the folder as a Python module.

---

### `service.py`

Defines the **public interface** of the forecasting subsystem.

Other modules in the system should interact with demand forecasting through this layer rather than calling internal components directly.

---

### `model.py`

Contains forecasting model implementations.

Examples that may be implemented later:

- baseline regression models
- gradient boosting models
- time-series models

---

### `features.py`

Responsible for **feature engineering and feature table construction**.

Main responsibilities:

- generating lag features
- generating rolling mean features
- constructing training feature rows
- constructing prediction feature rows
- converting feature rows into pandas DataFrames

---

### `data.py`

Responsible for **preparing demand data for forecasting**.

Key responsibilities:

- validating demand data
- sorting records chronologically
- splitting datasets into item-location series

---

### `evaluate.py`

Responsible for **forecast evaluation**.

Future metrics may include:

- MAE
- RMSE
- MAPE

These metrics measure the quality of model predictions.

---

### `schemas.py`

Defines structured data interfaces used across the forecasting module.

Examples include:

- `DemandRecord`
- `DemandDataset`
- `ForecastFeatureRow`
- `ForecastPredictionRow`

These structures ensure consistent communication between components.