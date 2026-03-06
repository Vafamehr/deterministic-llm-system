📄 Revised Day 12 — Tool Calling (Clean Version)


Day 12 — Tool Calling
1️⃣ What Tool Calling Is

Tool calling = the LLM outputs a structured function call instead of free text when external computation is required.

The model becomes a planner, not the executor.

2️⃣ Why Tool Calling Exists

LLMs are weak at:

exact math

real-time data

database queries

deterministic logic

Tools handle these reliably.

3️⃣ Full Architecture
User
↓
LLM
↓
Function Call (JSON)
↓
External Tool
↓
Result
↓
LLM
↓
Final Answer


Execution happens outside the model.

4️⃣ Tool Schema (The Contract)

A tool schema defines:

name

description

parameters

required fields

Example:

{
  "name": "multiply",
  "description": "Multiply two integers",
  "parameters": {
    "type": "object",
    "properties": {
      "a": { "type": "integer" },
      "b": { "type": "integer" }
    },
    "required": ["a", "b"]
  }
}

Schema Design Rules

Be precise

Be narrow

Define required fields

Avoid vague descriptions

Most tool failures come from poor schema design.

5️⃣ Minimal Tool Loop (Core Logic)

User message → LLM

LLM outputs:

final text OR

structured tool call

System executes tool

Tool result returned

LLM produces final response

6️⃣ Security Rule

Only execute tools from a whitelist:

TOOLS = {
  "add": add,
  "multiply": multiply
}


Reject unknown tool names.

Never execute arbitrary calls.

7️⃣ Realistic Model Output Format

Models typically return:

{
  "tool_calls": [
    {
      "function": {
        "name": "multiply",
        "arguments": "{\"a\":143,\"b\":27}"
      }
    }
  ]
}


Important:

Arguments come as JSON string

Must parse with json.loads()

May contain multiple tool calls

8️⃣ Execution Steps (Production Pattern)

Extract tool_calls

Get function name

Parse JSON arguments

Validate tool name

Execute tool

Send result back to LLM

9️⃣ Tool Result Reinjection

Tool output is not the final answer.

It must be sent back to the LLM so it can:

explain result

format response

combine with other reasoning

Final loop:

User
↓
LLM emits tool call
↓
Tool executes
↓
Tool result returned
↓
LLM produces final answer

🔑 What To Hook To Memory

Memorize these five things only:

LLM plans. Tools execute.

Tool schema is a contract.

Always whitelist tools.

Arguments arrive as JSON strings.

Tools produce facts. LLM produces narrative.

Everything else you can look up.

🧠 Mental Model

Tool calling transforms an LLM from:

Chatbot → System Controller

That is the major shift.