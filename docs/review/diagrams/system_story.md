# Deterministic-First LLM System Overview

  ```mermaid
flowchart TD

U[User Request] --> O[Orchestrator]

O --> D[Deterministic Layer: rules validation logic]

D -->|Resolved| C[Candidate Answer]

D -->|Unresolved| CAP{Missing capability}

CAP -->|Need tool| T[Tool Execution: registry and envelope]

CAP -->|Need context| RAG[Retrieval: bounded query]

CAP -->|Neither or ambiguous| LQ{Allow LLM}

T --> D
RAG --> D

D -->|Still unresolved| LQ

LQ -->|Yes| L[LLM Reasoning Secondary Layer]

LQ -->|No| C

L --> C

C --> G[Governance Gate: risk and ambiguity check]

G --> OUT[Final Output]

O -.-> TR[Trace Artifacts]
D -.-> TR
T -.-> TR
RAG -.-> TR
L -.-> TR
G -.-> TR
  ```