# Bounded Agent Control

```mermaid
flowchart TD

O[Orchestrator] --> DW{Agent Decision Window}

DW -->|Reasoning Allowed| A[Agent Reasoning]

A --> DEC[Structured Decision]

DEC --> D[Deterministic Layer]

D --> RES[Candidate Result]

O -.-> T[Trace Artifacts]
A -.-> T
D -.-> T