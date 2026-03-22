# Data Layer Concepts

## Why a Data Layer Exists

In a real supply chain system, the decision logic cannot operate without structured data describing the network and its historical behavior.

The **data layer** exists to provide these structured inputs in a clean and predictable way.

For the Supply Chain AI Lab, the data layer serves two major purposes:

1. describing the **operational supply chain network**
2. providing **historical demand observations** for forecasting

These two types of data are fundamentally different and are intentionally separated.

---

## Operational Network Data

Operational network data describes **how the supply chain is structured and what its current state is**.

This includes entities such as:

- products
- locations
- suppliers
- transportation lanes
- inventory levels

This information represents the **physical and logical structure of the supply chain**.

Operational modules such as:

- inventory evaluation
- replenishment decisions
- allocation logic
- network monitoring

require this information to reason about the current state of the system.

For this reason, operational network data is modeled using **typed domain objects** rather than raw tables.

This makes the operational system more explicit and easier to reason about.

---

## Historical Demand Data

Historical demand data represents **past sales or consumption over time**.

Typical attributes include:

- date
- sku_id
- location_id
- units_sold

Unlike operational network data, historical demand is **time-series data**.

It is used for:

- demand forecasting
- model training
- forecast evaluation
- feature engineering

Because forecasting workflows rely heavily on tabular operations such as filtering, aggregation, and joins, this data is typically handled using **DataFrames** rather than domain objects.

---

## Structural Data vs Operational State

Supply chain systems usually distinguish between **structural configuration** and **operational state**.

### Structural Data

Structural data defines the layout of the network.

Examples include:

- which products exist
- which locations exist
- which suppliers serve which locations
- which transportation lanes connect nodes

This information changes rarely and defines the **shape of the supply chain network**.

---

### Operational State

Operational state describes the **current condition of the system at a specific moment in time**.

Examples include:

- inventory on hand
- inventory on order
- reserved inventory

This information changes frequently as the system operates.

Operational modules consume this state to decide:

- whether inventory is sufficient
- whether to reorder
- how to allocate scarce supply

---

## Time-Series Demand Data

Historical demand introduces a third type of data: **time-indexed observations**.

Instead of describing a structure or a snapshot, time-series data records **how the system behaved over time**.

This is necessary because forecasting models rely on patterns such as:

- trends
- seasonality
- demand variability
- promotional spikes

By modeling demand history separately from the operational network, the architecture keeps the forecasting system independent from the operational decision engine.

---

## Why Synthetic Data Is Used

Real supply chain datasets are typically:

- proprietary
- confidential
- extremely large
- difficult to share publicly

For learning and demonstration purposes, the Supply Chain AI Lab uses **synthetic datasets**.

Synthetic data allows the system to:

- demonstrate realistic workflows
- train forecasting models
- simulate scenarios
- remain reproducible and shareable

The synthetic demand generator ensures that demand history is **consistent with the defined network products and locations**.

---

## Why the Project Uses Both Dataclasses and DataFrames

The system intentionally uses two complementary data representations.

### Dataclasses

Dataclasses represent **domain entities** inside the operational supply chain engine.

Examples include:

- products
- locations
- suppliers
- transportation lanes
- inventory records

These structures provide:

- explicit schemas
- strong typing
- clear module interfaces
- easier reasoning about domain objects

---

### DataFrames

DataFrames represent **tabular analytical datasets**.

They are particularly well suited for:

- demand history
- feature engineering
- statistical analysis
- model training

Using DataFrames for analytical workflows keeps the forecasting pipeline flexible and compatible with common ML tools.

---

## Conceptual Data Flow

The data layer feeds two major parts of the system.

Historical demand supports the **forecasting workflow**, which produces expected future demand.

Operational network data supports the **deterministic decision engine**, which uses the forecast and current inventory state to generate operational decisions.

In simplified terms:

Historical Demand  
→ Demand Forecasting  
→ Expected Demand

Operational Network  
→ Inventory Evaluation  
→ Replenishment Decisions  
→ Supply Chain Operations

---

## Why This Architecture Matters

Separating operational network data from historical demand data creates several benefits:

- the deterministic supply chain engine remains simple and transparent
- the forecasting system can evolve independently
- the architecture mirrors real enterprise supply chain systems
- the system remains easy to explain in interviews

The data layer therefore acts as the **foundation of the entire supply chain decision platform**, ensuring that every module operates on well-defined and structured inputs.