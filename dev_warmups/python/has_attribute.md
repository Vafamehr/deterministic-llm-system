# Python — hasattr()

hasattr(obj, "attr_name")

Returns True if the attribute exists, otherwise False.

Works for:
- Variables
- Methods
- Inherited attributes

Example:

class Person:
    def greet(self):
        return "Hi"

p = Person()

hasattr(p, "greet")  # True
hasattr(p, "age")    # False

Mental model:
If you can access it with a dot (obj.something),
hasattr checks whether it exists.

# Python — getattr()

getattr(obj, "attr_name", default)

Returns the attribute value if it exists.
If not, returns the default value.

Example:

class Person:
    def __init__(self):
        self.name = "Ali"

p = Person()

getattr(p, "name")          # "Ali"
getattr(p, "age", None)     # None

Works for methods too:

class Person:
    def greet(self):
        return "Hi"

p = Person()

method = getattr(p, "greet", None)
if method:
    method()

Mental model:
hasattr → check
getattr → retrieve safely