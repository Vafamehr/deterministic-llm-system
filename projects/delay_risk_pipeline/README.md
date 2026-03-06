# Deterministic-First LLM System

A small local project exploring how to build **reliable LLM systems** using deterministic execution, structured tools, bounded reasoning, governance checks, and trace-based observability.

The goal is not prompt engineering.  
The goal is to demonstrate **LLM system architecture**.

---

## Architecture Overview

The system follows a **deterministic-first execution model**.

Instead of relying on a language model as the primary controller, the system attempts to resolve requests using deterministic logic and structured capabilities first. Model reasoning is used only when earlier stages cannot resolve the task.

Core design principles:

- **Orchestrated execution** – a central orchestrator controls system flow
- **Deterministic-first pipeline** – predictable logic runs before model reasoning
- **Structured capability expansion** – tools and retrieval extend functionality in controlled ways
- **Bounded agent reasoning** – LLM reasoning is invoked only within defined execution windows
- **Governance checks** – candidate outputs are evaluated before being returned
- **Trace-based observability** – each stage emits trace artifacts for debugging and explanation

---

## Master Architecture

A high-level diagram of the execution pipeline:

[Master Architecture Diagram](./docs/review/diagrams/master_architecture.md)

---

## Architecture Documentation

Detailed design notes are available under:

`docs/review/`

These documents walk through the architecture step-by-step:

- System story
- Architecture overview
- Request execution pipeline
- Orchestrator control
- Tools and retrieval
- Agent control
- Governance and trace
- Failure modes

Each section includes diagrams explaining how the system behaves.

---

## Project Structure

Main folders in this repository:

- **src/**  
  Core system components such as the orchestrator, deterministic logic, tools, retrieval interface, agents, governance checks, and trace generation.

- **docs/review/**  
  Architecture documentation and diagrams explaining how the system works.

- **scripts/**  
  Small demo or testing scripts used during development.

- **data/**  
  Example retrieval data used for testing the retrieval interface.

---

## What This Project Demonstrates

This project focuses on **LLM system design**, including:

- deterministic-first execution pipelines  
- orchestrated control of reasoning components  
- structured tool and retrieval integration  
- bounded agent reasoning  
- governance-based output validation  
- trace-driven observability  

The intention is to show how LLM systems can be designed for **reliability, control, and debuggability**, rather than relying solely on model prompts.

---

## Notes

This repository is intended as a learning and exploration project focused on **LLM system architecture patterns** and how they can be implemented in a small local environment.

## Example System Run

A sample pipeline output is included in:

runs/example_run.json

This file shows the full system output including:

- deterministic risk scoring
- LLM reasoning layer
- RAG retrieval results
- governance decisions
- agent action selection
- decision trace

It demonstrates the structure produced by the end-to-end pipeline.