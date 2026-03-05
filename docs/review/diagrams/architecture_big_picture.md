# LLM System Architecture Overview
  
  ```mermaid

flowchart TD

User[User Request]

subgraph Control Layer
O[Orchestrator]
end

subgraph Deterministic Layer
D[Rules Validation Known Logic]
end

subgraph Capability Layer
T[Tool Execution]
RAG[Retrieval System]
LLM[LLM Reasoning Optional]
end

subgraph Safety Layer
G[Governance Checks]
end

subgraph Observability
TR[Trace Artifacts]
end

User --> O
O --> D

D -->|Need capability| T
D -->|Need context| RAG
D -->|Still unresolved| LLM

T --> D
RAG --> D
LLM --> D

D --> G
G --> Output[Final Output]

O -.-> TR
D -.-> TR
T -.-> TR
RAG -.-> TR
LLM -.-> TR
G -.-> TR

```