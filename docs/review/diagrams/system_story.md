# Deterministic-First LLM System Overview

```mermaid
flowchart TD

U[User Request] --> O[Orchestrator]

O --> D[Deterministic Layer]

D -->|Resolved| C[Candidate Result]

D -->|Unresolved| CAP{Missing Capability}

CAP -->|Need Tool| T[Tool Runner]
CAP -->|Need Context| RAG[Retrieval System]
CAP -->|Still Unresolved| LQ{Allow LLM Reasoning}

T --> D
RAG --> D

D -->|Still Unresolved| LQ

LQ -->|Yes| L[LLM or Agent Reasoning]
LQ -->|No| C

L --> C

C --> G[Governance Gate]
G --> OUT[Final Output]

O -.-> TR[Trace Artifacts]
D -.-> TR
T -.-> TR
RAG -.-> TR
L -.-> TR
G -.-> TR