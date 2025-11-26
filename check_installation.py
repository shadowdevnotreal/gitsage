#!/usr/bin/env python3
"""
GitSage v2.2.0 - Installation and System Check
============================================
Verifies that core components are properly installed and working.
"""

import sys
import subprocess
from pathlib import Path


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def check_item(name, check_func, critical=True):
    """Check an item and print status"""
    try:
        result = check_func()
        if result[0]:
            print(f"{Colors.GREEN}✓{Colors.END} {name}: {result[1]}")
            return True
        else:
            symbol = Colors.RED + "✗" if critical else Colors.YELLOW + "⚠"
            print(f"{symbol}{Colors.END} {name}: {result[1]}")
            return not critical
    except Exception as e:
        symbol = Colors.RED + "✗" if critical else Colors.YELLOW + "⚠"
        print(f"{symbol}{Colors.END} {name}: {str(e)}")
        return not critical


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version >= (3, 8):
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor} (requires 3.8+)"


def check_git():
    """Check Git installation"""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.strip()
    except:
        return False, "Not installed"


def check_gh_cli():
    """Check GitHub CLI"""
    gh = "gh.exe" if sys.platform == "win32" else "gh"
    try:
        result = subprocess.run(
            [gh, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip().split()[2]
        return True, f"gh {version}"
    except:
        return False, "Not installed"


def check_gh_auth():
    """Check GitHub CLI authentication"""
    gh = "gh.exe" if sys.platform == "win32" else "gh"
    try:
        result = subprocess.run(
            [gh, "auth", "status"],
            capture_output=True,
            text=True,
            check=False
        )
        if result.returncode == 0:
            return True, "Authenticated"
        return False, "Not authenticated"
    except:
        return False, "Cannot check"


def check_python_package(package_name):
    """Check if Python package is installed"""
    try:
        __import__(package_name)
        return True, "Installed"
    except ImportError:
        return False, "Not installed"


def check_file_exists(file_path):
    """Check if file exists"""
    if Path(file_path).exists():
        return True, "Found"
    return False, "Not found"


def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}GitSage v2.2.0 - Installation Check{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

    all_ok = True

    # Core Requirements
    print(f"{Colors.BOLD}Core Requirements:{Colors.END}")
    all_ok &= check_item("Python Version", check_python_version, critical=True)
    all_ok &= check_item("Git", check_git, critical=True)
    all_ok &= check_item("GitHub CLI", check_gh_cli, critical=True)
    all_ok &= check_item("GitHub Auth", check_gh_auth, critical=False)

    # Python Packages
    print(f"\n{Colors.BOLD}Python Packages:{Colors.END}")
    all_ok &= check_item("PyYAML", lambda: check_python_package("yaml"), critical=False)
    all_ok &= check_item("Rich", lambda: check_python_package("rich"), critical=False)

    # Core Scripts
    print(f"\n{Colors.BOLD}Core Scripts:{Colors.END}")
    all_ok &= check_item(
        "Main Launcher",
        lambda: check_file_exists("launcher.py"),
        critical=True
    )
    all_ok &= check_item(
        "Repository Manager (Bash)",
        lambda: check_file_exists("scripts/bash/repo-manager.sh"),
        critical=True
    )
    all_ok &= check_item(
        "Repository Deletion (Bash)",
        lambda: check_file_exists("scripts/bash/delete-repo.sh"),
        critical=True
    )
    all_ok &= check_item(
        "Wiki Generator (Basic)",
        lambda: check_file_exists("wiki-generator.py"),
        critical=False
    )
    all_ok &= check_item(
        "Wiki Generator (Enhanced)",
        lambda: check_file_exists("wiki-generator.py"),
        critical=False
    )

    # Configuration
    print(f"\n{Colors.BOLD}Configuration:{Colors.END}")
    all_ok &= check_item(
        "Requirements File",
        lambda: check_file_exists("requirements.txt"),
        critical=False
    )
    all_ok &= check_item(
        "Wiki Config",
        lambda: check_file_exists("wiki-config.yaml"),
        critical=False
    )

    # Documentation
    print(f"\n{Colors.BOLD}Documentation:{Colors.END}")
    check_item("README", lambda: check_file_exists("README.md"), critical=False)
    check_item("Contributing Guide", lambda: check_file_exists("CONTRIBUTING.md"), critical=False)
    check_item("License", lambda: check_file_exists("LICENSE"), critical=False)

    # Summary
    print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
    if all_ok:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ All critical checks passed!{Colors.END}")
        print(f"\n{Colors.GREEN}GitSage v2.2.0 is properly installed and ready to use.{Colors.END}")
        print(f"\n{Colors.BOLD}Next steps:{Colors.END}")
        print(f"  1. Launch GitSage: {Colors.BLUE}python launcher.py{Colors.END}")
        print(f"  2. Or run directly: {Colors.BLUE}bash scripts/bash/repo-manager.sh{Colors.END}")
        print(f"  3. For deletion: {Colors.BLUE}bash scripts/bash/delete-repo.sh{Colors.END}")
        print(f"  4. Read documentation: {Colors.BLUE}cat README.md{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ Some critical checks failed!{Colors.END}")
        print(f"\n{Colors.YELLOW}Please fix the issues above and try again.{Colors.END}")
        print(f"\n{Colors.BOLD}Common fixes:{Colors.END}")
        print(f"  • Install dependencies: {Colors.BLUE}pip install -r requirements.txt{Colors.END}")
        print(f"  • Install Git: {Colors.BLUE}https://git-scm.com/{Colors.END}")
        print(f"  • Install GitHub CLI: {Colors.BLUE}https://cli.github.com/{Colors.END}")
        print(f"  • Authenticate: {Colors.BLUE}gh auth login{Colors.END}")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Check cancelled.{Colors.END}")
        sys.exit(1)
