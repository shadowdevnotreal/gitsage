#!/usr/bin/env python3
"""
GitSage README Generator
========================
Generate awesome README.md files with badges, charts, and professional formatting.

Features:
- Multiple templates (CLI tool, library, web app, data science, etc.)
- Auto-generated shields.io badges
- Project statistics and charts
- Table of contents
- Code examples
- Contributing guidelines
- License detection
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
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


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
                '✨ Feature 1 - Brief description',
                '🚀 Feature 2 - What it does',
                '💡 Feature 3 - Why it\'s useful',
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

        self.print(f"✓ Created default config: {self.config_path}", "green")
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
        section = "## ✨ Features\n\n"

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

        section = "## 📦 Installation\n\n"

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

        section = "## 🚀 Quick Start\n\n"

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

        section = "## 💻 Usage\n\n"

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

        section = "## 🤝 Contributing\n\n"
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

        section = "## 📜 License\n\n"
        section += f"This project is licensed under the {license_name} License - see the [LICENSE](LICENSE) file for details.\n\n"

        return section

    def generate_support(self) -> str:
        """Generate support section"""
        if not self.config['sections'].get('support'):
            return ""

        support = self.config.get('support', {})
        if not any(support.values()):
            return ""

        section = "## 💬 Support\n\n"

        if support.get('email'):
            section += f"- 📧 Email: {support['email']}\n"
        if support.get('discord'):
            section += f"- 💬 Discord: {support['discord']}\n"
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
        self.print("\n🎨 Generating README.md...\n", "bold blue")

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

        self.print(f"✓ README generated: {output_path}", "green bold")
        self.print(f"  {len(readme)} characters", "dim")
        self.print(f"  {len(readme.splitlines())} lines", "dim")

        return readme


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Generate awesome README.md files')
    parser.add_argument('--config', default='readme-config.yaml', help='Config file path')
    parser.add_argument('--output', default='README.md', help='Output file path')
    parser.add_argument('--template', choices=['cli-tool', 'library', 'web-app', 'data-science', 'game'], help='Use template')

    args = parser.parse_args()

    generator = ReadmeGenerator(args.config)

    if args.template:
        generator.config['template']['type'] = args.template

    generator.generate(args.output)


if __name__ == '__main__':
    main()
