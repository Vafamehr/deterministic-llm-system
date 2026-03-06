# Deterministic-First LLM System Master Architecture

```mermaid
flowchart TD

U[User Request] --> O[Orchestrator]

O --> D{Deterministic Attempt}

D -->|Resolved| C[Candidate Result]

D -->|Need Tool| T[Tool Runner]
D -->|Need Retrieval| R[Retrieval System]
D -->|Still Unresolved| LQ{Allow LLM Reasoning}

T --> D
R --> D

LQ -->|Yes| L[LLM or Agent Reasoning]
LQ -->|No| C

L --> C

C --> G{Governance Gate}

G -->|Approved| OUT[Final Output]
G -->|Needs Review| SAFE[Safe Fallback or Review Output]

SAFE --> OUT

O -.-> TR[Trace Artifacts]
D -.-> TR
T -.-> TR
R -.-> TR
L -.-> TR
G -.-> TR