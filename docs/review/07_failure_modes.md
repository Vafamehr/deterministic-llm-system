# Failure Modes

This system is designed to fail **safely and visibly** rather than failing silently or producing confident nonsense.

Failure handling is not treated as an afterthought. It is part of the architecture because the system is deterministic-first, bounded, and governed.

---

## What “Failure” Means in This System

A failure is any condition where the system cannot produce a reliable answer using its normal deterministic-first flow, including:

- deterministic logic cannot resolve the request
- a required tool fails or returns unusable data
- retrieval returns no useful context
- the request is too ambiguous to answer confidently
- LLM/agent reasoning produces a low-confidence or inconsistent result
- governance determines the result is unsafe or insufficient

---

## Common Failure Modes

### 1) Deterministic Unresolved
Deterministic logic cannot answer due to missing capability or missing context.

Expected behavior:
- route to tools or retrieval
- if still unresolved, optionally allow LLM/agent reasoning
- if still unresolved, return a constrained output (ask for clarification or provide partial result)

### 2) Tool Failure
A tool call fails due to:
- execution error
- timeout
- invalid input/output schema
- tool returns data that does not help resolve the request

Expected behavior:
- log the failure in trace
- either retry under strict rules (if implemented) or fall back to retrieval / LLM reasoning
- governance may mark the final output as **needs review** depending on severity

### 3) Retrieval Miss
Retrieval returns:
- no chunks
- irrelevant chunks
- weak or conflicting context

Expected behavior:
- trace records retrieval quality outcome
- system either retries with adjusted query (if implemented) or proceeds to bounded reasoning
- governance may flag the answer if evidence is weak

### 4) LLM/Agent Reasoning Failure
LLM/agent reasoning can fail by producing:
- hallucinated details
- inconsistent output
- overconfident answers without support

Expected behavior:
- LLM/agent is treated as secondary, not authoritative
- governance checks for ambiguity or missing evidence
- system returns a constrained response rather than asserting unsupported claims

### 5) Governance Rejection / Needs Review
Even if a candidate answer exists, governance may decide it is not acceptable.

Expected behavior:
- return the best safe output available (often partial + clarification request)
- mark the response as **needs review** according to your governance model
- trace includes escalation reasons

---

## Degradation Behavior

When failures occur, the system degrades gracefully rather than breaking the entire run.

Typical degradation pattern:
- deterministic-first attempt
- capability expansion (tools / retrieval)
- bounded reasoning (LLM/agent) only if allowed
- governance gate decides whether output is acceptable
- trace records the full chain so failures are diagnosable

---

## Trace as the Failure Debugger

Trace artifacts are essential for failure analysis because they reveal:
- which step failed
- which fallback path was used
- whether the system entered degraded mode
- why governance approved or flagged the result

In other words, failures are not hidden; they are observable.

---

## Kitchen Analogy

| System Failure | Kitchen Equivalent |
|---|---|
Deterministic unresolved | Recipe does not cover the request |
Tool failure | Pantry runner cannot find ingredient |
Retrieval miss | Recipe book has no relevant page |
LLM/agent failure | Creative chef improvises incorrectly |
Governance flag | Quality check stops dish from being served |
Trace artifacts | Ticket history shows exactly what went wrong |