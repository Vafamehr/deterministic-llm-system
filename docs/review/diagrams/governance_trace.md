# Governance and Trace Flow

```mermaid
flowchart TD

C[Candidate Result] --> G{Governance Check}

G -->|Approved| OUT[Final Output]
G -->|Needs Review| OUT

subgraph Observability
T[Trace Artifacts]
end

C -.-> T
G -.-> T
OUT -.-> T