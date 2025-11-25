# GitSage v2.2 🚀

<img width="1024" height="1024" alt="gitsage" src="https://github.com/user-attachments/assets/84d13255-acc0-46e9-b014-7f033edac85f" />

> The Ultimate GitHub Management & Learning Platform - Automate your workflow while mastering GitHub from novice to expert!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#platform-support)

## 🎯 What GitSage Does

GitSage is your **all-in-one GitHub companion** that combines powerful automation with interactive learning!

### 🌟 Core Capabilities:

1. **📚 Script Generator & GitHub Learning** - Generate custom automation scripts while learning GitHub concepts interactively
2. **🗑️ Safe Repository Deletion** - Multiple safety confirmations, backups, and verification
3. **🔧 Repository Management** - Advanced Git/GitHub operations made simple
4. **📖 Wiki & GitBook Generation** - Professional documentation in minutes
5. **📝 README Generator** - Awesome READMEs with shields.io badges and templates
6. **🔄 Git History Tools** - Reset, migrate, and manage repository history safely

### 🎓 Perfect For:

- **Beginners**: Learn GitHub with interactive tutorials and educational script generation
- **Developers**: Automate repetitive tasks and manage repositories efficiently
- **Teams**: Consistent workflows with safe, documented operations
- **Everyone**: From your first commit to advanced Git workflows

## ✨ Features

### 🆕 What's New in v2.2

**🎓 Advanced Learning Content** - THREE COMPREHENSIVE GUIDES!

GitSage v2.2 takes your GitHub education to the next level with production-ready, expert-level learning modules:

**📚 Advanced Git Workflows** (`docs/learning/advanced-git-workflows.md`)
- Master interactive rebase for cleaner history
- Learn cherry-pick for selective commits and backporting
- Debug with git bisect using binary search
- 4 real-world scenarios with complete examples
- Practice exercises and quick reference guides

**⚙️ GitHub Actions Deep-Dive** (`docs/learning/github-actions-tutorial.md`)
- Complete CI/CD pipeline tutorials
- Workflow syntax and advanced patterns
- Secrets management and security best practices
- Matrix strategies and optimization techniques
- 6 common use cases with production-ready examples
- Troubleshooting guide and best practices

**🌟 Open Source Contribution Guide** (`docs/learning/open-source-contribution.md`)
- Find beginner-friendly projects to contribute to
- Master the complete forking workflow
- Create pull requests that get merged
- Navigate code review with confidence
- Build your reputation in open source
- Avoid common mistakes with proven strategies

**Each guide includes:**
- Step-by-step tutorials with code examples
- Practice exercises for hands-on learning
- Real-world scenarios from production workflows
- Quick reference sections for daily use
- Best practices and common pitfalls

<details>
<summary><b>📦 Previous Releases (click to expand)</b></summary>

### 🆕 What's New in v2.1

**💾 Automated Backup System** - IMPLEMENTED!
- Create backups before destructive operations
- Compress repositories to tar.gz with SHA256 verification
- List, restore, and manage all backups
- Automatic cleanup of old backups
- Accessible via `gitsage backup` command

**📜 Enhanced Documentation Templates** - ADDED!
- API Documentation template
- Mobile App template (iOS/Android)
- DevOps/Infrastructure template
- Machine Learning template
- Located in `templates/readme/` for easy customization

### 🎉 What's New in v2.0

**🎓 Script Generator & GitHub Learning System** - THE GAME CHANGER!
- Generate custom automation scripts for common GitHub tasks
- Interactive learning mode teaches Git/GitHub concepts
- Educational comments in every generated script
- 8+ script templates (auto-commit, branching, PR automation, backups, and more)
- Perfect for beginners learning GitHub through hands-on practice

**📚 Complete Beginner's Guide** - [GITHUB-FOR-BEGINNERS.md](GITHUB-FOR-BEGINNERS.md)
- Friendly, jargon-free GitHub tutorial
- Step-by-step examples
- Common troubleshooting solutions
- Practice exercises included

</details>

<details>
<summary><b>📋 Complete Feature List (click to expand)</b></summary>

### Current Features (v2.2)

✅ **Interactive Repository Deletion**
- Multiple safety confirmations before any destructive action
- Shows repository details before deletion
- Handles both local and remote cleanup
- Verifies successful deletion

✅ **Repository Manager**
- Advanced Git operations via Bash scripts
- GitHub CLI integration
- Cross-platform compatible (requires Bash)

✅ **Wiki Generator**
- Basic wiki generation from templates
- Enhanced version with additional customization
- YAML configuration for project details
- Automated page structure creation
- GitBook and GitHub Wiki support
- Multiple output formats

✅ **README Generator**
- Generate awesome READMEs with shields.io badges
- Multiple templates (CLI tool, library, web app, data science, game)
- Auto-generated table of contents
- Professional formatting with features, installation, usage sections
- YAML-based configuration

✅ **Git History Tools**
- Reset git history while keeping all files
- Migrate repositories between accounts/organizations
- Sync and swap repositories
- Safe operations with multiple confirmations

✅ **Automated Backup System**
- Create compressed backups (.tar.gz) of repositories
- SHA256 checksums for integrity verification
- List all backups with metadata
- Restore backups to any location
- Automatic cleanup of old backups
- Stores backups in `~/.gitsage/backups/`

✅ **Enhanced Templates**
- 4 new professional README templates
- API Documentation template
- Mobile App template
- DevOps/Infrastructure template
- Machine Learning template

✅ **Cross-Platform Launcher**
- Python-based environment detection
- Automatic tool availability checking
- Guided setup assistance
- Unified CLI wrapper for all tools

✅ **Test Suite**
- Comprehensive unit tests for all generators
- Integration tests for component verification
- 29+ automated tests ensuring reliability

</details>

### 🔮 Coming Soon (v2.3+)

**Planned Enhancements:**

📜 **Additional Script Templates**
- Automated testing workflows
- Deployment automation
- Repository analytics and reporting
- Bulk repository operations
- Team workspace setup

🔧 **Enhanced Automation**
- Watch mode for auto-commit on file changes
- Scheduled script execution
- Custom template creation
- Workflow builder (visual scripting)

🌐 **Better Integration**
- GitLab and Bitbucket support
- Jira/Linear issue integration
- Slack/Discord notifications
- VS Code extension

See [ROADMAP.md](ROADMAP.md) for detailed planning and timelines.

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Git 2.0+
- GitHub CLI (gh) authenticated
- Python 3.8+ (for launcher and wiki generator)
- Bash shell (for core scripts)

# Optional
- PyYAML (for wiki generator)
- Rich (for enhanced terminal output)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/shadowdevnotreal/gitsage.git
cd gitsage

# Install Python dependencies (optional but recommended)
pip install -r requirements.txt

# Run installation check
python check_installation.py

# Launch main menu
python launcher.py
```

## 📋 Available Tools

### Core Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| `launcher.py` | Main menu with environment detection | Root |
| `script-generator.py` | Generate scripts & learn GitHub | Root |
| `backup-manager.py` | Automated repository backups | Root |
| `delete-repo.sh` | Interactive repository deletion | `scripts/bash/` |
| `repo-manager.sh` | Advanced repository management | `scripts/bash/` |
| `wiki-generator.py` | Basic wiki generation | Root |
| `wiki-generator-enhanced.py` | Enhanced wiki with templates | Root |
| `readme-generator.py` | Awesome README with badges | Root |
| `check_installation.py` | Verify installation | Root |

### Git Reset Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| `reset_git_history.sh` | Complete history reset | `scripts/git-resets/` |
| `migrate_and_swap_repos.sh` | Repository migration | `scripts/git-resets/` |
| `migrate_sync_swap.sh` | Sync and swap repos | `scripts/git-resets/` |

## 🎮 Usage Examples

### Using the CLI Wrapper (Easiest)

```bash
# Make wrapper available (one time setup)
chmod +x gitsage
# Optional: Add to PATH or create alias

# Launch interactive menu
./gitsage launch

# Generate wiki
./gitsage wiki

# Generate awesome README with badges
./gitsage readme

# Generate custom scripts & learn GitHub
./gitsage script

# Manage backups (create, restore, list)
./gitsage backup list

# Safe repository deletion
./gitsage delete

# Repository management
./gitsage manage

# Reset git history (keep files)
./gitsage reset-history

# Migrate repository
./gitsage migrate

# Check installation
./gitsage check

# Show all commands
./gitsage help
```

**Windows users:**
```cmd
REM Use the batch wrapper
gitsage.bat launch
gitsage.bat wiki
gitsage.bat readme
gitsage.bat script
gitsage.bat check
```

### Using the Launcher Directly

```bash
# Launch interactive menu
python launcher.py

# The launcher will:
# 1. Detect your environment
# 2. Check for required tools
# 3. Provide options for all available features
# 4. Guide you through setup if needed
```

### Direct Script Usage

```bash
# Safe repository deletion
bash scripts/bash/delete-repo.sh

# Repository management
bash scripts/bash/repo-manager.sh

# Generate GitHub Wiki
python wiki-generator.py

# Enhanced wiki generation
python wiki-generator-enhanced.py
```

### Wiki Generation

```bash
# 1. Configure your project
edit wiki-config.yaml

# 2. Generate wiki
python wiki-generator-enhanced.py

# 3. Deploy to GitHub (follow generated instructions)
# Wiki files will be in generated-docs/ directory
```

### README Generation

```bash
# 1. Configure your project (optional, uses defaults if not provided)
edit readme-config.yaml

# 2. Generate README with badges and professional formatting
python readme-generator.py

# 3. Generated README.md will include:
#    - shields.io badges for license, version, build, etc.
#    - Table of contents
#    - Features, installation, usage sections
#    - Professional formatting based on template type
```

### Script Generation & Learning (NEW in v2.0!)

```bash
# Launch the interactive script generator
python script-generator.py
# or
./gitsage script

# Choose from 8+ templates:
# 1. Auto-Commit & Push - Learn git workflow
# 2. Feature Branch Workflow - Learn branching
# 3. Repository Sync - Learn git pull/fetch
# 4. Backup All Repos - Learn gh CLI
# 5. PR Automation - Learn pull requests
# 6. Issue Management - Learn project management
# 7. Release Automation - Learn versioning
# 8. CI/CD Setup - Learn GitHub Actions

# Every generated script includes:
#   - Educational comments explaining each step
#   - Best practices and tips
#   - Links to learn more
#   - Ready-to-use automation

# Learning Mode:
# Select option for GitHub Learning Mode
# Interactive tutorials on:
#   - Git basics
#   - GitHub workflow
#   - Branching strategies
#   - Pull requests
#   - GitHub CLI
#   - Common commands

# Generated scripts saved to:
# generated-scripts/
```

**Example Generated Script:**
```bash
#!/usr/bin/env bash
# Auto-Commit Script - Generated by GitSage
#
# EDUCATIONAL NOTES:
# This script automates the git commit and push workflow.
#
# Basic Git Workflow:
# 1. git add    - Stage changes for commit
# 2. git commit - Save changes to local repository
# 3. git push   - Upload changes to remote (GitHub)

# ... (script continues with educational comments)
```

### Backup Management (NEW in v2.1!)

```bash
# Create a backup of a repository
./gitsage backup create /path/to/repo --name "myorg/myrepo" --operation "before-deletion"
# or
python backup-manager.py create /path/to/repo --name "myorg/myrepo"

# List all backups
./gitsage backup list
# Filter by repository
./gitsage backup list --repo "myorg/myrepo"

# Restore a backup
./gitsage backup restore backup_id_12345
# Restore to specific location
./gitsage backup restore backup_id_12345 --path /path/to/restore

# Delete a backup
./gitsage backup delete backup_id_12345

# Clean up old backups (keep last 30 days, minimum 10 per repo)
./gitsage backup cleanup --days 30 --keep 10
```

**Backup Features:**
- Automatic compression (tar.gz format)
- SHA256 integrity verification
- Metadata tracking (repo name, operation type, timestamp)
- Stored in `~/.gitsage/backups/`
- Easy restore to original or new location

### Git History Management

```bash
# Reset git history (keeps all files, fresh start)
bash scripts/git-resets/reset_git_history.sh

# Migrate repository to new location
bash scripts/git-resets/migrate_and_swap_repos.sh

# Note: These operations are irreversible - use with caution!
```

## 🛡️ Safety Features

- **Multiple confirmations** for all destructive operations
- **Validation checks** before executing actions
- **Clear status messages** at each step
- **Error handling** with helpful messages
- **No silent failures** - you'll always know what happened

## 🌍 Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| **Linux** | ✅ Fully Supported | Native Bash environment |
| **macOS** | ✅ Fully Supported | Native Bash environment |
| **Windows** | ⚠️ Partial | Requires Git Bash or WSL |
| **WSL** | ✅ Fully Supported | Linux environment on Windows |

**Windows Users**: Install [Git for Windows](https://git-scm.com/download/win) which includes Git Bash, then run scripts via Git Bash.

## 📖 Documentation

### 🎓 Learning Resources (NEW in v2.2!)

**Master Git & GitHub - From Beginner to Expert:**
- **[GitHub for Beginners](GITHUB-FOR-BEGINNERS.md)** - Friendly, jargon-free introduction to GitHub
- **[Advanced Git Workflows](docs/learning/advanced-git-workflows.md)** - Rebase, cherry-pick, bisect mastery
- **[GitHub Actions Deep-Dive](docs/learning/github-actions-tutorial.md)** - Complete CI/CD pipeline guide
- **[Open Source Contribution Guide](docs/learning/open-source-contribution.md)** - Contributing to open source successfully

**Interactive Learning:**
- Run `./gitsage script` and choose "GitHub Learning Mode"
- 6 interactive lessons covering Git basics, branching, PRs, and more
- Learn by generating real automation scripts with educational comments

### Quick References
- **[Quick Reference](QUICK-REFERENCE.md)** - Fast command lookup for daily tasks
- **[Quick Start Guide](docs/user-guides/getting-started.md)** - Complete beginner to expert guide

### Comprehensive Guides
- **[Wiki & GitBook Guide](docs/user-guides/wiki-gitbook-guide.md)** - Create professional documentation
- **[Repository Management Guide](docs/user-guides/repository-management.md)** - Complete GitHub management
- **[Repository Deletion Guide](DEL-README.md)** - Safe deletion walkthrough
- **[Wiki Generator Guide](WIKI-GENERATOR-README.md)** - Documentation automation

### Project Information
- **[Contributing Guide](CONTRIBUTING.md)** - Help improve GitSage
- **[Changelog](CHANGELOG.md)** - Version history
- **[Roadmap](ROADMAP.md)** - Planned features
- **[Security Policy](SECURITY.md)** - Security and responsible disclosure
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community standards

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- How to submit pull requests
- Areas needing help

Quick contribution ideas:
- Report bugs or request features via [Issues](../../issues)
- Improve documentation
- Add more wiki templates
- Test on different platforms

## ⚠️ Important Safety Notes

**This tool can permanently delete repositories. Please understand:**

- Repository deletion is **permanent** and **cannot be undone**
- Deleted repositories cannot be recovered (even by GitHub support)
- Always backup important work before deletion
- Test on non-critical repositories first
- Read all prompts carefully before confirming

**Git history reset operations:**
- History reset is **irreversible**
- All commit history will be permanently lost
- Creates a new initial commit
- Requires force push to update remote

## 🔧 Troubleshooting

### Common Issues

**"GitHub CLI not installed"**
```bash
# Install GitHub CLI
# Visit: https://cli.github.com/

# Authenticate after installation
gh auth login
```

**"Bash command not found" (Windows)**
```bash
# Install Git for Windows (includes Git Bash)
# Visit: https://git-scm.com/download/win

# Then run scripts using Git Bash
```

**"Permission denied" when running scripts**
```bash
# Make scripts executable
chmod +x scripts/bash/*.sh
chmod +x scripts/git-resets/*.sh
```

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

You are free to use, modify, and distribute this software with attribution.

## 🙏 Acknowledgments

- **GitHub CLI Team** - Excellent command-line tool for GitHub operations
- **Git Community** - Powerful version control system
- **Open Source Contributors** - Everyone who helps improve this project

## 📊 Project Status

**Current Version**: 2.2.0 🎉
**Status**: Production Ready & Educational Powerhouse
**Last Updated**: November 2025
**Test Coverage**: 29+ automated tests
**New in v2.2**: Advanced Learning Content (Git, Actions, Open Source)!

GitSage v2.2 completes the educational transformation with expert-level content:
- 🆕 **Advanced Git workflows guide** (rebase, cherry-pick, bisect)
- 🆕 **GitHub Actions deep-dive** (CI/CD, secrets, optimization)
- 🆕 **Open source contribution guide** (forking, PRs, reputation building)
- 💾 **Automated backup system** (create, restore, manage backups)
- 📝 **Enhanced README templates** (API, Mobile, DevOps, ML)
- 🎓 **Script generator** (8+ templates, educational mode)
- 📚 **Complete beginner's guide** (GITHUB-FOR-BEGINNERS.md)
- 🎓 **Interactive GitHub learning** (6 comprehensive lessons)
- ✅ Repository deletion (production ready, fully tested)
- ✅ Repository management (production ready, fully tested)
- ✅ Wiki generation (production ready, multiple formats)
- ✅ README generation (production ready, with badges & templates)
- ✅ Git history tools (production ready, safe operations)
- ✅ Comprehensive test suite (29+ tests passing)
- ✅ Cross-platform CLI wrapper (Linux, macOS, Windows)

For planned enhancements, see [ROADMAP.md](ROADMAP.md).

## 💬 Support

- **Report Issues**: [GitHub Issues](../../issues)
- **Ask Questions**: Create an issue with the "question" label
- **Feature Requests**: Create an issue with the "enhancement" label

---

**Made for developers who value safety and automation in GitHub repository management.**

If GitSage helps you, please ⭐ star the repository!
