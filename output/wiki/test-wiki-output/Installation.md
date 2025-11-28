# Installation Guide

Complete installation instructions for GitHub Repository Manager.

## System Requirements

- **Operating System:** Windows 10+, macOS 10.14+, Linux
- **Python:** 3.8 or higher
- **Git:** Latest version
- **GitHub CLI:** Latest version

## Installation Steps

### 1. Install Prerequisites

**Git:**
- Windows: [Download from git-scm.com](https://git-scm.com/download/win)
- macOS: `brew install git`
- Linux: `sudo apt install git`

**GitHub CLI:**
- Windows: `winget install GitHub.cli`
- macOS: `brew install gh`
- Linux: `sudo snap install gh`

### 2. Clone Repository

```bash
git clone https://github.com/user/github-repo-manager.git
cd github-repository-manager
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Setup Wizard

```bash
python utils/setup_wizard.py
```

## Verification

Test your installation:

```bash
python launcher.py
```

You should see the main menu. Success!

## Troubleshooting

If you encounter issues, see the [Troubleshooting Guide](troubleshooting).
