# Data Layer Architecture

## Purpose

This document defines the **data layer of the Supply Chain AI Lab**.

The data layer provides **clean, structured inputs** for both:

- the deterministic decision system
- the forecasting / ML workflows

It separates data into two core categories:

1. **Operational network data**
2. **Historical demand data**

---

## One-Line Summary

The data layer separates **operational state (dataclasses)** from **historical demand (DataFrames)** to support both decision logic and forecasting cleanly.

---

## Design Principle

The system follows a **deterministic-first architecture**, which requires:

- structured and reliable inputs for decision modules
- flexible tabular data for ML workflows
- strict separation between:
  - network structure
  - current state
  - historical time-series data

This prevents mixing computation with system interfaces.

---

## Data Layer Components

Located under:

`src/sample_data/`

### Operational Network Files

- `network_products.csv`
- `network_locations.csv`
- `network_suppliers.csv`
- `network_lanes.csv`
- `inventory_snapshot.csv`

### Python Modules

- `sample_network.py`
- `synthetic_demand_history.py`

### Generated Dataset

- `synthetic_demand_history.csv`

---

## Two Data Worlds

### 1. Operational Network Data

Represents the **structure and current state** of the supply chain.

Includes:

- products
- locations
- suppliers
- transportation lanes
- inventory snapshot

Used by:

- inventory module
- replenishment module
- decision coordinator
- simulation
- disruption modeling
- allocation
- monitoring

This dataset is intentionally **small and readable** to make system behavior easy to trace.

---

### 2. Historical Demand Data

Represents **past demand over time**.

Includes:

- date
- sku_id
- location_id
- units_sold

Used by:

- forecasting
- model training
- evaluation
- feature engineering

This dataset is intentionally **larger and tabular** to support realistic ML workflows.

---

## Data Categories

The data layer separates data into three conceptual types.

### Structural Data
Defines the network configuration:

- products
- locations
- suppliers
- lanes

Changes infrequently.

---

### Snapshot State Data
Represents current system state:

- inventory snapshot

Used directly by decision modules.

---

### Time-Series Data
Represents historical observations:

- demand history

Used for forecasting and analysis.

---

## File-Level Architecture

### `sample_network.py`

Loads operational CSV data and converts it into structured objects.

Flow:

CSV → DataFrame → row dict → dataclass → `SampleNetwork`

Provides:

- products
- locations
- suppliers
- lanes
- inventory

This creates a **typed representation of the supply chain network**.

---

### `synthetic_demand_history.py`

Generates historical demand data for forecasting.

Responsibilities:

1. load product and location definitions  
2. create date × sku × location grid  
3. simulate demand  
4. return DataFrame  
5. optionally save to CSV  

This ensures consistency between demand data and the network.

---

## Data Representation Strategy

The system uses two complementary representations.

### Dataclasses (Operational System)

Used for:

- inventory records  
- product records  
- location records  
- supplier records  
- transportation lanes  
- network container  

Purpose:

- enforce schema
- define module interfaces
- support deterministic execution

---

### DataFrames (ML / Analytics)

Used for:

- demand history  
- feature engineering  
- aggregation  
- joins  
- model training  

Purpose:

- flexible computation
- efficient transformations

---

### Why This Separation Exists

- DataFrames are optimized for computation  
- Dataclasses enforce system boundaries  

The goal is to prevent raw tabular data from leaking into decision interfaces.

---

## Current Data Flow

### Operational Flow

CSV  
→ DataFrame  
→ dataclass objects  
→ `SampleNetwork`  
→ decision modules  

---

### Forecasting Flow

network definitions  
→ grid expansion (date × sku × location)  
→ demand simulation  
→ DataFrame  
→ CSV  
→ forecasting module  

---

## Architecture Summary

The data layer has two roles:

1. provide structured operational inputs for decision modules  
2. provide historical demand data for forecasting  

This results in a clean system:

- decision modules consume **typed network objects**  
- forecasting workflows consume **tabular demand data**  

The data layer contains **no decision logic**.  
It exists only to provide **reliable, structured inputs** to the system.