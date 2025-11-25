#!/usr/bin/env python3
"""
GitSage Uninstaller

Safely removes all GitSage-created files and directories from your system.
This script will:
  1. Remove user data directory (~/.gitsage/)
  2. Remove generated content directories (./generated-*)
  3. Optionally remove Python dependencies
  4. Show detailed removal report

Platform Support: Windows, macOS, Linux, WSL
"""

import sys
import os
import shutil
from pathlib import Path
from typing import List, Tuple

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def disable():
        """Disable colors on Windows or if not TTY"""
        if not sys.stdout.isatty() or os.name == 'nt':
            Colors.HEADER = ''
            Colors.BLUE = ''
            Colors.CYAN = ''
            Colors.GREEN = ''
            Colors.YELLOW = ''
            Colors.RED = ''
            Colors.ENDC = ''
            Colors.BOLD = ''
            Colors.UNDERLINE = ''


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 60}{Colors.ENDC}\n")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.ENDC}")


def get_user_confirmation(prompt: str) -> bool:
    """Get yes/no confirmation from user"""
    while True:
        response = input(f"{Colors.YELLOW}{prompt} (yes/no): {Colors.ENDC}").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print_warning("Please enter 'yes' or 'no'")


def get_size_mb(path: Path) -> float:
    """Calculate total size of directory in MB"""
    total = 0
    try:
        if path.is_file():
            return path.stat().st_size / (1024 * 1024)
        elif path.is_dir():
            for item in path.rglob('*'):
                if item.is_file():
                    total += item.stat().st_size
    except (OSError, PermissionError):
        pass
    return total / (1024 * 1024)


def find_gitsage_directories() -> Tuple[List[Path], List[Path]]:
    """
    Find all GitSage-related directories

    Returns:
        Tuple of (user_data_dirs, generated_content_dirs)
    """
    user_data_dirs = []
    generated_content_dirs = []

    # 1. User data directory
    gitsage_home = Path.home() / '.gitsage'
    if gitsage_home.exists():
        user_data_dirs.append(gitsage_home)

    # 2. Generated content directories (check current directory and common locations)
    current_dir = Path.cwd()

    # Check current directory
    for pattern in ['generated-scripts', 'generated-docs', 'generated-wikis']:
        gen_dir = current_dir / pattern
        if gen_dir.exists():
            generated_content_dirs.append(gen_dir)

    # Check if we're inside a GitSage installation
    gitsage_root = current_dir
    if (gitsage_root / 'launcher.py').exists() and (gitsage_root / 'gitsage').exists():
        for pattern in ['generated-scripts', 'generated-docs', 'generated-wikis']:
            gen_dir = gitsage_root / pattern
            if gen_dir.exists() and gen_dir not in generated_content_dirs:
                generated_content_dirs.append(gen_dir)

    return user_data_dirs, generated_content_dirs


def show_removal_plan(user_data_dirs: List[Path], generated_content_dirs: List[Path]):
    """Display what will be removed"""
    print_header("GitSage Uninstallation Plan")

    total_size = 0

    if user_data_dirs:
        print(f"{Colors.BOLD}User Data Directories:{Colors.ENDC}")
        for dir_path in user_data_dirs:
            size_mb = get_size_mb(dir_path)
            total_size += size_mb
            print(f"  📁 {dir_path}")
            print(f"     Size: {size_mb:.2f} MB")

            # Show contents
            try:
                subdirs = [d for d in dir_path.iterdir() if d.is_dir()]
                files = [f for f in dir_path.iterdir() if f.is_file()]
                if subdirs:
                    print(f"     Subdirectories: {len(subdirs)}")
                if files:
                    print(f"     Files: {len(files)}")
            except (OSError, PermissionError):
                print(f"     {Colors.YELLOW}(Unable to read contents){Colors.ENDC}")
        print()
    else:
        print(f"{Colors.GREEN}No user data directories found{Colors.ENDC}\n")

    if generated_content_dirs:
        print(f"{Colors.BOLD}Generated Content Directories:{Colors.ENDC}")
        for dir_path in generated_content_dirs:
            size_mb = get_size_mb(dir_path)
            total_size += size_mb
            print(f"  📁 {dir_path}")
            print(f"     Size: {size_mb:.2f} MB")

            # Show file count
            try:
                file_count = sum(1 for _ in dir_path.rglob('*') if _.is_file())
                print(f"     Files: {file_count}")
            except (OSError, PermissionError):
                print(f"     {Colors.YELLOW}(Unable to count files){Colors.ENDC}")
        print()
    else:
        print(f"{Colors.GREEN}No generated content directories found{Colors.ENDC}\n")

    print(f"{Colors.BOLD}Total disk space to be freed: {total_size:.2f} MB{Colors.ENDC}\n")

    # Show what WON'T be removed
    print(f"{Colors.BOLD}What Will NOT Be Removed:{Colors.ENDC}")
    print(f"  • GitSage source code (repository files)")
    print(f"  • Python packages (use 'pip uninstall' separately)")
    print(f"  • Git and GitHub CLI installations")
    print(f"  • Any repositories you've created or managed\n")


def remove_directory(path: Path) -> bool:
    """
    Safely remove a directory

    Returns:
        True if successful, False otherwise
    """
    try:
        if path.exists():
            shutil.rmtree(path)
            return True
        else:
            print_warning(f"Directory not found: {path}")
            return False
    except PermissionError:
        print_error(f"Permission denied: {path}")
        print_info("Try running with elevated privileges (sudo on Unix, Admin on Windows)")
        return False
    except Exception as e:
        print_error(f"Error removing {path}: {str(e)}")
        return False


def uninstall_python_packages():
    """Optionally uninstall Python dependencies"""
    print_header("Python Dependencies")

    packages = ['pyyaml', 'rich', 'pytest']

    print("GitSage uses the following Python packages:")
    for pkg in packages:
        print(f"  • {pkg}")

    print(f"\n{Colors.YELLOW}Note: These packages may be used by other applications.{Colors.ENDC}")

    if get_user_confirmation("Do you want to uninstall these Python packages?"):
        print_info("Uninstalling Python packages...")
        for pkg in packages:
            print(f"  Removing {pkg}...")
            os.system(f"{sys.executable} -m pip uninstall -y {pkg} > /dev/null 2>&1")
        print_success("Python packages uninstalled")
    else:
        print_info("Keeping Python packages installed")


def show_manual_cleanup():
    """Show instructions for manual cleanup"""
    print_header("Manual Cleanup (Optional)")

    print("If you want to completely remove GitSage, you may also want to:")
    print()
    print("1. Remove the GitSage repository:")
    print(f"   {Colors.CYAN}rm -rf /path/to/gitsage{Colors.ENDC}")
    print()
    print("2. Remove any GitSage aliases from your shell config:")
    print(f"   {Colors.CYAN}# Check ~/.bashrc, ~/.zshrc, or ~/.profile{Colors.ENDC}")
    print()
    print("3. Remove from PATH if added:")
    print(f"   {Colors.CYAN}# Edit your shell config file{Colors.ENDC}")
    print()


def main():
    """Main uninstaller function"""
    # Disable colors on Windows
    if os.name == 'nt':
        Colors.disable()

    print_header("GitSage Uninstaller")

    print(f"{Colors.BOLD}This will remove all GitSage-created files from your system.{Colors.ENDC}\n")

    # Find what needs to be removed
    user_data_dirs, generated_content_dirs = find_gitsage_directories()

    # Show removal plan
    show_removal_plan(user_data_dirs, generated_content_dirs)

    # Get confirmation
    if not user_data_dirs and not generated_content_dirs:
        print_success("No GitSage data found on your system!")
        print_info("GitSage may have already been uninstalled, or was never run.")

        if get_user_confirmation("Do you want to see manual cleanup instructions?"):
            show_manual_cleanup()

        return

    print(f"{Colors.RED}{Colors.BOLD}⚠ WARNING: This action cannot be undone!{Colors.ENDC}")
    print(f"{Colors.YELLOW}Make sure you have backed up any important generated scripts or documentation.{Colors.ENDC}\n")

    if not get_user_confirmation("Are you sure you want to proceed with uninstallation?"):
        print_info("Uninstallation cancelled")
        return

    # Perform removal
    print_header("Removing GitSage Data")

    removed_count = 0
    failed_count = 0

    # Remove user data directories
    if user_data_dirs:
        print(f"{Colors.BOLD}Removing user data...{Colors.ENDC}")
        for dir_path in user_data_dirs:
            print(f"  Removing {dir_path}...")
            if remove_directory(dir_path):
                print_success(f"Removed: {dir_path}")
                removed_count += 1
            else:
                failed_count += 1
        print()

    # Remove generated content directories
    if generated_content_dirs:
        print(f"{Colors.BOLD}Removing generated content...{Colors.ENDC}")

        # Ask about each generated directory
        for dir_path in generated_content_dirs:
            print(f"\nFound: {dir_path}")
            file_count = sum(1 for _ in dir_path.rglob('*') if _.is_file())
            print(f"  Contains {file_count} files")

            if get_user_confirmation(f"Remove this directory?"):
                if remove_directory(dir_path):
                    print_success(f"Removed: {dir_path}")
                    removed_count += 1
                else:
                    failed_count += 1
            else:
                print_info(f"Keeping: {dir_path}")
        print()

    # Python packages
    if get_user_confirmation("Do you want to check Python dependencies?"):
        uninstall_python_packages()

    # Summary
    print_header("Uninstallation Complete")

    if removed_count > 0:
        print_success(f"Successfully removed {removed_count} director{'y' if removed_count == 1 else 'ies'}")

    if failed_count > 0:
        print_warning(f"Failed to remove {failed_count} director{'y' if failed_count == 1 else 'ies'}")
        print_info("You may need elevated privileges to remove some directories")

    print()
    print(f"{Colors.BOLD}Thank you for using GitSage!{Colors.ENDC}")
    print(f"We hope it helped you automate your GitHub workflows and learn something new.\n")

    if get_user_confirmation("Would you like to see manual cleanup instructions?"):
        show_manual_cleanup()

    print(f"\n{Colors.CYAN}If you have feedback or found issues, please let us know:{Colors.ENDC}")
    print(f"{Colors.CYAN}https://github.com/shadowdevnotreal/gitsage/issues{Colors.ENDC}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Uninstallation cancelled by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
