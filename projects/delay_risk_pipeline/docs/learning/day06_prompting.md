# Day 6 — Prompt Engineering

## System + Role Prompting

Core idea:
Every prompt should define:
- Who the model is
- How it behaves
- What it must do

Example:

You are a senior analyst.
You explain clearly.
Use only given context.


## Few-Shot Prompting

Idea:
Teach by examples.

Pattern:
Example → Example → Task

Use when format and consistency matter.

Example:

Q: 2+2
A: 4

Q: 5+3
A: 8

Q: 7+6
A:


## Chain-of-Thought Prompting

Idea:
Force the model to reason step by step before answering.

Helps with:
- Math
- Logic
- Multi-step problems
- Reducing hallucinations

Pattern:
Think → Reason → Answer

Common triggers:
- "Think step by step"
- "Explain your reasoning"
- "Let’s solve this carefully"

Example:

Question: If I buy 3 items at $4 each, how much do I pay?

Let’s think step by step.

Each item costs $4.  
3 items cost 3 × 4 = 12.  
Total is $12.

---

Tip:
You can ask the model to think step by step
but only output the final answer.

Example:
"Think step by step, but only give the final result."

---

Rule:
Use when correctness matters more than speed.


## ReAct Prompting (Reason + Act)

Idea:
Combine reasoning with tool usage.

The model alternates between:
Thought → Action → Observation → Thought → Answer

Used in agent systems.

Purpose:
Prevent guessing.
Force verification.

Pattern:
Think first.
Use a tool if needed.
Observe result.
Continue reasoning.

Example:

Question: What is the current price of NVDA?

Thought: I need up-to-date data.
Action: search("NVDA stock price")
Observation: $620
Thought: Now I can answer.
Answer: NVDA is trading around $620.

---

Rule:
Use when external data is required.

Without ReAct:
Model guesses.

With ReAct:
Model verifies.


## Tool Prompting

Idea:
Let the model decide which tool or function to use.

The model acts as a controller, not just a responder.

LLM = Brain  
Tools = Hands

Purpose:
Connect the model to calculators, search, databases, APIs.

Pattern:
If tool is needed → call tool.
If not → answer directly.

Example:

Instruction:
If calculation is needed, call calculator().
If search is needed, call search().

Question: What is 45 × 19?

Action: calculator(45,19)
Observation: 855
Answer: 855

---

Rule:
Use when tasks require computation or external systems.


## Prompt Contracts

Idea:
Define strict rules the model must follow.

Use clear constraints instead of polite requests.

Purpose:
Reduce hallucination.
Enforce format.
Improve reliability.

Pattern:
Rules:
1. What to output
2. What to avoid
3. How to handle uncertainty

Example:

Rules:
1. Output valid JSON.
2. No explanations.
3. Use only provided data.
4. If unsure, return null.

---

Principle:
Weak prompt → vague answers  
Strong contract → controlled behavior



✅ Instinct 1 — If output is messy → add structure

→ Format, examples, contracts

✅ Instinct 2 — If model makes logic errors → slow it down

→ Chain-of-thought

✅ Instinct 3 — If model guesses → force tools

→ ReAct / Tool calling

✅ Instinct 4 — If model drifts → anchor it

→ System / role prompt

✅ Instinct 5 — If model hallucinates → constrain it

→ Contracts + retrieval