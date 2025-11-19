# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- GUI version completion
- Python CLI version implementation
- Automated testing suite
- Docker containerization
- Configuration file support

## [1.0.0] - 2024-01-XX

### Added
- **Interactive GitHub Repository Deletion Script** - Core deletion functionality with safety features
- **Universal Launcher** - Cross-platform environment detection and script routing
- **PowerShell Version** - Native Windows implementation with full feature parity
- **Enhanced Bash Version** - Extended functionality with Git history reset and synchronization
- **Cross-Platform Support** - Windows, macOS, and Linux compatibility
- **Multiple Safety Mechanisms**:
  - Repository validation before operations
  - Multiple confirmation prompts
  - Uncommitted changes detection
  - Operation verification
  - Detailed progress logging
- **Git History Reset Feature** - Remove all commit history while preserving current files
- **Full Repository Synchronization** - Update all local repositories after operations
- **Comprehensive Documentation**:
  - Main project README
  - Script-specific documentation
  - Quick start guide
  - Troubleshooting guide
  - Contributing guidelines

### Features
- Repository deletion (remote and local)
- Git history reset with orphan branch technique
- Interactive repository selection with details
- Colored output for better user experience
- Environment prerequisite checking
- Automatic installation guidance
- Error handling and recovery
- Operation summaries and verification

### Supported Platforms
- **Windows**: Command Prompt, PowerShell, Git Bash, WSL
- **macOS**: Terminal (bash/zsh), PowerShell Core
- **Linux**: Bash, Zsh, Fish shells, PowerShell Core

### Prerequisites
- Git (any recent version)
- GitHub CLI (gh) with authentication
- Python 3.6+ (for launcher and future GUI)
- PowerShell 5.0+ (for PowerShell version)

### Safety Features
- Multiple confirmation prompts for destructive operations
- Repository existence validation
- Local repository status checking
- Uncommitted changes warnings
- Post-operation verification
- Graceful error handling and recovery

## [0.1.0] - Initial Development

### Added
- Basic repository deletion functionality
- GitHub CLI integration
- Initial safety mechanisms
- Command-line interface
- Basic error handling

---

## Version History Notes

### Versioning Strategy
- **Major versions (x.0.0)**: Breaking changes or major new features
- **Minor versions (x.y.0)**: New features, improvements, non-breaking changes
- **Patch versions (x.y.z)**: Bug fixes, documentation updates, minor improvements

### Release Process
1. Update CHANGELOG.md with new version
2. Tag release in Git: `git tag -a v1.0.0 -m "Release v1.0.0"`
3. Push tags: `git push origin --tags`
4. Create GitHub release with release notes
5. Update documentation as needed

### Contributing to Changelog
When contributing, please:
- Add new entries under "Unreleased" section
- Use the categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Follow the existing format and style
- Include issue/PR references where applicable

### Categories
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities
