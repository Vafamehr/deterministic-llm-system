# Mental Model — The Restaurant Network Analogy

To understand the Supply Chain AI Lab, imagine operating a **large restaurant network**.

Each restaurant must run smoothly while sharing ingredients, suppliers, and logistics across the network.

This analogy provides an intuitive mental framework for understanding how modern retail supply chains operate.

---

# The Restaurant Network

Imagine a company operating **100 restaurants across the country**.

Each restaurant constantly needs to answer operational questions such as:

- how many meals will be ordered tomorrow
- how many ingredients must be stocked
- when ingredients must be reordered
- whether ingredients should be transferred between restaurants
- how to react when suppliers fail or deliveries are delayed

Retail supply chains operate in the same way, except the products are retail goods rather than meals.

---

# Mapping the Analogy

| Supply Chain Concept | Restaurant Analogy |
|---|---|
| SKU | Ingredient |
| Store | Restaurant |
| Distribution Center | Central kitchen |
| Demand | Customer orders |
| Forecast | Predicting tomorrow's orders |
| Inventory | Ingredients in the fridge |
| Replenishment | Ordering new ingredients |
| Allocation | Sending ingredients to restaurants |
| Disruption | Supplier delay |
| Stockout | Running out of ingredients |
| Service Level | Customers receive what they ordered |

This analogy helps visualize how supply chain planning decisions operate across a network.

---

# Where Machine Learning Fits

Machine learning primarily supports **demand understanding**.

Examples of ML-driven questions:

- How many burgers will customers order tomorrow?
- Which restaurants will experience higher demand next week?
- How will a promotion affect demand?

These questions belong to the **Demand Forecasting layer**, which provides signals used by downstream planning systems.

Mental Hook:

Machine learning predicts **what customers will want**.

---

# Where Inventory Logic Fits

After predicting demand, the system must evaluate the **current inventory state**.

Operational questions include:

- Do we have enough tomatoes for tomorrow?
- Which restaurants are close to running out of ingredients?
- How long will current inventory last?

This corresponds to the **Inventory State layer** of the system.

Mental Hook:

Inventory represents the **current reality of the supply chain**.

---

# Where Replenishment Fits

Once demand and inventory are known, the system must decide **what actions to take**.

Typical decisions include:

- reorder ingredients
- increase safety stock
- adjust ordering quantities

This corresponds to the **Replenishment Policy layer**.

Mental Hook:

Replenishment converts **signals into operational actions**.

---

# Where Simulation Fits

Forecasts and policies are built on assumptions.

Simulation helps test those assumptions by exploring possible futures.

Examples include:

- demand spikes during promotions
- sudden increases in customer traffic
- supplier delivery delays
- unexpected inventory losses

Simulation answers the question:

"What happens if conditions change?"

Mental Hook:

Simulation is the **supply chain laboratory** where policies are stress-tested.

---

# Where Disruption Modeling Fits

Real supply chains rarely operate under perfectly stable conditions.

Disruptions may include:

- supplier delays
- transportation failures
- manufacturing issues
- sudden demand spikes

Disruption modeling evaluates how these events affect the system.

Mental Hook:

Disruption modeling tests whether the supply chain is **resilient to uncertainty**.

---

# Where Allocation Fits

Sometimes the network does not have enough inventory to satisfy all locations.

For example:

- a central warehouse has limited ingredients
- multiple restaurants require the same supplies

The system must decide **which locations receive priority**.

Mental Hook:

Allocation answers the question:

"Who receives limited inventory first?"

---

# Where Monitoring Fits

Supply chain operators must monitor the health of the entire system.

Typical operational metrics include:

- service level
- fill rate
- forecast accuracy
- stockout rate
- inventory turnover

This monitoring layer acts as the **control tower** of the system.

Mental Hook:

Monitoring answers the question:

"Is the supply chain operating safely?"

---

# Where LLMs Fit

Large Language Models do not replace operational models.

Instead they interpret and explain the system.

Examples include:

- explaining forecast changes
- summarizing disruptions
- comparing scenario outcomes
- generating decision-support summaries

Example explanation:

"Three restaurants are projected to run out of chicken by Friday due to increased demand and delayed supplier deliveries."

Mental Hook:

LLMs act as the **Supply Chain Decision Copilot**.

---

# The Goal of the Supply Chain AI Lab

The Supply Chain AI Lab simulates a realistic supply chain decision platform.

The system combines:

- machine learning
- inventory logic
- replenishment policies
- scenario simulation
- disruption modeling
- network monitoring
- LLM reasoning

This creates a structured environment for experimenting with modern AI-powered supply chain decision systems.

---

# Four Operational Layers of Supply Chain Intelligence

Supply chains can be understood through four interacting layers.

---

## 1. Demand Layer

This layer answers:

"What will customers buy?"

Typical problems include:

- demand forecasting
- promotion impact modeling
- seasonality detection
- demand anomaly detection

Machine learning is heavily used in this layer.

---

## 2. Inventory Layer

This layer answers:

"What inventory do we currently have and how safe is it?"

Typical problems include:

- inventory position evaluation
- safety stock calculations
- stockout risk estimation

---

## 3. Decision Layer

This layer answers:

"What operational decisions should we make?"

Typical problems include:

- replenishment planning
- inventory allocation
- network balancing

---

## 4. Scenario & Resilience Layer

This layer answers:

"What happens if conditions change?"

Examples include:

- demand spikes
- supplier disruptions
- logistics failures
- inventory shocks

Simulation and disruption modeling are heavily used in this layer.

---

# Final Mental Model

The Supply Chain AI Lab follows a simple decision logic:

Predict demand  
Evaluate inventory health  
Decide replenishment actions  
Stress test decisions with simulation  
Manage disruptions and supply risk  
Allocate scarce inventory across the network  
Monitor system performance  
Explain outcomes with LLM reasoning