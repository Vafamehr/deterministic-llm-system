# Demand Forecasting Module

Location:

projects/supply_chain_ai_lab/src/demand_forecasting/

This module implements the demand forecasting subsystem of the Supply Chain AI Lab.

Its goal is to generate demand predictions that can later support:

- inventory planning
- replenishment decisions
- allocation and transfers
- simulation experiments
- LLM-based decision support


---

## Module Files

### __init__.py

Marks the folder as a Python module.


### service.py

The public interface of the forecasting system.

Other modules should interact with demand forecasting through this file.


### model.py

Contains forecasting model implementations.

Examples (later):

- baseline models
- tree models
- time series models


### features.py

Creates forecasting features such as:

- lag features
- rolling averages
- calendar indicators
- item/store descriptors


### data.py

Responsible for preparing input demand data:

- loading data
- validating schema
- sorting by time
- creating train/test splits


### evaluate.py

Measures forecast performance.

Will later contain metrics such as:

- MAE
- RMSE
- MAPE


### schemas.py

Defines structured inputs and outputs used across the forecasting module.

Helps keep interfaces stable across components.