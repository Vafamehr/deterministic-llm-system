# Python Imports + python -m (Practical Rules)

## 1) Absolute vs Relative Imports

Absolute import:
from package.module import X

Relative import (inside a package only):
from .module import X
from ..subpkg.module import Y

Rule:
- Inside a package → use relative imports
- Outside the package → use absolute imports

Never mix randomly.

---

## 2) When Relative Imports Break

If you run:
python file.py

Python treats it as a standalone script.
Relative imports will fail.

---

## 3) Correct Way to Run Modules

Always run from project root using:

python -m package.module

Example:
python -m mypackage.pipeline

Why:
- Preserves package structure
- Relative imports work
- Matches production behavior

---

## 4) Required Structure

project_root/
  src/
    mypackage/
      __init__.py
      module.py

Set:
PYTHONPATH=src

Run:
python -m mypackage.module no need .py in running

---

## Final Rule

Design your project like a library.
Run with -m.
Use clean import boundaries.