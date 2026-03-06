# Tools and Retrieval

This section explains how the system expands its capabilities through tool execution and retrieval without relying directly on the LLM.

See diagram:

[Tools and Retrieval Capability Flow](./diagrams/tools_and_retrieval.md)

Tools and retrieval provide **capability expansion** for the system.  
They allow the system to access external actions or knowledge while still maintaining the **deterministic-first execution model**.

In this architecture, the **orchestrator decides when these capabilities are invoked**.  
Tools and retrieval are therefore controlled extensions of deterministic logic rather than autonomous components.

---

## Tool Execution

Tools represent structured operations that the system can perform when deterministic logic requires external capability.

Examples include:

- calling external services
- performing specialized computations
- accessing structured data sources
- retrieving information from APIs or databases

Tools are executed through a **Tool Runner**, which interacts with a **Tool Registry**.

The registry defines:

- available tools
- expected input schema
- returned output structure

Each tool invocation is executed using a **Tool Envelope**, which ensures that the request and response remain structured and traceable.

This design makes tool execution:

- predictable
- auditable
- safe
- easy to integrate into deterministic reasoning

---

## Retrieval

Retrieval provides **contextual knowledge** when the system needs additional information to resolve a request.

The retrieval interface receives a query and returns **context chunks** from a knowledge index.

These chunks may include:

- documentation
- stored knowledge
- project-specific information
- reference materials

The retrieved context is returned to the deterministic layer, allowing the system to attempt resolution again using the newly available information.

---

## Deterministic Integration

Both **tool results** and **retrieved context** are fed back into the deterministic stage.

The system then attempts to resolve the request again using the structured outputs returned by these capabilities.

Only if the request remains unresolved does the system allow **LLM reasoning as a secondary capability**.

This ensures that structured and deterministic mechanisms are always attempted before invoking the language model.

---

## Kitchen Analogy

| System Component | Kitchen Role |
|---|---|
Tools | Pantry runner fetching ingredients |
Retrieval | Recipe book lookup |
Deterministic Layer | Cooking using the recipe |
LLM | Creative chef improvising if the recipe fails |