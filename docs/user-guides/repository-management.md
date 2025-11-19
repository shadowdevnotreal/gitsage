# Complete Repository Management Guide

Master GitHub repository management from the command line - novice to expert!

## Overview

GitSage provides comprehensive tools for:
- 🗑️ Safe repository deletion
- 🔄 Git history management
- 📦 Repository cloning and templates
- 🔀 Branch management
- 🏷️ Release management
- ⚙️ Repository configuration
- 🔐 Security and permissions

---

## Table of Contents

1. [Repository Deletion](#repository-deletion)
2. [Git History Management](#git-history-management)
3. [Repository Operations](#repository-operations)
4. [Advanced Management](#advanced-management)
5. [Automation](#automation)
6. [Best Practices](#best-practices)

---

## Repository Deletion

### Safe Interactive Deletion

The safest way to delete repositories with multiple confirmations:

```bash
# Launch interactive deletion script
bash scripts/bash/delete-repo.sh
```

**What Happens:**

1. **List Repositories**: Shows all your GitHub repositories
2. **Select Repository**: Choose which one to delete
3. **Show Details**: Displays repository information
   - Name and description
   - Stars and forks
   - Last updated
   - Size
4. **Local Check**: Checks for local copy
5. **Uncommitted Changes**: Warns if you have uncommitted work
6. **First Confirmation**: "Are you sure?"
7. **Second Confirmation**: Type repository name to confirm
8. **Remote Deletion**: Deletes from GitHub
9. **Local Deletion**: Removes local copy
10. **Verification**: Confirms deletion success

### Safety Features

✅ **Multiple Confirmations**
- Initial yes/no confirmation
- Type repository name confirmation
- Shows what will be deleted

✅ **Pre-Deletion Checks**
- Verifies repository exists
- Checks for uncommitted changes
- Warns about data loss

✅ **Post-Deletion Verification**
- Confirms remote deletion
- Confirms local deletion
- Shows final status

### Example Session

```
$ bash scripts/bash/delete-repo.sh

=== GitHub Repository Deletion Tool ===

Your repositories:
1. user/test-repo (0 stars, 0 forks)
2. user/old-project (5 stars, 2 forks)
3. user/archived-code (0 stars, 0 forks)

Which repository number to delete? 3

Repository Details:
Name: archived-code
Description: Old archived code
Stars: 0
Forks: 0
Last updated: 2024-01-15
Size: 1.2 MB

⚠️  WARNING: This operation is PERMANENT!
⚠️  Deleted repositories CANNOT be recovered!

Are you sure you want to delete 'archived-code'? (yes/no): yes

Type the repository name 'archived-code' to confirm: archived-code

Deleting remote repository...
✓ Remote repository deleted successfully

Deleting local copy at /home/user/repos/archived-code...
✓ Local copy deleted successfully

Repository 'archived-code' has been completely removed.
```

### Command Line Options

```bash
# Interactive mode (default)
bash scripts/bash/delete-repo.sh

# Future: Direct deletion (not yet implemented)
# bash scripts/bash/delete-repo.sh --repo user/repo-name
```

---

## Git History Management

### Complete History Reset

Remove all commit history while keeping current files:

```bash
bash scripts/git-resets/reset_git_history.sh
```

**Use Cases:**
- Remove sensitive data from history
- Start fresh with clean history
- Reduce repository size
- Clean up messy commit history

**What It Does:**

1. **Backup**: Creates backup branch
2. **Orphan Branch**: Creates new branch with no history
3. **Add Files**: Adds all current files
4. **Initial Commit**: Creates new first commit
5. **Replace Main**: Replaces main branch
6. **Force Push**: Updates remote (with confirmation)

**Example:**

```bash
$ bash scripts/git-resets/reset_git_history.sh

Current repository: my-project
Current branch: main
Total commits in history: 247

⚠️  WARNING: This will DELETE all commit history!
⚠️  Only current files will remain!
⚠️  This operation cannot be undone!

Create backup branch before proceeding? (yes/no): yes
Creating backup branch 'backup-before-reset'...
✓ Backup created

Proceed with history reset? (yes/no): yes

Creating orphan branch...
✓ Orphan branch created

Adding all files...
✓ Files added

Creating initial commit...
✓ Initial commit created

Replacing main branch...
✓ Branch replaced

Force push to remote? (yes/no): yes
⚠️  This will overwrite remote history!
Confirm by typing 'FORCE PUSH': FORCE PUSH

Pushing to remote...
✓ History reset complete!

Summary:
- Old history: 247 commits
- New history: 1 commit
- Backup branch: backup-before-reset
- All files preserved
```

### Repository Migration

Move repository to new location with history:

```bash
bash scripts/git-resets/migrate_and_swap_repos.sh
```

**Use Cases:**
- Move to different GitHub organization
- Transfer between accounts
- Rename repository properly
- Consolidate repositories

### Repository Sync and Swap

Synchronize and swap between repositories:

```bash
bash scripts/git-resets/migrate_sync_swap.sh
```

---

## Repository Operations

### Advanced Repository Manager

The main management tool:

```bash
bash scripts/bash/repo-manager.sh
```

**Features:**

1. **Repository Information**
   ```bash
   # View repository details
   # - Description
   # - Stars, forks, watchers
   # - Languages
   # - License
   # - Topics
   ```

2. **Clone Operations**
   ```bash
   # Clone with specific options
   # - Depth (shallow clone)
   # - Branch selection
   # - Submodules
   ```

3. **Branch Management**
   ```bash
   # List branches
   # Create branches
   # Delete branches
   # Protect branches
   ```

4. **Release Management**
   ```bash
   # Create releases
   # List releases
   # Download release assets
   ```

5. **Issue Management**
   ```bash
   # List issues
   # Create issues
   # Close issues
   # Assign issues
   ```

6. **Pull Request Operations**
   ```bash
   # List PRs
   # Create PRs
   # Merge PRs
   # Review PRs
   ```

### Using GitHub CLI Integration

GitSage integrates with GitHub CLI (`gh`) for powerful operations:

```bash
# View repository
gh repo view user/repo

# Clone repository
gh repo clone user/repo

# Create repository
gh repo create new-repo --public

# Fork repository
gh repo fork user/repo

# Delete repository
gh repo delete user/repo
```

### Batch Operations

**Clone Multiple Repositories:**

```bash
# Create list of repos
repos=(
  "user/repo1"
  "user/repo2"
  "user/repo3"
)

# Clone all
for repo in "${repos[@]}"; do
  gh repo clone "$repo"
done
```

**Delete Multiple Repositories:**

```bash
# List repos to delete
repos=(
  "user/old-repo1"
  "user/old-repo2"
)

# Delete each (with confirmation)
for repo in "${repos[@]}"; do
  echo "Deleting $repo..."
  gh repo delete "$repo" --confirm
done
```

---

## Advanced Management

### Repository Templates

Create new repositories from templates:

```bash
# Use GitHub template
gh repo create new-project --template user/template-repo

# Clone and customize
gh repo clone new-project
cd new-project
# Customize files
git add .
git commit -m "Initial customization"
git push
```

### Organization Management

**List Organization Repositories:**

```bash
# List all repos in organization
gh repo list orgname --limit 100

# List with specific criteria
gh repo list orgname --language python
gh repo list orgname --topic web
```

**Create Org Repository:**

```bash
# Create in organization
gh repo create orgname/new-repo --public

# With description and topics
gh repo create orgname/new-repo \
  --description "Project description" \
  --public \
  --add-topic "python,web,api"
```

### Security and Permissions

**Repository Settings:**

```bash
# View repository settings
gh repo view user/repo --json name,visibility,isPrivate

# Update visibility
gh repo edit user/repo --visibility public
gh repo edit user/repo --visibility private

# Enable/disable features
gh repo edit user/repo --enable-issues
gh repo edit user/repo --enable-wiki
gh repo edit user/repo --enable-projects
```

**Collaborators:**

```bash
# List collaborators
gh api repos/user/repo/collaborators

# Add collaborator
gh api repos/user/repo/collaborators/username -X PUT

# Remove collaborator
gh api repos/user/repo/collaborators/username -X DELETE
```

**Branch Protection:**

```bash
# Protect main branch
gh api repos/user/repo/branches/main/protection -X PUT \
  --field required_status_checks=null \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":1}'
```

### Repository Archiving

**Archive Repository:**

```bash
# Archive (read-only)
gh repo archive user/repo

# Unarchive
gh repo unarchive user/repo
```

### Repository Transfer

**Transfer to Another User:**

```bash
# Transfer repository
gh api repos/user/repo/transfer -X POST \
  --field new_owner="newuser"

# Transfer to organization
gh api repos/user/repo/transfer -X POST \
  --field new_owner="orgname"
```

---

## Automation

### Automated Repository Cleanup

```bash
#!/bin/bash
# cleanup-old-repos.sh

# Find repos not updated in 1 year
gh repo list --json name,updatedAt --limit 1000 | \
  jq -r '.[] | select(.updatedAt < "'$(date -d '1 year ago' -I)'") | .name' | \
  while read repo; do
    echo "Archive: $repo (not updated in 1 year)"
    gh repo archive "$repo"
  done
```

### Automated Backups

```bash
#!/bin/bash
# backup-all-repos.sh

BACKUP_DIR="$HOME/github-backups"
mkdir -p "$BACKUP_DIR"

# Get all repositories
gh repo list --limit 1000 --json name,sshUrl | \
  jq -r '.[] | "\(.name) \(.sshUrl)"' | \
  while read name url; do
    echo "Backing up $name..."

    # Clone if not exists, pull if exists
    if [ -d "$BACKUP_DIR/$name" ]; then
      cd "$BACKUP_DIR/$name"
      git pull
    else
      git clone "$url" "$BACKUP_DIR/$name"
    fi
  done

echo "Backup complete: $BACKUP_DIR"
```

### Scheduled Maintenance

```bash
# Add to crontab: crontab -e

# Backup all repos daily at 2 AM
0 2 * * * /path/to/backup-all-repos.sh

# Archive old repos monthly
0 0 1 * * /path/to/cleanup-old-repos.sh

# Update wiki documentation on commit
*/15 * * * * cd /path/to/project && python /path/to/gitsage/wiki-generator-enhanced.py
```

---

## Best Practices

### Organization

✅ **DO:**
- Use consistent naming conventions
- Add descriptions to all repositories
- Use topics for categorization
- Keep README.md updated
- Archive unused repositories

❌ **DON'T:**
- Leave repositories unnamed or undescribed
- Keep broken/obsolete code public
- Ignore security advisories
- Forget to document purposes

### Security

✅ **DO:**
- Use branch protection on main/master
- Require PR reviews
- Enable security scanning
- Keep dependencies updated
- Use .gitignore properly

❌ **DON'T:**
- Commit secrets or credentials
- Force push to main branch
- Disable security features
- Ignore dependency alerts

### Maintenance

✅ **DO:**
- Regularly review and clean up repositories
- Archive completed projects
- Delete truly unused repositories
- Keep wikis and documentation current
- Respond to issues and PRs

❌ **DON'T:**
- Hoard abandoned projects
- Leave issues unanswered
- Forget about old forks
- Keep duplicates

### Collaboration

✅ **DO:**
- Use descriptive commit messages
- Create feature branches
- Write good PR descriptions
- Review code thoroughly
- Communicate changes

❌ **DON'T:**
- Commit directly to main
- Push without testing
- Ignore code review feedback
- Make breaking changes without warning

---

## Troubleshooting

### "Permission denied" errors

```bash
# Check authentication
gh auth status

# Re-authenticate
gh auth login

# Check repository permissions
gh repo view user/repo --json permissions
```

### "Repository not found"

```bash
# Verify repository exists
gh repo view user/repo

# Check repository name spelling
gh repo list user

# Verify access (for private repos)
gh auth status
```

### "Branch is protected"

```bash
# Check branch protection
gh api repos/user/repo/branches/main/protection

# Create PR instead of direct push
gh pr create --title "Changes" --body "Description"
```

### Force push blocked

```bash
# Don't force push to main!
# Instead, create new branch:
git checkout -b fix-branch
git push -u origin fix-branch

# Then create PR
gh pr create
```

---

## Command Reference

### Essential Commands

```bash
# Repository Info
gh repo view [repo]
gh repo list [user/org]

# Repository Operations
gh repo create [name]
gh repo delete [repo]
gh repo clone [repo]
gh repo fork [repo]

# Visibility
gh repo edit [repo] --visibility [public/private]

# Features
gh repo edit [repo] --enable-wiki
gh repo edit [repo] --enable-issues

# Status
gh repo archive [repo]
gh repo unarchive [repo]
```

### GitSage Scripts

```bash
# Deletion (with safety checks)
bash scripts/bash/delete-repo.sh

# Repository Management
bash scripts/bash/repo-manager.sh

# History Reset
bash scripts/git-resets/reset_git_history.sh

# Migration
bash scripts/git-resets/migrate_and_swap_repos.sh

# Sync and Swap
bash scripts/git-resets/migrate_sync_swap.sh
```

---

## Advanced Workflows

### Full Repository Lifecycle

**1. Create**
```bash
gh repo create new-project --public
cd new-project
echo "# New Project" > README.md
git add README.md
git commit -m "Initial commit"
git push -u origin main
```

**2. Develop**
```bash
# Create feature branch
git checkout -b feature

# Make changes
# ...

# Commit and push
git add .
git commit -m "Add feature"
git push -u origin feature

# Create PR
gh pr create
```

**3. Maintain**
```bash
# Generate documentation
python /path/to/gitsage/wiki-generator-enhanced.py

# Update wiki
cd generated-docs
./deployment/deploy-wiki.sh
```

**4. Archive**
```bash
# When project is complete
gh repo archive user/new-project
```

**5. Delete**
```bash
# If truly no longer needed
bash /path/to/gitsage/scripts/bash/delete-repo.sh
```

---

## Expert Tips

### Speed Up Operations

```bash
# Use aliases
alias ghc='gh repo clone'
alias ghv='gh repo view'
alias ghl='gh repo list'

# Shallow clone for speed
gh repo clone user/repo -- --depth 1

# Parallel operations
repos=(repo1 repo2 repo3)
printf '%s\n' "${repos[@]}" | xargs -P 3 -I {} gh repo clone {}
```

### Scripting Integration

```bash
#!/bin/bash
# smart-clone.sh - Clone with automatic wiki download

REPO="$1"

# Clone repository
gh repo clone "$REPO"
cd "$(basename $REPO)"

# Download wiki if exists
if gh api "repos/$REPO" | jq -r '.has_wiki' | grep -q true; then
  echo "Cloning wiki..."
  git clone "https://github.com/$REPO.wiki.git" wiki
fi

# Generate local documentation
python /path/to/gitsage/wiki-generator-enhanced.py
```

### Monitoring

```bash
# Watch for changes
watch -n 60 'gh repo view --json stargazerCount,forks'

# Alert on new issues
gh issue list --state open --json number,title | \
  jq '.[] | "\(.number): \(.title)"' | \
  mail -s "New Issues" you@email.com
```

---

**You're now equipped to manage GitHub repositories like a professional!** 🚀

Next steps:
- Practice on test repositories
- Automate your workflows
- Integrate with your development process
- Explore GitHub CLI advanced features

For more help:
- GitHub CLI docs: https://cli.github.com/manual/
- Git docs: https://git-scm.com/doc
- GitSage issues: https://github.com/shadowdevnotreal/gitsage/issues
