# 🧾 Conventional Commits Guide

This project follows the **Conventional Commits** standard to keep commit messages structured, meaningful, and consistent.  
Using this format helps automate changelogs, track features and fixes easily, and maintain a clean project history.


## ✍️ Commit Message Format

Each commit message should be structured as:
<type>(optional scope): <description>

### Example:

```bash
feat(auth): add login endpoint
fix(ui): correct navbar alignment
docs(readme): update setup instructions
```

## 🧩 Commit Types

| Type | Description |
|------|--------------|
| **feat** | A new feature for the user or system. |
| **fix** | A bug fix. |
| **docs** | Documentation only changes. |
| **style** | Code style or formatting changes (no logic changes). |
| **refactor** | Code changes that neither fix a bug nor add a feature. |
| **perf** | Performance improvements. |
| **test** | Adding or modifying tests. |
| **chore** | Routine tasks, build updates, or maintenance. |

## 🧠 Guidelines

- Keep your **description short and clear** (max ~72 chars).  
- Use **present tense**: “add” not “added” or “adds.”  
- Don’t capitalize the first letter after the colon.  
- Don’t add a period `.` at the end.  
- Each commit should represent **one logical change** — avoid mixing unrelated changes.


## 🎯 Examples

```bash
git commit -m "feat(api): add endpoint for user rentals"
git commit -m "fix(auth): handle invalid password errors"
git commit -m "refactor(book): simplify rental validation logic"
git commit -m "docs(commits): add conventional commit guide"
```

## 🧼 Why It Matters
- ✅ Easier to understand the project history.
- ✅ Cleaner pull requests and changelogs.
- ✅ Helps tools like semantic-release or commitlint automate versioning.
- ✅ Keeps everyone on the same page in group projects.

## 🧠 Tip

If you’re unsure which type to use, start with:

```bash
git commit -m "chore: describe what you did"
```
