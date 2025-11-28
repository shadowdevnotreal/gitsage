# GitSage v2.3 🚀

<img width="1024" height="1024" alt="gitsage" src="https://github.com/user-attachments/assets/84d13255-acc0-46e9-b014-7f033edac85f" />

> The Ultimate GitHub Management & Learning Platform - Automate your workflow while mastering GitHub from novice to expert!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#platform-support)

## 🎯 What GitSage Does

GitSage is your **all-in-one GitHub companion** that combines powerful automation with interactive learning!

### 🌟 Core Capabilities:

1. **🌐 Web Interface** - Modern browser-based UI with real-time monitoring
2. **📚 Script Generator & GitHub Learning** - Generate custom automation scripts while learning GitHub concepts
3. **💾 Automated Backup System** - SHA256-verified backups with easy restoration
4. **🗑️ Safe Repository Deletion** - Multiple safety confirmations and verification
5. **🔧 Repository Management** - Unified migration tools and advanced Git operations
6. **📖 Wiki & GitBook Generation** - Professional documentation in minutes
7. **📝 README Generator** - Awesome READMEs with shields.io badges and templates
8. **🔄 Git History Tools** - Reset, migrate, and manage repository history safely

### 🎓 Perfect For:

- **Beginners**: Learn GitHub with interactive tutorials and educational script generation
- **Developers**: Automate repetitive tasks and manage repositories efficiently
- **Teams**: Consistent workflows with safe, documented operations
- **Everyone**: From your first commit to advanced Git workflows

## ✨ What's New in v2.3

**🚀 Universal Launchers & Installers**
- ONE universal installer for all platforms (install.sh, install.ps1)
- ONE universal launcher for all platforms (launch.sh, Launch-GitSage.ps1, launcher.py)
- Cross-platform parity: Python, PowerShell, Bash
- Post-install launch prompts on all platforms
- Two tools: CLI Interface and Web Interface

**📁 Native OS File Picker Dialogs**
- No tkinter needed - uses native OS dialogs!
- Windows: PowerShell FolderBrowserDialog
- macOS: AppleScript choose folder
- Linux: zenity/kdialog/yad
- Click to browse instead of typing paths
- Perfect for novice and pro users alike

**🎯 Full PowerShell Feature Parity** - Windows users rejoice!
- Complete PowerShell implementation of all interactive tools
- Launch-GitSage.ps1 - Universal launcher calling Python backend
- Generate-ReadmeInteractive.ps1 - Smart README generator with auto-detection
- Generate-Wiki.ps1 - Professional documentation wiki generator
- Test-RepositoryHealth.ps1 - Health checker with beautification scoring
- Initialize-Repository.ps1 - One-command complete repository setup
- 100% feature parity with Python versions

**🤖 Smart Project Detection**
- Auto-detects 10+ project types (npm, Python, CLI tools, web apps, etc.)
- Language and framework identification
- Smart defaults based on detection
- Confidence scoring for accuracy

**🏥 Repository Health & Beautification**
- 13 comprehensive health checks
- 100-point beautification scoring system
- 5 levels: Beginner → Intermediate → Advanced → Expert → Master
- 8 unlockable achievements
- 6 scoring categories (Documentation, Community, Automation, Code, Visual, Extras)
- Educational "WHY" explanations for each check
- Quick wins and critical issues identification

**🎨 Perfect Terminal Alignment**
- All ASCII characters (no emoji width issues)
- Consistent box drawing and alignment
- Professional terminal output across all platforms

## ✨ What's New in v2.2

**🌐 Web Interface** - Modern UI for GitSage!
- Browser-based dashboard with real-time status
- Script generation interface with live preview
- Backup management with one-click operations
- Repository browser integrated with GitHub CLI
- Settings management UI
- RESTful API for automation

**🏗️ Architectural Improvements**
- Professional src/ package structure
- Centralized configuration management
- Enhanced logging with Rich library
- Type hints and validation
- Comprehensive test suite
- Black/isort code formatting

**🛠️ Universal Installers**
- Automated install.sh for Linux/macOS
- Automated install.ps1 for Windows
- Three installation modes (user/system/dev)
- Dependency checking and virtual environment setup

**📚 Advanced Learning Resources**
- **[Advanced Git Workflows](docs/learning/advanced-git-workflows.md)** - Master rebase, cherry-pick, bisect
- **[GitHub Actions Tutorial](docs/learning/github-actions-tutorial.md)** - Complete CI/CD pipeline guide
- **[Open Source Contribution](docs/learning/open-source-contribution.md)** - Contributing successfully

**🔄 Consolidated Scripts**
- Unified repository migration tool
- Simplified launcher with CLI/Web mode selection
- Streamlined documentation structure

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Git 2.0+
- GitHub CLI (gh) authenticated
- Python 3.8+

# Optional (for web interface)
- Flask >= 3.0.0
- Flask-CORS >= 4.0.0
```

### Installation

**Automated Installation (Recommended):**

```bash
# Clone the repository
git clone https://github.com/shadowdevnotreal/gitsage.git
cd gitsage

# Linux/macOS
./install.sh

# Windows (PowerShell 7+ recommended, run as Administrator)
.\install.ps1

# Note: PowerShell 7+ is recommended for Windows
# Install from: https://aka.ms/powershell-release?tag=stable
# Or via winget: winget install Microsoft.PowerShell
```

**Manual Installation:**

```bash
# Clone the repository
git clone https://github.com/shadowdevnotreal/gitsage.git
cd gitsage

# Install Python dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e ".[dev]"

# Run installation check
python check_installation.py

# Launch main menu
python launcher.py
```

### Quick Launch

**All Platforms:**
```bash
# Interactive mode selection (CLI or Web)
python launcher.py
# Or: python -m gitsage

# Launch CLI directly
python launcher.py --cli

# Launch web interface directly
python launcher.py --web
# Access at http://localhost:5000

# After installation:
gitsage        # CLI interface
gitsage-web    # Web interface
```

**Bash (Linux/macOS):**
```bash
./launch.sh              # Interactive mode
./launch.sh --cli        # CLI directly
./launch.sh --web        # Web directly
./launch.sh --setup-repo # Repository setup wizard
```

**PowerShell (Windows):**
```powershell
.\scripts\powershell\Launch-GitSage.ps1           # Interactive mode
.\scripts\powershell\Launch-GitSage.ps1 -CLI      # CLI directly
.\scripts\powershell\Launch-GitSage.ps1 -Web      # Web directly
.\scripts\powershell\Launch-GitSage.ps1 -SetupRepo # Setup wizard
```

## 📋 Core Features

### Web Interface

| Feature | Description |
|---------|-------------|
| **Dashboard** | Environment status and system information |
| **Script Generator** | Generate automation scripts with live preview |
| **Backup Manager** | Create, restore, and manage repository backups |
| **Repository Browser** | Browse GitHub repos via integrated CLI |
| **Settings** | Web-based configuration management |
| **API** | RESTful endpoints for automation |

### CLI Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **Launcher** | Interactive menu with environment detection | `python launcher.py` |
| **Script Generator** | Generate scripts & learn GitHub | `python script-generator.py` |
| **Backup Manager** | Automated repository backups | `python backup-manager.py` |
| **Wiki Generator** | Professional wiki generation | `python wiki-generator.py` |
| **README Generator** | Awesome READMEs with badges | `python readme-generator.py` |
| **Installation Check** | Verify setup | `python check_installation.py` |
| **Uninstaller** | Safe removal | `python uninstall.py` |

### Git Operations (Bash)

| Script | Purpose | Location |
|--------|---------|----------|
| `delete-repo.sh` | Safe repository deletion | `scripts/bash/` |
| `repo-manager.sh` | Advanced repository management | `scripts/bash/` |
| `reset_git_history.sh` | Complete history reset | `scripts/git-resets/` |
| `migrate_repository.sh` | Unified repository migration | `scripts/git-resets/` |

### Git Operations (PowerShell)

| Script | Purpose | Location |
|--------|---------|----------|
| `Launch-GitSage.ps1` | Main launcher with interactive menu | `scripts/powershell/` |
| `Generate-ReadmeInteractive.ps1` | Interactive README generator | `scripts/powershell/` |
| `Generate-Wiki.ps1` | Documentation wiki generator | `scripts/powershell/` |
| `Test-RepositoryHealth.ps1` | Health checker & beautification scorer | `scripts/powershell/` |
| `Initialize-Repository.ps1` | One-command setup wizard | `scripts/powershell/` |
| `Delete-Repository.ps1` | Safe repository deletion | `scripts/powershell/` |
| `Manage-Repository.ps1` | Interactive repository manager | `scripts/powershell/` |
| `Reset-GitHistory.ps1` | Complete history reset | `scripts/powershell/` |
| `Migrate-Repository.ps1` | Repository migration | `scripts/powershell/` |

**NEW:** Full feature parity with Python tools! Windows users can now use native PowerShell for all interactive features.

## 🎮 Usage Examples

### Web Interface

```bash
# Launch web UI
python launcher.py --web
# or
gitsage-web

# Access at: http://localhost:5000

# Features available:
# - Generate scripts with templates
# - Manage backups (create/restore/delete)
# - Browse GitHub repositories
# - Configure settings
# - View environment status
```

### Script Generation

```bash
# Launch interactive script generator
python script-generator.py

# Choose from templates:
# 1. Auto-Commit & Push
# 2. Feature Branch Workflow
# 3. Repository Sync
# 4. Backup All Repos
# 5. PR Automation
# 6. Issue Management
# 7. Release Automation
# 8. CI/CD Setup

# Every script includes:
# - Educational comments
# - Best practices
# - Ready-to-use automation
```

### Backup Management

```bash
# Create a backup
python backup-manager.py create /path/to/repo --name "owner/repo"

# List all backups
python backup-manager.py list

# Restore a backup
python backup-manager.py restore backup_id_12345

# Delete a backup
python backup-manager.py delete backup_id_12345

# Backups are stored in ~/.gitsage/backups/
# with SHA256 checksums for integrity
```

### Repository Operations (Bash)

```bash
# Safe repository deletion
bash scripts/bash/delete-repo.sh

# Advanced repository management
bash scripts/bash/repo-manager.sh

# Reset git history (keeps files)
bash scripts/git-resets/reset_git_history.sh

# Migrate repository
bash scripts/git-resets/migrate_repository.sh --mode=full
```

### Repository Operations (PowerShell)

```powershell
# NEW: Main interactive launcher
.\scripts\powershell\Launch-GitSage.ps1

# NEW: One-command repository setup
.\scripts\powershell\Initialize-Repository.ps1

# NEW: Interactive README generator with auto-detection
.\scripts\powershell\Generate-ReadmeInteractive.ps1 -Interactive

# NEW: Wiki generator with all pages
.\scripts\powershell\Generate-Wiki.ps1 -All

# NEW: Repository health check with beautification scoring
.\scripts\powershell\Test-RepositoryHealth.ps1 -Full

# Safe repository deletion
.\scripts\powershell\Delete-Repository.ps1

# Interactive repository manager
.\scripts\powershell\Manage-Repository.ps1

# Reset git history (keeps files)
.\scripts\powershell\Reset-GitHistory.ps1

# Migrate repository
.\scripts\powershell\Migrate-Repository.ps1 -Mode full
```

## 🛡️ Safety Features

- **Multiple confirmations** for destructive operations
- **Automated backups** before dangerous actions
- **Validation checks** before execution
- **SHA256 verification** for backup integrity
- **Clear status messages** at each step
- **Error handling** with helpful guidance

## 🌍 Platform Support

| Platform | Python Scripts | Bash Scripts | PowerShell Scripts | Web Interface | Notes |
|----------|----------------|--------------|-------------------|---------------|-------|
| **Linux** | ✅ | ✅ | N/A | ✅ | Fully supported |
| **macOS** | ✅ | ✅ | ✅ (PS Core) | ✅ | Fully supported |
| **Windows** | ✅ | ⚠️ Git Bash | ✅ Native | ✅ | Full PowerShell support! |
| **WSL** | ✅ | ✅ | ✅ (PS Core) | ✅ | Linux on Windows |

### Windows Setup

```powershell
# 1. Install PowerShell 7+ (RECOMMENDED)
winget install Microsoft.PowerShell
# Or download: https://aka.ms/powershell-release?tag=stable

# 2. Install Git for Windows (includes Git Bash)
# Download: https://git-scm.com/download/win
winget install Git.Git

# 3. Install GitHub CLI
winget install GitHub.cli

# 4. Python tools work in PowerShell/CMD
python launcher.py
python backup-manager.py

# 5. Use native PowerShell scripts (RECOMMENDED for Windows)
.\scripts\powershell\Delete-Repository.ps1
.\scripts\powershell\Manage-Repository.ps1

# 6. Or use Bash scripts via Git Bash
bash scripts/bash/delete-repo.sh
```

**Windows Users:** GitSage now has complete PowerShell implementation! Use native PowerShell scripts for the best Windows experience.

## 📖 Documentation

### Learning Resources

- **[Advanced Git Workflows](docs/learning/advanced-git-workflows.md)** - Rebase, cherry-pick, bisect
- **[GitHub Actions Tutorial](docs/learning/github-actions-tutorial.md)** - Complete CI/CD guide
- **[Open Source Contribution](docs/learning/open-source-contribution.md)** - Contributing successfully

### User Guides

- **[Getting Started](docs/user-guides/getting-started.md)** - Complete beginner guide
- **[Repository Management](docs/user-guides/repository-management.md)** - GitHub management
- **[Wiki & GitBook Guide](docs/user-guides/wiki-gitbook-guide.md)** - Documentation creation

### Project Information

- **[Contributing](CONTRIBUTING.md)** - Help improve GitSage
- **[Changelog](CHANGELOG.md)** - Version history
- **[Security](SECURITY.md)** - Security policy
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community standards

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code style guidelines
- Pull request process
- Areas needing help

## ⚠️ Important Safety Notes

**Repository deletion is permanent and cannot be undone.**

- Deleted repositories cannot be recovered
- Git history reset is irreversible
- Always backup important work first
- Test on non-critical repositories
- Read all prompts carefully

## 🔧 Troubleshooting

**GitHub CLI not installed:**
```bash
# Visit: https://cli.github.com/
gh auth login
```

**Bash not found (Windows):**
```bash
# Install Git for Windows
# Visit: https://git-scm.com/download/win
```

**Permission denied:**
```bash
chmod +x scripts/bash/*.sh
chmod +x scripts/git-resets/*.sh
```

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **GitHub CLI Team** - Excellent command-line tool
- **Git Community** - Powerful version control
- **Open Source Contributors** - Everyone who helps improve this project

## 📊 Project Status

- **Version**: 2.2.0
- **Status**: Production Ready
- **Updated**: November 2024
- **Test Coverage**: Comprehensive test suite

**What's Working:**
- ✅ Web interface with modern UI
- ✅ Script generator with 8+ templates
- ✅ Automated backup system with SHA256
- ✅ Safe repository deletion (Bash + PowerShell)
- ✅ Repository management tools (Bash + PowerShell)
- ✅ Git history tools (Bash + PowerShell)
- ✅ Repository migration (Bash + PowerShell)
- ✅ Wiki & README generation
- ✅ Cross-platform support
- ✅ Complete PowerShell implementation for Windows
- ✅ Professional package structure
- ✅ Universal installers

## 💬 Support

- **Report Issues**: [GitHub Issues](../../issues)
- **Ask Questions**: Create an issue with "question" label
- **Feature Requests**: Create an issue with "enhancement" label

---

**Made for developers who value safety and automation in GitHub repository management.**

⭐ **Star this repository if GitSage helps you!**
