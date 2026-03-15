# Tool Interface Layer

## Purpose

The Tool Interface Layer provides a **stable interaction layer between the domain modules and higher-level system orchestration**.

Instead of other components calling forecasting, inventory, or replenishment modules directly, they interact with the system through standardized tools.

This allows the system to remain modular and prepares the project for higher-level orchestration components such as:

- the Decision Coordinator
- the Simulation Engine
- disruption analysis modules
- allocation logic
- LLM reasoning layers
- agent-based workflows

The tool layer therefore acts as a **controlled gateway into the operational capabilities of the system**.

---

# System Position

Within the full architecture, the tool layer sits between **system orchestration and domain logic**.

The system flow is structured as follows:

System Orchestration Layer  
(Decision Coordinator, Simulation Engine, LLM reasoning)

↓  

Tool Runner  

↓  

Tool Wrappers  

↓  

Service Layer  

↓  

Domain Modules

Domain modules currently include:

- Demand Forecasting
- Inventory State
- Replenishment Policy

Mental Hook:

The tool layer acts as the **API of the supply chain system**.

---

# Why the Tool Layer Exists

Each subsystem exposes services designed primarily for internal module usage.

Examples include:

Forecasting services require:

- a trained forecasting model
- historical demand records
- forecasting horizons

Inventory services expose calculations such as:

- inventory position
- days of supply
- stockout risk signals

Replenishment services expose:

- reorder point calculations
- reorder decisions
- recommended order quantities

These services are valid domain logic, but they are not ideal **system-level interfaces**.

The tool layer standardizes these capabilities so that the rest of the system interacts with them through **consistent operational tools**.

Mental Hook:

Tools expose **what the system can do**, not how the subsystem works internally.

---

# Tool Layer Structure

The tool layer is implemented in:

src/tools/

Key components include:

schemas.py  
forecast_tool.py  
inventory_tool.py  
replenishment_tool.py  
runner.py  

Each component has a clearly defined responsibility.

---

# Tool Schemas

schemas.py defines the explicit input and output contracts used by the tools.

Examples include:

ForecastToolInput / ForecastToolOutput  

InventoryStatusToolInput / InventoryStatusToolOutput  

ReplenishmentToolInput / ReplenishmentToolOutput  

These schemas define:

- required inputs
- returned results
- stable interface contracts

Mental Hook:

Schemas define the **contract between orchestration and computation**.

---

# Tool Wrappers

Each tool wraps the public service entry points of a subsystem.

Examples:

Forecast Tool

Wraps forecasting service functions to generate demand forecasts.

Inventory Tool

Aggregates multiple inventory metrics into a single operational status.

Replenishment Tool

Delegates to the replenishment recommendation service.

Tools do not implement new domain logic.

They simply expose subsystem capabilities in a structured and standardized form.

Mental Hook:

Tool wrappers translate **system requests into subsystem operations**.

---

# Tool Runner

runner.py provides a **centralized execution gateway** for the tool layer.

Tools are executed through a unified interface:

run_tool(tool_name, input_data)

Example usage:

run_tool("forecast", forecast_input)

run_tool("inventory_status", inventory_input)

run_tool("replenishment", replenishment_input)

This interface allows higher-level components to interact with system capabilities without knowing the internal implementation details.

Mental Hook:

The runner acts as the **command dispatcher of the supply chain system**.

---

# Runner Responsibilities

The runner performs four key tasks:

1. Receive the requested tool name  
2. Validate the input schema  
3. Dispatch execution to the appropriate tool  
4. Return structured output  

The runner does not determine which tool should be used.

Tool selection belongs to higher-level orchestration logic such as:

- the Decision Coordinator
- the Simulation Engine
- LLM reasoning systems
- bounded agents

---

# Dynamic Tool Execution

Tools are executed dynamically by name.

This design allows future components to select tools at runtime.

Examples of future tool users include:

- scenario engines
- disruption analysis modules
- decision coordinators
- LLM reasoning systems
- agent-based orchestration

Dynamic dispatch provides flexibility while schema validation ensures execution safety.

Mental Hook:

Dynamic tool execution enables **adaptive decision systems**.

---

# Dependency Direction

The dependency direction must always remain:

tools  
↓  
services  
↓  
domain modules  

Domain modules must never depend on the tool layer.

This preserves clean architecture and prevents circular dependencies.

---

# Architectural Role

The Tool Interface Layer transforms the project from a collection of independent modules into a **coherent operational system**.

It introduces:

- stable tool contracts
- standardized subsystem access
- a centralized execution gateway
- modular orchestration capability

This layer enables higher-level system capabilities such as:

- scenario simulation
- disruption analysis
- network decision coordination
- LLM-assisted reasoning

while keeping the underlying domain modules independent and reusable.

Mental Hook:

The tool layer turns subsystem capabilities into **system-level operations**.