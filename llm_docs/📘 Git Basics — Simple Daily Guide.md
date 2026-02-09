📘 Git Basics — Simple Daily Guide

This document explains the Git commands I use every day in this project.

No advanced stuff.
Just the essentials.

🚀 1. Start a New Project with Git
Initialize Git (do once per project)
git init


This starts version control in the current folder.

📁 2. Create Folders and Files
Create a Folder
mkdir folder_name


Example:

mkdir llm_docs

Create a File with Text
echo "Hello" > file.txt


Creates (or overwrites) a file.

⚠️ Careful: > deletes old content.

Create an Empty File (PowerShell)
New-Item file.txt

🔄 3. Daily Git Workflow (Most Important Part)

Every work session ends like this:

git status
git add .
git commit -m "What I did"


Example:

git status
git add .
git commit -m "Day 2: learned transformers"

📋 4. Check Project Status
git status


Shows:

New files

Changed files

Staged files

Always run this first.

📦 5. Stage Files (Prepare to Save)
Stage Everything (Beginner Mode)
git add .

Stage One File (Later Skill)
git add file.py


Staging = “ready to save”.

💾 6. Save Your Work (Commit)
git commit -m "message"


Example:

git commit -m "Day 3: RAG experiments"


Each commit is a checkpoint.

📜 7. See Your History
git log --oneline


Shows all saved versions.

🧠 8. How Git Really Works (Simple Model)

Git has 3 places:

Working Folder → Staging Area → History

Step	Command
Check	git status
Stage	git add
Save	git commit
👤 9. Set Your Name (One Time Only)

Before first commit:

git config --global user.name "Your Name"
git config --global user.email "you@email.com"


This shows who made each commit.

🌐 10. Local vs GitHub
For Now (Local Only)

You only use:

status → add → commit


No push / pull yet.

Later (With GitHub)
git push   # send work online
git pull   # download updates


We’ll learn this later.

⚠️ 11. Common Mistakes to Avoid
❌ Forgetting git status

Always check before adding.

❌ Overwriting Files
echo "text" > file.txt


Deletes old content.

Use carefully.

❌ Not Committing Often

Commit small and often.

It saves you.

📝 12. Quick Self-Test
Q1: What does git init do?

➡️ Starts Git in a folder.

Q2: What does git add . do?

➡️ Stages all files.

Q3: What does git commit do?

➡️ Saves a snapshot.

Q4: What is HEAD?

➡️ Your current position.

Q5: What is staging?

➡️ Preparing files for commit.

✅ 13. Daily Habit

At the end of every session:

git status
git add .
git commit -m "Day X: short note"


That’s it.

🎯 Summary

Git basics =

Edit → Check → Stage → Save → Repeat