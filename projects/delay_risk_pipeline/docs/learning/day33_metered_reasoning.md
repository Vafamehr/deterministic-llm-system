## Day 33 — Metered Reasoning (From Single-Step to Orchestrator-Scheduled Multi-Step)

### Goal
Extend the system from a single bounded reasoning call to controlled multi-step reasoning **without introducing agent autonomy, loops, or recursive behavior**.

The orchestrator must remain the authority that:
- Grants reasoning capacity
- Schedules each step explicitly
- Audits how that capacity was used

---

### What Changed

#### 1) Externalized Step Authority
- Removed `max_steps` from `AgentController`.
- Introduced `step_budget` provided by the orchestrator.
- The agent can no longer decide how long it runs.

#### 2) Orchestrator Leases Reasoning Capacity
- `step_budget` is defined at the orchestration layer.
- Passed into `agent.decide(...)` as an execution constraint.
- Converted reasoning from **self-directed iteration** to **metered allocation**.

#### 3) Scheduled Multi-Step Execution (No Loops)
- Orchestrator explicitly invokes:
  - Step 0 (`step_index=0`)
  - Optional Step 1 (`step_index=1`)
- No `while`, no recursion, no continuation requests from the agent.

Reasoning steps are **scheduled work units**, not a thinking loop.

#### 4) Deterministic Final Decision Selection
Collapsed results using:

```python
decision = decision_1 or decision_0
```

Downstream pipeline remains unchanged and unaware of internal metering.

#### 5) Governance and ExecutionEnvelope Remain the Gatekeepers
Every scheduled step still passes through:

Deterministic → Governance → ExecutionEnvelope → Agent

Multi-step reasoning does not bypass safety or policy controls.

#### 6) Trace Now Audits the Metered Window
Added a dedicated trace event: `metered_reasoning_window`

Captures:
- Allocated `step_budget`
- Whether Step 1 ran
- Which step produced the final decision

Reasoning capacity is now observable and auditable.

#### 7) Output Contract Carries the Budget Explicitly
- `_build_output(...)` now accepts `step_budget`.
- Budget is passed end-to-end from orchestrator → output.
- No hidden globals or agent-owned limits.

#### 8) Stabilized Trace / Output Schema
Replaced fragile attribute reads with:

```python
getattr(decision, "field", None)
```

This keeps the audit surface stable as internal structures evolve.

#### 9) Unified Metered Execution Path
Introduced `_run_metered_decision_window(...)` helper:
- Eliminates duplicated orchestration logic across early-exit and normal paths
- Guarantees consistent enforcement of metering behavior

---

### Why It Matters Architecturally

Day 33 converts the reasoning layer from:

**Embedded Intelligence Model**
- Agent decides how long to think

to:

**Governed Compute Model**
- System leases bounded reasoning capacity

This mirrors production decision systems:
- Optimization engines receive compute budgets
- Risk evaluators run under execution caps
- Workflow schedulers — not models — control depth

Reasoning is treated as a **bounded service**, not a driver.

---

### Control Architecture After Day 33

Routing  
↓  
Execution Plan  
↓  
Deterministic Processing  
↓  
Governance Evaluation  
↓  
ExecutionEnvelope (allowed actions)  
↓  
Orchestrator schedules Step 0 / Step 1  
↓  
Agent evaluates within leased budget  
↓  
Trace records metered usage  
↓  
Single governed decision emitted  

---

### What We Deliberately Did NOT Do
- No adaptive loops
- No autonomous continuation
- No recursive reasoning chains
- No model-selected depth
- No dynamic budgets

Day 33 establishes **control mechanics first**, before adding sophistication.

---

### Mental Line (Day 33)
Multi-step reasoning is safe only when the orchestrator schedules, bounds, and audits every step.