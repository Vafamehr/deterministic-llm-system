# Data Layer Architecture

## Purpose

This document explains the design of the data layer for the Supply Chain AI Lab.

The data layer provides the inputs required to run the system in a clean, modular, and interview-friendly way.

It supports two distinct purposes:

1. **Operational network data**
2. **Historical demand data**

These two data types serve different roles and are intentionally separated.

---

## Design Principle

The Supply Chain AI Lab follows a **deterministic-first architecture**.

That means:

- the operational supply chain engine should run on structured, trusted inputs
- the forecasting side should use tabular historical data suitable for ML workflows
- the system should clearly separate:
  - structural network data
  - current operational state
  - historical time-series demand

This separation keeps the architecture clean and scalable.

---

## Data Layer Components

The data layer currently consists of the following files under:

`src/sample_data/`

### Operational network files

- `network_products.csv`
- `network_locations.csv`
- `network_suppliers.csv`
- `network_lanes.csv`
- `inventory_snapshot.csv`

### Python loaders / generators

- `sample_network.py`
- `synthetic_demand_history.py`

### Generated historical demand file

- `synthetic_demand_history.csv`

---

## Two Data Worlds

### 1. Operational Network Data

Operational network data describes the structure and current state of the supply chain.

It includes:

- products
- locations
- suppliers
- transportation lanes
- inventory snapshot

This data is used by:

- inventory
- replenishment
- decision coordinator
- simulation engine
- scenario analysis
- disruption modeling
- allocation
- network monitoring

This dataset is intentionally **small and readable** so that the full system can be demonstrated clearly.

---

### 2. Historical Demand Data

Historical demand data describes past demand over time.

It includes:

- date
- sku_id
- location_id
- units_sold

This data is used by:

- demand forecasting
- model training
- evaluation
- future feature engineering

This dataset is intentionally **medium-sized** so that the forecasting side of the project becomes legitimate without making the system too large to understand.

---

## Architectural Separation

The system separates data into three conceptual categories.

### Structural Data

Structural data defines the configuration of the supply chain network.

Examples include:

- products
- locations
- suppliers
- transportation lanes

This information typically changes rarely and defines the structure of the system.

---

### Snapshot State Data

Snapshot data represents the operational state of the network at a specific point in time.

Example:

- inventory snapshot

This data is consumed by operational modules that evaluate stock positions and generate decisions.

---

### Time-Series Data

Time-series data represents historical observations indexed by time.

Example:

- synthetic demand history

This data powers forecasting models and future analytical workflows.

---

## File-Level Architecture

### `sample_network.py`

This module loads the operational network data from CSV files and converts the rows into typed dataclass objects.

It acts as the bridge between:

- tabular source files
- internal typed supply chain objects

The module exposes a single entry point:

`build_sample_network()`

This function returns a `SampleNetwork` object containing:

- products
- locations
- suppliers
- transportation lanes
- inventory records

This provides the rest of the system with a structured operational network representation.

---

### `synthetic_demand_history.py`

This module generates synthetic historical demand data for forecasting workflows.

It operates primarily in tabular form using pandas.

Its responsibilities include:

1. loading product and location definitions
2. creating the date × sku × location grid
3. simulating demand values
4. returning a demand history DataFrame
5. optionally saving the generated dataset to CSV

This approach keeps the forecasting dataset consistent with the operational network definitions.

---

## Why the Data Layer Uses Both Dataclasses and DataFrames

The data layer intentionally uses two complementary data representations.

### Dataclasses

Dataclasses are used for operational entities and decision-engine inputs.

Examples include:

- `InventoryRecord`
- `ProductRecord`
- `LocationRecord`
- `SupplierRecord`
- `TransportationLaneRecord`
- `SampleNetwork`

These structures are useful for:

- explicit schemas
- typed interfaces
- deterministic system modules
- clear domain modeling

---

### DataFrames

DataFrames are used for historical demand data and ML-oriented workflows.

They support operations such as:

- filtering
- joins
- aggregation
- feature engineering
- model training pipelines

---

This creates a clean separation:

- **DataFrames support tabular analytics and forecasting workflows**
- **Dataclasses define the contracts for operational system components**

---

## Current Data Flow

The operational network follows this path:

CSV files  
→ pandas DataFrames  
→ row dictionaries  
→ dataclass objects  
→ `SampleNetwork` object  
→ supply chain decision modules

The historical demand pipeline follows this path:

network product and location tables  
→ date expansion  
→ synthetic demand generation  
→ pandas DataFrame  
→ saved demand history CSV  
→ forecasting workflows

---

## Architecture Summary

The data layer is intentionally divided into two complementary parts.

The first part is the **operational network dataset**, which provides the structural configuration and snapshot state needed by the deterministic supply chain modules.

The second part is the **historical demand dataset**, which provides time-series demand observations for forecasting workflows.

This separation keeps the system architecture clean:

- operational modules consume structured network objects
- forecasting workflows consume tabular historical demand data

The data layer itself does not contain decision logic.  
Its role is to provide reliable, structured inputs to the rest of the Supply Chain AI Lab.