# Failure Modes

This system is designed to fail **safely and visibly**, rather than failing silently or producing confident but incorrect results.

Failure handling is treated as a **core part of the architecture**, not an afterthought. Because the system follows a deterministic-first, bounded, and governed design, failure conditions are anticipated and handled explicitly.

---

## What “Failure” Means in This System

A failure is any condition where the system cannot produce a reliable answer using its normal deterministic-first flow.

Examples include:

- deterministic logic cannot resolve the request
- a required tool fails or returns unusable data
- retrieval returns no useful context
- the request is too ambiguous to answer confidently
- LLM or agent reasoning produces a low-confidence or inconsistent result
- governance determines that the result is unsafe or insufficient

In all of these situations, the system attempts to degrade gracefully rather than producing misleading outputs.

---

## Common Failure Modes

### 1) Deterministic Unresolved

Deterministic logic cannot resolve the request because the system lacks capability or context.

**Expected behavior**

- route execution to tools or retrieval
- if still unresolved, optionally allow LLM or agent reasoning
- if the request remains unresolved, return a constrained response such as a clarification request or partial result

---

### 2) Tool Failure

A tool call may fail due to:

- execution errors
- timeouts
- invalid input or output schema
- tool results that do not help resolve the request

**Expected behavior**

- the failure is recorded in trace artifacts
- the system may retry under strict rules (if implemented) or fall back to retrieval or bounded reasoning
- governance may mark the final output as **needs review** depending on severity

---

### 3) Retrieval Miss

Retrieval may return:

- no context chunks
- irrelevant chunks
- weak or conflicting context

**Expected behavior**

- the trace records retrieval quality and outcome
- the system may retry with an adjusted query (if implemented) or proceed to bounded reasoning
- governance may flag the answer when evidence is weak

---

### 4) LLM or Agent Reasoning Failure

Model-driven reasoning can fail by producing:

- hallucinated details
- inconsistent output
- confident answers without supporting evidence

**Expected behavior**

- LLM or agent reasoning is treated as a secondary capability, not an authoritative source
- governance checks for ambiguity or missing evidence
- the system returns a constrained response instead of asserting unsupported claims

---

### 5) Governance Rejection or Needs Review

Even if a candidate answer exists, governance may determine that it should not be returned directly.

**Expected behavior**

- return the safest available response (often partial output plus a clarification request)
- mark the response as **needs review** according to governance rules
- include escalation reasons in trace artifacts

---

## Degradation Behavior

When failures occur, the system **degrades gracefully** instead of terminating execution abruptly.

Typical degradation sequence:

- deterministic-first attempt
- capability expansion (tools or retrieval)
- bounded reasoning (LLM or agent) if allowed
- governance evaluates the candidate result
- trace artifacts record the entire execution path

This degradation model allows the system to produce the safest possible output under uncertain conditions.

---

## Trace as the Failure Debugger

Trace artifacts are essential for diagnosing failures because they reveal:

- which step failed
- which fallback path was used
- whether the system entered degraded mode
- why governance approved or flagged the result

Failures are therefore **observable and explainable**, rather than hidden inside the system.

---

## Kitchen Analogy

| System Failure | Kitchen Equivalent |
|---|---|
Deterministic unresolved | Recipe does not cover the request |
Tool failure | Pantry runner cannot find the ingredient |
Retrieval miss | Recipe book has no relevant page |
LLM or agent failure | Creative chef improvises incorrectly |
Governance flag | Quality check stops dish from being served |
Trace artifacts | Ticket history shows exactly what went wrong |