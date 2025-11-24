# ⚡ Quick Start Guide

Get started with the enhanced GitHub Repository Manager in **2 minutes**.

---

## 🚀 Install & Setup

### Step 1: Install Dependencies

```bash
cd github-repo-manager
pip install -r requirements.txt
```

### Step 2: Run Setup Wizard

```bash
python utils/setup_wizard.py
```

Follow the prompts to configure your preferences (takes ~2 minutes).

### Step 3: You're Ready!

```bash
python launcher.py
```

---

## 🎯 Common Tasks

### Delete a Repository (Safely)

```bash
# Launch enhanced manager
python scripts/python/repo-manager-enhanced.py

# Choose option 1: Delete Remote Repository
# Select repository from list
# Review details
# Automatic backup created ✅
# Confirm deletion
# Done! (backup available for restore)
```

**Restore if needed:**
```bash
python -m utils.backup_manager list
python -m utils.backup_manager restore --backup-id <ID>
```

---

### Reset Git History

```bash
# Ensure you have local copy
git clone https://github.com/owner/repo.git

# Launch manager
python scripts/python/repo-manager-enhanced.py

# Choose option 2: Reset Git History
# Backup created automatically ✅
# Enter commit message
# Confirm
# Optionally force push
```

---

### Test Without Making Changes (Dry-Run)

```bash
# Launch manager
python scripts/python/repo-manager-enhanced.py

# Choose option 6: Toggle Dry-Run Mode
# Now perform any operation
# You'll see what WOULD happen
# No actual changes made ✅
```

---

### View Operation History

```bash
# Command line
python -m utils.logger history --limit 20

# Or in the manager
python scripts/python/repo-manager-enhanced.py
# Choose option 4
```

---

### List and Restore Backups

```bash
# List all backups
python -m utils.backup_manager list

# List for specific repo
python -m utils.backup_manager list --repo owner/repo

# Restore a backup
python -m utils.backup_manager restore --backup-id <BACKUP_ID>

# Clean up old backups
python -m utils.backup_manager cleanup --keep-days 30
```

---

### Configure Settings

```bash
# View current configuration
python -m utils.config_manager show

# Change a setting
python -m utils.config_manager set --key general.auto_backup --value true

# Reset to defaults
python -m utils.config_manager reset

# Validate configuration
python -m utils.config_manager validate
```

---

## 🎨 Choose Your Interface

### 1. Enhanced Python CLI (Recommended)
```bash
python scripts/python/repo-manager-enhanced.py
```
**Features:** Backup, logging, dry-run, history, beautiful UI

### 2. Original Python CLI
```bash
python scripts/python/repo-manager.py
```
**Features:** Simple, fast, no dependencies

### 3. Bash Script (Unix/Linux/Mac)
```bash
./repo-manager.sh
```
**Features:** Native shell, advanced features

### 4. Original Deletion Script
```bash
./delete-repo.sh
```
**Features:** Simple, focused, original tool

### 5. GUI (if Tkinter available)
```bash
python scripts/gui/repo-manager-gui.py
```
**Features:** Visual interface, mouse-driven

### 6. Universal Launcher
```bash
python launcher.py
```
**Features:** Environment detection, menu system

---

## 📚 Documentation

- **Full Features Guide:** `cat NEW_FEATURES.md`
- **Upgrade Summary:** `cat UPGRADE_SUMMARY.md`
- **Original README:** `cat README.md`
- **Troubleshooting:** See NEW_FEATURES.md § Troubleshooting

---

## 🧪 Run Tests (Optional)

```bash
# All tests
pytest

# With coverage
pytest --cov=utils --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

---

## ⚙️ Configuration Locations

- **Config:** `~/.repo-manager/config.yaml`
- **Backups:** `~/.repo-manager/backups/`
- **Logs:** `~/.repo-manager/logs/`

---

## 🔥 Pro Tips

### 1. Always Use Dry-Run First
```bash
# Enable dry-run in enhanced CLI (option 6)
# Test operations before running for real
```

### 2. Check Backups Regularly
```bash
# Weekly backup cleanup
python -m utils.backup_manager cleanup --keep-days 30
```

### 3. Review Operation History
```bash
# See what you did today
python -m utils.logger history --limit 10
```

### 4. Export Logs for Audits
```bash
# Monthly export
python -m utils.logger export --output logs_$(date +%Y%m).tar.gz
```

### 5. Share Configurations
```bash
# Export your config
python -m utils.config_manager export --file my_settings.yaml

# Import on another machine
python -m utils.config_manager import --file my_settings.yaml --merge
```

---

## ❓ Need Help?

### Quick Checks

1. **Prerequisites OK?**
   ```bash
   git --version
   gh --version
   gh auth status
   ```

2. **Config Valid?**
   ```bash
   python -m utils.config_manager validate
   ```

3. **Recent Errors?**
   ```bash
   python -m utils.logger errors --limit 10
   ```

### Get Support

- **Docs:** Read `NEW_FEATURES.md`
- **Issues:** Check `~/.repo-manager/logs/errors.log`
- **Tests:** Run `pytest -v` to verify installation

---

## 🎉 You're All Set!

Your GitHub Repository Manager is ready to use with:

✅ Automatic backups before every operation
✅ Complete logging and audit trail
✅ Dry-run mode for testing
✅ Flexible configuration
✅ Multiple interfaces (CLI, GUI, Bash)
✅ Comprehensive safety features

**Start managing repositories with confidence!** 🚀

---

**Quick Commands Reference:**

```bash
# Setup
python utils/setup_wizard.py

# Launch
python launcher.py

# Enhanced CLI
python scripts/python/repo-manager-enhanced.py

# View history
python -m utils.logger history

# List backups
python -m utils.backup_manager list

# Configure
python -m utils.config_manager show

# Test
pytest
```

---

*Happy repository managing!* ✨
