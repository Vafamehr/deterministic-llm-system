# Failure Handling and Degradation Flow

```mermaid
flowchart TD

REQ[User Request] --> DET{Deterministic Attempt}

DET -->|Resolved| RES[Candidate Result]

DET -->|Unresolved| CAP{Capability Expansion}

CAP --> TOOL[Tool Execution]
CAP --> RET[Retrieval]

TOOL --> DET
RET --> DET

DET -->|Still Unresolved| LLM[LLM or Agent Reasoning]

LLM --> RES

RES --> GOV{Governance Check}

GOV -->|Approved| OUT[Final Output]

GOV -->|Needs Review| SAFE[Safe Fallback Response]

SAFE --> OUT