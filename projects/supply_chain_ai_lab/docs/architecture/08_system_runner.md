# System Runner

## Purpose

Provides the entry point for executing the entire supply chain system.

---

## One-Line Summary

Runs the system end-to-end under different modes.

---

## Role in System

The system runner sits above all modules.

It controls:

- execution mode  
- input construction  
- output formatting  

---

## Execution Modes

### Baseline Mode

Runs the core decision pipeline once.

Flow:

Decision Coordinator → Output

---

### Simulation Mode

Runs multiple scenarios and compares results.

Flow:

Simulation Engine  
→ Scenario Analysis  
→ Output Contract  

---

### Extended Modes (future)

- disruption testing  
- allocation execution  
- monitoring analysis  

---

## Responsibilities

- build system inputs  
- call coordinator or simulation  
- collect outputs  
- print structured results  

---

## Inputs

- system configuration  
- decision input  
- simulation input  

---

## Outputs

- structured decision results  
- scenario comparison results  
- optional explanation  

---

## Design Rules

- no business logic  
- no calculations  
- no model logic  
- only orchestration and output handling  

---

## Relationship to Other Layers

- calls Decision Coordinator  
- triggers Simulation Engine  
- connects to Scenario Analysis  
- optionally invokes LLM  

---

## Mental Model

coordinator = engine  
runner = driver  

---

## One-Line Summary

A top-level execution layer that runs the system and produces final outputs.