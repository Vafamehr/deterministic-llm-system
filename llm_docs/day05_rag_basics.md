1. What Is RAG?

Retrieval-Augmented Generation (RAG) is a system pattern that combines:

External document retrieval

Prompt augmentation

LLM-based generation

Purpose:
To ground LLM responses in external data and reduce hallucination.

RAG is not a tool. It is an architecture.

2. High-Level RAG Pipeline
Documents → Chunking → Embeddings → Vector Index (FAISS)
                                      ↓
Query → Embedding → Similarity Search → Top Chunks
                                      ↓
                           Prompt Augmentation
                                      ↓
                                   LLM
                                      ↓
                                  Answer

3. Embeddings

An embedding is a numeric vector representation of text.

Properties:

Similar meaning → similar vectors

Dissimilar meaning → distant vectors

Used to compare semantic similarity.

In RAG, one embedding typically represents one chunk of text.

4. Token vs Sentence Embeddings

Inside the model:

Each token has its own vector (hidden states).

For retrieval:

Token vectors are pooled into a single sentence/chunk vector.

RAG uses sentence/chunk embeddings, not token-level embeddings.

5. Chunking

Chunking is the process of splitting documents into retrievable units.

Typical configuration:

Size: 200–800 tokens

Overlap: 50–150 tokens

Purpose:
Balance context and retrieval precision.

Bad chunking is a major cause of RAG failure.

6. Similarity Measurement

RAG systems usually use cosine similarity.

Cosine similarity measures:

Vector direction (semantic meaning)

Not magnitude

Formula:

cos(a, b) = (a · b) / (||a|| ||b||)


Values range from -1 to 1.

7. FAISS

FAISS (Facebook AI Similarity Search) is a library for fast vector search.

Purpose:
Efficient nearest-neighbor search over high-dimensional embeddings.

Functions:

Store vectors

Index vectors

Perform similarity search

FAISS acts as the retrieval engine in RAG systems.

8. Retrieval

Retrieval consists of:

Embedding the user query

Searching the vector index

Selecting top-k similar chunks

Example:

query_vector → FAISS.search → top documents

9. Augmentation

Augmentation means inserting retrieved documents into the prompt.

Example:

Context:
(doc1)
(doc2)

Question:
(user query)


This gives the LLM access to external knowledge.

10. Generation

The LLM receives:

Retrieved context

User question

Prompt instructions

It then generates a response using:

Retrieved facts

Pretrained knowledge

Reasoning ability

The LLM is not aware it is using RAG.

11. Source of Knowledge in RAG

RAG answers combine:

External documents (grounding layer)

Pretrained LLM knowledge (reasoning layer)

If documents are weak, the model relies more on pretraining.

12. Key RAG Parameters

Important tuning variables:

Parameter	Description
chunk_size	Size of text chunks
overlap	Overlap between chunks
k	Number of retrieved chunks
embedding_model	Encoder choice
prompt_format	Context injection style

These strongly affect answer quality.

13. Common Failure Modes

RAG fails when:

Chunking is poor

Documents are low quality

Embeddings are domain-mismatched

Retrieval returns irrelevant data

Prompt is underspecified

Most RAG problems are engineering problems, not model problems.

14. One-Line Summary

RAG retrieves relevant external documents using embeddings and vector search, injects them into the prompt, and uses an LLM to generate grounded answers.

15. Interview Answer Template

“How does RAG work?”

Answer:

We chunk documents, generate embeddings, index them in a vector store, retrieve top-k relevant chunks using cosine similarity, inject them into the prompt, and let the LLM generate a grounded response.

16. Practical Implementation (Local Setup)

Typical stack:

Embeddings: nomic-embed-text (Ollama)

Vector DB: FAISS

LLM: LLaMA/Qwen (Ollama)

Interface: Python + requests