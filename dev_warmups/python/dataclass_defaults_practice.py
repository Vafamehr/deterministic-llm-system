"""
Topic: dataclass defaults, field(), and why mutable defaults are dangerous

This file explains TWO important Python behaviors:

1️⃣ Mutable default arguments are shared across function/class instances.
2️⃣ dataclasses require field(default_factory=...) to avoid that bug.

This is not a dataclass rule.
This is a Python object model rule.
Dataclasses just expose it more clearly.

------------------------------------------------------------
THE PROBLEM (Plain Python First)
------------------------------------------------------------
"""


def bad_function(x, bucket=[]):  # <-- mutable default!
    bucket.append(x)
    return bucket


print("bad_function calls:")
print(bad_function(1))
print(bad_function(2))  # Why is 1 still there?!
print(bad_function(3))

"""
Expected (if defaults were recreated each call):
[1]
[2]
[3]

Actual:
[1]
[1,2]
[1,2,3]

Why?

Because Python evaluates default arguments ONCE at function definition time.
That list lives forever.
Every call reuses the SAME object.
"""

print("\n-----------------------------")

"""
------------------------------------------------------------
THE CORRECT PATTERN (Plain Python Fix)
------------------------------------------------------------
"""


def good_function(x, bucket=None):
    if bucket is None:
        bucket = []  # create a NEW list each call
    bucket.append(x)
    return bucket


print("good_function calls:")
print(good_function(1))
print(good_function(2))
print(good_function(3))

"""
Now each call gets a fresh list.

This pattern is extremely common in Python APIs.
"""

print("\n=============================")

"""
------------------------------------------------------------
NOW: HOW THIS RELATES TO DATACLASSES
------------------------------------------------------------

Dataclasses would have the SAME bug if we did this:
"""


from dataclasses import dataclass, field

print("\n=============================")
print("Dataclasses note:")
print("Modern Python often blocks mutable defaults like {} or [] in dataclasses.")
print("So we demonstrate the shared-default bug using a plain class first.\n")


class BadClass:
    # This is the classic shared-default bug (plain Python class attribute)
    numeric_ranges = {}  # shared across all instances


b1 = BadClass()
b2 = BadClass()

b1.numeric_ranges["risk_score"] = (0, 1)

print("Plain class sharing state (class attribute):")
print("b1:", b1.numeric_ranges)
print("b2:", b2.numeric_ranges)  # changes because it's shared


print("\n-----------------------------\n")


@dataclass
class GoodRules:
    # Correct dataclass pattern: fresh dict per instance
    numeric_ranges: dict = field(default_factory=dict)


g1 = GoodRules()
g2 = GoodRules()

g1.numeric_ranges["risk_score"] = (0, 1)

print("Dataclass with default_factory (independent state):")
print("g1:", g1.numeric_ranges)
print("g2:", g2.numeric_ranges)