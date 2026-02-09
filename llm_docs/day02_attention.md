This document summarizes how Transformer models (GPT-style) process text using self-attention.

It focuses on:

Why attention exists

Transformer blocks

Q / K / V

Multi-head attention

How prediction happens

Goal: build real intuition, not memorization.

1. Why Attention Exists

Before Transformers, models (RNN/LSTM) processed text sequentially.

Problems:

Slow (no parallelism)

Forget long-range context

Weak handling of references

Example:

“The trophy doesn’t fit in the suitcase because it is too big.”

RNNs struggled to link “it” → “trophy”.

Transformers solve this with self-attention.

Self-attention allows every token to look at every other token at once.

2. Transformer = Stack of Blocks

GPT models are stacks of identical blocks:

Block 1 → Block 2 → Block 3 → ... → Block N


Each block refines the representation.

No block starts from scratch.

3. Structure of One Transformer Block

Each block contains:

Input
 → Self-Attention
 → Add & Normalize
 → Feed-Forward Network
 → Add & Normalize
 → Output

Components
3.1 Self-Attention

Mixes contextual information between tokens.

Each word becomes context-aware.

3.2 Feed-Forward Network (FFN)

Processes each token independently.

Purpose: transform and enrich representations.

3.3 Residual Connections (Add)

Preserve original information.

Prevent loss of meaning.

3.4 Layer Normalization (Norm)

Stabilizes training.

Prevents exploding values.

4. Q / K / V: The Core of Attention

Each token vector x is projected into three vectors:

Q = x · Wq   (Query)
K = x · Wk   (Key)
V = x · Wv   (Value)

Meaning
Component	Role
Q	What am I looking for?
K	How can others find me?
V	What information do I give?

Every token has its own Q, K, and V.

5. How Attention Is Computed

For token i attending to token j:

Step 1 — Similarity
score(i,j) = Qi · Kj


Measures relevance.

Step 2 — Normalize
weights = softmax(scores)


Turns scores into probabilities.

Step 3 — Aggregate Values
output_i = Σ weight(i,j) × Vj


Builds new representation.

Each token becomes a weighted mix of others.

6. Role of V (Value)

Important distinction:

K → used for matching

V → used for content

K helps decide who matters.

V provides what is copied.

This separation improves expressiveness.

7. Evolution Across Layers

Early layers focus on:

Grammar

Position

Syntax

Middle layers:

Meaning

Coreference

Topics

Late layers:

Reasoning

Intent

Discourse

Each block refines understanding.

8. Multi-Head Attention

Single attention is limited.

Language has many relationships simultaneously.

So Transformers use multiple heads.

Each head has its own Q/K/V:

Q₁ K₁ V₁
Q₂ K₂ V₂
...


Each head learns different patterns.

Outputs are concatenated and combined.

Typical Head Specializations
Head Type	Focus
Grammar	Subject-verb
Reference	Pronouns
Topic	Semantic clusters
Structure	Sentence layout

This emerges automatically.

9. Why Many Heads Are Better

Multi-head attention allows:

Parallel perspectives

Richer representations

Better reasoning

One head = one view
Many heads = combined views

10. Where Prediction Happens

Attention does NOT directly predict tokens.

Pipeline:

Embeddings
 → Transformer Blocks (Attention + FFN)
 → Final Linear Layer
 → Softmax
 → Sampling


Prediction happens only at the end.

Attention builds representations.

11. Complete Mental Model
Tokens → Embeddings
      → Blocks:
         (Attention → FFN → Residuals)
      → Final Layer
      → Next Token


Each block = refinement.

12. Connection to RAG (Preview)

RAG uses the same idea externally:

Attention	RAG
Q	User query
K	Document embeddings
V	Document text

RAG = external attention.

13. Key Rules (Memorize)

Attention = learned relevance.

Every token has Q/K/V.

K matches, V delivers.

FFN processes independently.

Multi-head = multiple perspectives.

Prediction happens at the end.

14. Self-Test Questions
Q1: Why were RNNs weak for long text?

Answer: Sequential processing caused forgetting and slow training.

Q2: What is the role of FFN?

Answer: Independently transforms each token’s representation.

Q3: Difference between K and V?

Answer: K is for matching, V is for content.

Q4: Why multi-head attention?

Answer: To capture multiple relationships in parallel.

Q5: Does attention predict tokens?

Answer: No. Prediction happens after all layers.

15. Summary

Transformers work by repeatedly:

Mixing context (attention)

Processing tokens (FFN)

Preserving information (residuals)

Q/K/V enable learned relevance.

Multi-head attention enables parallel reasoning.

This forms the backbone of modern LLMs.