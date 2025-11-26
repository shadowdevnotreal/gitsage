# Changelog

All notable changes to GitSage are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.0] - 2025-11-26

### Major Enhancement - Interactive Wizard & Educational Features

This release transforms GitSage from config-based to interactive, educational, and automated! Major focus on teaching GitHub best practices while making repository management easier than ever.

### Added

#### Interactive README Generator
- **Interactive Wizard Mode** (`--interactive`) - No config files needed!
  - Smart project detection - automatically detects project type, languages, frameworks
  - Live codebase analysis - detects technologies and suggests appropriate templates
  - Badge selection wizard - choose from 10+ badge types interactively
  - Feature list builder - guided feature entry with prompts
  - Auto-detects GitHub username and repo name from git remote
  - Optional config file saving for reuse
- **Health Check Mode** (`--health-check`) - Shows repository health score
- **Analysis Mode** (`--analyze`) - Detailed project analysis and detection results
- **GitHub Stats Integration** - Auto-generates badges, stats cards, and visualizations

#### Repository Health & Scoring System
- **RepositoryHealthChecker** (`src/gitsage/utils/repo_health.py`)
  - Analyzes 13 aspects of repository health
  - Scores out of 100 points across multiple categories
  - Identifies critical issues, quick wins, and recommendations
  - Educational messages explaining WHY each check matters
  - Estimates fix time for each issue
  - Links to GitHub documentation for learning
- **BeautificationScorer** (`src/gitsage/utils/beautification_scorer.py`)
  - Gamified scoring system with 5 levels (Beginner to Master)
  - Achievement system (8 unlockable achievements)
  - Category breakdown (Documentation, Community, Automation, Security, Discoverability, Engagement)
  - Progress tracking and next milestone visualization
  - Prioritized improvement suggestions
- **ProjectDetector** (`src/gitsage/utils/project_detector.py`)
  - Auto-detects project type from codebase (10 types supported)
  - Analyzes languages, frameworks, and technologies
  - Smart template recommendations
  - Generates actionable suggestions for improvements
- **GitHubStatsGenerator** (`src/gitsage/utils/github_stats.py`)
  - Generates 15+ badge types (shields.io integration)
  - Creates comprehensive stats sections with graphs
  - GitHub Stats cards integration
  - Language statistics visualization
  - Trophy and contribution graph support

#### Enhanced Wiki Generator
- **GitHub Wiki Setup Instructions** - Prominent, educational guidance
  - Step-by-step instructions for enabling Wiki in GitHub
  - Automatically shows after wiki generation
  - Includes repository-specific URLs
  - Links to official GitHub documentation
  - Estimated setup time (30 seconds)

#### One-Command Repository Setup
- **Repository Setup Wizard** (`python launcher.py --setup-repo`)
  - Complete repository setup in one command
  - 6-step guided process:
    1. Project analysis and detection
    2. Repository health check and scoring
    3. Interactive README generation
    4. Documentation wiki generation
    5. GitHub features checklist
    6. Setup completion summary
  - Integrated into main launcher menu
  - Educational feedback at each step

### Enhanced

#### readme-generator.py
- Now supports both config-based and interactive modes
- Auto-detection of project information from codebase
- Smart defaults based on detected project type
- Integration with all new utility modules
- Improved badge generation
- Better template selection

#### wiki-generator.py
- Added prominent GitHub Wiki setup instructions
- Instructions shown automatically after generation
- Repository-specific guidance
- Educational links and time estimates

#### launcher.py
- Added Repository Setup Wizard option
- Enhanced help documentation
- Better error handling
- Integrated new features into main menu

### Technical Improvements
- **New Utility Modules** in `src/gitsage/utils/`:
  - `project_detector.py` - Smart project type detection
  - `repo_health.py` - Repository health analysis
  - `beautification_scorer.py` - Gamified scoring system
  - `github_stats.py` - GitHub stats and badges
- **Module Exports** - Updated `__init__.py` to export new utilities
- **Rich Integration** - Enhanced UI with Rich library for better UX
- **Educational Focus** - All tools now teach GitHub best practices

### User Experience
- **No Config Files Needed** - Interactive mode removes YAML editing requirement
- **Educational Feedback** - Every tool explains WHY features matter
- **Visual Progress** - Rich panels, tables, and progress bars throughout
- **Smart Defaults** - Auto-detected values for faster setup
- **Gamification** - Achievements and levels make improvement fun

### Documentation
- Enhanced README with new feature descriptions
- Updated help messages across all tools
- Added usage examples for new modes
- Improved error messages with actionable guidance

## [1.0.0] - 2025-11-19

### Major Release - Honesty & Cleanup

This release represents a complete reorganization and documentation cleanup of GitSage. Previous documentation made claims about features that didn't exist. v1.0 is an honest, stable release with working core functionality.

### Added
- **Comprehensive planning** - Clear future development direction
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
- Wiki generator: `wiki-generator.py`
- YAML configuration support
- Template-driven page creation
- Multiple output formats

✅ **Git History Reset Tools** (Production Ready)
- `scripts/git-resets/reset_git_history.sh`
- `scripts/git-resets/migrate_repository.sh` (unified migration tool)

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

### Not Yet Implemented (Planned for Future)

Planned features:
- PowerShell native version (lower priority)
- Advanced features (batch operations, templates)

### Implemented in v2.0+

- ✅ Python CLI launcher with environment detection
- ✅ Web interface (Flask-based) replacing GUI concept
- ✅ Utility modules (backup_manager, logger, config_manager)
- ✅ Comprehensive test suite
- ✅ Script generator with educational content

---

## [Unreleased] - Future Work

### Future Development

**Completed:**
- ✅ utils/ module implementation (backup, logging, config)
- ✅ Python CLI launcher
- ✅ Comprehensive test suite
- ✅ Enhanced documentation
- ✅ Web interface (Flask-based)
- ✅ PowerShell installer (install.ps1 for Windows)
- ✅ PowerShell repository management scripts (COMPLETE IMPLEMENTATION!)
  - Delete-Repository.ps1 - Safe repository deletion
  - Manage-Repository.ps1 - Interactive repository manager
  - Reset-GitHistory.ps1 - Git history reset tool
  - Migrate-Repository.ps1 - Repository migration tool

**Remaining:**
- Advanced automation features (medium priority)
- Enterprise features (low priority)

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

**See README.md for current feature status and GitHub Issues for planned features.**
