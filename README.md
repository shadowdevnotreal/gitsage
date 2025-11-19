# GitHub Repository Manager

<img width="1024" height="1024" alt="ChatGPT Image Jul 8, 2025, 09_48_49 PM" src="https://github.com/user-attachments/assets/0b6a8c7a-e479-4dbc-b24d-920f4225daf2" />


> A comprehensive, cross-platform toolkit for safe GitHub repository management and automated documentation generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform Support](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#platform-support)
[![GitHub CLI](https://img.shields.io/badge/requires-GitHub%20CLI-blue)](https://cli.github.com/)

## 🎯 **What This Project Solves**

Every developer faces these challenges:
- **🗑️ Safely deleting repositories** without losing important data
- **📚 Creating professional documentation** that takes hours to write
- **🔄 Managing repository history** when sensitive data needs removal
- **⚙️ Working across different platforms** with inconsistent tools

This toolkit automates these tedious tasks and provides safe, interactive solutions that work everywhere.

## ✨ **Core Features**

### 🗑️ **Interactive Repository Deletion**
- **Multiple safety confirmations** prevent accidental deletions
- **Local and remote cleanup** in one operation
- **Uncommitted changes detection** with clear warnings
- **Verification after deletion** to ensure success

### 📝 **Automated Documentation Generation**
- **Transform any project** into professional GitHub wikis in minutes
- **Template-driven approach** ensures consistency
- **One-command deployment** to GitHub Wiki
- **Customizable structure** for different project types

### 🔄 **Git History Management**
- **Complete history reset** while preserving current files
- **Orphan branch technique** for clean slate starts
- **Safe operation flow** with multiple confirmations
- **Force push protection** to prevent accidents

### 🌍 **Cross-Platform Compatibility**
- **Universal Python launcher** that detects your environment
- **Native PowerShell** version for Windows users
- **Enhanced Bash scripts** for Unix/Linux/macOS
- **Tkinter GUI** for visual interface preferences

## 🚀 **Quick Start**

### **One-Line Setup**
```bash
# Clone and run - it detects everything automatically
git clone https://github.com/user/github-repo-manager.git
cd github-repo-manager
python launcher.py
```

### **Platform-Specific Quick Start**
```bash
# Windows
launcher.bat

# Unix/Linux/macOS  
./launcher.sh

# Direct script usage
./delete-repo.sh                    # Your safe deletion script
python wiki-generator.py --all      # Generate documentation
```

## 📋 **What You Get**

### **🔧 Repository Management Tools**
| Tool | Purpose | Platform |
|------|---------|----------|
| `delete-repo.sh` | Interactive deletion with safety checks | Unix/Bash |
| `launcher.py` | Universal environment detection | Cross-platform |
| `scripts/python/repo-manager.py` | Full CLI with all features | Cross-platform |
| `scripts/powershell/repo-manager.ps1` | Windows PowerShell native | Windows/PS |
| `scripts/gui/repo-manager-gui.py` | Graphical interface | Cross-platform |

### **📚 Documentation Automation**
| Tool | Purpose | Output |
|------|---------|--------|
| `wiki-generator.py` | Automated wiki generation | GitHub Wiki files |
| `wiki-config.yaml` | Easy customization | Template configuration |
| Generated wikis | Professional documentation | Deploy-ready pages |

### **🛠️ Setup Assistance**
| Tool | Purpose | Platform |
|------|---------|----------|
| `installers/install-git.*` | Automated Git installation | Unix/Windows |
| `installers/install-gh-cli.*` | GitHub CLI setup | Unix/Windows |
| Environment detection | Prerequisites checking | Cross-platform |

## 🎮 **Usage Examples**

### **Safe Repository Deletion**
```bash
# Interactive mode with full safety checks
./delete-repo.sh

# The script will:
# 1. List all your repositories
# 2. Let you select which to delete
# 3. Show repository details
# 4. Confirm multiple times
# 5. Delete remote and local copies
# 6. Verify successful deletion
```

### **Instant Documentation**
```bash
# Generate complete wiki for any project
python wiki-generator.py --all

# Customize for your project
edit wiki-config.yaml

# Deploy to GitHub Wiki
./generated-docs/deployment/deploy-wiki.sh https://github.com/user/repo.git
```

### **Git History Reset**
```bash
# Remove all commit history but keep current files
python launcher.py
# Choose "Reset Git History" option
# Perfect for removing sensitive data from history
```

## 🛡️ **Safety Philosophy**

This toolkit is designed with **safety-first principles**:

- **🔍 Validation before action** - Every operation checks what it's about to do
- **⚠️ Multiple confirmations** - Destructive operations require explicit approval
- **📊 Clear information display** - You always know what will be affected
- **✅ Verification after completion** - Confirms operations succeeded
- **🚫 No silent failures** - If something goes wrong, you'll know

## 🌟 **Why This Project Exists**

### **Real Developer Problems**
- **Manual documentation takes 10-20 hours** per project
- **Repository deletion is scary** without proper safety checks
- **Git history cleanup is complex** and error-prone
- **Cross-platform tools are rare** in the GitHub ecosystem

### **Our Solutions**
- **5-minute automated documentation** generation
- **Interactive deletion with safety nets**
- **Guided history management** with clear explanations
- **Universal compatibility** across all platforms

## 🤝 **Contributing**

We'd love your help making this toolkit even better!

### **🐛 Found a Bug?**
- Check [existing issues](../../issues) first
- Create a detailed bug report with steps to reproduce
- Include your OS, Git version, and GitHub CLI version

### **💡 Have an Idea?**
- Open a [discussion](../../discussions) to talk about it
- Submit a feature request with use cases
- Fork and submit a pull request

### **🔧 Want to Code?**
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
- Check [open issues](../../issues) labeled "good first issue"
- All skill levels welcome - documentation improvements are valuable too!

### **📚 Improve Documentation?**
- Wiki generation is automated, but guides can always be better
- Submit improvements to help files
- Share your use cases and examples

## 📖 **Documentation**

- **[Quick Start Guide](help/quick-start.md)** - Get running in 5 minutes
- **[Deletion Script Guide](DELETE-REPO-README.md)** - Safe repository removal
- **[Wiki Generator Guide](WIKI-GENERATOR-README.md)** - Automated documentation
- **[Contributing Guide](CONTRIBUTING.md)** - How to help improve the project
- **[Troubleshooting](help/)** - Common issues and solutions

## 🌍 **Platform Support**

| Platform | Status | Recommended Method |
|----------|--------|-------------------|
| **Windows 10/11** | ✅ Full Support | `launcher.bat` or PowerShell version |
| **macOS** | ✅ Full Support | `python launcher.py` or Bash version |
| **Linux** | ✅ Full Support | `python launcher.py` or Bash version |
| **WSL** | ✅ Full Support | Bash version |
| **Git Bash** | ✅ Full Support | Bash version |

## ⚠️ **Important Safety Notes**

- **Repository deletion is permanent** - deleted repositories cannot be recovered
- **History reset is irreversible** - all commit history will be permanently lost
- **Always backup important repositories** before performing destructive operations
- **Test on non-critical repositories first** to understand the workflow

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You're free to use, modify, and distribute this software. We just ask that you retain the original license notice.

## 🙏 **Acknowledgments**

- **GitHub CLI Team** - For the excellent `gh` command-line tool
- **Git Community** - For the powerful and flexible version control system
- **Python Community** - For the cross-platform compatibility
- **Open Source Contributors** - Everyone who helps make this project better

## 💬 **Community & Support**

- **🐛 Issues**: [Report bugs or request features](../../issues)
- **💭 Discussions**: [Ask questions and share ideas](../../discussions)  
- **📖 Wiki**: [Community-maintained documentation](../../wiki)
- **⭐ Stars**: If this project helps you, consider giving it a star!

---

**Made with ❤️ for developers who want powerful, safe, and easy-to-use repository management tools.**

**Help us make GitHub repository management better for everyone!** 🚀
