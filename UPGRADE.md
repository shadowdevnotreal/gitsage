# GitSage v2.2 - Upgrade Guide

## What's New

GitSage v2.2 includes major architectural improvements while maintaining full backwards compatibility. All your existing workflows will continue to work!

### Major Improvements

1. **Modular Architecture** - Professional src/ layout with organized modules
2. **Type Safety** - Comprehensive type hints throughout codebase
3. **Centralized Configuration** - Single config file for all settings
4. **Professional Logging** - Structured logging with audit trails
5. **Input Validation** - Enhanced security and error prevention
6. **CI/CD Pipeline** - Automated testing across platforms
7. **Version Consistency** - All files now show v2.2.0

## For Users - No Action Required!

**Your existing commands still work:**

```bash
# Old way (still works)
python launcher.py
python script-generator.py
python wiki-generator.py
python backup-manager.py

# Bash wrapper (still works)
./gitsage launch
./gitsage script
./gitsage wiki
./gitsage backup
```

## New Features You Can Use

### 1. Improved Environment Detection

The launcher now detects more information:
- Python packages (PyYAML, rich, pytest)
- Better recommendations
- More helpful error messages

### 2. Configuration File

Create `~/.gitsage/config.yaml` to customize:

```yaml
backup:
  max_backups_per_repo: 20        # Default: 10
  retention_days: 60              # Default: 30

logging:
  level: DEBUG                    # Default: INFO
  console_output: true
  file_output: true

security:
  require_confirmations: true     # Default: true
  backup_before_delete: true      # Default: true
```

### 3. Log Files

Operations now create detailed logs:
- Location: `~/.gitsage/logs/`
- Automatic rotation
- Helpful for troubleshooting

### 4. Better Error Messages

```
# Before
Error: Repository not found

# After
✗ Repository not found: /path/to/repo
  Not a Git repository (no .git directory found)
  Solution: Run 'git init' or check the path
```

## For Developers

### Installing in Development Mode

```bash
# Clone the repository
git clone https://github.com/shadowdevnotreal/gitsage.git
cd gitsage

# Install in development mode with all dev dependencies
pip install -e ".[dev]"

# Now you can import from anywhere
python -c "from gitsage import __version__; print(__version__)"
```

### New Import Paths

```python
# Version information
from gitsage.__version__ import __version__, PROJECT_NAME

# Utilities
from gitsage.utils import (
    Colors,
    EnvironmentDetector,
    Validators,
    get_logger
)

# Configuration
from gitsage.config import get_config

# CLI
from gitsage.cli.launcher import UserInterface
```

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=src/gitsage --cov-report=term

# Run with coverage report
pytest --cov=src/gitsage --cov-report=html
open htmlcov/index.html

# Run linters
black --check src/ tests/
isort --check-only src/ tests/
flake8 src/ tests/

# Run type checker
mypy src/gitsage
```

### Pre-commit Checks

Before committing:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Check types
mypy src/gitsage

# Run tests
pytest

# Check everything passes
black --check src/ tests/ && \
  isort --check-only src/ tests/ && \
  flake8 src/ tests/ && \
  mypy src/gitsage && \
  pytest --cov=src/gitsage
```

## File Changes

### New Files

```
src/
└── gitsage/
    ├── __init__.py
    ├── __version__.py              # NEW: Centralized version
    ├── py.typed                    # NEW: Type hints marker
    ├── cli/
    │   ├── __init__.py
    │   └── launcher.py             # NEW: Refactored launcher
    ├── utils/
    │   ├── __init__.py
    │   ├── colors.py               # NEW: ANSI colors
    │   ├── environment.py          # NEW: Environment detection
    │   ├── validators.py           # NEW: Input validation
    │   └── logger.py               # NEW: Logging system
    ├── config/
    │   ├── __init__.py
    │   └── settings.py             # NEW: Configuration management
    └── utils/
        └── exceptions.py           # NEW: Custom exceptions

.github/
└── workflows/
    ├── ci.yml                      # NEW: CI pipeline
    └── release.yml                 # NEW: Release automation

docs/development/
└── V2.2-ARCHITECTURE.md            # NEW: Architecture docs

launcher_new.py                     # NEW: New entry point
```

### Modified Files

- `pyproject.toml` - Updated version (2.2.0), scripts, mypy config
- `gitsage` - Updated version string
- `gitsage.bat` - Updated version string
- `check_installation.py` - Updated version string

### Unchanged Files

All bash scripts, templates, and documentation remain unchanged and fully functional.

## Compatibility

### Python Versions

Tested on:
- ✅ Python 3.8
- ✅ Python 3.9
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12

### Operating Systems

Tested on:
- ✅ Ubuntu Linux
- ✅ macOS
- ✅ Windows (with Git Bash for bash scripts)

### Dependencies

**Required:**
- Python >= 3.8
- PyYAML >= 6.0
- rich >= 13.0.0

**Optional (for development):**
- pytest >= 7.0.0
- black >= 23.0.0
- mypy >= 1.0.0
- isort >= 5.12.0
- flake8 >= 6.0.0

## Migration Checklist

For existing users:

- [ ] Pull latest changes
- [ ] Install updated dependencies: `pip install -r requirements.txt`
- [ ] (Optional) Install dev dependencies: `pip install -e ".[dev]"`
- [ ] (Optional) Create config file: `~/.gitsage/config.yaml`
- [ ] Test your workflows still work
- [ ] Enjoy improved error messages and logging!

## Troubleshooting

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'gitsage'`

**Solution:**
```bash
# If running from source
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or install in development mode
pip install -e .
```

### Version Mismatch

**Problem:** Different tools showing different versions

**Solution:** All files now use centralized version from `src/gitsage/__version__.py`

```bash
# Check version
python -c "import sys; sys.path.insert(0, 'src'); from gitsage import __version__; print(__version__)"
```

### Tests Failing

**Problem:** Tests not finding modules

**Solution:**
```bash
# Install in editable mode
pip install -e ".[dev]"

# Run from project root
pytest
```

## Support

- **Issues:** https://github.com/shadowdevnotreal/gitsage/issues
- **Documentation:** See `docs/` directory
- **Architecture:** See `docs/development/V2.2-ARCHITECTURE.md`

## Rollback (if needed)

If you encounter issues:

```bash
# Check out previous version
git checkout v2.1.0

# Or use old launcher directly
python launcher.py  # Still works in v2.2!
```

## What's Next (v2.3+)

Planned for future releases:
- Async operations for faster bulk processing
- Plugin system for custom generators
- REST API for programmatic access
- Enhanced GitHub Actions integration
- GitLab and Bitbucket support

---

**Enjoy GitSage v2.2!** 🚀

We've made the codebase more professional while keeping everything you love about GitSage working exactly as before.
