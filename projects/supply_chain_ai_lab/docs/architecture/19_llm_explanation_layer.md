# LLM Explanation Layer

## Purpose

Generates explanations for system outputs using structured signals.

---

## One-Line Summary

Converts structured outputs into natural language explanations.

---

## Role in System

Position:

Scenario Analysis → Decision Intelligence → LLM

The LLM is downstream of all deterministic logic.

---

## Flow

1. scenario analysis produces signals  
2. decision intelligence produces classification  
3. context builder prepares structured input  
4. prompt builder creates prompt  
5. LLM client generates response  
6. validator checks output  

---

## Design Rules

- no decision-making  
- no modification of outputs  
- no control over execution  
- deterministic system remains source of truth  

---

## Client Implementation

- local model (Ollama)  
- simple HTTP call  
- returns plain text  

Interface:

generate(prompt: str) → str

---

## Constraints

- minimal implementation  
- no agents  
- no frameworks  
- no orchestration logic  
- no dependency on system internals  

---

## Failure Handling

- return fallback text if needed  
- keep behavior explicit  

---

## Role in System

The LLM explains:

- scenario differences  
- risk conditions  
- inventory state  

It does not influence outcomes.

---

## One-Line Summary

A lightweight explanation layer that converts structured system outputs into human-readable insights.
