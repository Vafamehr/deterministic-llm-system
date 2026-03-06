# Day 10 — Retrieval Control & Filtering

Default Retrieval:
Query → Embed → Similarity Search → Top-K

Problem:
Similarity ignores authority, freshness, and type.

Filtering:
Apply constraints like:
- document_type
- year
- source
- jurisdiction

Pre-filtering is safer than post-filtering.

Top-K:
Small K = precision
Large K = recall

Rule:
Similarity alone is insufficient.
Controlled retrieval increases reliability.
