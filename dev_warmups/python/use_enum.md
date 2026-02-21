## Enum — Controlled Constants in Python

`Enum` lets you define a fixed set of named values (instead of random numbers or fragile strings).

### Basic Example

```python
from enum import Enum

class Status(Enum):
    PENDING = 1
    APPROVED = 2
    REJECTED = 3

status = Status.PENDING

if status == Status.PENDING:
    print("Still waiting")
```

### Why Use It?

Instead of:
```python
status = "aproved"  # typo → bug
```

You use:
```python
status = Status.APPROVED
```

Safer. Cleaner. No magic values.

### Key Notes
- `Status.APPROVED.name` → `"APPROVED"`
- `Status.APPROVED.value` → `2`
- Not related to `enumerate()` (which is for indexing loops)