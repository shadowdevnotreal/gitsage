#!/usr/bin/env python3
"""
GitSage Launcher - Main Entry Point
====================================
Universal launcher offering both CLI and Web interface modes.
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from gitsage.__version__ import __version__, PROJECT_NAME
from gitsage.utils import Colors


def main():
    """Main entry point with mode selection."""
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{PROJECT_NAME} v{__version__}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}\n")

    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--web', '-w']:
            launch_web()
            return
        elif sys.argv[1] in ['--cli', '-c']:
            launch_cli()
            return
        elif sys.argv[1] in ['--help', '-h']:
            show_help()
            return

    # Interactive mode selection
    print(f"{Colors.BLUE}Choose interface mode:{Colors.END}\n")
    print(f"  {Colors.GREEN}1.{Colors.END} CLI Mode (Terminal Interface)")
    print(f"  {Colors.GREEN}2.{Colors.END} Web Mode (Browser Interface)")
    print(f"  {Colors.GREEN}3.{Colors.END} Exit\n")

    try:
        choice = input(f"{Colors.CYAN}Enter choice [1-3]: {Colors.END}").strip()

        if choice == '1':
            launch_cli()
        elif choice == '2':
            launch_web()
        elif choice == '3':
            print(f"\n{Colors.YELLOW}Goodbye!{Colors.END}\n")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}Invalid choice{Colors.END}\n")
            sys.exit(1)

    except (KeyboardInterrupt, EOFError):
        print(f"\n\n{Colors.YELLOW}Operation cancelled{Colors.END}\n")
        sys.exit(0)


def launch_cli():
    """Launch CLI interface."""
    print(f"\n{Colors.GREEN}Launching CLI interface...{Colors.END}\n")
    from gitsage.cli.launcher import main as cli_main
    cli_main()


def launch_web():
    """Launch web interface."""
    print(f"\n{Colors.GREEN}Launching web interface...{Colors.END}\n")
    print(f"{Colors.CYAN}Access at: http://localhost:5000{Colors.END}")
    print(f"{Colors.YELLOW}Press Ctrl+C to stop{Colors.END}\n")

    from gitsage.web.app import main as web_main
    web_main()


def show_help():
    """Show help information."""
    print(f"""
{Colors.BOLD}Usage:{Colors.END}
    python launcher.py [OPTIONS]

{Colors.BOLD}Options:{Colors.END}
    --cli, -c       Launch CLI interface directly
    --web, -w       Launch web interface directly
    --help, -h      Show this help message

{Colors.BOLD}Examples:{Colors.END}
    python launcher.py              # Interactive mode selection
    python launcher.py --cli        # Launch CLI directly
    python launcher.py --web        # Launch web directly

{Colors.BOLD}Alternative Commands:{Colors.END}
    gitsage                         # CLI interface
    gitsage-web                     # Web interface
    ./gitsage launch                # CLI via wrapper

{Colors.BOLD}More Information:{Colors.END}
    README.md                       # Full documentation
    docs/                           # User guides
    https://github.com/shadowdevnotreal/gitsage
""")


if __name__ == "__main__":
    main()
