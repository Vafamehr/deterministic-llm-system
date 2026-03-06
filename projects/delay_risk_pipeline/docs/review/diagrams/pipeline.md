# Request Execution Pipeline

```mermaid
flowchart TD

U[User Request] --> O[Orchestrator]

O --> D{Deterministic Attempt}

D -->|Resolved| R[Candidate Result]

D -->|Unresolved| CAP{Missing Capability}

CAP -->|Need Tool| T[Tool Runner]
CAP -->|Need Retrieval| RET[Retrieval System]
CAP -->|No Structured Option| LQ{Allow LLM Reasoning}

T --> D
RET --> D

D -->|Still Unresolved| LQ

LQ -->|Yes| L[LLM Reasoning]
LQ -->|No| R

L --> R

R --> G{Governance Check}

G -->|Approved| OUT[Final Output]
G -->|Needs Review| OUT

O -.-> TR[Trace Artifacts]
D -.-> TR
T -.-> TR
RET -.-> TR
L -.-> TR
G -.-> TR