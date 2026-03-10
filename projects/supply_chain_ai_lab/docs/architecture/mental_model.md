# Mental Model — The Restaurant Network Analogy

To understand the Supply Chain AI Lab, imagine operating a **large restaurant chain**.

Each restaurant must run smoothly while sharing ingredients, suppliers, and logistics across the network.

This analogy provides an intuitive way to understand how modern retail supply chains operate.

---

# The Restaurant Network

Imagine a company operating **100 restaurants across the country**.

Each restaurant must constantly make decisions such as:

- how many meals will be ordered tomorrow
- how many ingredients must be stocked
- when to reorder ingredients
- whether ingredients should be transferred between locations
- how to respond when a supplier fails

Retail supply chains operate in exactly the same way, except the products are retail goods instead of meals.

---

# Mapping the Analogy

| Supply Chain Concept | Restaurant Analogy |
|---|---|
| SKU | Ingredient |
| Store | Restaurant |
| Warehouse | Central kitchen |
| Demand | Customer orders |
| Forecast | Predicting tomorrow's orders |
| Inventory | Ingredients in the fridge |
| Replenishment | Ordering new ingredients |
| Allocation | Sending ingredients to restaurants |
| Disruption | Supplier delay |
| Stockout | Running out of ingredients |
| Service Level | Customers receive what they ordered |

---

# Where Machine Learning Fits

Machine learning helps answer demand-related questions such as:

- How many burgers will customers order tomorrow?
- Which restaurants are likely to run out of tomatoes?
- How will a promotion affect demand?

This problem is known as **Demand Forecasting**, which forms the foundation of many supply chain decisions.

---

# Where Simulation Fits

Forecasts are never perfect. Simulation helps answer:

> What happens if our predictions are wrong?

Examples:

- Will we run out of chicken next week?
- Will we waste too many ingredients?
- What if demand suddenly spikes?

Simulation allows the system to evaluate **what-if scenarios** before real decisions are implemented.

---

# Where Decision Logic Fits

Decision logic determines how the system responds to forecasts and simulations.

Examples include:

- reorder inventory
- transfer inventory between locations
- adjust safety stock levels

These decisions may be based on:

- simple rules
- heuristics
- optimization models
- machine-learning-assisted policies

---

# Where LLMs Fit

Large Language Models do not replace forecasting or optimization.

Instead, they help interpret and explain the system.

Examples include:

- explaining forecast changes
- summarizing disruptions
- comparing operational scenarios
- assisting planners in making decisions

Example explanation:

> "Three stores are projected to run out of chicken by Friday due to increased demand and delayed supplier shipments."

---

# The Goal of the Supply Chain AI Lab

The Supply Chain AI Lab simulates this restaurant-style network.

The system combines:

- machine learning
- simulation
- operational decision policies
- LLM reasoning

to create a realistic AI-powered supply chain decision environment.

---

# Three Operational Layers of Retail Supply Chains

Retail supply chains can be understood through three interacting layers.

---

## 1. Demand Layer

This layer answers:

**What will customers buy?**

Typical problems include:

- demand forecasting
- promotion impact modeling
- seasonality detection
- demand anomaly detection

Machine learning is heavily used in this layer.

---

## 2. Inventory and Flow Layer

This layer answers:

**Where should products be and when?**

Typical problems include:

- replenishment planning
- safety stock calculations
- inventory allocation
- store transfers
- warehouse distribution

This layer often combines:

- forecasts
- rules and heuristics
- optimization methods

---

## 3. Disruption and Decision Layer

This layer answers:

**What should we do when reality deviates from plan?**

Examples include:

- supplier delays
- demand spikes
- inventory shortages
- logistics failures

This layer benefits from:

- simulation
- scenario analysis
- LLM reasoning
- human decision support