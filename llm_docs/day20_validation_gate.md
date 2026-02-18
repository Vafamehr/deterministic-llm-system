# Day 20 — Chunk 1: Validation Gate (Minimal)

# Validation is the guardrail between retrieval and generation.

meaning:
User message
   ↓
Clarify / choose strategy
   ↓
Optimized RAG query
   ↓
Data interface retrieves rows / docs
   ↓
🔥 VALIDATION HAPPENS HERE 🔥-----------> we should validate schema , take care of schema, missing values etc, 
   ↓
Clean context goes to LLM
   ↓
Prompt assembly + output


## Goal
Add a single validation entrypoint that every pipeline run must call.

## What I Implemented
File: `src/delay_risk/validation/validate.py`

- `ValidationResult` dataclass:
  - ok, errors, warnings, stats

- `validate_inputs(df, mode=...)` checks:
  - required columns exist (project_id, snapshot_week)
  - in train mode, label column exists (will_slip_4_6w)
  - df not empty
  - no duplicate (project_id, snapshot_week)

## Python Fluency Notes
- `@dataclass` creates clean result objects without boilerplate.
- `*` makes arguments keyword-only (safer calls).

## Test
`test_validate.py` intentionally creates duplicate keys and validation fails fast with readable errors.



# Day 20 — Chunk 2: Data Quality Validation

## Goal
Move beyond structure validation to validate the content of the data.

## Added Checks

### Missingness Detection
Computed column-wise null fraction using:
df.isna().mean()

Columns with >50% missing values are flagged as warnings.

### Numeric Type Sanity
Used:
df.select_dtypes(include=["number"])

Ensures expected numeric features were not silently read as strings.

### Range Validation Example
Added bounded check for risk_score ∈ [0,1].
Violations raise errors.

## Why This Matters for LLM Systems
LLMs do not fail loudly on bad data — they produce confident outputs.
These checks prevent malformed context from reaching retrieval and generation layers.

## Result
Validation now enforces both:
- structural integrity (Chunk 1)
- semantic sanity (Chunk 2)


# Day 20 — Chunk 3: Configurable Validation Rules

## Goal
Remove hardcoded validation thresholds and column-specific checks.
Make rules configurable so validation logic stays stable as data changes.

## What Changed
- Added `ValidationRules` dataclass:
  - max_missing_frac
  - numeric_ranges (column -> (min, max))
- Updated `validate_inputs(..., rules=...)`
  - default rules created if not provided
- Missingness threshold now uses `rules.max_missing_frac`
- Range checks now iterate over `rules.numeric_ranges`

## Python Fluency Notes
- Used `field(default_factory=dict)` to avoid mutable-default bugs.
- Passing rules separates "policy" (rules) from "mechanism" (validation code).

## Outcome
Validation rules can be updated without modifying validator logic.


# Day 20 — Chunk 4: Validation Reporting

## Goal
Persist validation results as an artifact rather than only printing.

## Added
Function: write_validation_report(result, output_dir, mode)

Creates:
outputs/validation_report.json

Includes:
- timestamp
- mode (train/score)
- ok flag
- errors
- warnings
- dataset stats

## Why This Matters
Enables auditability, debugging, and monitoring of data quality over time.
Essential for production ML/LLM systems where failures are subtle.

## Python Notes
Used pathlib.Path for filesystem-safe handling.
mkdir(parents=True, exist_ok=True) ensures idempotent directory creation.
