# Tools and Retrieval

Tools and retrieval provide **capability expansion** for the system.  
They allow the system to access external actions or knowledge **without relying directly on the LLM**.

In the deterministic-first architecture, the **orchestrator decides when these capabilities are used**.

---

## Tool Execution

Tools represent structured operations the system can perform when deterministic logic needs external capability.

Examples include:
- calling external services
- performing specialized computations
- accessing structured data sources

Tools are executed through a **Tool Runner** that references a **Tool Registry**.

The registry defines:
- available tools
- expected input schema
- returned output structure

Each tool call is executed through a **Tool Envelope**, which ensures the request and response remain structured and traceable.

This keeps tool execution **predictable, auditable, and safe**.

---

## Retrieval

Retrieval provides **contextual knowledge** when the system needs additional information.

The retrieval interface receives a query and returns **context chunks** from a knowledge index.

These chunks may include:
- documentation
- stored knowledge
- project-specific information

The retrieved context is returned to the deterministic layer so the system can attempt resolution again.

---

## Deterministic Integration

Both **tool results** and **retrieved context** are fed back into the deterministic stage.

The system attempts to resolve the request again using the new information.

Only if the request is still unresolved does the system allow **LLM reasoning as a secondary capability**.

---

## Kitchen Analogy

| System Component | Kitchen Role |
|---|---|
Tools | Pantry runner fetching ingredients |
Retrieval | Recipe book lookup |
Deterministic Layer | Cooking using the recipe |
LLM | Creative chef improvising if the recipe fails |