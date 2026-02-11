# Day 8 — RAG Architecture

RAG = Retrieval-Augmented Generation

Goal: Ground LLM in documents.

Pipeline:
Query → Embed → Search → Context → LLM → Answer

Core Components:
1. Loader
2. Chunker
3. Vector Store
4. Retriever

Naive RAG = demo only
Real RAG = metadata, filtering, validation

Main Risk:
Too much context = confusion
Too little = hallucination

Rule:
LLM + no documents = guessing
LLM + good docs = system
