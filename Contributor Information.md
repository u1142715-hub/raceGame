# Contributing Guide

Thank you for your interest in contributing to this project.  
To keep the workflow simple and prevent accidental changes to the main repository, all contributors must use **forks**. Forking ensures everyone works independently and safely.

---

## 1. Fork the Repository

1. Visit the main GitHub page of this project.
2. Click the **Fork** button in the top-right corner.
3. GitHub will create your own copy of the project under your account.

You now have full control of your fork.

---

## 2. Clone Your Fork

Open a terminal and run:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
Replace <your-username> with your GitHub username.

3. Create a Branch for Your Work
Inside your cloned project folder:

bash
git checkout -b <your-branch-name>
Examples of branch names:

student-john

feature-new-car

bugfix-speed-calculation

This keeps your work organised and separate.

4. Make Your Changes
Edit files, add features, fix bugs — whatever your task requires.

When ready to save your work:

bash
git add .
git commit -m "Describe your changes here"
git push -u origin <your-branch-name>
This pushes your work to your fork, not the main project.

5. (Optional) Sync Your Fork With the Original Repository
Before submitting your work, update your fork so it matches the latest version of the main project:

bash
git remote add upstream https://github.com/<original-owner>/<repo-name>.git
git pull upstream main
This helps avoid merge conflicts.

6. Submit a Pull Request
Go to your fork on GitHub.

Switch to your branch.

Click Compare & pull request.

Write a short description of your changes.

Submit the pull request.

Your changes will be reviewed and merged if everything looks good.

Why Forking Is Required
Forking ensures:

You cannot accidentally break the main project.

You cannot overwrite other contributors’ work.

You can experiment freely in your own workspace.

The project owner can review and merge changes safely.

This is the standard workflow used in open‑source and team projects.

Thank you for contributing!

Code