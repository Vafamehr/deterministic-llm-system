
# Mental line for LLM system.
User message
↓
Clarify / choose strategy
↓
Optimized retrieval query
↓
Data interface retrieves rows / docs
↓
Validation layer
→ enforce schema + types
→ dedupe + key uniqueness checks
→ missingness rules (drop / impute / default)
→ range/sanity checks (no impossible values)
→ contract guardrails (required cols present)
↓
Feature layer
→ compute signals/aggregates (counts, rates, rolling stats)
→ trends/deltas (week-over-week, slope)
→ risk flags (threshold rules)
→ normalize/format units (percent vs fraction, hours vs days)
↓
Context builder
→ produce “clean table” + “summary dict”
→ produce fact_packet text blocks (LLM-ready)
↓
Prompt assembly + packaging
→ instructions + task + constraints
→ attach context (fact_packets + summaries)
↓
Model call (LLM)
↓
Output parsing
→ enforce output schema (JSON)
→ retries on invalid output
↓
Final response to user
→ concise answer + rationale + next action


# Day 22 — Chunk 1: Representation Layer

Goal:
Convert feature table into entity-level summaries usable by reasoning systems.

Why:
LLMs reason better over structured facts than raw rows.

Added:
src/delay_risk/representation/summarize.py

Function:
summarize_projects(df)

Transforms:
project-week rows → one record per project.



# Day 22 — Chunk 2: Pipeline Integration (Representation Layer)

## Goal
Integrate representation layer into pipeline execution.

## Added
- Import: summarize_projects
- After feature construction, generate one-row-per-project summary

## New Output Artifact
outputs/project_summary.csv

## Pipeline Now Produces
- validation_report.json
- feature_table.csv
- project_summary.csv

## Why This Matters
Representation turns engineered features into compact, entity-level records
that downstream reasoning / retrieval layers can consume.


# Day 22 — Chunk 3: Fact Packets (LLM-Readable Context)

## Goal
Convert project-level summary rows into deterministic text blocks ("fact packets")
that can be used as LLM context.

## Added
Module: delay_risk.representation.fact_packets

Functions:
- row_to_fact_packet(row) -> str
- build_fact_packets(summary_df) -> df with fact_packet column

## New Output Artifact
outputs/project_fact_packets.csv

## Why This Matters
LLMs reason best over structured, compact facts.
We compute facts deterministically rather than forcing the model to infer trends
from raw tables.


# Day 22 — Chunk 4 — Fact Packet Reader

## Goal
Consume project_fact_packets.csv through a clean interface.

## Added
- load_fact_packets(path)
- get_fact_packets_for_projects(df, project_ids)

## Guarantees
- Enforces required schema
- Fails early if columns missing
- Returns clean fact_packet text blocks

## Why
Separates data pipeline from LLM reasoning layer.
Acts as contract boundary.


# Day 22 — Chunk 5 — Deterministic Decision Stub

Goal:
Consume fact_packets and output structured risk assessments.

Added:
- assess_risk_from_packets()

Why:
Creates reasoning layer before introducing LLM.
Prevents model from doing deterministic work.
