# PowerShell Fluency — Daily Use

A short reference of commands actually used during development.
Goal: build muscle memory, not learn theory.

---

## Move Around

Show current path:
pwd


List files (same as `dir` / `Get-ChildItem`):
ls


Enter folder:
cd folder_name


Go back one level:
cd ..


---

## Create Files / Folders

Create directory:
mkdir folder_name


Create file (alias for `New-Item`):
ni file.txt


Example:
mkdir src\delay_risk\validation
ni src\delay_risk_init_.py


---

## Find Files

Filter listing:
Get-ChildItem -Filter *.py


---

## Delete (Use Carefully)

Delete folder and everything inside:
rmdir .\folder -Recurse -Force


- `-Recurse` → remove all contents  
- `-Force` → no confirmation prompt

---

## View Folder Structure

See tree layout:
tree


Great for understanding project structure.

---

## Inspect File Contents Quickly

Print file to terminal:
cat file.txt


Same as:
type file.txt
Get-Content file.txt


Example:
cat outputs\validation_report.json


Use to:
- Check pipeline outputs
- Inspect logs
- Quickly read small files

Avoid using on very large files.

---

## Alias Memory Table

| Use This | Same As |
|----------|---------|
ls | dir | Get-ChildItem |
cat | type | Get-Content |
ni | New-Item |

PowerShell commands often have aliases — these are the ones you’ll use daily.



## PYTHONPATH (For `src/` Layout Projects)

### Why Needed
If a project stores code inside `src/`:

project/
src/
my_package/


Python will NOT see `my_package` automatically.

You must expose `src` so imports work.

---

### One Command (Run From Project Root)

$env:PYTHONPATH = "$PWD\src"


This tells Python:
> Also search `src` when importing modules.

---

### When To Use
Use during local development when:
- Imports fail (`ModuleNotFoundError`)
- You opened a new terminal
- Project uses `src/` layout

---

### Verify It Worked

python -c "import my_package; print('OK')"


---

### Important Notes
- This is temporary (resets when terminal closes)
- Does NOT install anything
- Do NOT `cd src` — always run from project root
