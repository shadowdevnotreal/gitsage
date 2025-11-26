# GitSage PowerShell Scripts

Complete PowerShell implementation of GitSage repository management tools for Windows.

## 🚀 Features

All core GitSage functionality now available in native PowerShell:

### Repository Management
- **Delete-Repository.ps1** - Safe repository deletion with multiple confirmations
- **Manage-Repository.ps1** - Interactive repository manager with Git operations
- **Reset-GitHistory.ps1** - Reset Git history while keeping files
- **Migrate-Repository.ps1** - Migrate repositories between accounts/organizations

### Interactive Tools (NEW!)
- **Launch-GitSage.ps1** - Main launcher with interactive menu
- **Generate-ReadmeInteractive.ps1** - Interactive README generator with smart detection
- **Generate-Wiki.ps1** - Complete documentation wiki generator
- **Test-RepositoryHealth.ps1** - Repository health checker and beautification scorer
- **Initialize-Repository.ps1** - One-command complete repository setup

## 📋 Prerequisites

```powershell
# Required
- Windows PowerShell 5.1+ or PowerShell Core 7+
- Git for Windows
- GitHub CLI (gh) authenticated

# Check versions
git --version
gh --version
$PSVersionTable.PSVersion
```

## 🔧 Installation & Setup

### 1. Install Prerequisites

```powershell
# Install Git for Windows
winget install Git.Git

# Install GitHub CLI
winget install GitHub.cli

# Authenticate GitHub CLI
gh auth login
```

### 2. Enable Script Execution

```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Navigate to Scripts Directory

```powershell
cd path\to\gitsage\scripts\powershell
```

## 📖 Usage

### Quick Start - Interactive Tools

```powershell
# Launch main menu (easiest way to get started)
.\Launch-GitSage.ps1

# Or run one-command setup wizard
.\Initialize-Repository.ps1
```

### Interactive README Generator

```powershell
# Interactive wizard with auto-detection
.\Generate-ReadmeInteractive.ps1 -Interactive

# Analyze project only
.\Generate-ReadmeInteractive.ps1 -Analyze

# Show health report
.\Generate-ReadmeInteractive.ps1 -HealthCheck
```

### Documentation Wiki Generator

```powershell
# Generate all wiki pages
.\Generate-Wiki.ps1 -All

# Generate specific page
.\Generate-Wiki.ps1 -Page Home

# Show GitHub Wiki setup instructions
.\Generate-Wiki.ps1 -ShowSetup
```

### Repository Health Checker

```powershell
# Full detailed report
.\Test-RepositoryHealth.ps1 -Full

# Quick summary only
.\Test-RepositoryHealth.ps1 -Quick

# Beautification score with achievements
.\Test-RepositoryHealth.ps1 -Beauty
```

### Repository Management

### Delete Repository

```powershell
# Interactive mode
.\Delete-Repository.ps1

# With parameters
.\Delete-Repository.ps1 -Repository "username/repo"

# Skip backup (not recommended)
.\Delete-Repository.ps1 -Repository "username/repo" -SkipBackup
```

**Features:**
- Multiple safety confirmations
- Automatic backup creation
- Uncommitted changes detection
- Local and remote cleanup
- Deletion verification

### Manage Repository

```powershell
# Launch interactive menu
.\Manage-Repository.ps1
```

**Menu Options:**
1. Clone Repository
2. Create New Repository
3. List Your Repositories
4. Repository Status
5. Commit Changes
6. Push to Remote
7. Pull from Remote
8. Create Branch
9. Switch Branch
10. Merge Branch
11. Sync Fork
12. Create Pull Request
13. View Repository Issues

### Reset Git History

```powershell
# Interactive mode with prompts
.\Reset-GitHistory.ps1

# Force mode (skip confirmations - use with caution)
.\Reset-GitHistory.ps1 -Force
```

**What it does:**
- Creates backup of current history
- Deletes all commit history
- Keeps all current files
- Creates fresh initial commit
- Requires force push to remote

**⚠️ WARNING:** This operation is IRREVERSIBLE!

### Migrate Repository

```powershell
# Interactive mode
.\Migrate-Repository.ps1

# Simple migration (clone and push)
.\Migrate-Repository.ps1 -Mode simple `
    -Source "oldowner/repo" `
    -Destination "newowner/repo"

# Full migration (mirror all refs)
.\Migrate-Repository.ps1 -Mode full `
    -Source "oldowner/repo" `
    -Destination "newowner/repo"
```

**Migration Modes:**
- **Simple:** Clone repository and push to new location (easier, faster)
- **Full:** Complete mirror including all branches, tags, and refs (comprehensive)

## 🛡️ Safety Features

All PowerShell scripts include:

- ✅ **Prerequisite checks** - Verify Git and GitHub CLI are installed
- ✅ **Multiple confirmations** - Prevent accidental destructive operations
- ✅ **Automatic backups** - Create backups before dangerous operations
- ✅ **Colored output** - Easy-to-read status messages
- ✅ **Error handling** - Graceful error recovery
- ✅ **Input validation** - Verify repository names and paths

## 🎨 Color-Coded Output

Scripts use color-coded messages for clarity:

- 🔵 **INFO** - General information
- 🟢 **SUCCESS** - Operation completed successfully
- 🟡 **WARNING** - Caution required
- 🔴 **ERROR** - Operation failed
- 🟣 **QUESTION** - User input required

## 📁 Backup Locations

Scripts create backups in user-specific directories:

```powershell
# Repository backups (Delete-Repository.ps1)
$env:USERPROFILE\.gitsage\backups\

# History backups (Reset-GitHistory.ps1)
$env:USERPROFILE\.gitsage\history-backups\

# Migration temp directory (auto-cleaned)
$env:TEMP\gitsage_migration_*\
```

## 🔒 Security Best Practices

1. **Always review** what will be deleted/changed before confirming
2. **Create backups** before destructive operations (enabled by default)
3. **Test on non-critical repositories** first
4. **Verify prerequisites** are installed and authenticated
5. **Use -Force sparingly** - it skips safety confirmations

## 🆚 PowerShell vs Bash

| Feature | PowerShell | Bash |
|---------|-----------|------|
| **Platform** | Windows native | Linux/macOS/WSL |
| **Color Output** | Write-Host colors | ANSI codes |
| **Parameters** | Native cmdlet params | Getopt parsing |
| **Error Handling** | Try/Catch blocks | Exit codes |
| **Objects** | Rich objects | Text streams |

Both implementations have feature parity!

## 🚧 Troubleshooting

### "Script cannot be loaded" Error

```powershell
# Check execution policy
Get-ExecutionPolicy

# Set to RemoteSigned
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Git is not recognized"

```powershell
# Install Git for Windows
winget install Git.Git

# Or download from: https://git-scm.com/download/win
```

### "GitHub CLI is not authenticated"

```powershell
# Authenticate with GitHub
gh auth login

# Follow the prompts to complete authentication
```

### "Access Denied" when creating backups

```powershell
# Ensure backup directory exists and is writable
$backupDir = "$env:USERPROFILE\.gitsage\backups"
New-Item -ItemType Directory -Path $backupDir -Force
```

## 📚 Examples

### Complete Workflow Example

```powershell
# 1. Clone a repository
.\Manage-Repository.ps1
# Choose: 1 (Clone Repository)
# Enter: username/repo

# 2. Make changes and commit
cd repo
# ... make changes ...
.\Manage-Repository.ps1
# Choose: 5 (Commit Changes)
# Enter commit message

# 3. Push changes
.\Manage-Repository.ps1
# Choose: 6 (Push to Remote)

# 4. Create pull request
.\Manage-Repository.ps1
# Choose: 12 (Create Pull Request)
```

### Migration Example

```powershell
# Migrate from personal account to organization
.\Migrate-Repository.ps1 -Mode full `
    -Source "myusername/myproject" `
    -Destination "myorg/myproject"

# Result: Complete mirror at new location
```

### Reset History Example

```powershell
# Reset history and push
cd myrepo
.\Reset-GitHistory.ps1

# After reset completes:
git push origin main --force
```

## 🤝 Equivalent Bash Scripts

Each PowerShell script has a Bash equivalent:

| PowerShell | Bash |
|------------|------|
| Delete-Repository.ps1 | scripts/bash/delete-repo.sh |
| Manage-Repository.ps1 | scripts/bash/repo-manager.sh |
| Reset-GitHistory.ps1 | scripts/git-resets/reset_git_history.sh |
| Migrate-Repository.ps1 | scripts/git-resets/migrate_repository.sh |

## 📖 Additional Resources

- **Main README:** ../../README.md
- **Installation Guide:** ../../install.ps1
- **Contributing:** ../../CONTRIBUTING.md
- **Security:** ../../SECURITY.md

## 💬 Support

- **Report Issues:** https://github.com/shadowdevnotreal/gitsage/issues
- **Documentation:** https://github.com/shadowdevnotreal/gitsage
- **Discussions:** Create an issue with "question" label

---

**Made with ❤️ for Windows PowerShell users**

Full feature parity with Bash scripts - use whichever you prefer!
