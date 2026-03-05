# Day 21 — Chunk 1: Feature Construction Layer

## Goal
Transform validated rows into interpretable risk signals.

# RUle: Don’t ask the model to discover structure you can compute deterministically.


User message
   ↓
Clarify / choose strategy
   ↓
Optimized RAG query
   ↓
Data interface retrieves rows / docs
   ↓
🔥 VALIDATION HAPPENS HERE 🔥
   → enforce schema, check duplicates, handle missingness, guard data contract
   ↓
🔥 FEATURE LAYER HAPPENS HERE 🔥
   → transform clean rows into structured signals (risk indicators, aggregates, trends)
   ↓
Structured context goes to LLM / model
   ↓
Prompt assembly + packaging
   ↓
Output




## Added
Module: delay_risk.features.build_features

Function:
build_features(df) → returns enriched dataframe

## Example Features
- weeks_observed
- week_progress (relative lifecycle position)
- staffing_delta (change detection)

## Design Rules
- Pure function (no side effects)
- Does not mutate input dataframe
- Works independently of I/O

## Why This Exists
This layer converts raw observations into structured signals
that downstream ML or LLM components can reason over.


# Day 21 — Chunk 2: Additional Risk Features

## Added Features
- weeks_observed: count of snapshots per project
- week_progress: snapshot_week normalized by max week per project
- staffing_delta: week-over-week staffing change (if staffing_level exists)
- staffing_roll_std_3: rolling std over last 3 snapshots (instability proxy)

## Notes
- Feature code is robust to missing optional columns.
- No I/O and no validation inside feature layer.