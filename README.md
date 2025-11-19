# GitSage v1.0

![GitSage Logo](assets/logos/GitSage.png)

> A focused toolkit for GitHub repository deletion, management, and automated wiki generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#platform-support)

## 🎯 What GitSage Does

GitSage provides three core capabilities:

1. **Safe Repository Deletion** - Interactive Bash script with multiple safety confirmations
2. **Repository Management** - Advanced Bash tools for Git/GitHub operations
3. **Wiki Generation** - Automated GitHub Wiki creation from templates

## ✨ Features

### Current Features (v1.0)

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

✅ **Cross-Platform Launcher**
- Python-based environment detection
- Automatic tool availability checking
- Guided setup assistance

### Planned Features (v2.0)

See [ROADMAP.md](ROADMAP.md) for upcoming features including:
- Python CLI versions
- GUI interface
- PowerShell native support
- Automated backups
- Comprehensive test suite

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
| `delete-repo.sh` | Interactive repository deletion | `scripts/bash/` |
| `repo-manager.sh` | Advanced repository management | `scripts/bash/` |
| `wiki-generator.py` | Basic wiki generation | Root |
| `wiki-generator-enhanced.py` | Enhanced wiki with templates | Root |
| `check_installation.py` | Verify installation | Root |

### Git Reset Scripts

| Script | Purpose | Location |
|--------|---------|----------|
| `reset_git_history.sh` | Complete history reset | `scripts/git-resets/` |
| `migrate_and_swap_repos.sh` | Repository migration | `scripts/git-resets/` |
| `migrate_sync_swap.sh` | Sync and swap repos | `scripts/git-resets/` |

## 🎮 Usage Examples

### Using the Launcher (Recommended)

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

- [Quick Start Guide](docs/user-guides/getting-started.md) - Get up and running
- [Repository Deletion Guide](DEL-README.md) - Safe deletion walkthrough
- [Wiki Generator Guide](WIKI-GENERATOR-README.md) - Documentation automation
- [Contributing Guide](CONTRIBUTING.md) - Help improve GitSage
- [Changelog](CHANGELOG.md) - Version history
- [Roadmap](ROADMAP.md) - Planned features

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

**Current Version**: 1.0.0
**Status**: Stable
**Last Updated**: November 2025

GitSage v1.0 is a focused, stable release with core functionality:
- ✅ Repository deletion (production ready)
- ✅ Repository management (production ready)
- ✅ Wiki generation (production ready)

For planned enhancements, see [ROADMAP.md](ROADMAP.md).

## 💬 Support

- **Report Issues**: [GitHub Issues](../../issues)
- **Ask Questions**: Create an issue with the "question" label
- **Feature Requests**: Create an issue with the "enhancement" label

---

**Made for developers who value safety and automation in GitHub repository management.**

If GitSage helps you, please ⭐ star the repository!
