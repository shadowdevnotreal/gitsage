#!/usr/bin/env python3
"""
GitSage README Generator - ENHANCED WITH INTERACTIVE MODE
==========================================================
Generate awesome README.md files with badges, charts, and professional formatting.

Features:
- [>>] **INTERACTIVE WIZARD** - No config files needed!
- [AUTO] Auto-detect project type from codebase
- [STATS] GitHub stats integration
- [+] Multiple templates (CLI tool, library, web app, data science, etc.)
- [STYLE] Auto-generated shields.io badges
- [CHART] Project statistics and charts
- [DOCS] Table of contents
- [!] Code examples
- [CONTRIB] Contributing guidelines
- [LICENSE] License detection
"""

import os
import sys
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

try:
    from rich.console import Console
    from rich.progress import track
    from rich.prompt import Prompt, Confirm
    from rich.panel import Panel
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Try to import GitSage utilities
try:
    sys.path.insert(0, str(Path(__file__).parent / "src"))
    from gitsage.utils import ProjectDetector, GitHubStatsGenerator, BeautificationScorer
    GITSAGE_UTILS_AVAILABLE = True
except ImportError:
    GITSAGE_UTILS_AVAILABLE = False


class ReadmeGenerator:
    """Generate comprehensive README.md files"""

    def __init__(self, config_path="readme-config.yaml"):
        self.config_path = config_path
        self.config = self.load_or_create_config()
        self.console = Console() if RICH_AVAILABLE else None

    def print(self, message, style=""):
        """Print with rich if available, plain otherwise"""
        if self.console:
            self.console.print(message, style=style)
        else:
            print(message)

    def load_or_create_config(self) -> Dict:
        """Load existing config or create default"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        else:
            return self.create_default_config()

    def create_default_config(self) -> Dict:
        """Create default configuration"""
        config = {
            'project': {
                'name': 'My Awesome Project',
                'tagline': 'A brief description of what this project does',
                'description': 'Detailed project description here',
                'version': '1.0.0',
                'author': 'Your Name',
                'email': 'your.email@example.com',
                'github_username': 'yourusername',
                'repo_name': 'your-repo',
                'license': 'MIT',
                'homepage': '',
                'demo_url': '',
            },
            'template': {
                'type': 'cli-tool',  # cli-tool, library, web-app, data-science, game, mobile-app
                'style': 'professional',  # professional, minimal, creative, technical
            },
            'badges': {
                'enabled': True,
                'shields': [
                    'license',
                    'version',
                    'python-version',
                    'build-status',
                    'coverage',
                    'downloads',
                    'stars',
                    'issues',
                    'pr-welcome',
                    'maintained',
                ],
            },
            'sections': {
                'features': True,
                'installation': True,
                'quick_start': True,
                'usage': True,
                'examples': True,
                'api_reference': False,
                'configuration': True,
                'testing': True,
                'contributing': True,
                'changelog': True,
                'license': True,
                'acknowledgments': True,
                'support': True,
            },
            'features': [
                '[+] Feature 1 - Brief description',
                '[ROCKET] Feature 2 - What it does',
                '[!] Feature 3 - Why it\'s useful',
            ],
            'technologies': [
                {'name': 'Python', 'version': '3.8+'},
                {'name': 'FastAPI', 'version': '0.68+'},
            ],
            'installation': {
                'methods': ['pip', 'git'],
                'pip_package': 'your-package-name',
                'requirements': 'requirements.txt',
            },
            'usage_examples': [
                {
                    'title': 'Basic Usage',
                    'code': 'from mypackage import MyClass\n\nobj = MyClass()\nobj.do_something()',
                    'language': 'python',
                },
            ],
            'screenshots': [],
            'contributing': {
                'guidelines_file': 'CONTRIBUTING.md',
                'code_of_conduct': 'CODE_OF_CONDUCT.md',
            },
            'support': {
                'email': '',
                'discord': '',
                'forum': '',
            },
        }

        # Save default config
        with open(self.config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        self.print(f"[*] Created default config: {self.config_path}", "green")
        self.print("  Edit this file to customize your README", "dim")

        return config

    def generate_badges(self) -> str:
        """Generate shields.io badges"""
        if not self.config['badges']['enabled']:
            return ""

        project = self.config['project']
        shields = self.config['badges']['shields']
        username = project.get('github_username', 'user')
        repo = project.get('repo_name', 'repo')

        badges = []

        if 'license' in shields:
            license_name = project.get('license', 'MIT')
            badges.append(f"![License]({self.badge_url('license', license_name, 'green')})")

        if 'version' in shields:
            version = project.get('version', '1.0.0')
            badges.append(f"![Version]({self.badge_url('version', version, 'blue')})")

        if 'python-version' in shields:
            badges.append(f"![Python](https://img.shields.io/badge/python-3.8+-blue.svg)")

        if 'build-status' in shields:
            badges.append(f"![Build](https://img.shields.io/github/actions/workflow/status/{username}/{repo}/ci.yml?branch=main)")

        if 'coverage' in shields:
            badges.append(f"![Coverage](https://img.shields.io/codecov/c/github/{username}/{repo})")

        if 'downloads' in shields:
            badges.append(f"![Downloads](https://img.shields.io/pypi/dm/{project.get('name', 'package')})")

        if 'stars' in shields:
            badges.append(f"![Stars](https://img.shields.io/github/stars/{username}/{repo}?style=social)")

        if 'issues' in shields:
            badges.append(f"![Issues](https://img.shields.io/github/issues/{username}/{repo})")

        if 'pr-welcome' in shields:
            badges.append(f"![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)")

        if 'maintained' in shields:
            badges.append(f"![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)")

        return " ".join(badges) + "\n"

    def badge_url(self, label: str, message: str, color: str) -> str:
        """Generate shields.io badge URL"""
        return f"https://img.shields.io/badge/{label}-{message.replace('-', '--')}-{color}"

    def generate_header(self) -> str:
        """Generate README header"""
        project = self.config['project']
        name = project['name']
        tagline = project['tagline']

        header = f"# {name}\n\n"

        # Add logo if exists
        if os.path.exists('assets/logos/logo.png'):
            header += f"<p align=\"center\">\n  <img src=\"assets/logos/logo.png\" alt=\"{name} Logo\" width=\"200\"/>\n</p>\n\n"

        header += f"> {tagline}\n\n"
        header += self.generate_badges()

        return header

    def generate_toc(self) -> str:
        """Generate table of contents"""
        sections = self.config['sections']
        toc = "## 📋 Table of Contents\n\n"

        items = []
        if sections.get('features'): items.append("- [Features](#features)")
        if sections.get('installation'): items.append("- [Installation](#installation)")
        if sections.get('quick_start'): items.append("- [Quick Start](#quick-start)")
        if sections.get('usage'): items.append("- [Usage](#usage)")
        if sections.get('examples'): items.append("- [Examples](#examples)")
        if sections.get('api_reference'): items.append("- [API Reference](#api-reference)")
        if sections.get('configuration'): items.append("- [Configuration](#configuration)")
        if sections.get('testing'): items.append("- [Testing](#testing)")
        if sections.get('contributing'): items.append("- [Contributing](#contributing)")
        if sections.get('changelog'): items.append("- [Changelog](#changelog)")
        if sections.get('license'): items.append("- [License](#license)")

        toc += "\n".join(items) + "\n\n"
        return toc

    def generate_features(self) -> str:
        """Generate features section"""
        if not self.config['sections'].get('features'):
            return ""

        features = self.config['features']
        section = "## [+] Features\n\n"

        for feature in features:
            section += f"- {feature}\n"

        section += "\n"
        return section

    def generate_installation(self) -> str:
        """Generate installation section"""
        if not self.config['sections'].get('installation'):
            return ""

        install = self.config['installation']
        methods = install.get('methods', [])

        section = "## [PKG] Installation\n\n"

        if 'pip' in methods:
            package = install.get('pip_package', 'package-name')
            section += f"### Using pip\n\n```bash\npip install {package}\n```\n\n"

        if 'git' in methods:
            username = self.config['project'].get('github_username', 'user')
            repo = self.config['project'].get('repo_name', 'repo')
            section += f"### From source\n\n```bash\ngit clone https://github.com/{username}/{repo}.git\ncd {repo}\n"
            if install.get('requirements'):
                section += f"pip install -r {install['requirements']}\n"
            section += "```\n\n"

        return section

    def generate_quick_start(self) -> str:
        """Generate quick start section"""
        if not self.config['sections'].get('quick_start'):
            return ""

        template_type = self.config['template']['type']

        section = "## [ROCKET] Quick Start\n\n"

        if template_type == 'cli-tool':
            section += "```bash\n# Run the tool\nmycommand --help\n\n# Basic usage\nmycommand input.txt\n```\n\n"
        elif template_type == 'library':
            section += "```python\nfrom mypackage import MyClass\n\n# Create instance\nobj = MyClass()\n\n# Use it\nresult = obj.do_something()\nprint(result)\n```\n\n"
        elif template_type == 'web-app':
            section += "```bash\n# Start development server\npython app.py\n\n# Visit http://localhost:5000\n```\n\n"

        return section

    def generate_usage(self) -> str:
        """Generate usage section"""
        if not self.config['sections'].get('usage'):
            return ""

        section = "## [CODE] Usage\n\n"

        examples = self.config.get('usage_examples', [])
        for example in examples:
            section += f"### {example['title']}\n\n"
            language = example.get('language', 'python')
            section += f"```{language}\n{example['code']}\n```\n\n"

        return section

    def generate_contributing(self) -> str:
        """Generate contributing section"""
        if not self.config['sections'].get('contributing'):
            return ""

        section = "## [CONTRIB] Contributing\n\n"
        section += "Contributions are welcome! Please feel free to submit a Pull Request.\n\n"

        guidelines_file = self.config['contributing'].get('guidelines_file')
        if guidelines_file and os.path.exists(guidelines_file):
            section += f"For detailed guidelines, see [{guidelines_file}]({guidelines_file}).\n\n"

        section += "### Steps to Contribute\n\n"
        section += "1. Fork the repository\n"
        section += "2. Create your feature branch (`git checkout -b feature/AmazingFeature`)\n"
        section += "3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)\n"
        section += "4. Push to the branch (`git push origin feature/AmazingFeature`)\n"
        section += "5. Open a Pull Request\n\n"

        return section

    def generate_license(self) -> str:
        """Generate license section"""
        if not self.config['sections'].get('license'):
            return ""

        project = self.config['project']
        license_name = project.get('license', 'MIT')

        section = "## [LICENSE] License\n\n"
        section += f"This project is licensed under the {license_name} License - see the [LICENSE](LICENSE) file for details.\n\n"

        return section

    def generate_support(self) -> str:
        """Generate support section"""
        if not self.config['sections'].get('support'):
            return ""

        support = self.config.get('support', {})
        if not any(support.values()):
            return ""

        section = "## [CHAT] Support\n\n"

        if support.get('email'):
            section += f"- 📧 Email: {support['email']}\n"
        if support.get('discord'):
            section += f"- [CHAT] Discord: {support['discord']}\n"
        if support.get('forum'):
            section += f"- 💭 Forum: {support['forum']}\n"

        section += "\n"
        return section

    def generate_footer(self) -> str:
        """Generate footer"""
        author = self.config['project'].get('author', 'Author')
        year = datetime.now().year

        footer = "---\n\n"
        footer += f"Made with ❤️ by {author} © {year}\n"

        return footer

    def generate(self, output_path="README.md") -> str:
        """Generate complete README"""
        self.print("\n[STYLE] Generating README.md...\n", "bold blue")

        readme = ""
        readme += self.generate_header()
        readme += self.generate_toc()
        readme += "\n" + self.config['project']['description'] + "\n\n"
        readme += self.generate_features()
        readme += self.generate_installation()
        readme += self.generate_quick_start()
        readme += self.generate_usage()
        readme += self.generate_contributing()
        readme += self.generate_license()
        readme += self.generate_support()
        readme += self.generate_footer()

        # Write to file
        with open(output_path, 'w') as f:
            f.write(readme)

        self.print(f"[*] README generated: {output_path}", "green bold")
        self.print(f"  {len(readme)} characters", "dim")
        self.print(f"  {len(readme.splitlines())} lines", "dim")

        return readme

    def interactive_wizard(self) -> Dict:
        """
        Interactive wizard to collect README information

        Returns:
            Dict: Configuration dictionary
        """
        if not RICH_AVAILABLE:
            print("Error: Interactive mode requires 'rich' library")
            print("Install with: pip install rich")
            sys.exit(1)

        console = Console()

        console.print(Panel.fit(
            "[bold cyan][>>] README Generator - Interactive Wizard[/bold cyan]\n"
            "[dim]Answer the questions below to create an awesome README![/dim]",
            border_style="cyan"
        ))

        config = {
            'project': {},
            'template': {},
            'badges': {'enabled': True, 'shields': []},
            'sections': {},
            'features': [],
            'technologies': [],
            'installation': {},
            'usage_examples': [],
            'screenshots': [],
            'contributing': {},
            'support': {}
        }

        # Auto-detect project information
        auto_detected = {}
        if GITSAGE_UTILS_AVAILABLE:
            console.print("\n[bold yellow][SEARCH] Analyzing your codebase...[/bold yellow]")
            detector = ProjectDetector()
            detection = detector.detect()
            stats_gen = GitHubStatsGenerator()
            repo_info = stats_gen.get_repo_info()

            auto_detected = {
                'project_type': detection.get('detected_type', 'cli-tool'),
                'languages': detection.get('languages', {}),
                'frameworks': detection.get('frameworks', []),
                'technologies': detection.get('technologies', []),
                'username': repo_info.get('username', 'username'),
                'repo': repo_info.get('repo', 'repo'),
            }

            console.print(f"[green][*][/green] Detected: {auto_detected.get('project_type', 'Unknown')}")
            if auto_detected.get('languages'):
                langs = ', '.join(list(auto_detected['languages'].keys())[:3])
                console.print(f"[green][*][/green] Languages: {langs}")

        # Project Information
        console.print("\n[bold cyan][EDIT] Project Information[/bold cyan]")

        project_name = Prompt.ask(
            "Project name",
            default=auto_detected.get('repo', Path.cwd().name)
        )
        config['project']['name'] = project_name

        tagline = Prompt.ask(
            "Tagline (short description)",
            default=f"A {auto_detected.get('project_type', 'tool')} for developers"
        )
        config['project']['tagline'] = tagline

        description = Prompt.ask(
            "Detailed description",
            default=f"{project_name} is a powerful {auto_detected.get('project_type', 'tool')}."
        )
        config['project']['description'] = description

        config['project']['version'] = Prompt.ask("Version", default="1.0.0")
        config['project']['author'] = Prompt.ask("Author name", default="Your Name")
        config['project']['email'] = Prompt.ask("Email (optional)", default="")
        config['project']['github_username'] = Prompt.ask(
            "GitHub username",
            default=auto_detected.get('username', 'username')
        )
        config['project']['repo_name'] = Prompt.ask(
            "Repository name",
            default=auto_detected.get('repo', project_name.lower().replace(' ', '-'))
        )

        # License
        license_choices = ['MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause', 'Other']
        console.print("\nLicense: [dim](1=MIT, 2=Apache-2.0, 3=GPL-3.0, 4=BSD-3-Clause, 5=Other)[/dim]")
        license_choice = Prompt.ask("Choose license", choices=['1', '2', '3', '4', '5'], default='1')
        config['project']['license'] = license_choices[int(license_choice) - 1]

        # Template Type
        console.print("\n[bold cyan][STYLE] Template Type[/bold cyan]")

        template_types = {
            '1': 'cli-tool',
            '2': 'python-library',
            '3': 'web-application',
            '4': 'data-science',
            '5': 'npm-package',
            '6': 'mobile-app'
        }

        console.print("Choose template:")
        for key, val in template_types.items():
            prefix = "[bold green]->[/bold green]" if val == auto_detected.get('project_type') else " "
            console.print(f"  {prefix} {key}. {val}")

        # Determine default based on auto-detection
        default_template = '1'
        for key, val in template_types.items():
            if val == auto_detected.get('project_type'):
                default_template = key
                break

        template_choice = Prompt.ask("Template", choices=list(template_types.keys()), default=default_template)
        config['template']['type'] = template_types[template_choice]
        config['template']['style'] = 'professional'

        # Badges
        console.print("\n[bold cyan][BADGE]  Badges[/bold cyan]")

        all_badges = [
            'license', 'version', 'stars', 'forks', 'issues',
            'last-commit', 'build-status', 'coverage',
            'maintained', 'pr-welcome'
        ]

        if Confirm.ask("Include badges?", default=True):
            console.print("\nSelect badges (comma-separated numbers or 'all'):")
            for i, badge in enumerate(all_badges, 1):
                console.print(f"  {i}. {badge}")

            badge_input = Prompt.ask(
                "Badges",
                default="all"
            )

            if badge_input.lower() == 'all':
                config['badges']['shields'] = all_badges
            else:
                try:
                    indices = [int(x.strip()) - 1 for x in badge_input.split(',')]
                    config['badges']['shields'] = [all_badges[i] for i in indices if 0 <= i < len(all_badges)]
                except:
                    config['badges']['shields'] = ['license', 'version', 'stars', 'maintained']

        # Features
        console.print("\n[bold cyan][+] Features[/bold cyan]")
        if Confirm.ask("Add features list?", default=True):
            console.print("Enter features (one per line, empty line to finish):")
            features = []
            while True:
                feature = Prompt.ask(f"Feature {len(features) + 1}", default="")
                if not feature:
                    break
                features.append(f"[+] {feature}")
                if len(features) >= 5:
                    if not Confirm.ask("Add more features?", default=False):
                        break

            config['features'] = features if features else [
                "[+] Easy to use",
                "[ROCKET] Fast and efficient",
                "[PKG] Lightweight"
            ]

        # Sections
        console.print("\n[bold cyan][DOCS] Sections to Include[/bold cyan]")

        section_defaults = {
            'features': True,
            'installation': True,
            'quick_start': True,
            'usage': True,
            'examples': Confirm.ask("Include examples section?", default=True),
            'configuration': Confirm.ask("Include configuration section?", default=False),
            'testing': Confirm.ask("Include testing section?", default=True),
            'contributing': Confirm.ask("Include contributing section?", default=True),
            'license': True,
            'support': Confirm.ask("Include support section?", default=False),
        }

        config['sections'] = section_defaults

        # Installation
        if config['sections']['installation']:
            console.print("\n[bold cyan][PKG] Installation[/bold cyan]")
            install_methods = []

            if Confirm.ask("Install via pip/npm?", default=True):
                install_methods.append('pip' if 'python' in str(auto_detected.get('languages', {})).lower() else 'npm')

            if Confirm.ask("Install from source?", default=True):
                install_methods.append('git')

            config['installation']['methods'] = install_methods
            if 'pip' in install_methods:
                config['installation']['pip_package'] = Prompt.ask(
                    "Package name",
                    default=project_name.lower().replace(' ', '-')
                )

        # Support
        if config['sections']['support']:
            console.print("\n[bold cyan][CHAT] Support Channels[/bold cyan]")
            config['support']['email'] = Prompt.ask("Support email (optional)", default="")
            config['support']['discord'] = Prompt.ask("Discord server (optional)", default="")

        console.print("\n[bold green][*] Configuration complete![/bold green]")

        # Save config option
        if Confirm.ask("\nSave configuration for future use?", default=True):
            config_path = Prompt.ask("Config file name", default="readme-config.yaml")
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            console.print(f"[green][*][/green] Saved to {config_path}")

        return config


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate awesome README.md files - Now with Interactive Wizard!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (RECOMMENDED!)
  python readme-generator.py --interactive

  # Use existing config
  python readme-generator.py --config my-config.yaml

  # Quick template
  python readme-generator.py --template cli-tool
        """
    )

    parser.add_argument('--interactive', '-i', action='store_true',
                       help='[>>] Interactive wizard mode (no config file needed!)')
    parser.add_argument('--config', default='readme-config.yaml',
                       help='Config file path')
    parser.add_argument('--output', default='README.md',
                       help='Output file path')
    parser.add_argument('--template',
                       choices=['cli-tool', 'library', 'web-app', 'data-science', 'game', 'npm-package'],
                       help='Use template')
    parser.add_argument('--analyze', action='store_true',
                       help='[SEARCH] Analyze project and show detected information')
    parser.add_argument('--health-check', action='store_true',
                       help='[HEALTH] Show repository health report')

    args = parser.parse_args()

    # Health check mode
    if args.health_check:
        if GITSAGE_UTILS_AVAILABLE:
            from gitsage.utils import BeautificationScorer
            scorer = BeautificationScorer()
            console = Console() if RICH_AVAILABLE else None
            scorer.display_beautification_report(console)
        else:
            print("Health check requires GitSage utilities")
        return

    # Analyze mode
    if args.analyze:
        if GITSAGE_UTILS_AVAILABLE:
            detector = ProjectDetector()
            console = Console() if RICH_AVAILABLE else None
            detector.display_detection_results(console)
        else:
            print("Analysis requires GitSage utilities")
        return

    # Interactive mode
    if args.interactive or not os.path.exists(args.config):
        if not os.path.exists(args.config):
            if RICH_AVAILABLE:
                console = Console()
                console.print("\n[yellow][WARN]  No config file found. Launching interactive wizard...[/yellow]\n")
            else:
                print("\n[WARN]  No config file found. Use --interactive for wizard mode or create config file.\n")
                sys.exit(1)

        # Create generator without config, then run wizard
        generator = ReadmeGenerator.__new__(ReadmeGenerator)
        generator.console = Console() if RICH_AVAILABLE else None
        generator.config = generator.interactive_wizard()
        generator.generate(args.output)
    else:
        # Config-based mode
        generator = ReadmeGenerator(args.config)

        if args.template:
            generator.config['template']['type'] = args.template

        generator.generate(args.output)


if __name__ == '__main__':
    main()
