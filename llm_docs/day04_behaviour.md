📘 Day 4 — Context Windows, Memory, and Why LLMs “Forget”

Big idea today:

LLMs do not “remember.”
They only see what fits in their context window.

Everything else is gone.

If you understand this, you understand 70% of real-world LLM failures.

1️⃣ What Is a Context Window?

Every LLM has a limit:

Max tokens it can see at once


Examples:

Small models: 4k–8k tokens

LLaMA 3: ~8k–32k (varies by version)

Bigger models: 100k+

When you exceed it:

👉 Old text gets cut off.

Silently.

No warning.

2️⃣ Why Long Chats Degrade

In long conversations:

New tokens → push out old ones.

So:

Early instructions disappear

Earlier facts vanish

Style drifts

Mistakes repeat

That’s not “getting tired.”

That’s math.

3️⃣ KV Cache (Why Speed Improves Mid-Chat)

Inside transformers:

Attention stores:

Key / Value vectors


for previous tokens.

This is the KV cache.

It allows:

Fast continuation

No recomputation

But:

❌ Cache only works inside window
❌ Once tokens drop, cache drops

4️⃣ “Memory” Is Fake (Engineered)

LLMs have no internal memory.

So systems fake it.

Three main ways:

A) Sliding Window

Keep last N tokens only.

Simple.
Cheap.
Forgets fast.

B) Summarization Memory

Old chat → summarized → reinserted.

Example:

User prefers short answers. Working on LLM project.


Keeps gist.

Loses detail.

C) Retrieval Memory (RAG)

Store past info externally.

Search and re-inject.

This is “real memory.”

Most serious systems use this.

5️⃣ Why RAG Exists (Core Reason)

Without retrieval:

LLM = goldfish.

With retrieval:

LLM = researcher.

That’s the difference.

6️⃣ Long-Context ≠ Infinite Memory

Even 100k tokens:

Expensive

Slow

Attention degrades

Still forgets beyond window

So smart systems mix:

Context + RAG + summaries


Not just “bigger window.”

7️⃣ Failure Mode: Context Poisoning

If wrong info enters context:

LLM trusts it.

Example:

User: The capital of France is Lyon.


Later:

LLM repeats it.

Because context > training.

This is dangerous.

🧠 Interview-Level Summary

If asked:

How do LLMs handle memory?

Say:

“They only operate within a fixed context window. Any long-term memory is implemented externally via summarization or retrieval systems like RAG. Internally, KV caching improves speed but doesn’t extend memory.”

That’s a strong answer.