# LLM System Architecture Overview

```mermaid
flowchart TD

U[User Request] --> O[Orchestrator]

subgraph L1[Control Layer]
O
end

subgraph L2[Deterministic Layer]
D[Deterministic Execution]
end

subgraph L3[Capability Layer]
TR[Tool Runner]
RET[Retrieval System]
AR[Bounded Agent Step]
LLM[LLM Reasoning]
end

subgraph L4[Safety Layer]
G[Governance Gate]
end

subgraph L5[Observability Layer]
T[Trace Artifacts]
end

O --> D

D -->|Need tool| TR
D -->|Need context| RET
D -->|Need bounded decision| AR
D -->|Need model reasoning| LLM

TR --> D
RET --> D
AR --> D
LLM --> D

D --> C[Candidate Result]
C --> G
G --> OUT[Final Output]

O -.-> T
D -.-> T
TR -.-> T
RET -.-> T
AR -.-> T
LLM -.-> T
G -.-> T