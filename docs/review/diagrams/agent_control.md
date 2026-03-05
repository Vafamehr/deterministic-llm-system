# Bounded Agent Control

```mermaid
flowchart TD

O[Orchestrator] --> DW[Agent Decision Window]

DW -->|Allow Reasoning| A[Agent Reasoning]

A --> DEC[Structured Decision]

DEC --> DET[Deterministic Stage]

DET --> RES[Candidate Result]

O -.-> TRACE[Trace Artifacts]
A -.-> TRACE
DET -.-> TRACE