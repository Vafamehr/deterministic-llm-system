# Example System Run

This document explains a real execution of the deterministic-first LLM pipeline.  
The full structured trace for this run is available in `runs/example_run.json`.

---

## User Request

Assess risk levels for active projects and recommend next actions.

---

## Pipeline Execution

1. **Orchestrator**
   - Receives the request and creates an execution plan.

2. **Deterministic Layer**
   - Evaluates structured project signals (progress, staffing levels, volatility).
   - Generates fact packets describing project conditions.

3. **Retrieval**
   - The system retrieves governance rules and tool system design documents from the local knowledge index.
   - Retrieved context helps enforce execution constraints and system policies.

4. **LLM Reasoning**
   - Uses deterministic signals and retrieved context to assess project risk levels and produce recommendations.

5. **Cross-Check**
   - Verifies that LLM conclusions remain consistent with deterministic assessments.

6. **Governance**
   - Ensures no policy violations occurred and confirms the output can be emitted.

---

## Final Output

The system identified:

- **Project A:** Medium risk due to moderate staffing volatility.
- **Project B:** High risk due to lower progress and higher staffing volatility.

Recommended action:

- Review staffing allocation for Project A and monitor Project B closely.

---

## Trace Artifact

A real pipeline execution trace is stored in:

`runs/example_run.json`

This file contains the structured execution record of the system, including:

- execution plan
- deterministic stage results
- retrieval/tool activity
- LLM reasoning stage
- governance decision
- decision trace