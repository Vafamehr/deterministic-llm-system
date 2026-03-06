# Day 9 — Document Pipelines

A document pipeline converts raw files into structured, retrievable data.

Pipeline:
Raw → Parse → Clean → Extract Metadata → Chunk → Embed → Store

PDF Parsing Issues:
- Layout distortion
- Broken tables
- Split citations
- OCR noise

Cleaning:
- Remove headers/footers
- Remove page numbers
- Fix broken line breaks
- Remove artifacts

Metadata Extraction:
Attach structured fields like:
- source
- year
- document_type
- case_name
- court

Versioning:
Track document versions.
Re-embed when updated.
Avoid mixing old + new content.

Rule:
If ingestion is bad, retrieval fails.
