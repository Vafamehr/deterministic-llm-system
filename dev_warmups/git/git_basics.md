# Git — What I Actually Use

## Check
git status

## Stage
git add <file>
git add -A   # only if sure

## Commit
git commit -m "feat: what changed"

## End of Session
git status
git add -A
git commit -m "checkpoint"

## Rename / Move
git mv old.py new.py

## See History
git log --oneline


# Git Branching — Practical Use

## What Is a Branch?

A branch is a separate line of work.

It lets you experiment without touching the base branch (`master`).

---

## Create a Branch

git checkout -b feature/name

Creates the branch and switches to it.

---

## Work Normally

Edit → add → commit as usual:

git add file.py
git commit -m "feat: describe change"

These commits belong only to this branch.

---

## See Where You Are

git branch

`*` shows the current branch.

---

## Switch Branches

git checkout master
git checkout feature/name

Git will block switching if changes are not committed.

---

## If Git Blocks Checkout

Commit your work:

git add file.py
git commit -m "save work before switching"

Or temporarily hide changes:

git stash

---

## Delete Branch (If Experiment Not Needed)

git checkout master
git branch -d feature/name

-d → delete only if merged (safe mode)

-D → force delete (I know what I’m doing)

---

## Mental Model

Branch = isolated timeline of commits.

Use branches whenever trying:
- new features
- refactors
- risky ideas

Keep base branch stable.





