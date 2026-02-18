"""
Topic: *args, **kwargs, and keyword-only arguments

Why this exists:
I want to remember how Python controls positional vs named arguments.
This pattern is used in production code (e.g., validation functions)
to prevent ambiguous calls.

Key Ideas:
- *args collects extra positional arguments into a tuple.
- **kwargs collects named arguments into a dictionary.
- A bare * forces everything after it to be keyword-only.

Memory Hook:
Read '*' as → "from here on, name your arguments."
"""

# --- Practice code below ---

def add_all(*args):
    print("args:", args)
    return sum(args)


def show_settings(**kwargs):
    print("kwargs:", kwargs)


def keyword_only(a, *, b):
    return a + b


print(add_all(1, 2, 3))
show_settings(mode="train", k=5)
print(keyword_only(1, b=2))
