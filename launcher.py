#!/usr/bin/env python3
"""
GitSage v1.0 - GitHub Repository Management Tools
=================================================
Universal launcher for repository deletion, management, and wiki generation.
Detects your environment and provides appropriate tools.
"""

import os
import sys
import platform
import subprocess
import shutil
import webbrowser
from pathlib import Path
import json
import time


class Colors:
    """ANSI color codes for cross-platform terminal colors"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    QUESTION = '\033[96m'
    QUESTION_MAGENTA = '\033[95m'
    QUESTION_YELLOW = '\033[93m'
    QUESTION_BLUE = '\033[94m'

    @classmethod
    def disable_on_windows(cls):
        """Disable colors on older Windows terminals"""
        if platform.system() == "Windows" and not os.environ.get('TERM'):
            for attr in dir(cls):
                if not attr.startswith('_') and attr != 'disable_on_windows':
                    setattr(cls, attr, '')

# Initialize colors
if platform.system() == "Windows":
    try:
        os.system('color')
    except Exception:
        Colors.disable_on_windows()


class EnvironmentDetector:
    """Detects installed tools and system capabilities"""

    def __init__(self):
        self.system = platform.system()
        self.python_version = sys.version_info
        self.detected_tools = {}
        self.recommendations = []

    def check_command(self, command):
        """Check if a command is available"""
        return shutil.which(command) is not None

    def detect_shells(self):
        """Detect available shells and scripting environments"""
        shells = {}

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

    def detect_git_tools(self):
        """Detect Git and GitHub CLI"""
        tools = {}

        tools['git'] = self.check_command('git')
        if tools['git']:
            try:
                result = subprocess.run(['git', '--version'], capture_output=True, text=True)
                tools['git_version'] = result.stdout.strip()
            except Exception:
                tools['git_version'] = "Unknown"
        else:
            tools['git_version'] = "Not installed"

        tools['gh'] = self.check_command('gh')
        tools['gh_version'] = "Not installed"
        tools['gh_authenticated'] = False
        if tools['gh']:
            try:
                result = subprocess.run(['gh', '--version'], capture_output=True, text=True, check=True)
                tools['gh_version'] = result.stdout.splitlines()[0].strip()
                try:
                    auth_result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True, check=True)
                    tools['gh_authenticated'] = True
                except subprocess.CalledProcessError as e:
                    tools['gh_authenticated'] = False
                    print(f"{Colors.YELLOW}[WARNING] GitHub authentication failed:{Colors.END}")
                    print(f"{Colors.RED}{e.stderr.strip() or 'Unknown error'}{Colors.END}")
            except FileNotFoundError:
                tools['gh_version'] = "Not installed"
                tools['gh_authenticated'] = False
                print(f"{Colors.RED}[ERROR] GitHub CLI (gh) is not found in PATH.{Colors.END}")
            except Exception:
                tools['gh_version'] = "Unknown"
                tools['gh_authenticated'] = False

        return tools

    def detect_gui_capabilities(self):
        """Detect GUI framework availability"""
        gui = {}
        try:
            import tkinter
            gui['tkinter'] = True
        except ImportError:
            gui['tkinter'] = False

        if self.system != "Windows":
            gui['display'] = bool(os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'))
        else:
            gui['display'] = True

        return gui

    def detect_all(self):
        """Run comprehensive environment detection"""
        self.detected_tools = {
            'system': self.system,
            'python_version': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}",
            'shells': self.detect_shells(),
            'git_tools': self.detect_git_tools(),
            'gui': self.detect_gui_capabilities(),
        }
        self._generate_recommendations()
        return self.detected_tools

    def _generate_recommendations(self):
        """Generate setup recommendations based on detection"""
        self.recommendations = []
        git_tools = self.detected_tools['git_tools']

        if not git_tools.get('git'):
            self.recommendations.append({
                'priority': 'HIGH',
                'message': 'Git is not installed',
                'action': 'install_git'
            })

        if not git_tools.get('gh'):
            self.recommendations.append({
                'priority': 'HIGH',
                'message': 'GitHub CLI is not installed',
                'action': 'install_gh'
            })
        elif not git_tools.get('gh_authenticated'):
            self.recommendations.append({
                'priority': 'MEDIUM',
                'message': 'GitHub CLI is not authenticated',
                'action': 'auth_gh'
            })


class InstallationHelper:
    """Provides installation guidance and scripts"""

    def __init__(self, system):
        self.system = system

    def get_git_install_info(self):
        """Get Git installation instructions"""
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

    def get_gh_install_info(self):
        """Get GitHub CLI installation instructions"""
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
                'method': 'Package manager or snap',
                'command': 'sudo snap install gh  # or apt install gh',
                'instructions': 'Use snap or your distribution package manager'
            }


class UserInterface:
    """Enhanced user interface with menus and guidance"""
    def __init__(self):
        self.detector = EnvironmentDetector()
        self.installer = None

    def print_header(self, title):
        """Print a styled header"""
        width = max(60, len(title) + 10)
        print(f"\n{Colors.CYAN}{'=' * width}{Colors.END}")
        print(f"{Colors.CYAN}{Colors.BOLD}{title.center(width)}{Colors.END}")
        print(f"{Colors.CYAN}{'=' * width}{Colors.END}\n")

    def print_status(self, message, status="INFO"):
        """Print a status message with color coding"""
        color_map = {
            "INFO": Colors.BLUE,
            "SUCCESS": Colors.GREEN,
            "WARNING": Colors.YELLOW,
            "ERROR": Colors.RED,
            "QUESTION": Colors.MAGENTA
        }
        color = color_map.get(status, Colors.WHITE)
        print(f"{color}[{status}]{Colors.END} {message}")

    def get_user_choice(self, prompt, choices):
        """Get user choice from a list of options"""
        while True:
            print(f"\n{Colors.QUESTION}{prompt}{Colors.END}")
            for i, choice in enumerate(choices, 1):
                print(f"  {Colors.YELLOW}{i}.{Colors.END} {choice}")

            try:
                choice = input(f"\n{Colors.CYAN}Enter your choice (1-{len(choices)}): {Colors.END}")
                choice_num = int(choice)
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

    def show_environment_status(self, detected):
        """Display comprehensive environment status"""
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

        print(f"\n{Colors.BOLD}GUI Support:{Colors.END}")
        gui = detected['gui']
        tkinter_status = f"{Colors.GREEN}✓{Colors.END}" if gui.get('tkinter') else f"{Colors.RED}✗{Colors.END}"
        display_status = f"{Colors.GREEN}✓{Colors.END}" if gui.get('display') else f"{Colors.RED}✗{Colors.END}"
        print(f"  {tkinter_status} Tkinter (Python GUI)")
        print(f"  {display_status} Display available")

    def show_installation_help(self, detected):
        """Show installation guidance"""
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

    def open_installation_links(self, detected):
        """Open installation URLs in browser"""
        self.installer = InstallationHelper(detected['system'])
        git_tools = detected['git_tools']

        links = []

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
                except Exception:
                    self.print_status(f"Could not open {name}. Manual URL: {url}", "WARNING")
        else:
            self.print_status("No installation links needed.", "INFO")

    def launch_script(self, script_path, script_type):
        """Launch a specific script"""
        try:
            if script_type == "python":
                subprocess.run([sys.executable, script_path])
            elif script_type == "bash":
                subprocess.run(["bash", script_path])
            elif script_type == "powershell":
                subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path])
            else:
                self.print_status(f"Unknown script type: {script_type}", "ERROR")
        except FileNotFoundError:
            self.print_status(f"Script not found: {script_path}", "ERROR")
            self.print_status("Please ensure all script files are properly installed.", "INFO")
        except Exception as e:
            self.print_status(f"Error launching script: {e}", "ERROR")

    def main_menu(self):
        """Main application menu"""
        self.print_header("GitSage v1.0 - Repository Management Tools")

        self.print_status("Detecting environment...", "INFO")
        detected = self.detector.detect_all()

        self.show_environment_status(detected)

        if self.detector.recommendations:
            print(f"\n{Colors.YELLOW}Recommendations:{Colors.END}")
            for rec in self.detector.recommendations:
                priority_color = Colors.RED if rec['priority'] == 'HIGH' else Colors.YELLOW
                print(f"  {priority_color}{rec['priority']}: {rec['message']}{Colors.END}")

        while True:
            choices = [
                "🗑️  Repository Deletion (Interactive Bash Script)",
                "🔧 Repository Manager (Advanced Bash Features)",
                "📚 Wiki Generator (Basic)",
                "📚 Wiki Generator (Enhanced with Templates)",
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
                script_path = Path("scripts/bash/delete-repo.sh")
                if script_path.exists():
                    self.print_status("Launching Interactive GitHub Repository Deletion Script...", "INFO")
                    self.launch_script(str(script_path), "bash")
                else:
                    self.print_status("Deletion script not found at scripts/bash/delete-repo.sh", "ERROR")
            elif choice == 1:  # Repository Manager
                script_path = Path("scripts/bash/repo-manager.sh")
                if script_path.exists():
                    self.print_status("Launching Advanced Repository Manager (Bash)...", "INFO")
                    self.launch_script(str(script_path), "bash")
                else:
                    self.print_status("Repository manager not found at scripts/bash/repo-manager.sh", "ERROR")
            elif choice == 2:  # Wiki Generator Basic
                script_path = Path("wiki-generator.py")
                if script_path.exists():
                    self.print_status("Launching Wiki Generator...", "INFO")
                    self.launch_script(str(script_path), "python")
                else:
                    self.print_status("Wiki generator not found.", "ERROR")
            elif choice == 3:  # Wiki Generator Enhanced
                script_path = Path("wiki-generator-enhanced.py")
                if script_path.exists():
                    self.print_status("Launching Enhanced Wiki Generator...", "INFO")
                    self.launch_script(str(script_path), "python")
                else:
                    self.print_status("Enhanced wiki generator not found.", "ERROR")
            elif choice == 4:  # README Generator
                script_path = Path("readme-generator.py")
                if script_path.exists():
                    self.print_status("Launching README Generator...", "INFO")
                    self.launch_script(str(script_path), "python")
                else:
                    self.print_status("README generator not found.", "ERROR")
            elif choice == 5:  # Script Generator & GitHub Learning
                script_path = Path("script-generator.py")
                if script_path.exists():
                    self.print_status("Launching Script Generator & GitHub Learning...", "INFO")
                    self.print_status("Generate custom automation scripts while learning GitHub!", "INFO")
                    self.launch_script(str(script_path), "python")
                else:
                    self.print_status("Script generator not found.", "ERROR")
            elif choice == 6:  # Backup Manager
                script_path = Path("backup-manager.py")
                if script_path.exists():
                    self.print_status("Launching Backup Manager...", "INFO")
                    self.print_status("Create, restore, and manage repository backups", "INFO")
                    self.launch_script(str(script_path), "python")
                else:
                    self.print_status("Backup manager not found.", "ERROR")
            elif choice == 7:  # Reset Git History
                script_path = Path("scripts/git-resets/reset_git_history.sh")
                if script_path.exists():
                    self.print_status("Launching Git History Reset Tool...", "WARNING")
                    self.print_status("This will DELETE all commit history while keeping files.", "WARNING")
                    self.launch_script(str(script_path), "bash")
                else:
                    self.print_status("Git history reset script not found.", "ERROR")
            elif choice == 8:  # Migrate Repository
                script_path = Path("scripts/git-resets/migrate_and_swap_repos.sh")
                if script_path.exists():
                    self.print_status("Launching Repository Migration Tool...", "INFO")
                    self.launch_script(str(script_path), "bash")
                else:
                    self.print_status("Repository migration script not found.", "ERROR")
            elif choice == 9:  # Install tools
                self.show_installation_help(detected)
            elif choice == 10:  # Open links
                self.open_installation_links(detected)
            elif choice == 11:  # Re-check
                detected = self.detector.detect_all()
                self.show_environment_status(detected)
            elif choice == 12:  # Exit
                self.print_status("Thank you for using GitSage!", "SUCCESS")
                sys.exit(0)


def main():
    """Main entry point"""
    try:
        ui = UserInterface()
        ui.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()
