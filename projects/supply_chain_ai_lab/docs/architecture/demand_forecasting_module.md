# Demand Forecasting Module Architecture

The demand forecasting module predicts **future customer demand for each SKU at each location over time**.

Forecasts serve as the **primary signal that drives all downstream supply chain decisions**, including inventory risk evaluation, replenishment policies, and scenario simulations.

The module follows a layered architecture to keep responsibilities clean and extensible.

Mental structure of the module:

schemas → data → features → model → evaluate → service

Each layer performs a specific role in the forecasting pipeline.

---

# Role of Forecasting in the System

Forecasting is the **first stage of the supply chain decision pipeline**.

The broader system pipeline is:

Demand Forecasting  
→ Inventory State Evaluation  
→ Replenishment Policy  
→ Simulation Engine  
→ Disruption Modeling  
→ Allocation Decisions  
→ Network Monitoring  
→ LLM Decision Copilot

Because forecasting sits at the beginning of this chain, its outputs influence every downstream module.

Mental Hook:

Forecasting answers the question:  
**What demand should we expect?**

---

# Schemas Layer

The `schemas` module defines the structured data interfaces used by the forecasting system.

Key objects include:

- `DemandRecord`
- `DemandDataset`
- `ForecastFeatureRow`
- `ForecastPredictionRow`
- `ForecastEvaluationResult`

These dataclasses act as **system contracts**.

They ensure that each stage of the pipeline receives well-defined inputs and produces predictable outputs.

This prevents raw dictionaries or unstructured DataFrames from flowing through the system.

Mental Hook:

Schemas define **the language used inside the forecasting system**.

---

# Data Layer

The `data` module organizes raw demand records into structured time series.

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

Mental Hook:

Data preparation converts raw demand logs into **clean time series signals**.

---

# Feature Engineering Layer

The `features` module converts demand history into model-ready feature rows.

Typical feature types include:

- lag features (lag_1, lag_2, etc.)
- rolling statistics (rolling_mean_k)
- time indicators (optional extensions)

Example pipeline:

DemandRecord series  
→ build_feature_rows_for_series  
→ ForecastFeatureRow objects

Feature rows contain:

- identifiers (`sku_id`, `location_id`)
- timestamp
- engineered features
- target demand value

These rows are then converted into a tabular dataset for machine learning models.

Mental Hook:

Feature engineering transforms **raw demand history into predictive signals**.

---

# Model Layer

The `model` module contains forecasting models and training logic.

Possible models include:

- naive forecast baseline
- linear regression
- tree-based models such as XGBoost
- future extensions (deep learning or hierarchical models)

Model responsibilities:

- train forecasting models
- generate predictions from feature inputs

Example flow:

Feature rows  
→ feature_rows_to_dataframe  
→ train_model  
→ predict_with_model

The model layer remains modular so additional models can be added without affecting the rest of the pipeline.

Mental Hook:

Models convert **signals into demand predictions**.

---

# Evaluation Layer

The `evaluate` module measures forecasting performance.

Key responsibilities include:

- computing forecast error metrics
- evaluating forecasts on a single series
- evaluating forecasts across many series
- supporting rolling backtesting
- supporting train/test horizon evaluation

Primary metric currently used:

Mean Absolute Error (MAE)

Evaluation can operate at several levels:

- single time series
- dataset-level aggregation
- forecasting experiments across horizons

Mental Hook:

Evaluation answers the question:  
**How reliable are our forecasts?**

---

# Service Layer

The `service` module provides the **external interface for the forecasting system**.

Other modules should interact with forecasting only through these service functions.

Examples:

- `get_next_step_forecast`
- `get_forecast_horizon`

Example usage:

series → model → next-step forecast

or

series → model → multi-step forecast horizon

The service layer hides internal implementation details such as feature engineering and model selection.

Mental Hook:

Service functions expose **forecasting as a clean system capability**.

---

# Recursive Multi-Step Forecasting

The module supports multi-step forecasting using **recursive prediction**.

Process:

1. predict the next demand value
2. append the predicted value to the series
3. recompute features
4. predict the next step again

Example flow:

history  
→ predict t+1  
→ append prediction  
→ recompute features  
→ predict t+2  
→ repeat until forecast horizon is reached

This allows simple one-step models to generate longer-horizon forecasts.

Mental Hook:

Recursive forecasting extends **short-term prediction models into multi-period forecasts**.

---

# Full Forecasting Pipeline

The complete forecasting pipeline follows the structure below:

DemandDataset  
→ split_into_series  
→ feature generation  
→ training table  
→ model training  
→ prediction rows  
→ forecast generation  
→ evaluation

This modular pipeline makes the forecasting system:

- easier to debug
- easier to extend with new models
- easier to test
- easier to explain in interviews

Mental Hook:

Forecasting transforms **historical demand data into future demand signals** that drive the rest of the supply chain system.