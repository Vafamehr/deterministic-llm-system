# Supply Chain AI Lab — System Architecture

## Purpose

This document describes the **overall architecture of the Supply Chain AI Lab**.

The project simulates how a real retail supply chain AI platform can be structured.  
Each module represents a component commonly found in production supply chain analytics systems.

This file provides a **top-level architectural overview**, while detailed explanations are documented in the other architecture files.

---

# System Overview

The Supply Chain AI Lab is designed as a **modular system** that mirrors the structure of real-world supply chain AI platforms.

The architecture separates responsibilities into several conceptual layers:

- **Domain Layer** — defines the business context and problem space of the system.
- **Data Layer** — defines how retail demand data is structured and represented.
- **Feature Layer** — transforms demand history into model-ready signals.
- **Model Layer** — trains forecasting models and generates predictions.
- **Service Layer** — exposes forecasting functionality to downstream applications.

This layered design keeps responsibilities clearly separated and allows each component to evolve independently.

---

# Architecture Documents

This file acts as the **entry point for the architecture documentation**.

Detailed explanations of individual components are provided in the following documents:

- **domain_scope.md** — defines the business problems the lab is designed to address
- **mental_model.md** — explains the conceptual intuition behind the supply chain system
- **retail_data_model.md** — describes how retail demand data is structured
- **module_map.md** — outlines the system modules and their responsibilities
- **demand_forecasting_module.md** — explains the architecture of the forecasting component

Together, these documents describe the structure and design of the Supply Chain AI Lab.

---

# Top-Level Forecasting Pipeline

The forecasting system transforms retail demand data into model-ready inputs through a structured pipeline:

```
Retail Demand Table
        ↓
Demand Records
        ↓
Item–Location Series
        ↓
Feature Engineering
        ↓
Training Feature Tables / Prediction Feature Tables
```

Each stage progressively converts raw retail observations into structured signals that forecasting models can consume.

---

# System Architecture Diagram

The Supply Chain AI Lab can be viewed as a layered analytical system.

```
Retail Data Sources
    (sales, inventory, shipments, promotions)
                │
                ▼
        Retail Data Model
        (SKU × Location × Time)
                │
                ▼
        Demand Forecasting
        (feature engineering + models)
                │
                ▼
        Inventory Simulation
        (simulate inventory dynamics)
                │
                ▼
        Inventory & Replenishment
        (restocking decisions)
                │
                ▼
        Allocation & Transfers
        (network inventory balancing)
                │
                ▼
        Disruption Intelligence
        (detect supply chain anomalies)
                │
                ▼
        Decision Support Layer
        (LLM reasoning + explanations)
```

This layered structure allows the system to combine:

- machine learning
- simulation
- optimization
- LLM reasoning

within a unified supply chain decision platform.


---

# Demand Forecasting Pipeline

The demand forecasting subsystem transforms raw retail demand data into model-ready inputs.

```
Sales / Demand Table
        │
        ▼
DemandDataset
        │
        ▼
split_into_series
(group by SKU × Location)
        │
        ▼
Item–Location Time Series
        │
        ▼
Feature Engineering
(lags, rolling averages)
        │
        ▼
ForecastFeatureRow
(training rows)
        │
        ▼
Training Feature Table
(pandas DataFrame)
```

For prediction, the pipeline generates the next-step feature input:

```
Latest Demand Series
        │
        ▼
build_prediction_row_for_series
        │
        ▼
ForecastPredictionRow
        │
        ▼
Prediction Feature Table
(model input)
```

This pipeline is implemented in the forecasting module:

```
src/demand_forecasting/
```

Key components include:

- `schemas.py` — structured data interfaces
- `data.py` — series segmentation
- `features.py` — feature generation
- `model.py` — forecasting models (future)
- `evaluate.py` — forecast evaluation (future)
- `service.py` — public interface