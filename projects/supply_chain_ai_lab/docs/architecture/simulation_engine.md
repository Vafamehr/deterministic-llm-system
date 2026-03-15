# Simulation Engine - Architecture

## Purpose

The Simulation Engine is a **scenario execution layer** that sits above the decision pipeline.

Its role is to evaluate how the supply chain decision system behaves under different operating conditions.

Instead of executing the decision pipeline once, the Simulation Engine executes the same pipeline multiple times with controlled input modifications.

This allows planners to test system behavior under situations such as:

• demand spikes  
• supplier delays  
• promotions  
• inventory disruptions  

The Simulation Engine therefore acts as a **policy testing laboratory for the supply chain system**.

---

# Position in System Architecture

Current deterministic pipeline:

Demand Forecasting  
↓  
Inventory Evaluation  
↓  
Replenishment Decision  
↓  
Decision Coordinator

The Simulation Engine sits above the coordinator.

Final system flow:

Simulation Engine  
↓  
Decision Coordinator  
↓  
Tool Runner  
↓  
Domain Modules

The Simulation Engine must **reuse the existing decision pipeline** rather than reimplementing decision logic.

---

# Role of the Simulation Engine

The engine performs four main responsibilities.

1. Define scenarios.

2. Modify system inputs according to scenario rules.

3. Execute the existing decision pipeline.

4. Collect structured results for scenario comparison.

The Simulation Engine never performs forecasting or replenishment directly.

It only orchestrates **experiments using the real decision pipeline**.

---

# Example Scenarios

Baseline scenario  
No modifications to inputs.

Demand spike  
Demand increases by a multiplier.

Supplier delay  
Lead time increases.

Promotion event  
Temporary demand boost.

Inventory shock  
Sudden reduction in available inventory.

Each scenario modifies specific inputs before execution.

---

# Scenario Execution Flow

For each scenario:

1. Start with base input data.

2. Apply scenario modification rules.

Example:

Demand spike  
→ multiply demand history by a factor.

Supplier delay  
→ increase lead_time_days.

Inventory shock  
→ reduce inventory position.

3. Call the existing Decision Coordinator.

4. Capture the resulting decision output.

5. Store scenario results for later comparison.

---

# Expected Output

Each scenario execution returns a structured result containing fields such as:

• scenario_name  
• forecast_summary  
• inventory_risk_indicators  
• replenishment_recommendation  
• service_level_estimate  

These outputs allow the system to compare outcomes across scenarios.

---

# Scenario Comparison Purpose

After executing multiple scenarios the engine can answer questions such as:

• Which scenario causes the highest stockout risk?  
• Which scenario generates the largest replenishment orders?  
• Which scenario breaks the replenishment policy?  

This transforms the system into a **decision experimentation platform**.

---

# Project Location

Simulation Engine lives inside the source tree:

src/simulation_engine/

Expected structure:

simulation_engine/

__init__.py  
schemas.py  
scenarios.py  
service.py  
smoke_test.py  

---

# File Responsibilities

schemas.py

Defines simulation input schemas and scenario result schemas.

scenarios.py

Defines scenario modification rules.

service.py

Implements the Simulation Engine that executes scenarios and collects results.

smoke_test.py

Runs test scenarios to validate system behavior.

---

# Dependency Direction

The Simulation Engine depends on the existing system.

The dependency chain must remain:

simulation_engine  
↓  
decision_coordinator  
↓  
tools  
↓  
domain modules  

Domain modules must never depend on simulation.

This keeps the architecture modular and extensible.

---

# Mental Hook

Simulation Engine = **Supply Chain Policy Laboratory**

Instead of asking:

"What decision does the system make?"

Simulation asks:

"What decisions does the system make when the world changes?"