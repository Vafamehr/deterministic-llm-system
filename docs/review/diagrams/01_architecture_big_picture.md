# System Architecture

```mermaid
flowchart TD
A[Input Data] --> B[Validation]
B --> C[Features]
C --> D[Representation]
D --> E[Fact Packets]
E --> F[Orchestrator]
F --> G[Deterministic]
G --> H{Need Retrieval?}
H -- Yes --> I[ToolRunner + ToolEnvelope]
I --> J[rag.retrieve]
J --> K[Context Chunks]
H -- No --> L[LLM]
K --> L
L --> M[Cross-check]
M --> N[Governance]
N --> O[Bounded Agent Decision Window]
O --> P[Final Output + Trace]