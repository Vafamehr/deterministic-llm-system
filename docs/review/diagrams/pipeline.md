# Request Execution Pipeline

```mermaid
flowchart TD

U[User Request] --> O[Orchestrator]

O --> D{Deterministic Check}

D -->|Resolved| R[Candidate Result]

D -->|Unresolved| CAP{Missing Capability}

CAP -->|Need Tool| T[Tool Runner]
CAP -->|Need Retrieval| RET[Retrieval System]
CAP -->|Still Unresolved| LQ{Allow LLM Reasoning}

T --> TO{Tool Outcome}
RET --> RO{Retrieval Outcome}

TO -->|Returned Data| D
TO -->|Produced Answer| R
TO -->|Failed| LQ

RO -->|Returned Context| D
RO -->|No Useful Context| LQ

D -->|Still Unresolved| LQ

LQ -->|Yes| L[LLM or Agent Reasoning]
LQ -->|No| R

L --> R

R --> G{Governance Check}

G -->|Approved| OUT[Final Output]
G -->|Needs Review| OUT

O -.-> TR[Trace Artifacts]
D -.-> TR
CAP -.-> TR
T -.-> TR
RET -.-> TR
L -.-> TR
G -.-> TR