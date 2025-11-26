"""Environment detection utilities for GitSage."""

import platform
import shutil
import subprocess
import sys
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class Recommendation:
    """A recommendation for system setup."""
    priority: str  # HIGH, MEDIUM, LOW
    message: str
    action: str


class EnvironmentDetector:
    """Detects installed tools and system capabilities."""

    def __init__(self) -> None:
        self.system: str = platform.system()
        self.python_version: sys.version_info = sys.version_info
        self.detected_tools: Dict[str, Any] = {}
        self.recommendations: List[Recommendation] = []

    def check_command(self, command: str) -> bool:
        """Check if a command is available in PATH."""
        return shutil.which(command) is not None

    def detect_shells(self) -> Dict[str, bool]:
        """Detect available shells and scripting environments."""
        shells: Dict[str, bool] = {}

        if self.system != "Windows":
            shells['bash'] = self.check_command('bash')
            shells['zsh'] = self.check_command('zsh')
            shells['fish'] = self.check_command('fish')
        else:
            shells['bash'] = self.check_command('bash')  # Git Bash, WSL

        shells['powershell'] = self.check_command('powershell') or self.check_command('pwsh')

        if self.system == "Windows":
            shells['cmd'] = True

        shells['python'] = sys.executable is not None

        return shells

    def detect_git_tools(self) -> Dict[str, Any]:
        """Detect Git and GitHub CLI installation and authentication status."""
        tools: Dict[str, Any] = {}

        # Detect Git
        tools['git'] = self.check_command('git')
        if tools['git']:
            try:
                result = subprocess.run(
                    ['git', '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                tools['git_version'] = result.stdout.strip()
            except Exception:
                tools['git_version'] = "Unknown"
        else:
            tools['git_version'] = "Not installed"

        # Detect GitHub CLI
        tools['gh'] = self.check_command('gh')
        tools['gh_version'] = "Not installed"
        tools['gh_authenticated'] = False

        if tools['gh']:
            try:
                result = subprocess.run(
                    ['gh', '--version'],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=5
                )
                tools['gh_version'] = result.stdout.splitlines()[0].strip()

                # Check authentication
                try:
                    subprocess.run(
                        ['gh', 'auth', 'status'],
                        capture_output=True,
                        text=True,
                        check=True,
                        timeout=5
                    )
                    tools['gh_authenticated'] = True
                except subprocess.CalledProcessError:
                    tools['gh_authenticated'] = False
            except (FileNotFoundError, subprocess.TimeoutExpired):
                tools['gh_version'] = "Not installed"
                tools['gh_authenticated'] = False
            except Exception:
                tools['gh_version'] = "Unknown"
                tools['gh_authenticated'] = False

        return tools

    def detect_python_packages(self) -> Dict[str, bool]:
        """Detect optional Python packages."""
        packages: Dict[str, bool] = {}

        try:
            import yaml
            packages['pyyaml'] = True
        except ImportError:
            packages['pyyaml'] = False

        try:
            import rich
            packages['rich'] = True
        except ImportError:
            packages['rich'] = False

        try:
            import pytest
            packages['pytest'] = True
        except ImportError:
            packages['pytest'] = False

        return packages

    def detect_all(self) -> Dict[str, Any]:
        """Run comprehensive environment detection."""
        self.detected_tools = {
            'system': self.system,
            'python_version': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}",
            'shells': self.detect_shells(),
            'git_tools': self.detect_git_tools(),
            'python_packages': self.detect_python_packages(),
        }
        self._generate_recommendations()
        return self.detected_tools

    def _generate_recommendations(self) -> None:
        """Generate setup recommendations based on detection."""
        self.recommendations = []
        git_tools = self.detected_tools.get('git_tools', {})
        packages = self.detected_tools.get('python_packages', {})

        if not git_tools.get('git'):
            self.recommendations.append(Recommendation(
                priority='HIGH',
                message='Git is not installed',
                action='install_git'
            ))

        if not git_tools.get('gh'):
            self.recommendations.append(Recommendation(
                priority='HIGH',
                message='GitHub CLI is not installed',
                action='install_gh'
            ))
        elif not git_tools.get('gh_authenticated'):
            self.recommendations.append(Recommendation(
                priority='MEDIUM',
                message='GitHub CLI is not authenticated',
                action='auth_gh'
            ))

        if not packages.get('pyyaml'):
            self.recommendations.append(Recommendation(
                priority='LOW',
                message='PyYAML is not installed (required for wiki generator)',
                action='install_pyyaml'
            ))

        if not packages.get('rich'):
            self.recommendations.append(Recommendation(
                priority='LOW',
                message='Rich is not installed (enhanced terminal output)',
                action='install_rich'
            ))


class InstallationHelper:
    """Provides installation guidance and scripts."""

    def __init__(self, system: Optional[str] = None) -> None:
        self.system: str = system or platform.system()

    def get_git_install_info(self) -> Dict[str, str]:
        """Get Git installation instructions for current platform."""
        if self.system == "Windows":
            return {
                'method': 'Download installer',
                'url': 'https://git-scm.com/download/win',
                'instructions': 'Download and run the Git for Windows installer'
            }
        elif self.system == "Darwin":
            return {
                'method': 'Homebrew or Xcode',
                'command': 'brew install git',
                'instructions': 'Install via Homebrew or Xcode Command Line Tools'
            }
        else:
            return {
                'method': 'Package manager',
                'command': 'sudo apt install git  # Ubuntu/Debian\nsudo yum install git  # CentOS/RHEL',
                'instructions': 'Use your distribution package manager'
            }

    def get_gh_install_info(self) -> Dict[str, str]:
        """Get GitHub CLI installation instructions for current platform."""
        if self.system == "Windows":
            return {
                'method': 'Download installer or Winget',
                'url': 'https://github.com/cli/cli/releases',
                'command': 'winget install GitHub.cli',
                'instructions': 'Download installer or use winget'
            }
        elif self.system == "Darwin":
            return {
                'method': 'Homebrew',
                'command': 'brew install gh',
                'instructions': 'Install via Homebrew'
            }
        else:
            return {
                'method': 'Package manager or download',
                'url': 'https://github.com/cli/cli/releases',
                'command': 'sudo apt install gh  # Ubuntu/Debian',
                'instructions': 'Use package manager or download from GitHub'
            }

    def get_python_packages_install_info(self) -> str:
        """Get Python package installation command."""
        return "pip install -r requirements.txt"
