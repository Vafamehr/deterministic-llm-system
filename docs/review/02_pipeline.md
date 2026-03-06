# Request Execution Pipeline

This section describes how a user request flows through the system from intake to final output.

See diagram:

[Request Execution Pipeline](./diagrams/pipeline.md)

The system processes every request through a **deterministic-first execution pipeline** controlled by the orchestrator.

The guiding principle is simple: **use reliable logic first**, then expand system capability only when deterministic methods cannot resolve the request.

This approach improves reliability, makes system behavior easier to debug, and ensures that LLM reasoning is used only when necessary.

---

## Pipeline Stages

### 1. Request Intake

The **Orchestrator** receives the user request and initializes the execution pipeline.

Its responsibilities include:

- interpreting the request
- determining the next execution step
- coordinating the pipeline stages

The orchestrator acts as the **central controller of system flow**.

---

### 2. Deterministic Attempt

The system first attempts to resolve the request using deterministic logic.

Examples include:

- validation
- rule execution
- known transformations
- structured reasoning

If a valid result is produced, the pipeline proceeds directly to the **Governance stage**.

This is the **preferred execution path** because deterministic logic is predictable and easy to test.

---

### 3. Capability Expansion

If deterministic logic cannot resolve the request, the orchestrator identifies the missing capability.

Two structured expansion mechanisms are available.

#### Tool Execution

The system invokes a **Tool** through a registry.

Tools:

- perform structured external operations
- return well-defined outputs
- provide capabilities that deterministic logic alone cannot perform

#### Retrieval

The system performs **Retrieval** to obtain contextual knowledge.

Retrieval:

- queries a knowledge source
- returns relevant context chunks
- feeds structured context back into the deterministic layer

After tools or retrieval complete, deterministic reasoning runs again using the newly available data.

---

### 4. Optional LLM Reasoning

If deterministic logic combined with tools or retrieval still cannot resolve the request, the system may allow **LLM reasoning**.

The LLM acts as a **bounded reasoning component** used only when earlier stages cannot complete the task.

This design prevents the LLM from becoming the primary controller of the system.

---

### 5. Governance

Before returning a result, the system passes the candidate output through the **Governance Gate**.

Governance checks may include:

- safety evaluation
- ambiguity detection
- evidence verification
- policy validation

Only approved results move to the final stage.

---

### 6. Final Output

If governance approves the result, the system returns the **final answer** to the user.

---

### 7. Observability

Every stage in the pipeline produces **trace artifacts**.

Trace data records:

- which components executed
- decision points in the pipeline
- execution outcomes
- timing information

This observability allows the system to be **debugged, inspected, and explained**.

---

## Kitchen Analogy

| Pipeline Stage | Kitchen Equivalent |
|---|---|
User Request | Order ticket |
Orchestrator | Head chef |
Deterministic Logic | Standard recipe |
Tool Execution | Pantry runner |
Retrieval | Recipe book lookup |
LLM Reasoning | Creative chef |
Governance | Quality check |
Trace | Ticket history |