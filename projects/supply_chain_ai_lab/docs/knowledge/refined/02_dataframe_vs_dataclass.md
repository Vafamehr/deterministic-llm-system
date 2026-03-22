# DataFrame vs Dataclass

This is a separation of roles.

Not a style preference.
Not extra complexity for no reason.

It exists because the system does two different kinds of work.

---

# The Core Idea

Use:

- **DataFrames** for computation
- **Dataclasses** for system boundaries

Mental hook:

DataFrames are for **working**.
Dataclasses are for **handing off**.

---

# Why DataFrames Exist

DataFrames are good for analytical work.

They are built for:

- filtering
- grouping
- joining
- aggregating
- feature creation
- model training

This is the natural form for demand history and forecasting workflows.

Example:

You have sales by SKU, store, and date.
You need rolling averages, lag features, weekly totals, or train/test splits.

That is DataFrame work.

---

# Why Dataclasses Exist

Dataclasses are good for structured interfaces.

They make it clear:

- what a module expects
- what a module returns
- what fields matter

This is useful when one module hands work to another.

Example:

A forecasting tool should not receive a random loose object.
It should receive a clearly defined input.

That makes the system easier to read, test, and trust.

---

# Why Not Use Only DataFrames?

Because DataFrames are flexible, but loose.

They are great for analytics.
They are weak as system contracts.

Problems with using only DataFrames everywhere:

- expected columns become implicit
- bad inputs fail late
- boundaries become blurry
- module interfaces become vague

In a notebook, that is survivable.

In a system, it becomes messy fast.

---

# Why Not Use Only Dataclasses?

Because they are too rigid for heavy analytical work.

Forecasting pipelines often need:

- slicing by time
- aggregating across locations
- generating many features
- quick transformations

That is painful if everything is forced into small typed objects.

So the point is not to pick one.
The point is to use each where it fits.

---

# The Two Worlds

## DataFrame World

This is the **analytics world**.

Used for:

- demand history
- time-series processing
- feature engineering
- model inputs
- evaluation tables

This world is flexible and computation-heavy.

---

## Dataclass World

This is the **system world**.

Used for:

- tool inputs
- tool outputs
- inventory state
- decision handoffs
- explicit interfaces

This world is strict and interface-heavy.

---

# Where the Boundary Happens

A common pattern is:

1. load raw data into DataFrames
2. do analytical work
3. produce a clean result
4. package that result into a dataclass
5. pass it to the next module

That boundary matters.

It tells you:

"The analysis is done. Now the system will act on a defined result."

---

# Simple Example

Forecasting side:

- demand history lives in a DataFrame
- model generates predicted demand

Decision side:

- predicted demand is packaged into a dataclass
- inventory module reads that structured result
- replenishment module makes a decision

So yes, the system may start with CSVs and DataFrames.

But it should not stay shapeless all the way through.

---

# Why This Matters:

This separation shows maturity.

It tells:

- you understand analytics workflows
- you understand system design
- you know that models alone are not systems
- you care about stable interfaces

That is the real point.

Not "I like dataclasses."

The point is:

"I keep computation flexible and system boundaries explicit."

---

# Mental Model

Think of it like this:

- DataFrame = workshop
- Dataclass = shipping box

You build and transform inside the workshop.
When it is ready to move safely through the system, you put it in a box.

---

# Common Mistake

People say:

"If the real system uses tables anyway, why bother?"

Because raw tables do not automatically create clean module boundaries.

A production system still needs:

- explicit inputs
- explicit outputs
- readable contracts
- predictable handoffs

The table is the data format.
The dataclass is the interface.

Those are not the same thing.

---

# One-Line Summary

Use DataFrames for analytical computation and dataclasses for clear module boundaries, so the system stays both flexible in modeling and stable in decision flow.