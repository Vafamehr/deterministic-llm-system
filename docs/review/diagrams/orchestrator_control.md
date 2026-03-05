# Orchestrator Control Flow
 ```mermaid
flowchart TD

REQ[User Request] --> O[Orchestrator]

O --> PLAN[Execution Plan]

PLAN --> DET[Deterministic Stage]

DET -->|Resolved| RESULT[Candidate Result]

DET -->|Needs Tool| TOOL[Tool Runner]
DET -->|Needs Retrieval| RET[Retrieval System]
DET -->|Still unresolved| LLMQ{Allow LLM}

TOOL --> DET
RET --> DET

LLMQ -->|Yes| LLM[LLM Reasoning]
LLMQ -->|No| RESULT

LLM --> RESULT

RESULT --> GOV[Governance Check]

O -.-> TRACE[Trace Artifacts]
PLAN -.-> TRACE
DET -.-> TRACE
TOOL -.-> TRACE
RET -.-> TRACE
LLM -.-> TRACE
GOV -.-> TRACE

 ```