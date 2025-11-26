#!/usr/bin/env python3
"""
GitSage - GitHub Repository Management Tools
============================================
Universal launcher for repository management, generation, and automation tools.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gitsage.__version__ import __version__, PROJECT_NAME
from gitsage.utils import Colors, EnvironmentDetector, InstallationHelper, get_logger


logger = get_logger(__name__, use_rich=True)


class UserInterface:
    """Enhanced user interface with menus and guidance."""

    def __init__(self) -> None:
        """Initialize the user interface."""
        self.detector = EnvironmentDetector()
        self.installer: Optional[InstallationHelper] = None
        self.logger = get_logger(__name__, use_rich=True)

    def print_header(self, title: str) -> None:
        """Print a styled header."""
        width = max(60, len(title) + 10)
        print(f"\n{Colors.CYAN}{'=' * width}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{title.center(width)}{Colors.END}")
        print(f"{Colors.CYAN}{'=' * width}{Colors.END}\n")

    def print_status(self, message: str, status: str = "INFO") -> None:
        """Print a status message with color coding."""
        color_map = {
            "INFO": Colors.BLUE,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "QUESTION": Colors.MAGENTA
        }
        color = color_map.get(status, Colors.WHITE)
        print(f"{color}[{status}]{Colors.END} {message}")

    def get_user_choice(self, prompt: str, choices: List[str]) -> int:
        """
        Get user choice from a list of options.

        Args:
            prompt: Prompt message
            choices: List of choice strings

        Returns:
            Index of selected choice (0-based)
        """
        while True:
            print(f"\n{Colors.QUESTION}{prompt}{Colors.END}")
            for i, choice in enumerate(choices, 1):
                print(f"  {Colors.YELLOW}{i}.{Colors.END} {choice}")

            try:
                choice_input = input(f"\n{Colors.CYAN}Enter your choice (1-{len(choices)}): {Colors.END}")
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(choices):
                    return choice_num - 1
                else:
                    self.print_status("Invalid choice. Please try again.", "ERROR")
            except ValueError:
                self.print_status("Please enter a valid number.", "ERROR")
            except EOFError:
                self.print_status("No input detected (EOF). Exiting.", "ERROR")
                sys.exit(1)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Operation cancelled by user.{Colors.END}")
                sys.exit(0)

    def show_environment_status(self, detected: Dict[str, Any]) -> None:
        """Display comprehensive environment status."""
        self.print_header("Environment Detection Results")

        print(f"{Colors.BOLD}System Information:{Colors.END}")
        print(f"  OS: {detected['system']}")
        print(f"  Python: {detected['python_version']}")

        print(f"\n{Colors.BOLD}Available Environments:{Colors.END}")
        for shell, available in detected['shells'].items():
            status = f"{Colors.GREEN}✓{Colors.END}" if available else f"{Colors.RED}✗{Colors.END}"
            print(f"  {status} {shell.capitalize()}")

        print(f"\n{Colors.BOLD}Git Tools:{Colors.END}")
        git_tools = detected['git_tools']

        if git_tools.get('git'):
            print(f"  {Colors.GREEN}✓{Colors.END} Git: {git_tools.get('git_version', 'Unknown version')}")
        else:
            print(f"  {Colors.RED}✗{Colors.END} Git: Not installed")

        if git_tools.get('gh'):
            auth_status = "Authenticated" if git_tools.get('gh_authenticated') else "Not authenticated"
            auth_color = Colors.GREEN if git_tools.get('gh_authenticated') else Colors.YELLOW
            print(f"  {Colors.GREEN}✓{Colors.END} GitHub CLI: {git_tools.get('gh_version', 'Unknown')}")
            print(f"    {auth_color}Authentication: {auth_status}{Colors.END}")
        else:
            print(f"  {Colors.RED}✗{Colors.END} GitHub CLI: Not installed")

        # Show Python packages
        if 'python_packages' in detected:
            print(f"\n{Colors.BOLD}Python Packages:{Colors.END}")
            packages = detected['python_packages']
            for pkg, installed in packages.items():
                status = f"{Colors.GREEN}✓{Colors.END}" if installed else f"{Colors.RED}✗{Colors.END}"
                print(f"  {status} {pkg}")

    def show_installation_help(self, detected: Dict[str, Any]) -> None:
        """Show installation guidance."""
        self.print_header("Installation & Setup Help")

        self.installer = InstallationHelper(detected['system'])
        git_tools = detected['git_tools']

        if not git_tools.get('git'):
            print(f"{Colors.BOLD}Installing Git:{Colors.END}")
            git_info = self.installer.get_git_install_info()
            print(f"  Method: {git_info['method']}")
            if 'url' in git_info:
                print(f"  URL: {Colors.UNDERLINE}{git_info['url']}{Colors.END}")
            if 'command' in git_info:
                print(f"  Command: {Colors.CYAN}{git_info['command']}{Colors.END}")
            print(f"  Instructions: {git_info['instructions']}\n")

        if not git_tools.get('gh'):
            print(f"{Colors.BOLD}Installing GitHub CLI:{Colors.END}")
            gh_info = self.installer.get_gh_install_info()
            print(f"  Method: {gh_info['method']}")
            if 'url' in gh_info:
                print(f"  URL: {Colors.UNDERLINE}{gh_info['url']}{Colors.END}")
            if 'command' in gh_info:
                print(f"  Command: {Colors.CYAN}{gh_info['command']}{Colors.END}")
            print(f"  Instructions: {gh_info['instructions']}\n")

        if git_tools.get('gh') and not git_tools.get('gh_authenticated'):
            print(f"{Colors.BOLD}Authenticating GitHub CLI:{Colors.END}")
            print(f"  Command: {Colors.CYAN}gh auth login{Colors.END}")
            print(f"  Follow the prompts to authenticate with GitHub\n")

        # Python packages
        if 'python_packages' in detected:
            packages = detected['python_packages']
            if not all(packages.values()):
                print(f"{Colors.BOLD}Installing Python Packages:{Colors.END}")
                print(f"  Command: {Colors.CYAN}pip install -r requirements.txt{Colors.END}")
                print(f"  This will install: PyYAML, rich, and other dependencies\n")

    def open_installation_links(self, detected: Dict[str, Any]) -> None:
        """Open installation URLs in browser."""
        self.installer = InstallationHelper(detected['system'])
        git_tools = detected['git_tools']

        links: List[Tuple[str, str]] = []

        if not git_tools.get('git'):
            git_info = self.installer.get_git_install_info()
            if 'url' in git_info:
                links.append(("Git", git_info['url']))

        if not git_tools.get('gh'):
            gh_info = self.installer.get_gh_install_info()
            if 'url' in gh_info:
                links.append(("GitHub CLI", gh_info['url']))

        if links:
            self.print_status("Opening installation links in your browser...", "INFO")
            for name, url in links:
                try:
                    webbrowser.open(url)
                    self.print_status(f"Opened {name}: {url}", "SUCCESS")
                    time.sleep(1)
                except Exception as e:
                    self.logger.error(f"Could not open {name}: {e}")
                    self.print_status(f"Could not open {name}. Manual URL: {url}", "WARNING")
        else:
            self.print_status("No installation links needed.", "INFO")

    def launch_script(self, script_path: Path, script_type: str) -> None:
        """
        Launch a specific script.

        Args:
            script_path: Path to the script
            script_type: Type of script (python, bash, powershell)
        """
        try:
            if script_type == "python":
                subprocess.run([sys.executable, str(script_path)])
            elif script_type == "bash":
                subprocess.run(["bash", str(script_path)])
            elif script_type == "powershell":
                subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(script_path)])
            else:
                self.print_status(f"Unknown script type: {script_type}", "ERROR")
                self.logger.error(f"Unknown script type: {script_type}")
        except FileNotFoundError:
            self.print_status(f"Script not found: {script_path}", "ERROR")
            self.print_status("Please ensure all script files are properly installed.", "INFO")
            self.logger.error(f"Script not found: {script_path}")
        except Exception as e:
            self.print_status(f"Error launching script: {e}", "ERROR")
            self.logger.error(f"Error launching script {script_path}: {e}")

    def main_menu(self) -> None:
        """Main application menu."""
        self.print_header(f"{PROJECT_NAME} v{__version__} - Repository Management Tools")

        self.print_status("Detecting environment...", "INFO")
        detected = self.detector.detect_all()

        self.show_environment_status(detected)

        if self.detector.recommendations:
            print(f"\n{Colors.YELLOW}Recommendations:{Colors.END}")
            for rec in self.detector.recommendations:
                priority_color = Colors.RED if rec.priority == 'HIGH' else Colors.YELLOW
                print(f"  {priority_color}{rec.priority}: {rec.message}{Colors.END}")

        # Find the project root (where scripts/ directory is)
        project_root = Path(__file__).parent.parent.parent.parent

        while True:
            choices = [
                "🗑️  Repository Deletion (Interactive Bash Script)",
                "🔧 Repository Manager (Advanced Bash Features)",
                "📚 Documentation Generator (Wiki, GitBook, Confluence & More)",
                "📝 README Generator (Awesome READMEs with Badges)",
                "🎓 Script Generator & GitHub Learning (Educational!)",
                "💾 Backup Manager (Create/Restore Repository Backups)",
                "🔄 Reset Git History (Keep Files, Fresh Start)",
                "🔀 Migrate Repository (Move/Transfer)",
                "🛠️  Install Missing Tools",
                "🔗 Open Installation Links",
                "🔍 Check Environment Again",
                "❌ Exit"
            ]

            choice = self.get_user_choice("What would you like to do?", choices)

            if choice == 0:  # Delete Repository
                script_path = project_root / "scripts" / "bash" / "delete-repo.sh"
                if script_path.exists():
                    self.print_status("Launching Interactive GitHub Repository Deletion Script...", "INFO")
                    self.launch_script(script_path, "bash")
                else:
                    self.print_status(f"Deletion script not found at {script_path}", "ERROR")

            elif choice == 1:  # Repository Manager
                script_path = project_root / "scripts" / "bash" / "repo-manager.sh"
                if script_path.exists():
                    self.print_status("Launching Advanced Repository Manager (Bash)...", "INFO")
                    self.launch_script(script_path, "bash")
                else:
                    self.print_status(f"Repository manager not found at {script_path}", "ERROR")

            elif choice == 2:  # Documentation Generator
                script_path = project_root / "wiki-generator.py"
                if script_path.exists():
                    self.print_status("Launching Documentation Generator...", "INFO")
                    self.print_status("Generate GitHub Wiki, GitBook, Confluence & more!", "INFO")
                    self.launch_script(script_path, "python")
                else:
                    self.print_status("Documentation generator not found.", "ERROR")

            elif choice == 3:  # README Generator
                script_path = project_root / "readme-generator.py"
                if script_path.exists():
                    self.print_status("Launching README Generator...", "INFO")
                    self.launch_script(script_path, "python")
                else:
                    self.print_status("README generator not found.", "ERROR")

            elif choice == 4:  # Script Generator & GitHub Learning
                script_path = project_root / "script-generator.py"
                if script_path.exists():
                    self.print_status("Launching Script Generator & GitHub Learning...", "INFO")
                    self.print_status("Generate custom automation scripts while learning GitHub!", "INFO")
                    self.launch_script(script_path, "python")
                else:
                    self.print_status("Script generator not found.", "ERROR")

            elif choice == 5:  # Backup Manager
                script_path = project_root / "backup-manager.py"
                if script_path.exists():
                    self.print_status("Launching Backup Manager...", "INFO")
                    self.print_status("Create, restore, and manage repository backups", "INFO")
                    self.launch_script(script_path, "python")
                else:
                    self.print_status("Backup manager not found.", "ERROR")

            elif choice == 6:  # Reset Git History
                script_path = project_root / "scripts" / "git-resets" / "reset_git_history.sh"
                if script_path.exists():
                    self.print_status("Launching Git History Reset Tool...", "WARNING")
                    self.print_status("This will DELETE all commit history while keeping files.", "WARNING")
                    self.launch_script(script_path, "bash")
                else:
                    self.print_status("Git history reset script not found.", "ERROR")

            elif choice == 7:  # Migrate Repository
                script_path = project_root / "scripts" / "git-resets" / "migrate_and_swap_repos.sh"
                if script_path.exists():
                    self.print_status("Launching Repository Migration Tool...", "INFO")
                    self.launch_script(script_path, "bash")
                else:
                    self.print_status("Repository migration script not found.", "ERROR")

            elif choice == 8:  # Install tools
                self.show_installation_help(detected)

            elif choice == 9:  # Open links
                self.open_installation_links(detected)

            elif choice == 10:  # Re-check
                detected = self.detector.detect_all()
                self.show_environment_status(detected)

            elif choice == 11:  # Exit
                self.print_status("Thank you for using GitSage!", "SUCCESS")
                sys.exit(0)


def main() -> None:
    """Main entry point."""
    try:
        ui = UserInterface()
        ui.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()
