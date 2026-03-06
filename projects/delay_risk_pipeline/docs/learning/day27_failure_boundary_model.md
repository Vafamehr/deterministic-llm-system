# Day 27 — Chunk 1
## Introducing StageResult (Failure Boundary Contract)

### Problem
Pipeline stages currently return raw data.
If a stage fails, the entire pipeline can crash.

### Solution
Introduce a typed StageResult envelope.

### Implementation

File: src/stage_result.py

from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class StageResult:
    status: str
    data: Optional[Any]
    error: Optional[str]
    latency_ms: float

### Purpose
- Isolate stage failures
- Prevent full pipeline crash
- Support observability
- Enable partial success
- Prepare for production-grade orchestration

This becomes the standard return type for:
- _run_deterministic
- _run_llm
- _cross_check


# Day 27 — Chunk 2
## Type-Safe Stage Status (Enum)

### Why
Using raw strings for stage status is fragile (typos, inconsistency).
We want a guaranteed set of allowed statuses across the system.

### Added
File: `src/stage_status.py`

```python
from enum import Enum

class StageStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


# Day 27 — Chunk 3
## Wrapping Deterministic Stage with Failure Boundary

### Previous Version
_run_deterministic returned raw Dict.

### Problem
If assess_risk_from_packets raises an exception,
the entire pipeline crashes.

### Upgrade
Now _run_deterministic returns StageResult.

### Implementation Pattern

- Start timer
- try deterministic engine
- return SUCCESS with data
- except → return FAILED with error string
- Always record latency_ms

### Accessing Result
- det_result.status
- det_result.data
- det_result.error
- det_result.latency_ms

### Outcome
Deterministic stage is now isolated and production-safe.    



# Day 27 — Chunk 3
## Wrapping Deterministic Stage with Failure Boundary

### Previous Version
_run_deterministic returned raw Dict.

### Problem
If assess_risk_from_packets raises an exception,
the entire pipeline crashes.

### Upgrade
Now _run_deterministic returns StageResult.

### Implementation Pattern

- Start timer
- try deterministic engine
- return SUCCESS with data
- except → return FAILED with error string
- Always record latency_ms

### Accessing Result
- det_result.status
- det_result.data
- det_result.error
- det_result.latency_ms

### Outcome
Deterministic stage is now isolated and production-safe.


# Day 27 — Chunk 4
## Wrapping LLM Stage with Failure Boundary

### Goal
Make LLM execution non-fatal to the pipeline.

### Change
_run_llm now returns StageResult instead of raw output.

### Pattern
- Start timer
- try LLM call
- SUCCESS with data + latency
- except → FAILED with error + latency

### Access
- llm_result.status
- llm_result.data
- llm_result.error
- llm_result.latency_ms

### Outcome
LLM failures/timeouts can be captured without crashing the system.


# Day 27 — Chunk 5 (Part A)
## Cross-Check Failure Boundary (Wrapped, Non-Disruptive)

### What Changed
_cross_check now takes StageResult inputs and returns StageResult.

### Upstream Gating Rule
Cross-check runs only if BOTH upstream stages are SUCCESS.
Otherwise:
- status = SKIPPED
- error explains why
- latency_ms = 0.0

### Cross-Check Output (on SUCCESS)
StageResult.data contains:
- inconsistencies (List[Dict])
- consistency_ratio (float)
- confidence (str)

### Why This Matters
- Cross-check can never crash the pipeline
- Failures are contained and observable
- Still preserves the original cross-check logic





# Day 27 — Chunk 5 (Part B)
## Wiring StageResult into run_full_assessment (Non-Breaking)

### Problem Found
After wrapping stages with StageResult, run_full_assessment still treated outputs as Dict:
- used `.get()` on StageResult
- called `_run_llm()` twice
- referenced undefined `det_result`
- cross-check gating used truthiness instead of StageStatus

### Fix
- Treat `det_res`, `llm_res`, `cc_res` as StageResult objects end-to-end
- Only expose `.data` into existing `deterministic_layer` / `llm_layer` keys
- Keep existing `metrics` keys unchanged
- Add new `stage_results` field (additive)

### Added Output Field
stage_results: {
  deterministic: { status, error, latency_ms },
  llm:          { status, error, latency_ms },
  cross_check:  { status, error, latency_ms }
}

### Early Exit (Correct Version)
Only triggers when:
- plan.run_llm is True
- det_res.status == SUCCESS
- all deterministic risk_level == LOW
Then:
- llm_res = SKIPPED with reason
- cc_res = SKIPPED with reason
- returns early with HIGH confidence




# Day 27 — Resilience & Failure Boundaries (Completed)

## Upgrades Introduced

1. StageResult dataclass (failure boundary contract)
2. StageStatus Enum (type-safe status control)
3. Deterministic stage wrapped in try/except
4. LLM stage wrapped in try/except
5. Cross-check stage wrapped + upstream gating
6. Early-exit logic preserved and corrected
7. stage_results added to final output (non-breaking)

## System Now Guarantees

- No stage can crash the pipeline
- All failures are recorded with:
  - status
  - error
  - latency_ms
- Cross-check only runs when safe
- Output contract remains stable

## Architectural Level Achieved

This is now a production-style orchestrated AI pipeline,
not a prototype script.