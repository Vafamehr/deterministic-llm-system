# Demand Forecasting Module

## Purpose

Predicts future demand for each SKU-location pair.

---

## One-Line Summary

Converts historical demand into a demand signal.

---

## Role in System

Forecasting is called by the coordinator.

* it does not control execution
* it does not interact with other modules directly
* it only produces predictions

All outputs return to the coordinator.

---

## Inputs

* historical demand data
* model
* forecast horizon

---

## Output

* predicted demand values

---

## Processing Steps

* group time series by SKU-location
* generate features
* run model
* produce predictions

---

## Service Interface

* get_next_step_forecast
* get_forecast_horizon

---

## What It Does Not Do

* no inventory logic
* no replenishment logic
* no orchestration

---

## Key Rule

Forecast output is not passed directly to other modules.
The coordinator transforms it into expected demand.

---

## One-Line Summary

A modular forecasting component that produces demand signals for the coordinator.
