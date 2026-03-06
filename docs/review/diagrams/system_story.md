# Deterministic-First LLM System Overview

```mermaid
flowchart TD

U[User Request] --> O[Orchestrator]

O --> D[Deterministic Layer]

D -->|Resolved| C[Candidate Result]

D -->|Unresolved| CAP{Missing Capability}

CAP -->|Tool Needed| T[Tool Runner]
CAP -->|Context Needed| R[Retrieval System]
CAP -->|No Structured Option| LQ{Allow LLM Reasoning}

T --> D
R --> D

D -->|Still Unresolved| LQ

LQ -->|Yes| L[LLM Reasoning]
LQ -->|No| C

L --> C

C --> G[Governance Gate]

G --> OUT[Final Output]

O -.-> TR[Trace Artifacts]
D -.-> TR
T -.-> TR
R -.-> TR
L -.-> TR
G -.-> TR