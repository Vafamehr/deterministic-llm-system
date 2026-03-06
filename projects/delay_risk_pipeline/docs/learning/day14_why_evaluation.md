# Day 14 — RAG Evaluation (Practical)

## Why Evaluation Matters
RAG systems often *sound* correct even when they are wrong.
Without evaluation, you can't tell whether improvements help or just “feel better.”

RAG must be evaluated across stages:
- retrieval behavior: does it fetch the right book?
- answer grounding: read it
- task alignment: answer my question?
- coverage: check the whole thing?

This is closer to *search testing* than classic ML benchmarking.

---

## The 4 Golden Checks (Library Story)
Ask:
**Did my assistant bring the right book, read it, answer my question, and check the whole thing?**

1) **Retrieval Quality (Right book)**
- Did we fetch the correct document/chunks?

2) **Groundedness (Read it)**
- Is the answer supported by retrieved text, or invented?

3) **Relevance (Answer my question)**
- Does the response address the user’s intent, or ramble?

4) **Completeness (Check the whole thing)**
- Did we miss key facts/sections that existed in the corpus?

---

## Step 1 — Build a Small Ground-Truth Set
Start with a tiny eval set (5–20 cases) where you specify:
- the question
- expected source (or expected document)
- expected fact(s)

Example fields:
- `question`
- `expected_source`
- `expected_fact`

This becomes your “unit tests” for RAG behavior.

---

## Step 2 — Manual Evaluation Loop (Deterministic First)
Begin with simple checks before fancy metrics:

### A) Retrieval Correctness
- Compare retrieved source to expected source

### B) Fact Presence (Minimal Groundedness Proxy)
- Check expected_fact appears in answer text  
(cheap signal; not perfect grounding yet)

### C) Relevance Check (Task Alignment Proxy)
- Simple keyword rule: answer should contain terms consistent with question  
(cheap, catches obvious off-topic answers)

**Why start rule-based?**
Because it helps you debug quickly and teaches you *where failures originate*.

---

## What This Gives You (Immediate Value)
With these checks, you can tell:
- retrieval failed vs generation failed
- answer is off-topic vs missing evidence
- changes to chunking/top-k/filters improved coverage or not

---

## Step 4 — Completeness Signal
Check whether all expected facts were covered, not just one.
Completeness detects partial answers even when retrieval succeeded.
