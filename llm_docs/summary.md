# Must Knows — LLM Systems (Working Playbook)

This file is not notes.
This is what I should be able to recall without looking.

Keep it short. Rewrite to sharpen understanding.

---

## Core Mental Model

• LLMs generate tokens, they do NOT retrieve facts.
• RAG exists because models forget — retrieval supplies grounding.
• Most failures in LLM apps are retrieval/data problems, not model problems.
• Treat LLM systems like data pipelines, not magic APIs.

---

## Documents → Answers Pipeline (Know This Cold)

Raw Docs
→ parsing / cleaning
→ chunking (this determines quality!)
→ embeddings (semantic coordinates)
→ vector search (similarity lookup)
→ context assembly
→ LLM generation
→ structured output / decision layer

If something breaks, inspect this chain — not the model first.

---

## Chunking & Embeddings

• Chunk size controls meaning resolution.
• Smaller, clean chunks outperform large noisy ones.
• Overlap prevents context fragmentation.
• Embeddings store similarity, not knowledge.
• Changing chunk strategy often improves results more than changing models.

---

## Retrieval Reality

• Always inspect retrieved chunks before trusting answers.
• Bad retrieval = confident hallucination.
• Metadata filtering is as important as similarity search.
• Vector DB = fast math, not intelligence.

---

## Prompting (In Applications)

• Prompts should constrain, not “ask nicely”.
• Structure > creativity.
• If output must be reliable → demand schema / format.
• Prompt design is interface design, not chatting.

---

## Tool Use / Function Calling

• Tools turn LLM from text generator into system component.
• Always validate tool inputs/outputs.
• Deterministic code should do deterministic work — don’t delegate math to LLMs.

---

## Memory (System Design, Not Human Analogy)

• “Memory” = storing state externally (DB, cache, files).
• Never rely on model conversation history for real workflows.
• Persist what matters explicitly.

---

## Architecture Principles

• Pipelines beat notebooks.
• Observability matters — log intermediate steps.
• You must be able to debug retrieval independently of generation.
• Local-first development forces understanding (this is good).

---

## Common Failure Modes

• Garbage parsing → useless embeddings.
• Large chunks → vague retrieval.
• No filtering → irrelevant context.
• Over-trusting LLM output.
• Mixing experimentation code with pipeline code.

---

## What This Work Is Actually About

I am not building a chatbot.
I am building systems that combine:

structured data + unstructured context + reasoning layer

Goal = decision support, not conversation.

---

## Additions Rule

Only add a line when:
✔ I discovered this through building
✔ I can explain it without notes

If it grows too long → compress it.
