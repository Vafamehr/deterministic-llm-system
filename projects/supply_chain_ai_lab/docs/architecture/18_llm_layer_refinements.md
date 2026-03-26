# Ollama Integration Refinement

## Goal
Replace the current stub LLM client with a real local model call while keeping the existing V3 architecture unchanged.

## Why this refinement
The current explanation layer works end-to-end, but the client still returns hardcoded text. Replacing the stub with a local model makes the explanation layer real without changing the deterministic system design.

## Scope
This refinement only updates:

`src/llm_support/client.py`

No schema changes.  
No service refactor.  
No prompt refactor.  
No validator redesign.  
No system runner redesign.

## Design rule
Keep the existing interface exactly the same:

- `LLMClient`
- `generate(prompt: str) -> str`

Only the internal implementation changes from:

hardcoded stub → local Ollama HTTP call

## Architectural position
The flow remains:

Scenario Analysis → Context Builder → Prompt Builder → LLM Client → Validator → Explanation Response

The deterministic supply chain outputs remain the source of truth.  
The LLM still has no authority to make decisions.  
The LLM still only explains structured outputs.

## Expected behavior after refinement
When simulation mode runs with explanation enabled:

1. deterministic simulation produces structured scenario analysis
2. context builder converts outputs into explanation context
3. prompt builder creates grounded prompt
4. client sends prompt to local Ollama model
5. validator checks returned text
6. final explanation is printed by `run_system.py`

## Why Ollama fits this project
- local execution
- simple HTTP API
- no architecture change required
- easy to swap models later
- good for demo and interview walkthroughs

## Constraints
- keep implementation minimal
- return plain text only
- no agents
- no framework dependency
- no new orchestration layer
- no decision-making by LLM
- keep failure handling simple and explicit

## Implementation target
Update `src/llm_support/client.py` so that:
- it sends the prompt to Ollama
- it reads back generated text
- it returns a plain string to the existing service layer

## Success criteria
This refinement is complete when:
- `python run_system.py` succeeds
- simulation output still prints normally
- LLM explanation comes from a real local model
- no other module contracts need to change

## Interview framing
This refinement strengthens the project from:

“LLM explanation layer with stubbed client”

to:

“LLM explanation layer backed by a real local model, while preserving deterministic decision logic and strict separation of responsibilities”