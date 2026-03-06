# Orchestrator Control Flow

```mermaid
flowchart TD

REQ[User Request] --> O[Orchestrator]

O --> PLAN[Execution Plan]

PLAN --> DET{Deterministic Stage}

DET -->|Resolved| RESULT[Candidate Result]

DET -->|Need Tool| TOOL[Tool Runner]
DET -->|Need Retrieval| RET[Retrieval System]
DET -->|Still Unresolved| LLMQ{Allow LLM Reasoning}

TOOL --> DET
RET --> DET

LLMQ -->|Yes| LLM[LLM Reasoning]
LLMQ -->|No| RESULT

LLM --> RESULT

RESULT --> GOV[Governance Check]

GOV --> OUT[Final Output]

O -.-> TRACE[Trace Artifacts]
PLAN -.-> TRACE
DET -.-> TRACE
TOOL -.-> TRACE
RET -.-> TRACE
LLM -.-> TRACE
GOV -.-> TRACE