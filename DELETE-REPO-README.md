# Interactive GitHub Repository Deletion Script

A comprehensive bash script for safely deleting GitHub repositories with enhanced features including Git history reset, full synchronization, and interactive guidance.

## 🚀 Quick Start

```bash
# Make the script executable
chmod +x delete-repo.sh

# Run the script
./delete-repo.sh
```

## ✨ Features

### 🛡️ **Safety First**
- **Multiple confirmation prompts** for all destructive operations
- **Repository validation** before any actions
- **Uncommitted changes detection** with warnings
- **Operation verification** after completion
- **Colored output** for clear status indication

### 🔧 **Core Operations**
- **Repository Deletion**: Remove both remote (GitHub) and local repositories
- **Git History Reset**: Clean slate with orphan branch technique
- **Full Synchronization**: Update all local repositories with remotes
- **Interactive Selection**: Browse and select from your repository list

### 🎯 **Enhanced Functionality**
- **Repository Details**: View comprehensive repository information
- **Local Detection**: Automatically finds local copies
- **Batch Processing**: Handle multiple repositories in one session
- **Progress Tracking**: Clear status updates throughout operations

## 📋 Prerequisites

### Required Tools
- **Git**: Version control system
  - Install: https://git-scm.com/
  - Verify: `git --version`

- **GitHub CLI (gh)**: GitHub command-line tool
  - Install: https://cli.github.com/
  - Verify: `gh --version`
  - Authenticate: `gh auth login`

### System Requirements
- **Bash shell** (Linux, macOS, Git Bash on Windows, WSL)
- **Internet connection** for GitHub operations
- **Terminal** with color support (recommended)

## 🎮 Usage

### Interactive Mode (Recommended)
```bash
./delete-repo.sh
```
The script will guide you through:
1. Repository list display
2. Repository selection
3. Operation choice (delete/reset/sync)
4. Safety confirmations
5. Execution and verification

### Available Operations

#### 1. **Delete Repository**
- Removes repository from GitHub
- Deletes local directory if present
- Verifies successful deletion
- Updates local repository cache

#### 2. **Reset Git History**
- Preserves current files
- Removes all commit history
- Creates fresh initial commit
- Force pushes clean history (with confirmation)

#### 3. **Sync Repositories**
- Fetches latest changes for all local repos
- Updates default branches
- Prunes deleted remote branches
- Refreshes repository metadata

## 🔒 Safety Features

### Pre-Operation Checks
- ✅ Validates GitHub CLI installation and authentication
- ✅ Confirms repository exists and is accessible
- ✅ Checks for local repository presence
- ✅ Detects uncommitted changes
- ✅ Shows repository details before actions

### During Operations
- ⚠️ Multiple confirmation prompts
- 📊 Real-time progress updates
- 🔍 Status verification at each step
- 📝 Detailed logging of all actions

### Post-Operation
- ✅ Verification of successful completion
- 📋 Summary of actions taken
- 🔄 Automatic synchronization
- 📊 Updated repository listings

## 📖 Detailed Workflow

### Repository Deletion Process
```
1. List all repositories → 
2. Select target repository → 
3. Display repository details → 
4. Confirm deletion → 
5. Delete remote repository → 
6. Remove local directory (if exists) → 
7. Verify deletion → 
8. Sync remaining repositories → 
9. Show completion summary
```

### Git History Reset Process
```
1. Navigate to local repository → 
2. Check for uncommitted changes → 
3. Reset and clean working directory → 
4. Pull latest changes → 
5. Create orphan branch → 
6. Add all files to new commit → 
7. Replace main branch → 
8. Force push to remote (with confirmation) → 
9. Verify clean history
```

## 🎨 Output Examples

### Repository List Display
```
Your repositories:
1. username/project-alpha (Public) ⭐15 🍴3
   A cool web application for productivity
2. username/data-analysis (Private) ⭐2 🍴0
   Personal data analysis scripts
3. username/old-website (Public) ⭐0 🍴1
   Archived personal website
```

### Operation Progress
```
[INFO] Deleting remote repository: username/old-project
[SUCCESS] Remote repository deleted successfully
[INFO] Found local directory: old-project
[WARNING] Local directory contains uncommitted changes
[SUCCESS] Local directory deleted
[SUCCESS] Repository deletion verified
```

## ⚙️ Configuration

### Environment Variables
```bash
# Optional: Set default behavior
export GH_REPO_DELETE_FORCE=false    # Always ask for confirmation
export GH_REPO_DELETE_BACKUP=true    # Create backups when possible
export GH_REPO_DELETE_VERIFY=true    # Always verify operations
```

### Customization
Edit the script to modify:
- Default commit messages for history reset
- Color schemes for output
- Timeout values for operations
- Repository list limits

## 🚨 Important Warnings

### ⚠️ **Repository Deletion**
- **PERMANENT**: Deleted repositories cannot be recovered
- **ALL DATA LOST**: Issues, PRs, releases, and wiki content are deleted
- **COLLABORATORS**: Notify team members before deleting shared repositories
- **FORKS**: Consider impact on existing forks

### ⚠️ **History Reset**
- **IRREVERSIBLE**: All commit history is permanently lost
- **COLLABORATION**: Team members will need to re-clone
- **REFERENCES**: Issues/PRs may reference non-existent commits
- **SIGNATURES**: All commit signatures are lost

## 🛠️ Troubleshooting

### Common Issues

#### "gh command not found"
```bash
# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh
```

#### "Authentication failed"
```bash
# Re-authenticate with GitHub
gh auth logout
gh auth login
```

#### "Repository not found"
- Verify repository name format: `owner/repository`
- Check repository permissions and access
- Ensure repository exists on GitHub

#### "Permission denied"
- Check file permissions: `chmod +x delete-repo.sh`
- Verify write access to current directory
- Ensure you own the repository being deleted

### Debug Mode
Run with verbose output:
```bash
bash -x delete-repo.sh
```

## 🔗 Integration

### Use in Scripts
```bash
#!/bin/bash
# Automated cleanup script
source delete-repo.sh

# Set variables to skip confirmations
GH_REPO_DELETE_FORCE=true
delete_repository "username/temp-repo"
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Clean up test repositories
  run: |
    chmod +x scripts/delete-repo.sh
    ./scripts/delete-repo.sh
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 📚 Related Tools

This script is part of a larger **Repository Manager** suite:
- **GUI Version**: Graphical interface with tkinter
- **PowerShell Version**: Windows-native implementation
- **Python Version**: Cross-platform CLI with enhanced features
- **Universal Launcher**: Auto-detects best version for your system

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 🆘 Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: Check the help/ directory for more guides
- **Community**: Join discussions in GitHub Discussions

---

**⚠️ Use this tool responsibly. Always ensure you have backups of important repositories before performing destructive operations.**

**Made with ❤️ for developers who need to clean up their GitHub repositories safely.**