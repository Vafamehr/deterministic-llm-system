# Supply Chain Decision Pipeline — Architecture

This system is a **deterministic, modular supply chain decision pipeline** that transforms demand into inventory decisions.

Core flow:

forecast → inventory → replenishment

Execution is controlled by a **Decision Coordinator**, and orchestration across scenarios is handled by the **System Runner**.

---

## One-Line Summary

A coordinator-driven pipeline where demand is computed centrally, modules execute sequentially, and external capabilities (simulation, disruption, allocation, monitoring) operate outside the core flow.

---

## End-to-End Flow

```mermaid
flowchart LR
    A[Demand History] --> B[Forecast Tool]
    B --> C[Forecast Output]
    C --> D[Decision Coordinator]
    D --> E[Inventory Tool]
    E --> F[Replenishment Tool]
    F --> G[Decision Output]
```

---

## Coordinator Logic (Causal Flow)

```mermaid
flowchart LR
    A[Forecast Output] --> B[Decision Coordinator]
    D[Disruption Impact] --> B
    E[Demand Multiplier Override] --> B

    B --> C[Expected Demand]
    C --> F[Inventory Tool]
    F --> G[Inventory Output]
    G --> H[Replenishment Tool]
    H --> I[Replenishment Decision]
``` 

### Coordinator Responsibilities

- execute modules in correct order  
- recompute expected demand from forecast  
- apply optional demand adjustments  
- construct clean inputs for downstream modules  
- return decision + trace  

### Rules

- forecast is not directly passed to inventory  
- expected demand is always computed inside coordinator  
- adjustments are optional inputs:
  - disruption impact  
  - demand multiplier override  
- inventory and replenishment only consume coordinator outputs  

---

## System Runner (Execution Modes)

```mermaid
flowchart TB
    A[System Runner]

    B[Baseline Mode]
    C[Disruption Mode]
    D[Simulation Mode]
    E[Allocation Mode]
    F[Monitoring Mode]

    G[Decision Coordinator]
    H[Disruption Module]
    I[Simulation Engine]
    J[Allocation Module]
    K[Monitoring Module]

    A --> B --> G
    A --> C --> H --> G
    A --> D --> I --> G

    A --> E --> J
    A --> F --> K
```

### Runner Responsibilities

- selects execution mode  
- routes flow correctly  
- keeps core pipeline unchanged  

### Rules

- coordinator always executes core pipeline  
- disruption produces impact → then coordinator runs  
- simulation produces overrides → then coordinator runs  
- allocation operates outside core pipeline (multi-location)  
- monitoring evaluates state, not decisions  

---

## Dependency Flow

```mermaid
flowchart LR
    A[Forecast] --> B[Coordinator Demand Computation]
    B --> C[Inventory Evaluation]
    C --> D[Replenishment Decision]
```

---

## Layered Architecture

```mermaid
flowchart TB
    subgraph Data_Layer
        A[Demand Data]
        B[Feature Engineering]
        C[Forecast Model]
    end

    subgraph Module_Layer
        D[Forecast Tool]
        E[Inventory Tool]
        F[Replenishment Tool]
        G[Disruption Module]
        H[Simulation Engine]
        I[Allocation Module]
        J[Monitoring Module]
    end

    subgraph Control_Layer
        K[Decision Coordinator]
        L[System Runner]
    end

    A --> D
    B --> D
    C --> D

    D --> K
    K --> E --> F

    L --> K
    L --> G
    L --> H
    L --> I
    L --> J
```

---

## Data Representation Separation

### DataFrame World

- data loading  
- transformation  
- feature engineering  
- model computation  

### Dataclass World

- module inputs  
- module outputs  
- system interfaces  

### Why

- DataFrames are optimized for computation  
- dataclasses enforce stable system boundaries  
- prevents leakage of raw computation into decision interfaces  

---

## Module Positioning

```mermaid
flowchart TB
    subgraph Core Pipeline
        A[Forecast]
        B[Inventory]
        C[Replenishment]
        D[Coordinator]
    end

    subgraph External Modules
        E[Disruption]
        F[Simulation]
        G[Allocation]
        H[Monitoring]
    end

    D --> A --> B --> C

    E --> D
    F --> D

    G -. external .- D
    H -. evaluation .- D
```

---

## Key Principles

- coordinator owns demand computation  
- pipeline is strictly sequential  
- system runner controls orchestration  
- external modules do not alter pipeline structure  
- clear separation between computation and interfaces  

---

## Common Failure Modes

- skipping inventory step  
- passing forecast directly to replenishment  
- embedding allocation inside pipeline  
- letting simulation alter core logic  
- mixing orchestration into modules  
- using DataFrames as system interfaces  

---

## Mental Model

```mermaid
flowchart LR
    A[Predict] --> B[Adjust] --> C[Evaluate] --> D[Decide]
```

Forecast → Coordinator → Inventory → Replenishment