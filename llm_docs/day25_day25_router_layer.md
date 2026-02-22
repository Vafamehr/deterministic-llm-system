# LLM System Architecture — Day 25 State

## 1. Stable Base: Linear Execution Pipeline

### Execution Flow

User message
→ Strategy selection (deterministic router)
→ Retrieval query construction
→ Data interface (rows/docs)
→ Validation layer
→ Feature layer
→ Context builder
→ Prompt assembly
→ LLM call
→ Output parsing
→ Final response

---

## 2. Data Discipline Layer

### Validation Layer
- Schema + type enforcement
- Deduplication + key uniqueness
- Missingness handling (drop / impute / default)
- Range / sanity checks
- Contract guardrails (required columns)

### Feature Layer
- Aggregates (counts, rates, rolling stats)
- Trends (WoW deltas, slope)
- Risk flags (threshold rules)
- Unit normalization

### Context Builder
- Structured summary dict
- Clean tabular representation
- Fact packets (LLM-ready blocks)

---

## 3. Output Discipline

- Prompt constraints enforced
- JSON schema validation
- Retry loop on invalid output
- Final answer + rationale + next action

---

# Architectural Property

System is strictly linear.
One fixed execution path.
No dynamic planning.
No autonomous loops.

Deterministic and observable.

---

# Day 25 Upgrade

## Deterministic Strategy Router

System evolved from:

User → Linear Pipeline

To:

User → Router → Linear Pipeline

### Strategy Enum
- ANALYTICS
- POLICY
- SUMMARY
- GENERAL (fallback)

### Router Responsibilities
- Inspect user input
- Select execution strategy
- No execution logic
- No LLM
- No planning

---

# Why This Matters

- Clean separation of decision vs execution
- Enables multiple pipeline variants
- Prepares for planner/executor layer (future)
- Improves observability and testing

System status:
**Routed, deterministic, production-structured linear pipeline.**



Orchestrator Refactor (Chunk 3)

Previously, run_full_assessment() contained:

routing

deterministic scoring

LLM execution

cross-check logic

Now it is split into:

_run_deterministic()

_run_llm()

_cross_check()

run_full_assessment() is now only a coordination layer.

Impact:

Clear separation of concerns

Swappable components

Testable layers

Production-safe structure

System remains linear and deterministic, but is now modular and scalable.