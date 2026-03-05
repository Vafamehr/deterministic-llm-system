# Day 16 — Data Curation

RAG systems depend more on how documents are prepared than on which model is used.

Data curation converts raw documents into structured knowledge that can be reliably retrieved.

Goal:
Messy text → Clean semantic units → Indexed context for the LLM.

## Chunking Principle

RAG retrieves chunks, not documents.
If chunk boundaries break meaning, retrieval loses facts.

Chunk by semantic structure (paragraphs, clauses, sections), not fixed length.

## Metadata Enables Controlled Retrieval

Each chunk should carry structured metadata (source, section, date, type, etc.).

Retrieval should combine:
semantic similarity + metadata filters.

Embeddings find related text.
Metadata enforces contextual correctness.

## Day 16 Insight

Well-curated chunks serve two purposes:
1. Retrieval units for RAG today.
2. Potential supervision data for future fine-tuning.

Data curation is the foundation of both retrieval quality and model customization.
