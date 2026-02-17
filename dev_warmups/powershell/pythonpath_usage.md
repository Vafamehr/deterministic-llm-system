# Using PYTHONPATH in a `src/` Layout (Why + When + How)

## The Situation

This project uses the **src layout**:

delay_risk_pipeline/
  src/
    delay_risk/
      ...

The actual Python package (`delay_risk`) lives inside `src/`, not at the project root.

Python does NOT automatically search inside `src`.
It only searches directories listed in `sys.path`.

So running Python from the project root cannot see the package unless we expose `src`.

---

## What PYTHONPATH Does (Concept)

`PYTHONPATH` tells Python:

"Also treat these directories as places to search for imports."

It does NOT affect Windows.
It does NOT install anything.
It only changes Python’s import behavior for the current session.

Think of it as temporarily saying:
> Pretend `src` is already installed like a library.

---

## When To Use This

Use this method when:
- Working locally in development
- You don't want to install the project yet
- You just opened a fresh terminal
- Imports fail with `ModuleNotFoundError`

Do NOT rely on this for production.
It is a developer convenience only.

---

## The One Command That Matters

From the project root:

$env:PYTHONPATH = "$PWD\src"

This adds:
delay_risk_pipeline/src
to Python's search path.

That's all.

---

## How To Confirm It Worked

Run:

python -c "import delay_risk; print(delay_risk.__file__)"

If it prints a file path inside `src/delay_risk`, you’re good.

---

## How Python Actually Builds sys.path

When Python starts, it builds a search list like:

1. Current working directory
2. Entries from PYTHONPATH
3. Standard library
4. site-packages

Without PYTHONPATH, `src` is missing from that list.
That is why imports fail.

---

## Why NOT Just `cd src`

Running Python from inside `src` *appears* to work because the
current directory is automatically added to `sys.path`.

But this breaks:
- scripts launched from project root
- tests
- debuggers
- automation
- reproducibility

So we stay in the root and expose `src` explicitly.

---

## If You Need Multiple Local Libraries

You can add more paths separated by `;` (Windows):

$env:PYTHONPATH = "$PWD\src;C:\shared_lib\src"

Always add the directory that CONTAINS the package, not the package itself.

Correct:
.../shared_lib/src

Wrong:
.../shared_lib/src/my_package

---

## Remember

PYTHONPATH changes disappear when the terminal closes.
That is intentional.
It keeps your system clean.
