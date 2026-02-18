🔍 Check Status (Always First)
git status

📦 Stage Changes

Safe default:

git add -A


Simple:

git add .


One file:

git add file.py

💾 Save Work
git commit -m "Short clear message"


Example:

git commit -m "Day 6: prompt notes"

🔁 Daily Habit
git status
git add -A
git commit -m "What I did"

📁 Move Files Safely
git mv old.py new_folder/

📜 View History
git log --oneline






Here it is all together, ready to paste as-is into git_basics.md:

# Git Basics — Daily Workflow

This is a practical routine, not a full Git guide.
Use this to build muscle memory.

---

## 0️⃣ Start a New Project (One-Time Setup)

Create project folder and enter it:



mkdir my_project
cd my_project


Initialize Git:



git init


Create `.gitignore` early (very important):



ni .gitignore


Example contents to add:



llm_env/
pycache/
*.pyc
outputs/
.env
.vscode/


First commit:



git add -A
git commit -m "Initial project structure"


---

## 1️⃣ Always Check Status First



git status


Shows what changed. Never skip this.

---

## 2️⃣ Stage Changes

Safe default (stage everything):



git add -A


Alternative (current folder only):



git add .


Single file:



git add file.py


---

## 3️⃣ Commit (Save Snapshot)



git commit -m "Short clear message"


Examples:



git commit -m "Day21 pipeline wiring"
git commit -m "Add validation layer"
git commit -m "Fix feature bug"


Message = what changed.

---

## 4️⃣ Daily Habit (End of Work Session)



git status
git add -A
git commit -m "What I did"


That’s the real workflow.

---

## 5️⃣ Move / Rename Files Safely

Preserve history:



git mv old.py new_folder/


Avoid manual moves when tracked.

---

## 6️⃣ View History



git log --oneline


Shows commit timeline.

---

## Mental Model

Git is not backup.
Git is a timeline of decisions.

Each commit = a checkpoint you can return to.