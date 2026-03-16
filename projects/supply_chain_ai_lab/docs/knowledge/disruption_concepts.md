# Supply Chain Disruptions — Core Concepts

## Why Disruptions Matter

Real-world supply chains rarely operate under stable conditions. Operational planning systems must handle unexpected disruptions that affect demand, supply, and logistics.

Examples include:

* supplier production delays
* transportation bottlenecks
* sudden demand spikes
* warehouse outages
* inventory shrinkage or damage

These disruptions introduce uncertainty into supply chain planning and can lead to stockouts, overstocking, delayed deliveries, and service failures.

Because of this, modern supply chain systems include **scenario planning and disruption simulation** capabilities.

---

## Categories of Supply Chain Disruptions

Disruptions generally fall into several categories.

### Supply Disruptions

Supply disruptions occur when inbound supply becomes delayed or unavailable.

Examples:

* supplier production delays
* supplier bankruptcy
* raw material shortages
* quality issues leading to rejected shipments

Operational effects may include:

* increased lead time
* reduced supply availability
* missed replenishment cycles

---

### Demand Disruptions

Demand disruptions occur when demand suddenly increases or decreases beyond forecast expectations.

Examples:

* viral product popularity
* emergency demand spikes
* promotional campaigns exceeding expectations
* seasonal shifts

Operational effects may include:

* demand multipliers
* faster inventory depletion
* unexpected stockouts

---

### Logistics Disruptions

Logistics disruptions occur when transportation or distribution networks fail to move inventory as expected.

Examples:

* port congestion
* trucking shortages
* extreme weather events
* customs delays

Operational effects may include:

* transportation delays
* increased transit times
* missed replenishment schedules

---

### Infrastructure Disruptions

Infrastructure disruptions occur when physical facilities become unavailable or degraded.

Examples:

* warehouse fires
* power outages
* IT system failures
* labor strikes

Operational effects may include:

* reduced warehouse capacity
* delayed order fulfillment
* restricted inventory movement

---

### Inventory Disruptions

Inventory disruptions involve the loss or damage of inventory already in the system.

Examples:

* spoilage
* theft or shrinkage
* product recalls
* damage during transportation

Operational effects may include:

* sudden inventory reductions
* increased stockout risk

---

## Disruptions in Planning Systems

Planning systems typically model disruptions in two layers.

### Business Event Layer

This layer describes the disruption in real-world business terms.

Examples:

* supplier delay
* warehouse shutdown
* demand surge

These events are understandable by planners and analysts.

---

### Operational Impact Layer

This layer expresses the disruption in numeric parameters that the planning system can simulate.

Examples:

* lead time increase
* demand multiplier
* inventory loss
* capacity reduction

Simulation engines apply these numeric parameters to evaluate how the system behaves under disruption scenarios.

---

## Role of Disruption Modeling in the Supply Chain AI Lab

In this project, disruption modeling enables the simulation engine to test how the supply chain decision pipeline behaves under abnormal conditions.

The system can evaluate questions such as:

* What happens if a supplier shipment is delayed?
* How does the system respond to a regional demand spike?
* Which locations face the highest stockout risk during a disruption?
* How should inventory be reallocated when supply becomes constrained?

By running disruption scenarios, planners can identify vulnerabilities and evaluate alternative decision strategies.

---

## Why Scenario Simulation is Important

Scenario simulation allows organizations to:

* stress-test planning systems
* identify operational bottlenecks
* prepare contingency plans
* evaluate inventory buffers
* improve supply chain resilience

Instead of reacting to disruptions after they occur, organizations can **anticipate risks and prepare responses ahead of time**.

This capability is a core feature of modern supply chain decision platforms.
