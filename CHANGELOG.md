# Changelog

All notable changes to GitSage are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-19

### Major Release - Honesty & Cleanup

This release represents a complete reorganization and documentation cleanup of GitSage. Previous documentation made claims about features that didn't exist. v1.0 is an honest, stable release with working core functionality.

### Added
- **Comprehensive ROADMAP.md** - Clear plan for v2.0 features
- **Accurate README.md** - Honest about what works vs. what's planned
- **Organized directory structure**:
  - `scripts/bash/` - Bash scripts organized properly
  - `scripts/git-resets/` - Git reset utilities
  - `assets/` - Images and logos organized
  - `docs/` - Documentation structure (for future organization)
  - `tests/` - Test directory prepared for v2.0
- **Updated launcher.py** - Menu only shows working features
- **Improved check_installation.py** - Only validates existing components
- **Pattern library** - Documentation patterns for future development

### Changed
- **Version set to v1.0.0** - Accurate versioning (was falsely claiming v2.0/v2.5)
- **Documentation rewritten** - All docs now reflect actual capabilities
- **File paths updated** - Scripts moved to proper locations
- **Asset naming** - Professional names without spaces

### Removed
- **Duplicate files deleted**:
  - `launcher.old.py` (duplicate of launcher.py)
  - `DELETE-REPO-README.md` (duplicate of DEL-README.md)
  - `GitSageREADME.md` (8-line stub file)
  - `DAY_5_COMPLETE.md` (outdated status update)
- **Misleading documentation removed**:
  - All references to non-existent `utils/` modules
  - Claims about "60+ tests" (no tests exist yet)
  - References to non-existent Python CLI versions
  - Claims about GUI and PowerShell versions
  - False feature claims about backups, logging, config management

### Fixed
- **launcher.py menu** - Removed broken options 2-5 that referenced missing scripts
- **check_installation.py** - No longer checks for non-existent files
- **pytest.ini** - Coverage options commented out until tests exist
- **Asset organization** - Images renamed and moved to assets/
- **Directory naming** - "GIT RESETS" → "git-resets" (no spaces)

### Core Features (What Actually Works)

✅ **Repository Deletion** (Production Ready)
- Interactive Bash script: `scripts/bash/delete-repo.sh`
- Multiple safety confirmations
- Local and remote cleanup
- Uncommitted changes detection
- Deletion verification

✅ **Repository Management** (Production Ready)
- Advanced Bash script: `scripts/bash/repo-manager.sh`
- Git operations automation
- GitHub CLI integration
- Cross-platform (requires Bash)

✅ **Wiki Generation** (Production Ready)
- Basic generator: `wiki-generator.py`
- Enhanced generator: `wiki-generator-enhanced.py`
- YAML configuration: `wiki-config.yaml`
- Template-driven page creation

✅ **Git History Reset Tools** (Production Ready)
- `scripts/git-resets/reset_git_history.sh`
- `scripts/git-resets/migrate_and_swap_repos.sh`
- `scripts/git-resets/migrate_sync_swap.sh`

✅ **Cross-Platform Launcher** (Production Ready)
- Environment detection
- Tool availability checking
- Guided setup assistance

### Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Linux | ✅ Full | Native Bash support |
| macOS | ✅ Full | Native Bash support |
| Windows | ⚠️ Partial | Requires Git Bash or WSL |
| WSL | ✅ Full | Linux environment |

### Prerequisites

**Required:**
- Git 2.0+
- GitHub CLI (gh) authenticated
- Python 3.8+
- Bash shell (Linux/macOS native, Git Bash for Windows)

**Optional:**
- PyYAML (for wiki generator)
- Rich (for enhanced terminal output)

### Not Yet Implemented (Planned for v2.0)

See [ROADMAP.md](ROADMAP.md) for details on planned features:
- Python CLI versions of repo manager
- GUI interface (Tkinter)
- PowerShell native version
- Utility modules (backup_manager, logger, config_manager, setup_wizard)
- Comprehensive test suite
- Advanced features (batch operations, templates, migration tools)

---

## [Unreleased] - Future Work

### Planned for v2.0 (Q1-Q2 2026)

See [ROADMAP.md](ROADMAP.md) for complete roadmap.

**High Priority:**
- utils/ module implementation (backup, logging, config)
- Python CLI versions
- Comprehensive test suite (>80% coverage)
- Enhanced documentation

**Medium Priority:**
- GUI interface (Tkinter)
- PowerShell native version
- Advanced features

**Low Priority:**
- Web interface
- SaaS platform
- Enterprise features

---

## Version History

### v1.0.0 (2025-11-19)
Honest, stable release with core functionality:
- Repository deletion ✅
- Repository management ✅
- Wiki generation ✅
- Git history reset ✅

### v0.x (Pre-release)
Initial development with misleading documentation. Not recommended.

---

## Notes

### What Changed from "v2.0" Claims?

Previous documentation claimed this was v2.0/v2.5 with extensive features. That was inaccurate. This is v1.0 with honest capabilities.

**What was claimed but doesn't exist:**
- utils/ modules (backup_manager, logger, config_manager, setup_wizard)
- Python CLI versions
- GUI interface
- PowerShell native version
- 60+ automated tests
- Advanced backup/logging features

**What actually works:**
- Bash scripts (deletion, management, git resets)
- Wiki generators (basic and enhanced)
- Cross-platform launcher (Python)

### Versioning Strategy

- **v1.0**: Current stable release (Bash scripts + wiki generators)
- **v2.0**: Planned expansion (Python CLIs, GUI, utils, tests)
- **v3.0**: Future (web interface, SaaS platform)

### Contributing to Changelog

When contributing:
1. Add entries under "Unreleased" section
2. Use categories: Added, Changed, Deprecated, Removed, Fixed, Security
3. Be specific about what changed and why
4. Include issue/PR references where applicable
5. Move to versioned section on release

### Categories

- **Added** - New features
- **Changed** - Changes to existing functionality
- **Deprecated** - Soon-to-be removed features
- **Removed** - Removed features
- **Fixed** - Bug fixes
- **Security** - Vulnerability fixes

---

**For detailed future plans, see [ROADMAP.md](ROADMAP.md)**
