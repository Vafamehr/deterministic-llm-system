# Day 15 — When NOT to Fine-Tune

Fine-tuning should not be the first response to bad answers.

Most RAG failures come from retrieval, context design, or data quality—not model capability.

Rule:
Fix the system before changing the model.

## When Fine-Tuning Is Justified

Fine-tuning is needed only when the model fails despite having correct inputs.

Use it for:
- enforcing structure or format
- stabilizing repeated behaviors
- domain reasoning patterns

Do NOT use it to insert knowledge or compensate for retrieval failures.


## Pre-Fine-Tuning Ladder

Before training, teams adjust:
1. Prompt design
2. Context structure
3. Data quality
4. Retrieval configuration

Most issues are resolved without modifying model weights.

## Decision Checklist

Before fine-tuning, verify:
- Retrieval is correct.
- Context is well-structured.
- Data is clean.
- Instructions are precise.

Only train when the model still fails with correct inputs.

RAG optimization is primarily a systems problem, not a training problem.

