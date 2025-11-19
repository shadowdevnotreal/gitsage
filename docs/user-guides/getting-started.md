# Getting Started with GitSage

Welcome to GitSage - your ultimate GitHub repository management toolkit!

## Quick Overview

GitSage provides powerful command-line tools for:
- 🗑️ Safe repository deletion
- 📚 Automated wiki and GitBook generation
- 🔄 Git history management
- ⚙️ Advanced repository operations
- 🌍 Cross-platform compatibility

## Installation

### Step 1: Prerequisites

**Required Tools:**
```bash
# Check if you have the required tools
git --version        # Git 2.0+
gh --version         # GitHub CLI
python --version     # Python 3.8+
bash --version       # Bash shell
```

**Install Missing Tools:**

**Git:**
- Windows: https://git-scm.com/download/win
- macOS: `brew install git` or Xcode Command Line Tools
- Linux: `sudo apt install git` or `sudo yum install git`

**GitHub CLI:**
- Windows: `winget install GitHub.cli`
- macOS: `brew install gh`
- Linux: `sudo snap install gh`

**Python:**
- Windows: https://www.python.org/downloads/
- macOS: `brew install python3`
- Linux: Usually pre-installed

**Authenticate GitHub CLI:**
```bash
gh auth login
# Follow the prompts to authenticate
```

### Step 2: Clone GitSage

```bash
git clone https://github.com/shadowdevnotreal/gitsage.git
cd gitsage
```

### Step 3: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Or use pip3 on some systems
pip3 install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python check_installation.py
```

This will check all prerequisites and show what's working.

---

## Platform-Specific Setup

### Windows

**Option 1: Git Bash (Recommended)**
1. Install Git for Windows (includes Git Bash)
2. Open Git Bash
3. Run GitSage commands in Git Bash

**Option 2: WSL (Windows Subsystem for Linux)**
1. Install WSL: https://docs.microsoft.com/en-us/windows/wsl/install
2. Open WSL terminal
3. Run GitSage as on Linux

**Option 3: PowerShell**
- Coming in v2.0 (see ROADMAP.md)

### macOS

Works natively with Terminal:
```bash
# Make scripts executable
chmod +x scripts/bash/*.sh
chmod +x scripts/git-resets/*.sh

# Run directly
bash scripts/bash/repo-manager.sh
```

### Linux

Works natively with any Bash-compatible terminal:
```bash
# Make scripts executable (if needed)
chmod +x scripts/bash/*.sh
chmod +x scripts/git-resets/*.sh

# Run directly
bash scripts/bash/repo-manager.sh
```

---

## Your First Use

### Using the Launcher (Recommended for Beginners)

The easiest way to use GitSage is through the interactive launcher:

```bash
python launcher.py
```

This will:
1. Detect your environment
2. Check for required tools
3. Show you available options
4. Guide you through setup if needed

### Direct Script Usage (For Advanced Users)

```bash
# Repository deletion
bash scripts/bash/delete-repo.sh

# Repository management
bash scripts/bash/repo-manager.sh

# Wiki generation
python wiki-generator.py

# Enhanced wiki generation
python wiki-generator-enhanced.py
```

---

## Common Tasks

### 1. Delete a Repository Safely

```bash
# Launch deletion script
bash scripts/bash/delete-repo.sh

# OR use launcher
python launcher.py
# Select option 1: Repository Deletion
```

**What happens:**
1. Shows all your repositories
2. You select which to delete
3. Shows repository details
4. Asks for confirmation (multiple times)
5. Deletes remote repository
6. Deletes local copy
7. Verifies deletion

### 2. Generate GitHub Wiki

```bash
# Using basic generator
python wiki-generator.py

# Using enhanced generator (recommended)
python wiki-generator-enhanced.py
```

**Steps:**
1. Configure `wiki-config.yaml` for your project
2. Run the generator
3. Wiki files created in `generated-docs/`
4. Follow deployment instructions

### 3. Generate GitBook

```bash
# Enhanced generator creates GitBook-compatible structure
python wiki-generator-enhanced.py

# Files will be in generated-docs/ with:
# - SUMMARY.md (GitBook structure)
# - Organized chapters
# - Ready for GitBook deployment
```

### 4. Reset Git History

```bash
# Complete history reset (keeps files)
bash scripts/git-resets/reset_git_history.sh

# This will:
# - Create a backup branch
# - Create orphan branch
# - Add all current files
# - Create new initial commit
# - Force push to remote
```

⚠️ **Warning**: This permanently deletes all commit history!

### 5. Manage Multiple Repositories

```bash
# Advanced repository management
bash scripts/bash/repo-manager.sh

# Features:
# - Batch operations
# - Sync multiple repos
# - Clone with specific settings
# - Repository templates
```

---

## Skill Level Guide

### 👶 Novice (New to Command Line)

**Start Here:**
1. Install prerequisites using graphical installers
2. Use `python launcher.py` (interactive menu)
3. Follow on-screen prompts carefully
4. Read all confirmations before proceeding

**Recommended First Task:**
- Use wiki generator to create documentation (non-destructive)

**Resources:**
- This guide
- In-app help messages
- Safety confirmations guide you

### 🧑‍💻 Intermediate (Comfortable with Terminal)

**Start Here:**
1. Use direct script commands
2. Customize `wiki-config.yaml`
3. Understand Bash script options

**Recommended Tasks:**
- Generate wikis and GitBooks
- Use repository management features
- Explore git history tools

**Resources:**
- Script help: `bash scripts/bash/repo-manager.sh --help`
- Wiki generator guide: WIKI-GENERATOR-README.md
- Deletion guide: DEL-README.md

### 🚀 Expert (Command Line Pro)

**Start Here:**
1. Review source code for customization
2. Chain commands for automation
3. Integrate into your workflows

**Recommended Tasks:**
- Automate with cron jobs or GitHub Actions
- Customize scripts for your needs
- Contribute improvements

**Resources:**
- CONTRIBUTING.md
- ROADMAP.md
- Source code in scripts/

---

## Configuration

### Wiki Generator Configuration

Edit `wiki-config.yaml`:

```yaml
project:
  name: "Your Project Name"
  description: "Project description"
  version: "1.0.0"
  author: "Your Name"
  github_url: "https://github.com/user/repo"

wiki:
  sidebar: true
  search: true
  auto_nav: true

content:
  sections:
    - title: "Getting Started"
      pages:
        - "Home"
        - "Installation"
    - title: "User Guide"
      pages:
        - "Features"
        - "Examples"
```

### Environment Variables (Optional)

```bash
# Set default GitHub user
export GITHUB_USER="your-username"

# Set default branch
export DEFAULT_BRANCH="main"
```

---

## Troubleshooting

### "Command not found: python"

Try `python3` instead:
```bash
python3 launcher.py
python3 check_installation.py
```

### "Permission denied" on scripts

Make them executable:
```bash
chmod +x scripts/bash/*.sh
chmod +x scripts/git-resets/*.sh
```

### GitHub CLI not authenticated

```bash
gh auth login
# Follow the authentication flow
```

### "Bash command not found" (Windows)

You need Git Bash:
1. Install Git for Windows: https://git-scm.com/download/win
2. Open "Git Bash" from Start Menu
3. Run commands in Git Bash

### Wiki generator fails

Check dependencies:
```bash
pip install PyYAML rich
# or
pip3 install PyYAML rich
```

### Can't delete repository - "not found"

Make sure:
1. Repository exists on GitHub
2. You're authenticated with `gh auth status`
3. You have correct permissions
4. Repository name is spelled correctly

---

## Advanced Usage

### Batch Operations

```bash
# Delete multiple repositories (carefully!)
# The script will ask for each one
bash scripts/bash/delete-repo.sh
```

### Automation

**Example: Automated Wiki Updates**

```bash
#!/bin/bash
# auto-update-wiki.sh

cd /path/to/your/project
python /path/to/gitsage/wiki-generator-enhanced.py
cd generated-docs
git add .
git commit -m "Auto-update wiki"
git push
```

**Example: Scheduled History Cleanup**

```bash
# Use with caution! Set up with cron
0 0 1 * * cd /path/to/repo && /path/to/gitsage/scripts/git-resets/reset_git_history.sh
```

### Integration with Other Tools

**GitHub Actions Example:**

```yaml
name: Generate Wiki
on:
  push:
    branches: [main]

jobs:
  wiki:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install PyYAML rich
      - name: Generate wiki
        run: python wiki-generator-enhanced.py
      - name: Deploy wiki
        run: |
          cd generated-docs
          # Deploy to wiki
```

---

## Best Practices

### Safety
- ✅ Always review what will be deleted before confirming
- ✅ Test on non-critical repositories first
- ✅ Keep backups of important data
- ✅ Read all prompts carefully
- ✅ Understand the operations before running them

### Efficiency
- ✅ Use launcher for guided workflows
- ✅ Use direct scripts when you know what you want
- ✅ Configure wiki-config.yaml for your needs
- ✅ Set up shell aliases for frequent commands

### Organization
- ✅ Keep GitSage in a dedicated directory
- ✅ Update regularly: `git pull`
- ✅ Track your own customizations separately
- ✅ Use version control for your configs

---

## Next Steps

**After Getting Started:**

1. **Read specific guides:**
   - Repository Deletion: `DEL-README.md`
   - Wiki Generation: `WIKI-GENERATOR-README.md`
   - Contributing: `CONTRIBUTING.md`

2. **Explore features:**
   - Try each tool on test repositories
   - Generate wikis for your projects
   - Experiment with git history tools (carefully!)

3. **Customize:**
   - Adjust wiki-config.yaml for your projects
   - Create shell aliases for frequent tasks
   - Set up automation if needed

4. **Contribute:**
   - Report bugs: https://github.com/shadowdevnotreal/gitsage/issues
   - Suggest features
   - Improve documentation
   - Submit pull requests

---

## Getting Help

**Resources:**
- 📖 Documentation in `docs/` directory
- 🐛 Issues: https://github.com/shadowdevnotreal/gitsage/issues
- 💬 Discussions: https://github.com/shadowdevnotreal/gitsage/discussions
- 📋 README: Main project overview
- 🗺️ ROADMAP: Future plans

**Common Questions:**

**Q: Is GitSage safe to use?**
A: Yes! GitSage has multiple safety confirmations for destructive operations. It shows you exactly what will happen before doing it.

**Q: Can I use this on Windows?**
A: Yes! Install Git for Windows (includes Git Bash) and run commands in Git Bash.

**Q: Do I need to know programming?**
A: No! The launcher provides an interactive menu. Just follow the prompts.

**Q: Can I recover deleted repositories?**
A: No. Repository deletion is permanent. Always backup important data first.

**Q: Does this work with private repositories?**
A: Yes! As long as you're authenticated with `gh auth login`.

**Q: Can I customize the wiki templates?**
A: Yes! Edit wiki-config.yaml and templates in the generator scripts.

---

**Welcome to GitSage! You're ready to start managing your GitHub repositories like a pro.** 🚀

For your next steps, try running:
```bash
python launcher.py
```

Happy coding!
