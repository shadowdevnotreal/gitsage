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
        elif sys.argv[1] in ['--setup-repo', '--setup']:
            setup_repository_wizard()
            return
        elif sys.argv[1] in ['--help', '-h']:
            show_help()
            return

    # Interactive mode selection
    print(f"{Colors.BLUE}What would you like to do?{Colors.END}\n")
    print(f"  {Colors.GREEN}1.{Colors.END} Repository Tools (Interactive Menu)")
    print(f"      View tools, generate READMEs, wikis, manage repositories")
    print()
    print(f"  {Colors.GREEN}2.{Colors.END} Complete Repository Setup (Wizard)")
    print(f"      One-command setup: analyze + README + wiki + best practices")
    print()
    print(f"  {Colors.GREEN}3.{Colors.END} Web Interface (Browser)")
    print(f"      Launch browser-based interface at http://localhost:5000")
    print()
    print(f"  {Colors.GREEN}4.{Colors.END} Exit\n")

    try:
        choice = input(f"{Colors.CYAN}Enter choice [1-4]: {Colors.END}").strip()

        if choice == '1':
            launch_cli()
        elif choice == '2':
            setup_repository_wizard()
        elif choice == '3':
            launch_web()
        elif choice == '4':
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


def setup_repository_wizard():
    """One-command repository setup wizard"""
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from gitsage.utils import (
            ProjectDetector,
            RepositoryHealthChecker,
            BeautificationScorer,
            GitHubStatsGenerator
        )
        from rich.console import Console
        from rich.panel import Panel
        from rich.prompt import Confirm
        import os

        console = Console()

        console.print(Panel.fit(
            "[bold cyan]GitSage Repository Setup Wizard[/bold cyan]\n"
            "[dim]Complete repository setup in one command![/dim]",
            border_style="cyan"
        ))

        # Step 0: Determine project location
        console.print("\n[bold yellow][>>] Project Location[/bold yellow]")
        current_dir = Path.cwd()

        # Check if current directory is a git repository
        is_git_repo = (current_dir / ".git").exists()

        if is_git_repo:
            console.print(f"[green]Detected git repository:[/green] {current_dir}")
            use_current = Confirm.ask("Use this directory?", default=True)
            if not use_current:
                project_path = console.input("[cyan]Enter project path:[/cyan] ").strip()
                if project_path:
                    os.chdir(project_path)
                    console.print(f"[green]Changed to:[/green] {project_path}")
        else:
            console.print(f"[yellow]Current directory is not a git repository:[/yellow] {current_dir}")
            console.print("[dim]GitSage works best with git repositories[/dim]\n")

            choice = console.input(
                "[cyan]Options:[/cyan]\n"
                "  1. Use current directory anyway\n"
                "  2. Enter different project path\n"
                "  3. Cancel\n"
                "[cyan]Choice [1-3]:[/cyan] "
            ).strip()

            if choice == '2':
                project_path = console.input("[cyan]Enter project path:[/cyan] ").strip()
                if project_path:
                    os.chdir(project_path)
                    console.print(f"[green]Changed to:[/green] {project_path}")
            elif choice == '3':
                console.print("[yellow]Cancelled[/yellow]")
                return
            # choice == '1' continues with current directory

        # Step 1: Analyze project
        console.print("\n[bold yellow][1/6] Analyzing project...[/bold yellow]")
        detector = ProjectDetector()
        detection = detector.detect()
        detector.display_detection_results(console)

        # Step 2: Health check
        console.print("\n[bold yellow][2/6] Checking repository health...[/bold yellow]")
        scorer = BeautificationScorer()
        scorer.display_beautification_report(console)

        # Step 3: Generate README
        if Confirm.ask("\n[bold cyan][3/6] Generate professional README?[/bold cyan]", default=True):
            console.print("[green]Launching README generator...[/green]")
            import subprocess
            subprocess.run([sys.executable, "readme-generator.py", "--interactive"])

        # Step 4: Generate Wiki
        if Confirm.ask("\n[bold cyan][4/6] Generate documentation wiki?[/bold cyan]", default=True):
            console.print("[green]Launching wiki generator...[/green]")
            import subprocess
            subprocess.run([sys.executable, "wiki-generator.py", "--all"])

        # Step 5: Setup GitHub features
        console.print("\n[bold cyan][5/6] GitHub Setup Checklist[/bold cyan]")
        console.print("\nPlease enable these features in your GitHub repository:")
        console.print("  [ ] Enable Wiki (Settings -> Features -> Wikis)")
        console.print("  [ ] Enable Issues (Settings -> Features -> Issues)")
        console.print("  [ ] Enable Discussions (Settings -> Features -> Discussions)")
        console.print("  [ ] Add repository description")
        console.print("  [ ] Add 3-5 topics/tags")
        console.print("  [ ] Add LICENSE file (if not exists)")

        # Step 6: Summary
        console.print(Panel.fit(
            "[bold green]Repository Setup Complete![/bold green]\n\n"
            "[white]Your repository now has:[/white]\n"
            "  [green][*][/green] Professional README.md\n"
            "  [green][*][/green] Complete documentation wiki\n"
            "  [green][*][/green] GitHub best practices applied\n\n"
            "[yellow]Next steps:[/yellow]\n"
            "  1. Review and commit changes\n"
            "  2. Enable GitHub features (see checklist above)\n"
            "  3. Deploy wiki pages\n"
            "  4. Share your awesome repository!",
            border_style="green",
            title="[6/6] Setup Complete"
        ))

    except ImportError as e:
        print(f"\n{Colors.RED}Error: Missing dependencies{Colors.END}")
        print(f"Please install: pip install rich pyyaml{Colors.END}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.END}\n")
        sys.exit(1)


def show_help():
    """Show help information."""
    print(f"""
{Colors.BOLD}Usage:{Colors.END}
    python launcher.py [OPTIONS]

{Colors.BOLD}Options:{Colors.END}
    --cli, -c          Launch CLI interface directly
    --web, -w          Launch web interface directly
    --setup-repo       One-command repository setup wizard
    --help, -h         Show this help message

{Colors.BOLD}Examples:{Colors.END}
    python launcher.py                  # Interactive mode selection
    python launcher.py --cli            # Launch CLI directly
    python launcher.py --web            # Launch web directly
    python launcher.py --setup-repo     # Complete repository setup

{Colors.BOLD}Alternative Commands:{Colors.END}
    gitsage                             # CLI interface
    gitsage-web                         # Web interface
    ./gitsage launch                    # CLI via wrapper

{Colors.BOLD}More Information:{Colors.END}
    README.md                           # Full documentation
    docs/                               # User guides
    https://github.com/shadowdevnotreal/gitsage
""")


if __name__ == "__main__":
    main()
