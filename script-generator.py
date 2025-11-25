#!/usr/bin/env python3
"""
GitSage Script Generator - Educational GitHub Automation
Generates custom scripts while teaching GitHub concepts to novices
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
try:
    from rich.console import Console
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich import print as rprint
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    Console = None

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class ScriptGenerator:
    """Generate custom GitHub automation scripts with educational content"""

    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.templates = self._load_templates()
        self.educational_mode = True

    def _load_templates(self):
        """Load script templates"""
        return {
            'auto-commit': {
                'name': 'Automatic Commit & Push',
                'description': 'Automatically commit changes and push to GitHub',
                'difficulty': 'Beginner',
                'learns': ['git add', 'git commit', 'git push', 'commit messages']
            },
            'branch-workflow': {
                'name': 'Feature Branch Workflow',
                'description': 'Create feature branch, make changes, create PR',
                'difficulty': 'Intermediate',
                'learns': ['git branch', 'git checkout', 'pull requests', 'code review']
            },
            'repo-sync': {
                'name': 'Repository Synchronization',
                'description': 'Keep local repos in sync with remote',
                'difficulty': 'Beginner',
                'learns': ['git fetch', 'git pull', 'remote tracking', 'merge conflicts']
            },
            'release-automation': {
                'name': 'Automated Release Creation',
                'description': 'Tag commits and create GitHub releases',
                'difficulty': 'Advanced',
                'learns': ['git tag', 'semantic versioning', 'releases', 'changelogs']
            },
            'backup-all-repos': {
                'name': 'Backup All Repositories',
                'description': 'Clone/backup all your GitHub repositories',
                'difficulty': 'Intermediate',
                'learns': ['gh CLI', 'git clone', 'batch operations', 'automation']
            },
            'pr-automation': {
                'name': 'Pull Request Automation',
                'description': 'Automate PR creation with templates',
                'difficulty': 'Intermediate',
                'learns': ['gh pr create', 'PR templates', 'labels', 'assignees']
            },
            'issue-management': {
                'name': 'Issue Management Script',
                'description': 'Batch create/update/close issues',
                'difficulty': 'Intermediate',
                'learns': ['gh issue', 'labels', 'milestones', 'project management']
            },
            'ci-setup': {
                'name': 'CI/CD Pipeline Setup',
                'description': 'Generate GitHub Actions workflow',
                'difficulty': 'Advanced',
                'learns': ['GitHub Actions', 'YAML', 'CI/CD', 'automation']
            }
        }

    def print(self, message, style=""):
        """Print with optional rich styling"""
        if self.console and RICH_AVAILABLE:
            if style:
                self.console.print(message, style=style)
            else:
                self.console.print(message)
        else:
            print(message)

    def show_menu(self):
        """Display interactive menu"""
        if self.console:
            self.console.print(Panel.fit(
                "[bold cyan]GitSage Script Generator[/bold cyan]\n"
                "[yellow]Learn GitHub while automating your workflow[/yellow]",
                border_style="cyan"
            ))
        else:
            print("\n=== GitSage Script Generator ===")
            print("Learn GitHub while automating your workflow\n")

        print("\n[bold]Available Script Templates:[/bold]\n" if self.console else "\nAvailable Script Templates:\n")

        for idx, (key, template) in enumerate(self.templates.items(), 1):
            difficulty_color = {
                'Beginner': 'green',
                'Intermediate': 'yellow',
                'Advanced': 'red'
            }.get(template['difficulty'], 'white')

            if self.console:
                self.console.print(
                    f"{idx}. [{difficulty_color}]{template['difficulty']}[/{difficulty_color}] - "
                    f"[bold]{template['name']}[/bold]\n"
                    f"   {template['description']}\n"
                    f"   [dim]Teaches: {', '.join(template['learns'][:3])}...[/dim]"
                )
            else:
                print(f"{idx}. {template['difficulty']} - {template['name']}")
                print(f"   {template['description']}")
                print(f"   Teaches: {', '.join(template['learns'][:3])}...")

        print(f"\n{len(self.templates) + 1}. Custom Script (Advanced)")
        print(f"{len(self.templates) + 2}. GitHub Learning Mode")
        print(f"{len(self.templates) + 3}. Exit")

    def get_user_choice(self):
        """Get user's menu choice"""
        if self.console and RICH_AVAILABLE:
            choice = Prompt.ask(
                "\n[cyan]Select an option[/cyan]",
                default="1"
            )
        else:
            choice = input("\nSelect an option (1-{0}): ".format(len(self.templates) + 3))

        try:
            return int(choice)
        except ValueError:
            return 0

    def generate_auto_commit_script(self, config):
        """Generate auto-commit script with education"""
        script = f"""#!/usr/bin/env bash
# Auto-Commit Script - Generated by GitSage
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# EDUCATIONAL NOTES:
# This script automates the git commit and push workflow.
#
# Basic Git Workflow:
# 1. git add    - Stage changes for commit
# 2. git commit - Save changes to local repository
# 3. git push   - Upload changes to remote (GitHub)
#
# Learn more: https://git-scm.com/book/en/v2/Getting-Started-What-is-Git

set -e  # Exit on error

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo "🔄 Auto-Commit Script Starting..."

# Configuration
REPO_PATH="{config.get('repo_path', '.')}"
COMMIT_MESSAGE="{config.get('commit_message', 'Auto-commit: Update files')}"
BRANCH="{config.get('branch', 'main')}"

cd "$REPO_PATH" || exit 1

# LESSON: Check git status before committing
# 'git status' shows what files have changed
echo -e "${{YELLOW}}📊 Checking repository status...${{NC}}"
git status

# LESSON: Add files to staging area
# You can add specific files or all changes (.)
echo -e "${{YELLOW}}📦 Staging changes...${{NC}}"
git add .

# LESSON: Create a commit
# A commit is like a snapshot of your code
# Good commit messages explain WHAT changed and WHY
echo -e "${{YELLOW}}💾 Creating commit...${{NC}}"
git commit -m "$COMMIT_MESSAGE" || {{
    echo -e "${{RED}}⚠️  No changes to commit${{NC}}"
    exit 0
}}

# LESSON: Push to remote repository
# This uploads your changes to GitHub
# -u origin <branch> sets up tracking for first push
echo -e "${{YELLOW}}🚀 Pushing to GitHub...${{NC}}"
git push -u origin "$BRANCH"

echo -e "${{GREEN}}✅ Successfully committed and pushed changes!${{NC}}"

# LEARN MORE:
# - Commit best practices: https://chris.beams.io/posts/git-commit/
# - Understanding git push: https://git-scm.com/docs/git-push
"""
        return script

    def generate_branch_workflow_script(self, config):
        """Generate feature branch workflow script"""
        script = f"""#!/usr/bin/env bash
# Feature Branch Workflow - Generated by GitSage
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# EDUCATIONAL NOTES:
# This script implements the Feature Branch workflow - a best practice
# for collaborative development.
#
# Why use feature branches?
# - Keep main/master branch stable
# - Work on features independently
# - Easy code review via Pull Requests
# - Simple to discard failed experiments
#
# Learn more: https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow

set -e

# Colors
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
CYAN='\\033[0;36m'
NC='\\033[0m'

FEATURE_NAME="{config.get('feature_name', 'new-feature')}"
BASE_BRANCH="{config.get('base_branch', 'main')}"
REPO_PATH="{config.get('repo_path', '.')}"

cd "$REPO_PATH" || exit 1

echo -e "${{CYAN}}🌿 Feature Branch Workflow Starting...${{NC}}"

# LESSON 1: Update base branch
# Always start from latest code
echo -e "${{YELLOW}}📥 Step 1: Updating $BASE_BRANCH...${{NC}}"
git checkout "$BASE_BRANCH"
git pull origin "$BASE_BRANCH"

# LESSON 2: Create feature branch
# Branch naming: feature/name, fix/name, or descriptive names
echo -e "${{YELLOW}}🌱 Step 2: Creating feature branch '$FEATURE_NAME'...${{NC}}"
git checkout -b "feature/$FEATURE_NAME"

echo -e "${{GREEN}}✅ Feature branch created!${{NC}}"
echo ""
echo "Now you can:"
echo "  1. Make your changes"
echo "  2. Commit with: git commit -m 'Your message'"
echo "  3. Push with: git push -u origin feature/$FEATURE_NAME"
echo "  4. Create Pull Request on GitHub"
echo ""

# LESSON 3: After work is done
echo "When ready to create Pull Request:"
echo "  gh pr create --title 'Add $FEATURE_NAME' --body 'Description'"
echo ""

# TIP: Best practices
echo "💡 Best Practices:"
echo "  - Keep feature branches short-lived"
echo "  - Commit often with clear messages"
echo "  - Update from $BASE_BRANCH regularly"
echo "  - Request code reviews"

# LEARN MORE:
# - Pull Request guide: https://docs.github.com/en/pull-requests
# - Code review: https://google.github.io/eng-practices/review/
"""
        return script

    def generate_repo_sync_script(self, config):
        """Generate repository sync script"""
        script = f"""#!/usr/bin/env bash
# Repository Sync Script - Generated by GitSage
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# EDUCATIONAL NOTES:
# This script keeps your local repository in sync with remote (GitHub).
#
# Understanding git fetch vs pull:
# - fetch: Downloads changes but doesn't merge them
# - pull: Downloads AND merges changes (fetch + merge)
#
# Why sync regularly?
# - Stay up-to-date with team changes
# - Avoid merge conflicts
# - See latest features/fixes
#
# Learn more: https://www.atlassian.com/git/tutorials/syncing

set -e

GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
RED='\\033[0;31m'
NC='\\033[0m'

REPOS=(
{chr(10).join(f'    "{repo}"' for repo in config.get('repos', ['.']))}
)

echo "🔄 Syncing repositories with GitHub..."

for repo in "${{REPOS[@]}}"; do
    echo -e "${{YELLOW}}📂 Processing: $repo${{NC}}"

    if [ ! -d "$repo/.git" ]; then
        echo -e "${{RED}}⚠️  Not a git repository: $repo${{NC}}"
        continue
    fi

    cd "$repo" || continue

    # LESSON: Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo -e "${{YELLOW}}⚠️  Uncommitted changes detected${{NC}}"
        echo "Stashing changes temporarily..."
        git stash save "Auto-stash before sync $(date)"
        STASHED=1
    fi

    # LESSON: Fetch latest changes
    echo "📥 Fetching from origin..."
    git fetch origin

    # LESSON: Get current branch
    BRANCH=$(git branch --show-current)
    echo "Current branch: $BRANCH"

    # LESSON: Pull changes
    echo "⬇️  Pulling latest changes..."
    git pull origin "$BRANCH" || {{
        echo -e "${{RED}}❌ Merge conflict detected!${{NC}}"
        echo "You'll need to resolve conflicts manually."
        exit 1
    }}

    # LESSON: Restore stashed changes
    if [ "$STASHED" = "1" ]; then
        echo "📤 Restoring your changes..."
        git stash pop
    fi

    echo -e "${{GREEN}}✅ Synced: $repo${{NC}}"
    echo ""

    cd - > /dev/null
done

echo -e "${{GREEN}}🎉 All repositories synced!${{NC}}"

# LEARN MORE:
# - Git stash: https://git-scm.com/docs/git-stash
# - Merge conflicts: https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts
"""
        return script

    def generate_backup_repos_script(self, config):
        """Generate backup all repos script"""
        script = f"""#!/usr/bin/env bash
# Backup All Repositories - Generated by GitSage
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# EDUCATIONAL NOTES:
# This script uses GitHub CLI (gh) to backup all your repositories.
#
# Why backup your code?
# - Protection against accidental deletion
# - Local copy for offline work
# - Disaster recovery
# - Migration between services
#
# GitHub CLI (gh) is a powerful command-line tool for GitHub operations.
# Learn more: https://cli.github.com/

set -e

GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
CYAN='\\033[0;36m'
NC='\\033[0m'

BACKUP_DIR="{config.get('backup_dir', '~/github-backups')}"
DATE=$(date +%Y%m%d)

echo -e "${{CYAN}}💾 GitHub Repository Backup${{NC}}"
echo "Backup location: $BACKUP_DIR"
echo ""

# Create backup directory
mkdir -p "$BACKUP_DIR"
cd "$BACKUP_DIR" || exit 1

# LESSON: Check if gh CLI is authenticated
echo -e "${{YELLOW}}🔐 Checking GitHub CLI authentication...${{NC}}"
if ! gh auth status > /dev/null 2>&1; then
    echo "Not authenticated. Running 'gh auth login'..."
    gh auth login
fi

# LESSON: List all your repositories
echo -e "${{YELLOW}}📋 Fetching repository list...${{NC}}"
REPOS=$(gh repo list --limit 1000 --json nameWithOwner --jq '.[].nameWithOwner')

TOTAL=$(echo "$REPOS" | wc -l)
CURRENT=0

echo "Found $TOTAL repositories to backup"
echo ""

# LESSON: Clone or update each repository
for repo in $REPOS; do
    CURRENT=$((CURRENT + 1))
    echo -e "${{CYAN}}[$CURRENT/$TOTAL]${{NC}} Processing: $repo"

    REPO_NAME=$(basename "$repo")

    if [ -d "$REPO_NAME" ]; then
        # LESSON: Update existing repository
        echo "  📥 Updating existing backup..."
        cd "$REPO_NAME" || continue
        git pull --all
        cd ..
    else
        # LESSON: Clone new repository
        echo "  📦 Cloning repository..."
        gh repo clone "$repo"
    fi

    echo -e "  ${{GREEN}}✅ Done${{NC}}"
done

echo ""
echo -e "${{GREEN}}🎉 Backup complete!${{NC}}"
echo "Backed up $TOTAL repositories to: $BACKUP_DIR"

# LEARN MORE:
# - GitHub CLI manual: https://cli.github.com/manual/
# - Git clone: https://git-scm.com/docs/git-clone
"""
        return script

    def generate_pr_automation_script(self, config):
        """Generate PR automation script"""
        script = f"""#!/usr/bin/env bash
# Pull Request Automation - Generated by GitSage
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
#
# EDUCATIONAL NOTES:
# Pull Requests (PRs) are how teams review code before merging.
#
# PR Best Practices:
# - Clear, descriptive title
# - Detailed description of changes
# - Link to related issues
# - Request specific reviewers
# - Add appropriate labels
#
# Learn more: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests

set -e

GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
CYAN='\\033[0;36m'
NC='\\033[0m'

PR_TITLE="{config.get('pr_title', 'Feature: Description')}"
BASE_BRANCH="{config.get('base_branch', 'main')}"

echo -e "${{CYAN}}🔀 Pull Request Automation${{NC}}"

# LESSON: Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" = "$BASE_BRANCH" ]; then
    echo -e "${{YELLOW}}⚠️  You're on $BASE_BRANCH branch!${{NC}}"
    echo "Create a feature branch first:"
    echo "  git checkout -b feature/your-feature-name"
    exit 1
fi

# LESSON: Ensure branch is pushed
echo -e "${{YELLOW}}📤 Pushing branch to GitHub...${{NC}}"
git push -u origin "$CURRENT_BRANCH"

# LESSON: Create pull request
echo -e "${{YELLOW}}🔀 Creating Pull Request...${{NC}}"

PR_BODY="## Summary
Changes made in this PR:
-

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Comments added where needed
- [ ] Documentation updated
"

gh pr create \\
    --title "$PR_TITLE" \\
    --body "$PR_BODY" \\
    --base "$BASE_BRANCH"

echo -e "${{GREEN}}✅ Pull Request created!${{NC}}"
echo ""
echo "Next steps:"
echo "  1. View PR: gh pr view --web"
echo "  2. Request reviews: gh pr edit --add-reviewer username"
echo "  3. Add labels: gh pr edit --add-label bug,enhancement"
echo "  4. After approval: gh pr merge"

# LEARN MORE:
# - Writing good PRs: https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/
# - Code review: https://google.github.io/eng-practices/review/reviewer/
"""
        return script

    def show_learning_mode(self):
        """Interactive GitHub learning mode"""
        if self.console:
            self.console.print(Panel.fit(
                "[bold green]GitHub Learning Mode[/bold green]\n"
                "[yellow]Interactive tutorials for GitHub beginners[/yellow]",
                border_style="green"
            ))
        else:
            print("\n=== GitHub Learning Mode ===")

        lessons = {
            '1': ('Git Basics', self.teach_git_basics),
            '2': ('GitHub Workflow', self.teach_github_workflow),
            '3': ('Branching Strategy', self.teach_branching),
            '4': ('Pull Requests', self.teach_pull_requests),
            '5': ('GitHub CLI', self.teach_github_cli),
            '6': ('Common Commands', self.teach_common_commands)
        }

        print("\n📚 Available Lessons:\n")
        for key, (name, _) in lessons.items():
            print(f"{key}. {name}")
        print("7. Back to Main Menu")

        choice = input("\nSelect lesson (1-7): ")

        if choice in lessons:
            _, lesson_func = lessons[choice]
            lesson_func()

    def teach_git_basics(self):
        """Teach git basics"""
        lesson = """
# Git Basics - Understanding Version Control

## What is Git?
Git is a version control system that tracks changes to your files.
Think of it like "Track Changes" in Microsoft Word, but for code.

## Key Concepts:

### 1. Repository (repo)
A folder containing your project and its history.

### 2. Commit
A snapshot of your code at a specific point in time.
Like saving your game progress!

### 3. Remote
The version of your repository stored on GitHub.

## Basic Workflow:

```bash
# 1. Check status (what changed?)
git status

# 2. Add changes (stage them)
git add filename.txt
# or add everything:
git add .

# 3. Commit (save snapshot)
git commit -m "Describe what you changed"

# 4. Push (upload to GitHub)
git push
```

## Analogy:
- Working Directory = Your desk
- Staging Area = A box ready to ship
- Repository = The archive
- Remote = Cloud storage

## Try It:
1. Create a new file: `echo "Hello" > test.txt`
2. Check status: `git status`
3. Add it: `git add test.txt`
4. Commit: `git commit -m "Add test file"`
5. Push: `git push`

Press Enter to continue...
"""

        if self.console:
            self.console.print(Markdown(lesson))
        else:
            print(lesson)

        input()

    def teach_github_workflow(self):
        """Teach GitHub workflow"""
        lesson = """
# GitHub Workflow - The Professional Way

## Standard Workflow:

### 1. Fork or Clone
```bash
# Clone a repository
git clone https://github.com/user/repo.git
cd repo
```

### 2. Create Branch
```bash
# Never work on main!
git checkout -b feature/my-feature
```

### 3. Make Changes
Edit your files, test your code.

### 4. Commit
```bash
git add .
git commit -m "Add amazing feature"
```

### 5. Push
```bash
git push -u origin feature/my-feature
```

### 6. Create Pull Request
On GitHub:
- Go to your repository
- Click "Pull Requests"
- Click "New Pull Request"
- Fill in description
- Request reviews

### 7. Code Review
- Team reviews your code
- Make requested changes
- Push updates to same branch

### 8. Merge
After approval:
- Merge PR on GitHub
- Delete feature branch
- Update local main branch

## Why This Workflow?
- ✅ Keeps main branch stable
- ✅ Enables code review
- ✅ Documents decisions
- ✅ Easy to revert if needed

Press Enter to continue...
"""

        if self.console:
            self.console.print(Markdown(lesson))
        else:
            print(lesson)

        input()

    def teach_common_commands(self):
        """Teach common Git/GitHub commands"""
        commands = """
# Common Git & GitHub Commands - Quick Reference

## Repository Setup

```bash
# Clone a repository
git clone <url>

# Initialize new repository
git init

# Add remote
git remote add origin <url>
```

## Daily Workflow

```bash
# Check what changed
git status

# See detailed changes
git diff

# Add files
git add file.txt        # Specific file
git add .               # Everything

# Commit changes
git commit -m "Message"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## Branching

```bash
# List branches
git branch

# Create branch
git branch feature-name

# Switch branch
git checkout feature-name

# Create and switch
git checkout -b feature-name

# Delete branch
git branch -d feature-name
```

## Viewing History

```bash
# See commit history
git log

# See recent commits
git log --oneline -10

# See changes in commit
git show <commit-hash>
```

## Undoing Changes

```bash
# Discard local changes
git checkout -- file.txt

# Unstage file
git reset HEAD file.txt

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

## GitHub CLI

```bash
# Create repository
gh repo create

# List repositories
gh repo list

# Create pull request
gh pr create

# View pull requests
gh pr list

# Create issue
gh issue create

# List issues
gh issue list
```

## Helpful Aliases

Add to ~/.gitconfig:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
```

Then use: `git st` instead of `git status`

Press Enter to continue...
"""

        if self.console:
            self.console.print(Markdown(commands))
        else:
            print(commands)

        input()

    def teach_branching(self):
        """Teach branching strategy"""
        lesson = """
# Branching Strategy - Organizing Your Work

## Common Branch Types:

### 1. main/master
- Production-ready code
- Always stable
- Protected from direct commits

### 2. develop
- Latest development changes
- Integration branch
- Not always stable

### 3. feature/ branches
- New features
- Created from develop
- Example: feature/user-auth

### 4. bugfix/ or fix/ branches
- Bug fixes
- Created from develop or main
- Example: fix/login-error

### 5. hotfix/ branches
- Urgent fixes for production
- Created from main
- Merged back to both main and develop

## Git Flow Workflow:

```bash
# Start new feature
git checkout develop
git checkout -b feature/awesome-feature

# Work on feature...
git add .
git commit -m "Add feature"

# Finish feature
git checkout develop
git merge feature/awesome-feature
git branch -d feature/awesome-feature
```

## Branch Naming Tips:

✅ Good:
- feature/user-authentication
- fix/broken-link
- docs/update-readme

❌ Bad:
- mybranch
- temp
- test

## Keeping Branches Updated:

```bash
# Update feature branch from main
git checkout feature/my-feature
git merge main

# Or rebase (cleaner history)
git rebase main
```

## When to Create a Branch?

- ✅ Every new feature
- ✅ Every bug fix
- ✅ Experimental changes
- ❌ Tiny typo fixes (maybe)

Press Enter to continue...
"""

        if self.console:
            self.console.print(Markdown(lesson))
        else:
            print(lesson)

        input()

    def teach_pull_requests(self):
        """Teach about pull requests"""
        lesson = """
# Pull Requests - Code Review Done Right

## What is a Pull Request?

A pull request (PR) is a request to merge your changes into another branch.
It enables code review, discussion, and quality control.

## Creating a Good PR:

### 1. Title
Clear and descriptive:
- ✅ "Add user authentication with OAuth"
- ❌ "Update code"

### 2. Description
Include:
- What changed
- Why it changed
- How to test it
- Screenshots (if UI changes)
- Links to related issues

Example:
```markdown
## Summary
Implements user authentication using OAuth 2.0

## Changes
- Added OAuth provider integration
- Created login/logout endpoints
- Added user session management

## Testing
1. Run `npm start`
2. Click "Login" button
3. Authenticate with Google
4. Verify dashboard access

## Screenshots
[Include screenshots here]

Closes #123
```

### 3. Keep PRs Small
- One feature per PR
- Easier to review
- Faster to merge
- Less risky

### 4. Request Reviewers
Ask specific people who know the code.

### 5. Address Feedback
- Be receptive to suggestions
- Explain your decisions
- Make requested changes quickly

## PR Commands:

```bash
# Create PR (GitHub CLI)
gh pr create --title "Add feature" --body "Description"

# View PRs
gh pr list

# View specific PR
gh pr view 123

# Checkout PR locally
gh pr checkout 123

# Merge PR
gh pr merge 123

# Close without merging
gh pr close 123
```

## PR Checklist:

Before creating PR:
- [ ] Code works and is tested
- [ ] No console errors
- [ ] Comments added where needed
- [ ] Documentation updated
- [ ] Follows project style guide
- [ ] Passes CI/CD checks

## After PR is Merged:

```bash
# Update your local main branch
git checkout main
git pull

# Delete feature branch
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

Press Enter to continue...
"""

        if self.console:
            self.console.print(Markdown(lesson))
        else:
            print(lesson)

        input()

    def teach_github_cli(self):
        """Teach GitHub CLI usage"""
        lesson = """
# GitHub CLI (gh) - GitHub in Your Terminal

## What is GitHub CLI?

`gh` is an official command-line tool for GitHub.
It brings pull requests, issues, and more to your terminal.

## Installation:

### macOS
```bash
brew install gh
```

### Linux
```bash
# Debian/Ubuntu
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### Windows
Download from: https://cli.github.com/

## Authentication:

```bash
# Login to GitHub
gh auth login

# Check auth status
gh auth status
```

## Common Operations:

### Repositories
```bash
# Create repository
gh repo create my-project --public

# Clone repository
gh repo clone user/repo

# View repository
gh repo view user/repo

# List your repositories
gh repo list

# Fork repository
gh repo fork user/repo
```

### Pull Requests
```bash
# Create PR
gh pr create

# List PRs
gh pr list

# View PR
gh pr view 123

# Review PR
gh pr review 123 --approve

# Merge PR
gh pr merge 123

# Close PR
gh pr close 123
```

### Issues
```bash
# Create issue
gh issue create

# List issues
gh issue list

# View issue
gh issue view 123

# Close issue
gh issue close 123

# Reopen issue
gh issue reopen 123
```

### Releases
```bash
# Create release
gh release create v1.0.0

# List releases
gh release list

# Download release
gh release download v1.0.0
```

## Powerful Features:

### Interactive Mode
Most commands work interactively:
```bash
gh pr create  # Prompts for title, body, etc.
gh issue create  # Interactive issue creation
```

### JSON Output
Great for scripts:
```bash
gh repo list --json name,stars
gh pr list --json number,title,state
```

### Aliases
Create shortcuts:
```bash
# Set alias
gh alias set prs 'pr list --state open'

# Use it
gh prs
```

## Pro Tips:

1. **Web View**
   ```bash
   gh repo view --web  # Opens in browser
   gh pr view --web
   ```

2. **Check CI Status**
   ```bash
   gh pr checks
   ```

3. **Create from Template**
   ```bash
   gh repo create --template user/template-repo
   ```

4. **Bulk Operations**
   ```bash
   # Close all PRs from a user
   gh pr list --author username --json number --jq '.[].number' | xargs -I{} gh pr close {}
   ```

Press Enter to continue...
"""

        if self.console:
            self.console.print(Markdown(lesson))
        else:
            print(lesson)

        input()

    def save_script(self, script_content, script_type):
        """Save generated script to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"generated_{script_type}_{timestamp}.sh"

        # Create generated-scripts directory
        output_dir = Path("generated-scripts")
        output_dir.mkdir(exist_ok=True)

        filepath = output_dir / filename

        with open(filepath, 'w') as f:
            f.write(script_content)

        # Make executable (Unix/Linux/macOS only)
        if sys.platform != 'win32':
            os.chmod(filepath, 0o755)

        if self.console:
            self.console.print(f"\n[green]✅ Script saved to:[/green] {filepath}")
            self.console.print(f"[yellow]Make it executable:[/yellow] chmod +x {filepath}")
            self.console.print(f"[cyan]Run it:[/cyan] ./{filepath}")
        else:
            print(f"\n✅ Script saved to: {filepath}")
            print(f"Make it executable: chmod +x {filepath}")
            print(f"Run it: ./{filepath}")

    def run(self):
        """Main application loop"""
        while True:
            self.show_menu()
            choice = self.get_user_choice()

            if choice == len(self.templates) + 3:  # Exit
                print("\n👋 Thanks for using GitSage Script Generator!")
                break

            elif choice == len(self.templates) + 2:  # Learning Mode
                self.show_learning_mode()
                continue

            elif 1 <= choice <= len(self.templates):
                # Get template
                template_key = list(self.templates.keys())[choice - 1]
                template = self.templates[template_key]

                print(f"\n📝 Generating: {template['name']}")

                # Get configuration
                config = {}

                if template_key == 'auto-commit':
                    config['repo_path'] = input("Repository path (default: .): ") or "."
                    config['commit_message'] = input("Commit message: ") or "Auto-commit: Update files"
                    config['branch'] = input("Branch (default: main): ") or "main"
                    script = self.generate_auto_commit_script(config)

                elif template_key == 'branch-workflow':
                    config['feature_name'] = input("Feature name: ") or "new-feature"
                    config['base_branch'] = input("Base branch (default: main): ") or "main"
                    config['repo_path'] = input("Repository path (default: .): ") or "."
                    script = self.generate_branch_workflow_script(config)

                elif template_key == 'repo-sync':
                    repos_input = input("Repositories to sync (comma-separated, default: .): ")
                    config['repos'] = [r.strip() for r in repos_input.split(',')] if repos_input else ['.']
                    script = self.generate_repo_sync_script(config)

                elif template_key == 'backup-all-repos':
                    config['backup_dir'] = input("Backup directory (default: ~/github-backups): ") or "~/github-backups"
                    script = self.generate_backup_repos_script(config)

                elif template_key == 'pr-automation':
                    config['pr_title'] = input("PR title: ") or "Feature: Description"
                    config['base_branch'] = input("Base branch (default: main): ") or "main"
                    script = self.generate_pr_automation_script(config)

                else:
                    print("Template not yet implemented!")
                    continue

                # Save script
                self.save_script(script, template_key)

                # Show preview
                if self.console and Confirm.ask("\nView generated script?", default=False):
                    self.console.print(Panel(script, title="Generated Script", border_style="green"))

                input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="GitSage Script Generator - Learn GitHub while automating")
    parser.add_argument('--no-rich', action='store_true', help='Disable rich terminal output')

    args = parser.parse_args()

    if args.no_rich and RICH_AVAILABLE:
        # Disable rich
        import builtins
        builtins.rprint = print

    generator = ScriptGenerator()

    try:
        generator.run()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
