# --- String cleanup ---
text = "   Contract A   "
clean = text.strip().lower()
print(clean)

# --- f-string formatting ---
task = "deadline extraction"
doc = "Contract A"
msg = f"Working on {task} for {doc}"
print(msg)

# --- Safe dictionary access ---
data = {"domain": "law"}
domain = data.get("domain", "unknown")
print(domain)

# --- Simple validation ---
def process_amount(x):
    if not isinstance(x, (int, float)):
        raise ValueError("Amount must be numeric")
    return round(x, 2)

print(process_amount(10.456))

# --- Joining clean output ---
items = ["deadlines", "payment", "termination"]
summary = ", ".join(items)
print(summary)

use all([True, True]) or any([True, False]) ----> good tool

# --- nonlocal — Modify Variables in an Enclosing Function

1. nonlocal — Modify Variables in an Enclosing Function

Use nonlocal inside a nested function when you need to update a variable defined in the outer function.

Without it, Python treats the variable as a new local one and raises an error.

Example
def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1
        return count

    return inner

counter = outer()
print(counter())  # 1
print(counter())  # 2

When to Use

Small helper functions inside a workflow

Updating shared state (buffers, counters, accumulators)

When you want logic scoped locally, not globally

Mental Model



# --- @dataclass — Lightweight Structured Objects

dataclass removes boilerplate when creating classes meant to hold data, not behavior.

Instead of writing constructors and repr methods manually, Python generates them automatically.

Example
from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    meta: dict


Usage:

chunk = Chunk(text="Example", meta={"section": "termination"})
print(chunk.text)

Why Use It

Cleaner than dictionaries (structured + type-aware)

Much lighter than full classes

Great for pipelines passing data between steps

Improves readability and debugging

When to Use

✔ Data containers (RAG chunks, configs, results)
✔ Objects with fields but little logic

When Not to Use

✖ Classes with heavy behavior or complex methods

Quick Comparison
Tool	Use Case
dict	Quick, loose data
dataclass	Structured lightweight data
class	Full behavior + logic
