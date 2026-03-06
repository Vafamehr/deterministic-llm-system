# Day 13 — Memory Systems (Intro)

## Why Memory Exists
LLMs are stateless. Applications cannot be.

Memory allows:
- follow-up questions
- persistent preferences
- contextual reasoning

## Two Types
Short-term:
Conversation/session context.

Long-term:
Stored user/system knowledge.

## Memory Is NOT Chat History
Good systems store structured summaries, not raw logs.

## Pattern
Read memory → answer → update memory.

## Key Insight
Memory is curated state, not conversation storage.



# Day 13 — Memory Summarization

## Problem
Storing full conversation causes:
- token explosion
- slower reasoning
- noisy prompts

## Rule
Store meaning, not messages.

## Memory Should Capture
- current task
- important entities
- focus areas
- exclusions

## Approach
Summarize interactions into structured state.

## Insight
Memory is not a transcript.
Memory is a task model.

# Day 13 — Short-Term vs Long-Term Memory

Short-Term Memory:
Tracks session context and resets after task completion.

Long-Term Memory:
Stores persistent user/system knowledge.

Do not mix them.

Short-term = task state.
Long-term = user model.

# Day 13 — Memory Injection

Memory must be translated into structured context before sending to the LLM.

Never dump raw conversation.

Inject curated task + user state instead.

Memory is context engineering, not storage.