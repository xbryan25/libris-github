# 📚 Libris

A full-stack web application for renting and purchasing books online — built with a modern tech stack that ensures scalability, maintainability, and great user experience.

## 🧰 Tech Stack

### 🖥️ Frontend
- **Vue 3 / Nuxt 3** – modern full-stack framework for Vue
- **Nuxt UI** – prebuilt components for consistent styling
- **TailwindCSS** – utility-first CSS framework for rapid UI design

### ⚙️ Backend
- **Flask (Python)** – lightweight backend framework following MVC pattern
- **Raw SQL + Repository Layer** – for direct control over database queries

### 🗄️ Database
- **PostgreSQL** – primary relational database
- **Supabase** – PostgreSQL hosting and management platform

## 🧩 How to Contribute

### 🔐 Setting Up SSH and Cloning

If you haven’t connected your local machine to Bitbucket yet:

1. Open **Command Prompt (CMD)** or **Terminal**.
2. Generate a new SSH key (replace your email):

   ```bash
   ssh-keygen -t rsa -b 4096 -C "youremail@example.com"
   ```

3. Press **Enter** to accept the default save location.
4. (Optional) Add a passphrase for extra security.
5. Show your new public key:

   ```bash
   type %userprofile%\.ssh\id_rsa.pub      # on Windows
   cat ~/.ssh/id_rsa.pub                   # on macOS/Linux
   ```

6. Copy the key and go to **Bitbucket → Personal settings → SSH Keys → Add key**.
7. Paste the key and save.
8. After adding your SSH key, contact the repository owner to grant you access to the project on Bitbucket before cloning.

### 💻 Cloning the Repository

1. Go to the repository on Bitbucket.
2. Click the **Clone** button (top right).
3. Copy the **SSH URL**.
4. Clone to your local machine:

   ```bash
   git clone git@bitbucket.org:username/repository.git
   ```

## 🌳 Branching Model

This project follows a **two-branch workflow** to maintain code stability and streamline development.

### 1. 🚀 `main` — Production Branch
- This is the **stable production branch**.  
- Contains only reviewed, tested, and approved code.  
- Merges into `main` should come **only from a jira ticket branch** via a pull request.  
- Deployed to the **production environment**.

### 2. 🎫 Jira Ticket Branches
- Each Jira issue (feature, fix, or improvement) should have its **own branch**.  
- Created automatically from Jira via **“Create branch”** or manually from `main`.  
- The branch name **must match the Jira ticket key and description** format.  
  
    Example naming conventions:

    ```bash
    LIBRIS-1-configure-project/structure
    fix/BOOK-210-fix-pagination
    chore/BOOK-300-update-dependencies
    ```

### 🌿 Working on a Feature

Most tasks will start from **Jira**, which automatically creates a **corresponding branch in Bitbucket** when you click **“Create branch”** in the Jira issue.  
This ensures every feature or fix stays linked to its ticket.

#### 🚨 IMPORTANT — READ THIS CAREFULLY

**YOUR LOCAL BRANCH NAME MUST BE EXACTLY THE SAME AS THE REMOTE BRANCH IT TRACKS.**  
No extra words. No typos. No shortcuts.  
If the remote branch is `feature/BOOK-123-add-login`,  
your local branch **must** also be:

```bash
git checkout -b feature/BOOK-123-add-login origin/feature/BOOK-123-add-login
```

❌ Do **NOT** rename it.  
❌ Do **NOT** create your own differently named branch.  
✅ Always match the exact name from Bitbucket/Jira.  

This prevents confusion, broken tracking, and pull request errors.

#### 🧭 Regular Workflow

1. Make sure your local copy is up to date:

   ```bash
   git fetch origin
   ```

2. Checkout the remote branch created by Jira (replace with your branch name):

   ```bash
   git checkout -b feature/BOOK-123-add-login origin/feature/BOOK-123-add-login
   ```

3. Make your code changes locally.

4. Stage and commit them:

   ```bash
   git add .
   git commit -m "Implement login functionality for BOOK-123"
   ```

> 💡 **Group members can make multiple commits** while working on their branch before making a pull request.  
> It’s better to commit often with clear messages than to dump everything in one huge commit.

5. Push your updates to Bitbucket:

   ```bash
   git push origin feature/BOOK-123-add-login
   ```

6. Once your feature is done and tested, go to **Bitbucket → Pull Requests** and create a **Pull Request** for review.

#### 🚨 IMPORTANT — READ THIS CAREFULLY
**DO NOT DELETE THE LOCAL AND REMOTE BRANCHES AFTER IT HAS BEEN MERGED TO THE `main` BRANCH.**  

#### 🧼 Notes

- Never push directly to the `main` branch.  
- Always work through feature branches tied to a Jira issue.  
- Keep your local branch synced with the remote one frequently (`git pull` if needed).  
- Resolve merge conflicts **on your feature branch** before requesting a merge.

### ⚙️ Development Setup

#### Frontend (Nuxt)

To be added...

#### Backend (Flask)

##### ⚙️ Environment Configuration

Before running the Flask app, make sure to configure your environment files.

1. Copy the example environment files:

   ```bash
   cp .env.example .env
   cp .flaskenv.example .flaskenv
   ```

2. Open `.env` and `.flaskenv` and update the variables with your local configuration (e.g., database URL, secret key, etc.).

3. Save the files — Flask will automatically load these when you run `flask run`.

##### ⚙️ Loading the Flask server

```bash
# Go to backend directory
cd app

# Create virtual environment using pipenv
pipenv shell

# Install dependencies and dev dependencies
pipenv install --dev

# Install pre-commit
pre-commit install

# Run Flask app
flask run
```

### 🧼 Coding Guidelines

- Follow the **PEP8** style guide for Flask (Python).
  - Occasionally run `pre-commit run --all-files` in the terminal to check for linting, formatting, and type hints even when not planning to commit.
  - If you only want to run a specific tool instead of all hooks, you can do so:
    - Formatting:
      - `pre-commit run black --all-files`
    - Linting:
      - `pre-commit run flake8 --all-files`
    - Type checking:
      - `pre-commit run mypy --all-files`
- Follow **ESLint** rules for Nuxt (JavaScript/TypeScript).
- Keep commits clean and meaningful.
- Do not commit `.env` or credentials.
