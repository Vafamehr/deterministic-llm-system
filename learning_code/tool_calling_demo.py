# learning_code/tool_calling_demo.py
"""
Day 12 — Tool Calling Demo (Simulated)

Goal:
- Show the core tool-calling loop (without a real LLM yet)
- Execute only whitelisted tools
- Validate arguments
"""


from __future__ import annotations

from typing import Any, Callable, Dict

import json


def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


TOOLS: Dict[str, Callable[..., Any]] = {
    "add": add,
    "multiply": multiply,
}

#--------------------------------------

# 2) Simulated "LLM" response
#    (Later, we will replace this with real function-calling output)
# ----------------------------
def simulated_llm_response(user_text: str) -> Dict[str, Any]:
    """
    Returns either:
    - {"type": "final", "content": "..."}  (normal answer)
    - {"type": "tool_call", "name": "...", "arguments": {...}}  (tool call)
    """
    text = user_text.lower().strip()

    # Extremely simple routing logic just for demo purposes.
    if "143" in text and "27" in text and ("*" in text or "multiply" in text):
        return {"type": "tool_call", "name": "multiply", "arguments": {"a": 143, "b": 27}}

    if "2" in text and "3" in text and ("+" in text or "add" in text):
        return {"type": "tool_call", "name": "add", "arguments": {"a": 2, "b": 3}}

    # Otherwise, act like the LLM answered directly (no tool call).
    return {"type": "final", "content": "I can answer directly (no tool needed) in this demo."}


def simulated_llm_tool_response():
    return {
        "tool_calls": [
            {
                "id": "call_1",
                "function": {
                    "name": "multiply",
                    "arguments": json.dumps({"a": 143, "b": 27})
                }
            }
        ]
    }


def execute_tool_from_response(response):
    tool_calls = response.get("tool_calls", [])

    if not tool_calls:
        return "No tool calls."

    call = tool_calls[0]
    function_data = call["function"]

    tool_name = function_data["name"]
    arguments_json = function_data["arguments"]

    arguments = json.loads(arguments_json)

    if tool_name not in TOOLS:
        raise ValueError("Unknown tool.")

    result = TOOLS[tool_name](**arguments)

    return result


def simulated_llm_final_answer(user_text: str, tool_name: str, tool_result: int) -> str:
    return f"{user_text.strip()} → {tool_name} result = {tool_result}"


# 3) Tool execution with validation (security + correctness)
# ----------------------------
def run_tool(tool_name: str, arguments: Dict[str, Any]) -> Any:
    if tool_name not in TOOLS:
        raise ValueError(f"Tool '{tool_name}' is not allowed.")

    # Minimal validation for this demo: require a and b as ints
    if not isinstance(arguments, dict):
        raise TypeError("Tool arguments must be a dictionary.")

    if "a" not in arguments or "b" not in arguments:
        raise ValueError("Missing required arguments: 'a' and 'b'.")

    a, b = arguments["a"], arguments["b"]
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Arguments 'a' and 'b' must be integers for this demo.")

    return TOOLS[tool_name](a=a, b=b)


# ----------------------------
# 4) The minimal tool loop
# ----------------------------
def tool_loop(user_text: str) -> str:
    llm_msg = simulated_llm_response(user_text)

    if llm_msg["type"] == "final":
        return llm_msg["content"]

    if llm_msg["type"] == "tool_call":
        name = llm_msg["name"]
        args = llm_msg["arguments"]

        print(f"Tool called: {name}(a={args.get('a')}, b={args.get('b')})")
        result = run_tool(name, args)
        print(f"Tool result: {result}")

        # In real systems, we would send the tool result back to the LLM to draft the final text.
        # For this demo, we generate a simple deterministic final response.
        if name == "multiply":
            return f"Final: {args['a']} * {args['b']} = {result}"
        if name == "add":
            return f"Final: {args['a']} + {args['b']} = {result}"

        return f"Final: result = {result}"

    raise RuntimeError(f"Unknown message type: {llm_msg}")


if __name__ == "__main__":
    # Demo #1
    user = "What is 143 * 27?"
    print(f"\nUser: {user}")
    print(tool_loop(user))

    # Demo #2
    user = "Can you add 2 + 3?"
    print(f"\nUser: {user}")
    print(tool_loop(user))

    # Demo #3 (no tool)
    user = "Explain what tool calling is."
    print(f"\nUser: {user}")
    print(tool_loop(user))

    print("\n--- Realistic Tool Call Simulation ---")
    response = simulated_llm_tool_response()
    result = execute_tool_from_response(response)
    print("--------------Result:", result)

    