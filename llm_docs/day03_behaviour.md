✅ Day 3 — LLM Training & Behavior (Brief Summary)
1. Tokenization

LLMs do not read words. They read tokens (subword units).
Context limits and costs are based on tokens, not characters or words.

2. Pretraining

LLMs are pretrained using next-token prediction on massive datasets (books, code, web, papers).

Objective:

Learn P(next token | previous tokens)

All “intelligence” comes from this stage.

3. Supervised Fine-Tuning (SFT)

After pretraining, models are trained on human-written examples:

Prompt → Ideal Answer

This makes responses more useful and structured.

4. RLHF (Reinforcement Learning from Human Feedback)

Humans rank model answers.
The model learns to optimize for preferred behavior.

Result:

More polite

Safer

More aligned

Sometimes less creative

5. Inference Parameters

Output is controlled by sampling:

Temperature → randomness

Top-p / Top-k → restrict choices

Higher randomness = more creativity + more hallucinations.

6. Hallucination

LLMs do not know facts.
They generate what sounds most likely.

When uncertain, they guess confidently.

This is inherent to next-token prediction.

7. Alignment Tradeoff

Alignment improves safety but may reduce:

Honesty

Reasoning depth

Creativity

There is always a tradeoff.

🧠 One-Line Interview Answer

“LLMs are pretrained with next-token prediction, then fine-tuned using supervised data and RLHF. They operate on tokens, and inference parameters control randomness, which also contributes to hallucinations.”