# Tools and Retrieval Capability Flow

```mermaid
flowchart TD

D[Deterministic Layer] --> CAP{Missing Capability}

CAP -->|Need Tool| TR[Tool Runner]
CAP -->|Need Retrieval| RET[Retrieval System]

TR --> REG[Tool Registry]
REG --> TOOL[Tool Execution]

TOOL --> RES[Structured Tool Result]

RET --> IDX[Knowledge Index]
IDX --> CHUNK[Retrieved Context]

RES --> D
CHUNK --> D

D -->|Still Unresolved| LLM[LLM Reasoning]