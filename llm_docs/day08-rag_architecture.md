# Day 8 — RAG Architecture (Practical)

## What RAG Is
RAG (Retrieval-Augmented Generation) = use a retriever to fetch evidence from documents, then have the LLM answer using that evidence.

Goal: reduce hallucinations and answer with *grounded* info.

---

## End-to-End Pipeline

User Query
→ (optional) Query Rewrite / Expansion
→ Embed query
→ Retrieve candidate chunks (vector / hybrid)
→ (optional) Filter (metadata) + Re-rank
→ Build context (top chunks + citations)
→ LLM generates answer (grounded)
→ (optional) Post-checks (citations, refusal, formatting)

---

## Core Components (What Each Does)

### 1) Ingestion / Loader
Purpose: turn raw data into text + metadata.
Inputs: PDFs, DOCX, HTML, emails, CSV.
Outputs: `{"text": ..., "metadata": {...}}`

Key idea: keep metadata early (source, date, doc_type, jurisdiction).

### 2) Chunking
Purpose: split text into retrievable units.
Tradeoff:
- too small → loses meaning
- too big → wastes context / hurts retrieval

Common chunk features:
- chunk_text
- chunk_id
- source_id
- section / page
- timestamps / version

### 3) Index / Vector Store
Purpose: store embeddings + metadata for fast retrieval.
Examples: FAISS (local), Chroma (local), Milvus (server).

You store:
- embedding vector
- chunk text
- metadata

### 4) Retrieval
Purpose: given a query, return top-k candidate chunks.
Retrieval modes:
- vector (semantic)
- BM25 (keyword)
- hybrid (best practical default in many domains)

### 5) Re-ranking (Often Needed)
Purpose: reorder candidates using a stronger scorer (cross-encoder or LLM).
Pattern:
retrieve 20–50 → rerank → keep top 3–8

### 6) Context Builder
Purpose: pack selected chunks into a prompt safely.
Includes:
- chunk text
- short source label (doc + page/section)
- optional quote snippets

Rules:
- avoid dumping too much
- keep structure consistent
- include citations per chunk

---

## “Naive RAG” vs “Real RAG”

Naive RAG (demo):
- vector search only
- no metadata filters
- no reranking
- no evaluation
- no failure handling

Real RAG (production mindset):
- metadata + filtering (doc_type, date, source, jurisdiction)
- query rewrite/expansion
- reranking
- evaluation set (retrieval + groundedness)
- guardrails (refuse when evidence is weak)
- logging + tracing

---

## Main Failure Modes (Memorize)

1) Retrieval miss: correct doc exists but not retrieved.
2) Context dilution: too many chunks → model gets confused.
3) Chunking loss: split breaks the key sentence.
4) Stale/wrong source: outdated doc retrieved.
5) Grounding failure: model ignores retrieved text.

---

## Key Rules (Interview-ready)

- Bad retrieval → bad answer, even with a strong LLM.
- Prefer pre-filtering (metadata) before similarity search.
- Use reranking when top-k contains mixed quality.
- RAG must be evaluated at retrieval *and* groundedness.
