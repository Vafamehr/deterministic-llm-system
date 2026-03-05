# Tools and Retrieval Capability Flow

```mermaid
flowchart TD

DET[Deterministic Stage] --> CAP{Missing Capability}

CAP -->|Need Tool| TR[Tool Runner]
CAP -->|Need Retrieval| RET[Retrieval Interface]

TR --> REG[Tool Registry]
REG --> TOOL[Tool Execution]

TOOL --> RES[Structured Tool Result]

RET --> IDX[Knowledge Index]
IDX --> CHUNK[Retrieved Context Chunks]

RES --> DET
CHUNK --> DET

DET -->|Still Unresolved| LLM[LLM or Agent Reasoning]