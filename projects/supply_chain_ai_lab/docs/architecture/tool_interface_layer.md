# Tool Interface Layer

## Purpose

The Tool Interface Layer provides a stable bridge between the supply chain subsystems and higher-level system logic.

Instead of future components calling forecasting, inventory, or replenishment modules directly, they interact with the system through standardized tools.

This allows the system to remain modular and prepares the project for later additions such as scenario engines, coordinators, and LLM agents.

---

## System Position

The architecture now looks like this:

Decision Logic (future)  
↓  
Tool Runner  
↓  
Tool Wrappers  
↓  
Service Layer  
↓  
Domain Modules  

Domain modules currently include:

• Demand Forecasting  
• Inventory  
• Replenishment  

The tool layer sits between **system control logic and domain computation**.

---

## Why the Tool Layer Exists

Each subsystem exposes services designed for internal module usage.

Examples:

Forecasting requires:
• a trained model  
• historical demand records  

Inventory exposes:
• inventory position calculation  
• days of supply  
• stock risk signals  

Replenishment exposes:
• reorder point  
• reorder decision  
• order quantity recommendation  

These are valid domain services, but they are not ideal system-level interfaces.

The tool layer standardizes access so future components interact with the system through a consistent surface.

---

## Tool Layer Structure

src/tools/

schemas.py  
forecast_tool.py  
inventory_tool.py  
replenishment_tool.py  
runner.py  

Each component has a clear responsibility.

---

## Tool Schemas

schemas.py defines explicit input and output contracts for each tool.

Examples include:

ForecastToolInput / ForecastToolOutput  
InventoryStatusToolInput / InventoryStatusToolOutput  
ReplenishmentToolInput / ReplenishmentToolOutput  

These schemas define:

• required inputs  
• returned results  
• stable interface contracts  

---

## Tool Wrappers

Each tool wraps the public service entry points of a subsystem.

Examples:

Forecast Tool  
Wraps the forecasting service functions.

Inventory Tool  
Aggregates multiple inventory metrics into one operational status.

Replenishment Tool  
Delegates to the replenishment recommendation service.

Tools do not implement new domain logic.  
They simply expose subsystem capabilities in a structured form.

---

## Tool Runner

runner.py provides a single execution gateway.

Tools are executed through:

run_tool(tool_name, input_data)

Example usage:

run_tool("forecast", forecast_input)  
run_tool("inventory_status", inventory_input)  
run_tool("replenishment", replenishment_input)

This allows future components to interact with tools through one centralized interface.

---

## Runner Responsibilities

The runner performs four tasks:

1. Receive the tool name  
2. Validate the input type  
3. Dispatch execution to the correct tool  
4. Return the structured output  

The runner does not decide which tool should be used.  
Tool selection belongs to higher-level logic such as coordinators or agents.

---

## Dynamic Tool Execution

Tools are executed dynamically by name.

This allows future components such as:

• scenario engines  
• decision coordinators  
• LLM reasoning systems  
• bounded agents  

to select tools at runtime.

Dynamic dispatch provides flexibility while input validation maintains safety.

---

## Dependency Direction

The dependency direction must always remain:

tools  
↓  
services  
↓  
domain modules  

Domain modules must never depend on the tool layer.

This preserves clean architectural layering and prevents circular dependencies.

---

## Architectural Role

The Tool Interface Layer transforms the project from a set of independent modules into a usable system.

It introduces:

• stable tool contracts  
• standardized subsystem access  
• a centralized execution gateway  

This layer enables future system capabilities such as scenario simulation, disruption analysis, and agent-driven workflows while keeping the domain modules independent.