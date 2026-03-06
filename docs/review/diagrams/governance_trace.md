# Governance and Trace Flow

```mermaid
flowchart TD

C[Candidate Result] --> G{Governance Gate}

G -->|Approved| OUT[Final Output]
G -->|Needs Review| OUT

subgraph Observability Layer
T[Trace Artifacts]
end

C -.-> T
G -.-> T
OUT -.-> T