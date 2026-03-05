# LLM System Architecture Overview
  
  ```mermaid

flowchart TD

User[User Request] --> O[Orchestrator]

subgraph Core Execution
D[Deterministic Layer]
end

subgraph Capability Layer
TR[Tool Runner]
RET[Retrieval System]
end

subgraph Reasoning Layer
A[Agent Reasoning Optional]
LLM[LLM Reasoning Optional]
end

subgraph Safety and Observability
G[Governance Gate]
T[Trace Artifacts]
end

O --> D

D -->|Need tool| TR
D -->|Need context| RET
D -->|Need bounded decision| A
D -->|Need freeform reasoning| LLM

TR --> D
RET --> D
A --> D
LLM --> D

D --> C[Candidate Result]
C --> G --> OUT[Final Output]

O -.-> T
D -.-> T
TR -.-> T
RET -.-> T
A -.-> T
LLM -.-> T
G -.-> T

```