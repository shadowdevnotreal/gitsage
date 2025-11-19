# 🚀 New Features Guide

## Version 2.0 - Enhanced Safety & Automation

This document describes the major enhancements added to GitHub Repository Manager in version 2.0.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [New Features](#new-features)
  - [Automatic Backup System](#automatic-backup-system)
  - [Structured Logging](#structured-logging)
  - [Configuration Management](#configuration-management)
  - [Dry-Run Mode](#dry-run-mode)
  - [Enhanced Python CLI](#enhanced-python-cli)
- [Testing Infrastructure](#testing-infrastructure)
- [CI/CD Pipeline](#cicd-pipeline)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)

---

## Overview

Version 2.0 introduces **enterprise-grade safety features** that protect you from data loss while maintaining the simplicity of the original tool.

### What's New?

✅ **Automatic Backups** - Every destructive operation creates a backup first
✅ **Audit Logging** - Complete history of all operations
✅ **Configuration System** - Customize behavior to your preferences
✅ **Dry-Run Mode** - Preview changes before applying them
✅ **Automated Tests** - 50+ tests ensuring reliability
✅ **CI/CD Pipeline** - Automated testing on every change

---

## Quick Start

### First-Time Setup

Run the setup wizard to configure your preferences:

```bash
python utils/setup_wizard.py
```

This interactive wizard will:
- Check prerequisites
- Configure safety features
- Set your preferences
- Create initial configuration

### Launch Enhanced Manager

```bash
# Use the launcher
python launcher.py
# Choose option 4: Enhanced Python CLI

# Or launch directly
python scripts/python/repo-manager-enhanced.py
```

---

## New Features

### 🛡️ Automatic Backup System

**Location:** `utils/backup_manager.py`

Every destructive operation (deletion, history reset) now automatically creates a backup before making changes.

#### Features:
- **Automatic**: No manual intervention required
- **Compressed**: TAR.GZ format saves space
- **Verified**: SHA256 checksums ensure integrity
- **Restorable**: One-command restore to original state
- **Configurable**: Control retention and storage location

#### Usage:

**List available backups:**
```bash
python -m utils.backup_manager list
```

**Restore a backup:**
```bash
python -m utils.backup_manager restore --backup-id <BACKUP_ID>
```

**Delete old backups:**
```bash
python -m utils.backup_manager cleanup --keep-days 30
```

**Create manual backup:**
```bash
python -m utils.backup_manager backup \
    --repo-path ./my-repo \
    --repo-name owner/repo \
    --operation manual
```

#### Configuration:

```yaml
general:
  auto_backup: true  # Enable automatic backups
  backup_before_deletion: true
  backup_before_history_reset: true
  backup_retention_days: 30  # Keep backups for 30 days
  backup_keep_count: 10  # Keep at least 10 backups per repo
```

#### Backup Storage:

Default location: `~/.repo-manager/backups/`

Structure:
```
~/.repo-manager/backups/
├── backup_index.json              # Metadata index
├── owner_repo_deletion_20250101_120000/
│   ├── owner_repo_deletion_20250101_120000.tar.gz
│   └── metadata.json
└── owner_repo_history_reset_20250101_130000/
    ├── owner_repo_history_reset_20250101_130000.tar.gz
    └── metadata.json
```

---

### 📝 Structured Logging

**Location:** `utils/logger.py`

Complete audit trail of all operations with structured logging and security event tracking.

#### Features:
- **Operation Logging**: Every action is recorded
- **Audit Trail**: Who did what, when, and where
- **Security Events**: Track sensitive operations
- **Error Tracking**: Detailed error logs with stack traces
- **Session Tracking**: Group operations by session
- **Queryable**: Search logs by repo, operation, date

#### Log Files:

Location: `~/.repo-manager/logs/`

```
~/.repo-manager/logs/
├── operations.log          # All operations
├── audit.log              # Human-readable audit trail
├── errors.log             # Error details with stack traces
├── security.log           # Security-sensitive events
├── audit_structured.jsonl # Machine-readable audit trail
└── security_structured.jsonl  # Structured security events
```

#### Usage:

**View operation history:**
```bash
python -m utils.logger history --limit 50
```

**Filter by repository:**
```bash
python -m utils.logger history --repo owner/repo
```

**View recent errors:**
```bash
python -m utils.logger errors --limit 20
```

**Export logs:**
```bash
python -m utils.logger export --output logs_export.tar.gz
```

#### What Gets Logged:

✅ Repository deletions (remote and local)
✅ Git history resets
✅ Repository syncs
✅ Backup operations
✅ Configuration changes
✅ Security events (authentication, access attempts)
✅ Errors and exceptions
✅ Session information (user, hostname, timestamp)

---

### ⚙️ Configuration Management

**Location:** `utils/config_manager.py`

Comprehensive configuration system for customizing tool behavior.

#### Features:
- **User Preferences**: Customize confirmations, defaults, and behavior
- **Safety Controls**: Fine-tune safety features
- **Path Configuration**: Custom backup and log locations
- **Import/Export**: Share configurations across machines
- **Validation**: Automatic validation of settings
- **Backup & Restore**: Configuration backups on every change

#### Usage:

**View current configuration:**
```bash
python -m utils.config_manager show
```

**View specific section:**
```bash
python -m utils.config_manager show --section general
```

**Change a setting:**
```bash
python -m utils.config_manager set --key general.auto_backup --value true
```

**Reset to defaults:**
```bash
python -m utils.config_manager reset
```

**Export configuration:**
```bash
python -m utils.config_manager export --file my_config.yaml
```

**Import configuration:**
```bash
python -m utils.config_manager import --file my_config.yaml --merge
```

**Validate configuration:**
```bash
python -m utils.config_manager validate
```

#### Configuration Sections:

**General Settings:**
```yaml
general:
  auto_backup: true
  dry_run_by_default: false
  enable_logging: true
  backup_retention_days: 30
  backup_keep_count: 10
```

**Confirmations:**
```yaml
confirmations:
  deletion_enabled: true
  force_push_enabled: true
  local_deletion_enabled: true
  history_reset_enabled: true
  require_double_confirm: true
```

**Security:**
```yaml
security:
  log_security_events: true
  require_backup_verification: true
  prevent_force_push_to_main: true
  warn_uncommitted_changes: true
```

**UI Preferences:**
```yaml
ui:
  use_colors: true
  verbose_mode: false
  show_progress: true
  table_format: pretty
```

**Custom Paths:**
```yaml
paths:
  backup_root: null  # null = use default ~/.repo-manager/backups
  log_root: null     # null = use default ~/.repo-manager/logs
```

---

### 🎯 Dry-Run Mode

Preview changes before making them. Perfect for testing or verifying operations.

#### How to Use:

**In Enhanced Python CLI:**
1. Launch: `python scripts/python/repo-manager-enhanced.py`
2. Choose option 6: "Toggle Dry-Run Mode"
3. Perform operations as normal
4. See what WOULD happen without actual changes

**Via Configuration:**
```bash
python -m utils.config_manager set --key general.dry_run_by_default --value true
```

#### What Gets Shown:

```
[DRY-RUN] Would delete remote repository: owner/repo
[DRY-RUN] Would delete local directory: repo
[DRY-RUN] Would create backup: owner_repo_deletion_20250101_120000
```

All operations are logged with `dry_run: true` flag.

---

### 🐍 Enhanced Python CLI

**Location:** `scripts/python/repo-manager-enhanced.py`

Fully-featured repository manager integrating all new systems.

#### Features:
- ✅ Automatic backups before destructive operations
- ✅ Comprehensive logging and audit trail
- ✅ Dry-run mode support
- ✅ Operation history viewer
- ✅ Backup browser and restore
- ✅ Configuration management
- ✅ Rich terminal UI with colors and tables
- ✅ Error recovery and rollback

#### Launch:

```bash
# Via launcher
python launcher.py
# Choose option 4

# Or directly
python scripts/python/repo-manager-enhanced.py
```

#### Menu Options:

1. **Delete Remote Repository**
   - Shows repository details
   - Creates backup if local copy exists
   - Multiple confirmations (configurable)
   - Logs the entire operation
   - Provides restore instructions

2. **Reset Git History**
   - Always creates backup (includes full history)
   - Verifies backup integrity
   - Shows detailed progress
   - Offers force-push option
   - Logs with commit message

3. **List Remote Repositories**
   - Beautiful table output
   - Configurable limit
   - Shows visibility and update time

4. **View Operation History**
   - Last 20 operations
   - Filter by repository
   - Color-coded status
   - Timestamps

5. **List Available Backups**
   - All backups with metadata
   - Size and date information
   - Easy identification

6. **Toggle Dry-Run Mode**
   - Enable/disable preview mode
   - Visual indicator in menu
   - Logs the toggle

7. **Configuration Settings**
   - View current settings
   - Toggle common options
   - Reset to defaults

---

## Testing Infrastructure

### Test Suite

**Location:** `tests/`

Comprehensive test coverage for all core systems.

#### Test Files:
- `test_backup_manager.py` - Backup system tests (25+ tests)
- `test_logger.py` - Logging system tests (20+ tests)
- `test_config_manager.py` - Configuration tests (15+ tests)

#### Run Tests:

**All tests:**
```bash
pytest
```

**With coverage:**
```bash
pytest --cov=utils --cov-report=html
```

**Specific test file:**
```bash
pytest tests/test_backup_manager.py -v
```

**Specific test:**
```bash
pytest tests/test_backup_manager.py::TestBackupManager::test_create_backup -v
```

#### Test Coverage:

Current coverage: **~95%** of core utilities

Coverage report location: `htmlcov/index.html`

---

## CI/CD Pipeline

**Location:** `.github/workflows/ci.yml`

Automated testing and quality checks on every commit.

### Pipeline Jobs:

1. **Test Matrix**
   - Python 3.8, 3.9, 3.10, 3.11, 3.12
   - Ubuntu, Windows, macOS
   - Full pytest suite with coverage

2. **Lint & Code Quality**
   - flake8 (syntax checking)
   - black (code formatting)
   - pylint (code analysis)

3. **Security Scanning**
   - Bandit (security issues)
   - Safety (dependency vulnerabilities)

4. **Shell Script Validation**
   - ShellCheck on all bash scripts

5. **Integration Tests**
   - End-to-end workflow testing

### Status Badges:

Add to README.md:
```markdown
![CI/CD](https://github.com/username/github-repo-manager/workflows/CI%2FCD%20Pipeline/badge.svg)
```

---

## Usage Examples

### Example 1: Safe Repository Deletion

```bash
# Launch enhanced manager
python scripts/python/repo-manager-enhanced.py

# Select option 1: Delete Remote Repository
# Choose repository from list
# Review details shown
# Confirm deletion (2x confirmation)
# Backup created automatically
# Repository deleted
# Restore instructions displayed

# If needed, restore from backup
python -m utils.backup_manager list
python -m utils.backup_manager restore --backup-id <ID>
```

### Example 2: History Reset with Verification

```bash
# Ensure local copy exists
cd /path/to/repos
git clone https://github.com/owner/repo.git

# Launch manager
python scripts/python/repo-manager-enhanced.py

# Select option 2: Reset Git History
# Choose repository
# Backup created (with full history)
# Enter commit message
# Confirm operation
# History reset locally
# Option to force push

# Verify in git log
cd repo
git log --oneline
```

### Example 3: Dry-Run Testing

```bash
# Launch manager
python scripts/python/repo-manager-enhanced.py

# Enable dry-run mode (option 6)
# Perform any operation
# See what WOULD happen
# No actual changes made
# Check logs to see dry-run entries

# View dry-run logs
python -m utils.logger history --limit 10
```

### Example 4: Scheduled Backup Cleanup

Create a cron job or scheduled task:

```bash
# Linux/Mac crontab
0 2 * * 0 /usr/bin/python3 /path/to/utils/backup_manager.py cleanup --keep-days 30

# Windows Task Scheduler
python C:\path\to\utils\backup_manager.py cleanup --keep-days 30
```

### Example 5: Export Operation History

```bash
# Export last month's operations
python -m utils.logger export --output audit_jan_2025.tar.gz

# Send to compliance team
scp audit_jan_2025.tar.gz compliance@company.com:/audits/
```

---

## Troubleshooting

### Common Issues

#### Issue: "Backup failed: No space left on device"

**Solution:**
```bash
# Check backup directory size
du -sh ~/.repo-manager/backups/

# Clean up old backups
python -m utils.backup_manager cleanup --keep-days 7 --keep-count 5

# Or use custom backup location
python -m utils.config_manager set --key paths.backup_root --value /mnt/external/backups
```

#### Issue: "Configuration file corrupted"

**Solution:**
```bash
# List configuration backups
python -m utils.config_manager backups

# Restore from backup
python -m utils.config_manager restore

# Or reset to defaults
python -m utils.config_manager reset
```

#### Issue: "Tests failing on Windows"

**Solution:**
```bash
# Ensure pytest and dependencies installed
pip install -r requirements.txt

# Run with verbose output
pytest -v --tb=short

# Check specific failures
pytest tests/test_backup_manager.py -v
```

#### Issue: "Rich library not found"

**Solution:**
```bash
# Install rich
pip install rich

# Or install all dependencies
pip install -r requirements.txt
```

#### Issue: "Permission denied on backup restore"

**Solution:**
```bash
# Check permissions on restore location
ls -la /restore/path

# Restore to different location
python -m utils.backup_manager restore --backup-id <ID> --restore-path ./restored-repo
```

### Getting Help

1. **Check Logs:**
   ```bash
   cat ~/.repo-manager/logs/errors.log
   ```

2. **View Recent Operations:**
   ```bash
   python -m utils.logger history --limit 20
   ```

3. **Validate Configuration:**
   ```bash
   python -m utils.config_manager validate
   ```

4. **Run Tests:**
   ```bash
   pytest tests/ -v
   ```

5. **Open Issue:**
   https://github.com/username/github-repo-manager/issues

---

## What's Next?

### Planned Features (Future Releases):

- [ ] Bulk operations (delete/sync multiple repos)
- [ ] Repository migration tools (GitLab → GitHub, etc.)
- [ ] Analytics and insights
- [ ] Plugin system for extensibility
- [ ] Web dashboard
- [ ] Scheduled operations
- [ ] Team collaboration features
- [ ] Integration with CI/CD systems

### Contributing

We welcome contributions! See `CONTRIBUTING.md` for guidelines.

---

## Version History

**v2.0.0** (Current)
- ✅ Automatic backup system
- ✅ Structured logging and audit trail
- ✅ Configuration management
- ✅ Dry-run mode
- ✅ Enhanced Python CLI
- ✅ Comprehensive test suite
- ✅ CI/CD pipeline
- ✅ First-run setup wizard

**v1.0.0**
- Basic repository deletion
- Git history reset
- Cross-platform support
- Wiki generation

---

**Made with ❤️ and COT (Chain of Thought) thinking** 🧠✨
