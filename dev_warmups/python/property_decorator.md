## Python `@property` — Quick Note

### What it is

`@property` lets a method behave like an attribute.

It allows you to expose computed or protected values **without using `get_...()` methods**.

---

### Why use it?

* Cleaner API (`obj.value` instead of `obj.get_value()`).
* Encapsulation (hide internal state).
* Can make values read-only or validated.
* Lets you change implementation later without breaking callers.

---

### Example

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius  # internal

    @property
    def area(self):
        return 3.14 * self._radius ** 2
```

Usage:

```python
c = Circle(2)
print(c.area)  # looks like a field, actually computed
```

You can read `area`, but you cannot assign to it unless you add a setter.

---

### Mental Model

**`@property` = controlled window into an object.**
Looks like data → runs logic safely behind the scenes.
