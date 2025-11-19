# GitSage Quick Reference

Fast command reference for daily GitHub management tasks.

## 🚀 Quick Start

```bash
# Launch interactive menu (easiest)
python launcher.py

# Check installation
python check_installation.py
```

## 📚 Documentation Generation

```bash
# Generate wiki (recommended)
python wiki-generator-enhanced.py

# Generate basic wiki
python wiki-generator.py

# Configure first
edit wiki-config.yaml
```

## 🗑️ Repository Deletion

```bash
# Interactive safe deletion
bash scripts/bash/delete-repo.sh

# What it does:
# 1. Lists your repositories
# 2. Shows details
# 3. Multiple confirmations
# 4. Deletes remote + local
# 5. Verifies success
```

## 🔧 Repository Management

```bash
# Advanced management tools
bash scripts/bash/repo-manager.sh

# Quick operations with gh CLI
gh repo view user/repo          # View details
gh repo clone user/repo         # Clone
gh repo create new-repo         # Create
gh repo delete user/repo        # Delete (use script instead!)
gh repo fork user/repo          # Fork
gh repo list                    # List your repos
```

## 🔄 Git History Operations

```bash
# Reset history (keep files)
bash scripts/git-resets/reset_git_history.sh

# Migrate repository
bash scripts/git-resets/migrate_and_swap_repos.sh

# Sync and swap
bash scripts/git-resets/migrate_sync_swap.sh
```

## 🛠️ Common Tasks

### Clone Repository
```bash
gh repo clone user/repo
# or
git clone https://github.com/user/repo.git
```

### Create Repository
```bash
gh repo create my-project --public
cd my-project
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"
git push -u origin main
```

### Create Wiki for Your Project
```bash
# 1. Configure
cat > wiki-config.yaml << EOF
project:
  name: "My Project"
  description: "My awesome project"
  github_url: "https://github.com/user/my-project"
content:
  sections:
    - title: "Guide"
      pages: ["Home", "Installation", "Usage"]
EOF

# 2. Generate
python wiki-generator-enhanced.py

# 3. Deploy
cd generated-docs/deployment
./deploy-wiki.sh https://github.com/user/my-project.git
```

### Delete Repository Safely
```bash
bash scripts/bash/delete-repo.sh
# Follow prompts carefully
# Type repository name to confirm
```

### Reset Git History
```bash
cd your-repo
bash /path/to/gitsage/scripts/git-resets/reset_git_history.sh
# Creates backup branch
# Resets to single initial commit
# Keeps all current files
```

## 🔍 Information Commands

```bash
# View repository info
gh repo view user/repo

# List your repositories
gh repo list

# View with specific details
gh repo view user/repo --json name,description,stars,forks

# Repository statistics
gh api repos/user/repo | jq '{name, stars: .stargazers_count, forks: .forks_count}'
```

## 🌿 Branch Operations

```bash
# List branches
gh api repos/user/repo/branches

# Create branch
git checkout -b new-feature
git push -u origin new-feature

# Delete branch locally
git branch -d branch-name

# Delete branch remotely
git push origin --delete branch-name
```

## 📦 Release Management

```bash
# List releases
gh release list

# Create release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"

# Download release
gh release download v1.0.0

# View release
gh release view v1.0.0
```

## 🐛 Issues

```bash
# List issues
gh issue list

# Create issue
gh issue create --title "Bug report" --body "Description"

# View issue
gh issue view 123

# Close issue
gh issue close 123
```

## 🔀 Pull Requests

```bash
# List PRs
gh pr list

# Create PR
gh pr create --title "Add feature" --body "Description"

# View PR
gh pr view 123

# Merge PR
gh pr merge 123

# Checkout PR locally
gh pr checkout 123
```

## ⚙️ Repository Settings

```bash
# Change visibility
gh repo edit user/repo --visibility public
gh repo edit user/repo --visibility private

# Enable/disable features
gh repo edit user/repo --enable-wiki
gh repo edit user/repo --enable-issues
gh repo edit user/repo --enable-projects

# Archive repository
gh repo archive user/repo

# Unarchive
gh repo unarchive user/repo
```

## 🔐 Security

```bash
# Check authentication
gh auth status

# Login/refresh
gh auth login

# View permissions
gh repo view user/repo --json permissions
```

## 📊 Statistics

```bash
# Stars and forks
gh repo view user/repo --json stargazerCount,forkCount

# Contributors
gh api repos/user/repo/contributors | jq '.[].login'

# Languages
gh repo view user/repo --json languages

# Recent activity
gh repo view user/repo --json pushedAt,updatedAt
```

## 🔧 GitSage Configuration

### Wiki Generator Config

```yaml
# wiki-config.yaml
project:
  name: "Project Name"
  description: "Description"
  version: "1.0.0"
  github_url: "https://github.com/user/repo"

content:
  sections:
    - title: "Section"
      pages: ["Page1", "Page2"]
```

### Environment Variables

```bash
# Optional: Set defaults
export GITHUB_USER="your-username"
export GITHUB_TOKEN="your-token"  # For API access
export DEFAULT_BRANCH="main"
```

## 🚨 Emergency Commands

### Undo Last Commit (Not Pushed)
```bash
git reset --soft HEAD~1  # Keep changes
git reset --hard HEAD~1  # Discard changes
```

### Undo Force Push (If Immediately Caught)
```bash
git reflog
git reset --hard HEAD@{1}
git push origin main --force
```

### Recover Deleted Branch (Not Garbage Collected)
```bash
git reflog
git checkout -b recovered-branch <commit-hash>
```

### Stop Accidental Force Push
```bash
# Enable push protection
git config --global receive.denyNonFastForwards true
```

## 💡 Pro Tips

### Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias gs='python /path/to/gitsage/launcher.py'
alias gswiki='python /path/to/gitsage/wiki-generator-enhanced.py'
alias ghv='gh repo view'
alias ghc='gh repo clone'
alias ghl='gh repo list'
```

### Git Aliases

```bash
# Add to ~/.gitconfig
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --graph --oneline --all
```

### Batch Operations

```bash
# Clone multiple repos
repos=(repo1 repo2 repo3)
for repo in "${repos[@]}"; do gh repo clone user/$repo; done

# Update all local repos
find . -name .git -type d -prune | while read d; do
    cd "$d/.." && echo "Updating $(basename $(pwd))" && git pull
done
```

## 📱 Platform-Specific

### Windows (Git Bash)
```bash
# Use Git Bash for all commands
# Launch: Start Menu > Git Bash

# Python might be 'python' or 'python3'
python launcher.py
# or
python3 launcher.py
```

### macOS
```bash
# Use Terminal.app or iTerm2
# Python is usually 'python3'
python3 launcher.py

# Make scripts executable
chmod +x scripts/bash/*.sh
```

### Linux
```bash
# Use any terminal
# Python might be 'python' or 'python3'
python launcher.py

# Ensure Bash is available
which bash
```

## 🆘 Troubleshooting

### Command Not Found
```bash
# Check if tools are installed
which git
which gh
which python

# Install missing tools (see getting-started.md)
```

### Permission Denied
```bash
# Make scripts executable
chmod +x scripts/bash/*.sh
chmod +x scripts/git-resets/*.sh

# Check file permissions
ls -la scripts/bash/
```

### GitHub CLI Not Authenticated
```bash
gh auth status
gh auth login
# Follow prompts
```

### Python ModuleNotFoundError
```bash
# Install dependencies
pip install -r requirements.txt
# or
pip3 install -r requirements.txt
```

## 📚 Documentation

**Full Guides:**
- Getting Started: `docs/user-guides/getting-started.md`
- Wiki/GitBook: `docs/user-guides/wiki-gitbook-guide.md`
- Repository Management: `docs/user-guides/repository-management.md`

**Project Info:**
- README: Main project overview
- ROADMAP: Future plans
- CHANGELOG: Version history
- CONTRIBUTING: How to help

## 🔗 Quick Links

- GitHub CLI Manual: https://cli.github.com/manual/
- Git Documentation: https://git-scm.com/doc
- GitBook Docs: https://docs.gitbook.com/
- GitSage Issues: https://github.com/shadowdevnotreal/gitsage/issues

---

**Keep this reference handy for quick command lookup!** 📖

For detailed explanations, see the full documentation in `docs/user-guides/`.
