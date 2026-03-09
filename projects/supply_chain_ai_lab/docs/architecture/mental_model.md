# Mental Model — The Restaurant Network Analogy

To understand the Supply Chain AI Lab, imagine running a **large restaurant chain**.

Each restaurant must operate smoothly while sharing supply resources across the network.

This analogy helps explain how supply chains operate.

---

## The Restaurant System

Imagine a company that owns **100 restaurants across the country**.

Each restaurant must decide:

- how many meals will be ordered tomorrow
- how many ingredients must be stocked
- when to order new ingredients
- whether to move ingredients between locations
- how to react if a supplier fails

This is exactly how a **retail supply chain** operates.

---

## Mapping the Analogy

| Supply Chain Concept | Restaurant Analogy |
|---|---|
| SKU | Ingredient |
| Store | Restaurant |
| Warehouse | Central kitchen |
| Demand | Customer orders |
| Forecast | Predicting tomorrow’s orders |
| Inventory | Ingredients in the fridge |
| Replenishment | Ordering new ingredients |
| Allocation | Sending ingredients to restaurants |
| Disruption | Supplier delay |
| Stockout | Running out of food |
| Service Level | Customers get what they ordered |

---

## Where Machine Learning Fits

Machine learning helps answer questions like:

- How many burgers will customers order tomorrow?
- Which restaurant will run out of tomatoes?
- How does a promotion change demand?

This is **Demand Forecasting**.

---

## Where Simulation Fits

Simulation answers:

> What happens if our predictions are wrong?

Example questions:

- Will we run out of chicken next week?
- Will we waste too many ingredients?
- What if demand suddenly spikes?

Simulation allows the system to test **what-if scenarios**.

---

## Where Decision Logic Fits

Decision logic determines actions such as:

- reorder inventory
- transfer inventory between locations
- adjust safety stock

These decisions can be:

- rule-based
- heuristic
- optimization-driven
- ML-assisted

---

## Where LLMs Fit

LLMs do not replace forecasting or simulation.

Instead, they help with:

- explaining system outputs
- summarizing disruptions
- comparing scenarios
- assisting human decision-makers

Example:

"Three stores will likely run out of chicken by Friday due to higher demand and delayed supplier shipments."

---

## The Goal of the Lab

The Supply Chain AI Lab simulates this restaurant network.

It combines:

- machine learning
- simulation
- decision policies
- LLM reasoning

to create a realistic AI-powered supply chain system.

---

## The Three Operational Layers of Retail Supply Chains

Retail supply chains can also be understood through three operational layers.

### 1. Demand Layer

This layer answers:

**What will customers buy?**

Typical problems:

- demand forecasting
- promotion impact modeling
- seasonality detection
- demand anomaly detection

This is where **machine learning is most heavily used**.

---

### 2. Inventory and Flow Layer

This layer answers:

**Where should products be and when?**

Typical problems:

- replenishment planning
- safety stock decisions
- inventory allocation
- store transfers
- warehouse distribution

This layer often combines:

- forecasting
- rules and heuristics
- optimization

---

### 3. Disruption and Decision Layer

This layer answers:

**What should we do when reality deviates from plan?**

Typical problems:

- supplier delays
- demand spikes
- stockout risks
- logistics failures

This layer benefits from:

- simulation
- scenario analysis
- LLM reasoning
- human decision support