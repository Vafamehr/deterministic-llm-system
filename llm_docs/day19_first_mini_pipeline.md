# Day 19 — Mini Pipeline Build

## Goal of Day 19

Take a simple question and run it through a complete LLM workflow:

1. Intent handling
2. Retrieval (mocked with local data)
3. Data interface formatting
4. Prompt construction
5. LLM call
6. Controlled structured output

Nothing fancy. The goal is to **prove the pipeline works end-to-end**.

Think of this as the skeleton that later becomes a real production system.

---

## Chunk 1 — Use Case + Contract

### Use Case

Decide whether to escalate shipment delays for a region based on recent operational metrics and a policy rule.

### Example User Input

"Do we need to escalate delays in Region West this week?"

### Required Output (JSON Contract)

The model must return structured data, not prose:

```json
{
  "escalate": true,
  "risk_level": "HIGH",
  "primary_cause": "PORT_CONGESTION",
  "evidence": ["..."],
  "recommended_actions": ["..."],
  "confidence": 0.0
}
```

This output contract drives how the entire pipeline is designed.

---

## Chunk 2 — Mock Retrieval (Local Stand-In for RAG)

We simulated two real-world retrieval modes:

| Type                 | Simulated By   | Real System Equivalent      |
| -------------------- | -------------- | --------------------------- |
| Structured facts     | `metrics.json` | SQL / API / warehouse query |
| Unstructured context | `policy.md`    | Vector search over docs     |

RAG’s job is only to **find relevant information**, not interpret it.

---

## Chunk 3 — Data Interface Implementation

### Purpose

Convert retrieved structured + unstructured inputs into a single reasoning-ready packet.

This step:

* Removes noise
* Normalizes signals
* Aligns facts with policy
* Presents evidence clearly to the LLM

### Function Created

```python
build_decision_packet(metrics: dict, policy: str) -> str
```

### Important

This is **NOT retrieval**.
Retrieval already happened.

This is the translation layer between:

```
RAG → finds evidence
Data Interface → prepares evidence
Prompt → asks for reasoning
LLM → thinks
```

### Why It Matters

LLMs reason far better over curated inputs than raw database rows or document dumps.
This layer controls signal-to-noise quality.

---

## Chunk 4 — LLM Execution Layer

### Purpose

Send the prepared decision packet to the model with strict instructions and enforce structured output.

### Function Created

```python
analyze_with_llm(decision_packet: str)
```

This layer:

* Adds reasoning instructions (prompt engineering)
* Forces JSON output (output contract)
* Calls the model locally via Ollama using `subprocess`

### Architectural Role

This is the **only place the LLM is invoked**.

Everything earlier prepares context.
Everything later will validate results.

---

## Day 19 System Flow (End-to-End)

```
User Question
   ↓
Retrieve structured facts        (metrics.json → simulating DB)
Retrieve document context        (policy.md → simulating vector search)
   ↓
Build Decision Packet            (data interface layer)
   ↓
Send to LLM                      (subprocess → Ollama)
   ↓
Receive structured analysis
```

---

## Key Insight from Day 19

LLM systems are mostly **data preparation pipelines**.

The model itself is just one stage.
Reliability comes from:

* controlling inputs
* structuring context
* constraining outputs

---

## What Day 19 Achieved

Moved from:

> “Calling an LLM”

to:

> “Engineering a reasoning workflow around an LLM.”
