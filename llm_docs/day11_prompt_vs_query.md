# Prompting vs Query Optimization

## Prompt Engineering
Controls how the LLM responds.

Affects:
- tone
- format
- reasoning
- verbosity

Location:
retrieval → prompt → LLM

---

## Query Optimization
Controls what documents are retrieved.

Affects:
- relevance
- recall
- grounding

Location:
query rewrite → retrieval → LLM

---

## Core Principle
Prompting controls generation.
Query optimization controls evidence.

---

## Debug Rule
Bad output → check retrieval first, prompt second.

---

## Analogy
Query optimization = selecting books.
Prompting = writing the argument.

Wrong books → wrong answer even with perfect writing.


# Day 11 — Query Expansion

## Definition
Query expansion = adding related terms to improve retrieval.

We do NOT change meaning.
We only add signal.

---

## Why It Exists
Users rarely include all relevant keywords.

Example:
asylum deadline
vs
asylum filing deadline application deadline statute limitations

More terms → better recall.

---

## Good Expansion
Adds synonyms or related phrases without changing intent.

Bad expansion changes topic.

---

## Pipeline Location
User Query
↓
Expansion
↓
Retriever

---

## Key Insight
Many retrieval failures occur because the correct document was never retrieved.

Expansion fixes recall failures.


# Day 11 — Filter Injection

## Definition
Filter injection = adding structured constraints to restrict retrieval scope.

Filters control where search is allowed.

---

## Why It Exists
Similarity search can return:
- wrong jurisdiction
- outdated info
- wrong document type

Filtering prevents irrelevant documents from entering candidate pool.

---

## Pipeline
User Query
↓
Rewrite / Expansion
↓
Filter Injection
↓
Retriever
↓
LLM

Filtering always happens before retrieval.

---

## Examples of Filters
jurisdiction = US
year >= 2020
document_type = statute
source = official

---

## Key Insight
Candidate pool quality determines final answer quality.

Better filtering improves retrieval more than better embeddings.


# Day 11 — Query Reformulation

## Definition
Query reformulation = rewriting a query to better match document style and structure.

It changes structure, not meaning.

---

## Why It Exists
Users write informally.
Documents are often formal and structured.

Reformulation improves matching quality.

---

## Example

User:
late paycheck rules

Reformulated:
regulations governing delayed wage payment employer compliance requirements

---

## Difference From Expansion
Expansion adds related words.
Reformulation restructures wording.

---

## When Useful
- formal documents
- title-heavy corpora
- hybrid search
- messy user queries

---

## Key Insight
Reformulation stabilizes embeddings and improves alignment.