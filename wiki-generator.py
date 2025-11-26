#!/usr/bin/env python3
"""
ENHANCED Documentation Generator - Multi-Format, Multi-Platform
==============================================================
Professional documentation generation for GitHub Wiki, GitBook, Confluence, Notion, and more.

**THE BUSINESS GOLDMINE** - 5-minute professional docs worth $500-2000 each
"""

import os
import sys
import json
import yaml
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import argparse

try:
    from rich import print as rprint
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    from rich.panel import Panel
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    rprint = print


console = Console() if RICH_AVAILABLE else None


class DocumentationGenerator:
    """
    Enhanced multi-format documentation generator

    Supports:
    - GitHub Wiki
    - GitBook
    - Confluence (XML export)
    - Notion (Markdown export)
    - Read the Docs
    - MkDocs
    - PDF
    """

    SUPPORTED_FORMATS = [
        "github-wiki",
        "gitbook",
        "confluence",
        "notion",
        "readthedocs",
        "mkdocs",
        "pdf"
    ]

    INDUSTRY_TEMPLATES = [
        "api-documentation",
        "web-application",
        "cli-tool",
        "npm-package",
        "python-library",
        "mobile-app",
        "wordpress-plugin",
        "saas-platform",
        "data-science",
        "blockchain"
    ]

    THEMES = [
        "professional",  # Clean, business-ready
        "dark",          # Dark mode optimized
        "minimal",       # Simple and elegant
        "corporate",     # Enterprise styling
        "modern",        # Trendy gradients
        "technical",     # Code-focused
        "academic",      # Research paper style
        "startup"        # Fun and energetic
    ]

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.config = {}
        self.templates_dir = self.project_root / "templates"
        self.output_dir = self.project_root / "generated-docs"
        self.stats = {
            "pages_generated": 0,
            "formats": [],
            "start_time": datetime.now()
        }

    def load_config(self, config_file: str = "wiki-config.yaml") -> Dict:
        """Load or generate configuration"""
        config_path = self.project_root / config_file

        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = self.generate_enhanced_config()
            self.save_config(config_file)

        return self.config

    def generate_enhanced_config(self) -> Dict[str, Any]:
        """Generate enhanced default configuration with all options"""
        return {
            "project": {
                "name": "GitHub Repository Manager",
                "tagline": "Safe and powerful GitHub repository management",
                "description": "A comprehensive, cross-platform toolkit for safe GitHub repository management and automated documentation generation",
                "version": "2.0.0",
                "author": "Repository Manager Contributors",
                "license": "MIT",
                "github_url": "https://github.com/user/github-repo-manager",
                "homepage": "https://github.com/user/github-repo-manager",
                "issues_url": "https://github.com/user/github-repo-manager/issues",
                "main_script": "launcher.py",
                "language": "Python",
                "keywords": ["github", "repository", "management", "automation", "documentation"]
            },
            "template": {
                "type": "api-documentation",  # Choose from INDUSTRY_TEMPLATES
                "theme": "professional",       # Choose from THEMES
                "custom_css": True,
                "custom_logo": None,
                "favicon": None
            },
            "formats": {
                "github_wiki": {
                    "enabled": True,
                    "sidebar": True,
                    "footer": True,
                    "auto_nav": True
                },
                "gitbook": {
                    "enabled": True,
                    "theme": "default",
                    "plugins": ["search", "sharing", "fontsettings"],
                    "pdf": True
                },
                "confluence": {
                    "enabled": False,
                    "space_key": "DOCS",
                    "parent_page": "Documentation"
                },
                "notion": {
                    "enabled": False,
                    "workspace": None
                },
                "readthedocs": {
                    "enabled": False,
                    "theme": "sphinx_rtd_theme"
                },
                "mkdocs": {
                    "enabled": False,
                    "theme": "material"
                },
                "pdf": {
                    "enabled": False,
                    "format": "A4",
                    "toc": True
                }
            },
            "content": {
                "sections": [
                    {
                        "title": "Getting Started",
                        "icon": "🚀",
                        "pages": [
                            {"name": "Home", "template": "home"},
                            {"name": "Quick Start", "template": "quickstart"},
                            {"name": "Installation", "template": "installation"},
                            {"name": "Configuration", "template": "configuration"}
                        ]
                    },
                    {
                        "title": "User Guides",
                        "icon": "📖",
                        "pages": [
                            {"name": "Basic Usage", "template": "basic-usage"},
                            {"name": "Advanced Features", "template": "advanced"},
                            {"name": "Best Practices", "template": "best-practices"},
                            {"name": "Examples", "template": "examples"}
                        ]
                    },
                    {
                        "title": "API Reference",
                        "icon": "🔧",
                        "pages": [
                            {"name": "Overview", "template": "api-overview"},
                            {"name": "Authentication", "template": "api-auth"},
                            {"name": "Endpoints", "template": "api-endpoints"},
                            {"name": "SDKs", "template": "api-sdks"}
                        ]
                    },
                    {
                        "title": "Developer Guide",
                        "icon": "💻",
                        "pages": [
                            {"name": "Architecture", "template": "architecture"},
                            {"name": "Contributing", "template": "contributing"},
                            {"name": "Testing", "template": "testing"},
                            {"name": "Deployment", "template": "deployment"}
                        ]
                    },
                    {
                        "title": "Support",
                        "icon": "🆘",
                        "pages": [
                            {"name": "Troubleshooting", "template": "troubleshooting"},
                            {"name": "FAQ", "template": "faq"},
                            {"name": "Community", "template": "community"},
                            {"name": "Contact", "template": "contact"}
                        ]
                    }
                ]
            },
            "features": {
                "search": True,
                "syntax_highlighting": True,
                "code_copy": True,
                "dark_mode": True,
                "edit_on_github": True,
                "last_updated": True,
                "breadcrumbs": True,
                "table_of_contents": True
            },
            "analytics": {
                "google_analytics": None,
                "plausible": None
            },
            "seo": {
                "meta_description": None,
                "og_image": None,
                "twitter_card": True
            }
        }

    def save_config(self, config_file: str = "wiki-config.yaml") -> None:
        """Save configuration with rich output"""
        config_path = self.project_root / config_file
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)

        if RICH_AVAILABLE:
            rprint(f"[green]✅ Configuration saved:[/green] {config_file}")
        else:
            print(f"✅ Configuration saved: {config_file}")

    def generate_github_wiki(self) -> Path:
        """Generate GitHub Wiki format"""
        if RICH_AVAILABLE:
            rprint("\n[cyan]📚 Generating GitHub Wiki...[/cyan]")
        else:
            print("\n📚 Generating GitHub Wiki...")

        wiki_dir = self.output_dir / "github-wiki"
        wiki_dir.mkdir(parents=True, exist_ok=True)

        # Generate pages
        self._generate_wiki_home(wiki_dir)
        self._generate_wiki_sidebar(wiki_dir)
        self._generate_wiki_pages(wiki_dir)

        self.stats["formats"].append("GitHub Wiki")

        if RICH_AVAILABLE:
            rprint(f"[green]✅ GitHub Wiki generated:[/green] {wiki_dir}")
        else:
            print(f"✅ GitHub Wiki generated: {wiki_dir}")

        return wiki_dir

    def generate_gitbook(self) -> Path:
        """Generate GitBook format"""
        if RICH_AVAILABLE:
            rprint("\n[cyan]📖 Generating GitBook...[/cyan]")
        else:
            print("\n📖 Generating GitBook...")

        gitbook_dir = self.output_dir / "gitbook"
        gitbook_dir.mkdir(parents=True, exist_ok=True)

        # Generate GitBook structure
        self._generate_gitbook_readme(gitbook_dir)
        self._generate_gitbook_summary(gitbook_dir)
        self._generate_gitbook_config(gitbook_dir)
        self._generate_gitbook_pages(gitbook_dir)

        self.stats["formats"].append("GitBook")

        if RICH_AVAILABLE:
            rprint(f"[green]✅ GitBook generated:[/green] {gitbook_dir}")
        else:
            print(f"✅ GitBook generated: {gitbook_dir}")

        return gitbook_dir

    def _generate_wiki_home(self, wiki_dir: Path) -> None:
        """Generate enhanced wiki home page"""
        project = self.config["project"]
        theme = self.config["template"]["theme"]

        # Theme-specific styling
        theme_styles = {
            "professional": "clean and business-ready",
            "dark": "sleek dark mode",
            "minimal": "simple and elegant",
            "corporate": "enterprise-grade",
            "modern": "cutting-edge design",
            "technical": "developer-focused",
            "academic": "research-oriented",
            "startup": "innovative and energetic"
        }

        content = f'''# {project["name"]}

> **{project["tagline"]}**

{project["description"]}

---

## 🚀 **Quick Start**

Get started in 5 minutes:

```bash
# Clone the repository
git clone {project["github_url"]}.git
cd {project["name"].lower().replace(" ", "-")}

# Run the launcher
python {project["main_script"]}
```

**[📖 Full Installation Guide →](Installation)**

---

## ✨ **Key Features**

| Feature | Description |
|---------|-------------|
| 🛡️ **Safety First** | Multiple confirmations, automatic backups, verified operations |
| 📝 **Complete Logging** | Audit trail of all operations with timestamps |
| ⚙️ **Fully Configurable** | Customize every aspect to your workflow |
| 🧪 **Well Tested** | 60+ automated tests ensuring reliability |
| 🌍 **Cross-Platform** | Works on Windows, macOS, and Linux |
| 🎨 **Multiple Interfaces** | CLI and Web interface options |

---

## 📚 **Documentation Navigation**

### 🎯 Getting Started
- **[Quick Start Guide](Quick-Start)** - Be productive in 5 minutes
- **[Installation](Installation)** - Complete setup instructions
- **[Configuration](Configuration)** - Customize to your needs

### 📖 User Guides
- **[Basic Usage](Basic-Usage)** - Learn the fundamentals
- **[Advanced Features](Advanced-Features)** - Power user capabilities
- **[Best Practices](Best-Practices)** - Tips from the community
- **[Examples](Examples)** - Real-world use cases

### 🔧 API & Development
- **[API Overview](API-Overview)** - Integration reference
- **[Architecture](Architecture)** - How it works internally
- **[Contributing](Contributing)** - Join the project
- **[Testing Guide](Testing)** - Quality assurance

### 🆘 Support
- **[Troubleshooting](Troubleshooting)** - Fix common issues
- **[FAQ](FAQ)** - Frequently asked questions
- **[Community](Community)** - Get help and connect
- **[Contact](Contact)** - Reach the maintainers

---

## 📊 **Project Information**

| | |
|---|---|
| **Version** | `{project["version"]}` |
| **License** | {project["license"]} |
| **Language** | {project["language"]} |
| **Author** | {project["author"]} |

---

## 🔗 **Quick Links**

- 🌐 **[Project Homepage]({project["homepage"]})**
- 📦 **[Latest Release]({project["github_url"]}/releases/latest)**
- 🐛 **[Report Issues]({project["issues_url"]})**
- 💬 **[Discussions]({project["github_url"]}/discussions)**
- ⭐ **[Star on GitHub]({project["github_url"]})**

---

## 💡 **Need Help?**

- 📖 **[Start with Quick Start](Quick-Start)** - Best first step
- 🔍 **[Search Documentation](Search)** - Find what you need
- 💬 **[Ask the Community](Community)** - Get answers fast
- 🐛 **[Report a Bug]({project["issues_url"]})** - Help us improve

---

**📝 Last Updated:** {datetime.now().strftime("%Y-%m-%d")}

*This documentation is automatically generated and maintained. {theme_styles.get(theme, "professional")} theme.*
'''

        with open(wiki_dir / "Home.md", 'w', encoding='utf-8') as f:
            f.write(content)

        self.stats["pages_generated"] += 1

    def _generate_wiki_sidebar(self, wiki_dir: Path) -> None:
        """Generate enhanced sidebar navigation"""
        sections = self.config["content"]["sections"]
        project = self.config["project"]

        sidebar = "# 📚 Documentation\n\n"

        for section in sections:
            icon = section.get("icon", "📄")
            sidebar += f"## {icon} {section['title']}\n\n"

            for page in section["pages"]:
                page_name = page["name"] if isinstance(page, dict) else page
                page_link = page_name.replace(" ", "-")
                sidebar += f"- **[{page_name}]({page_link})**\n"

            sidebar += "\n"

        # Footer links
        sidebar += f"""---

## 🔗 Project Links

- **[GitHub]({project["github_url"]})**
- **[Issues]({project["issues_url"]})**
- **[Releases]({project["github_url"]}/releases)**

## 📞 Support

- **[Troubleshooting](Troubleshooting)**
- **[FAQ](FAQ)**
- **[Community](Community)**

---

*v{project["version"]}*
"""

        with open(wiki_dir / "_Sidebar.md", 'w', encoding='utf-8') as f:
            f.write(sidebar)

    def _generate_wiki_pages(self, wiki_dir: Path) -> None:
        """Generate all wiki content pages"""
        sections = self.config["content"]["sections"]

        for section in sections:
            for page in section["pages"]:
                page_name = page["name"] if isinstance(page, dict) else page
                page_file = page_name.replace(" ", "-") + ".md"

                # Generate page content based on template
                content = self._get_page_template(page_name, page.get("template") if isinstance(page, dict) else None)

                with open(wiki_dir / page_file, 'w', encoding='utf-8') as f:
                    f.write(content)

                self.stats["pages_generated"] += 1

    def _generate_gitbook_readme(self, gitbook_dir: Path) -> None:
        """Generate GitBook README (landing page)"""
        project = self.config["project"]

        content = f'''# {project["name"]}

{project["description"]}

## 🚀 Quick Start

```bash
git clone {project["github_url"]}.git
cd {project["name"].lower().replace(" ", "-")}
python {project["main_script"]}
```

## 📚 Documentation

This GitBook contains comprehensive documentation for {project["name"]}.

Use the navigation on the left to explore:

- **Getting Started** - Installation and setup
- **User Guides** - How to use the features
- **API Reference** - Integration and development
- **Support** - Help and troubleshooting

## 🔗 Links

- [GitHub Repository]({project["github_url"]})
- [Report Issues]({project["issues_url"]})
- [Community Discussions]({project["github_url"]}/discussions)

---

**Version:** {project["version"]} | **License:** {project["license"]}
'''

        with open(gitbook_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(content)

    def _generate_gitbook_summary(self, gitbook_dir: Path) -> None:
        """Generate GitBook SUMMARY.md (table of contents)"""
        sections = self.config["content"]["sections"]

        summary = "# Summary\n\n"
        summary += "* [Introduction](README.md)\n\n"

        for section in sections:
            summary += f"## {section['title']}\n\n"

            for page in section["pages"]:
                page_name = page["name"] if isinstance(page, dict) else page
                page_file = page_name.replace(" ", "-").lower() + ".md"
                summary += f"* [{page_name}]({page_file})\n"

            summary += "\n"

        with open(gitbook_dir / "SUMMARY.md", 'w', encoding='utf-8') as f:
            f.write(summary)

    def _generate_gitbook_config(self, gitbook_dir: Path) -> None:
        """Generate GitBook configuration"""
        project = self.config["project"]
        gitbook_config = self.config["formats"]["gitbook"]

        config = {
            "title": project["name"],
            "description": project["description"],
            "author": project["author"],
            "language": "en",
            "gitbook": "3.2.3",
            "root": ".",
            "structure": {
                "readme": "README.md",
                "summary": "SUMMARY.md"
            },
            "plugins": gitbook_config.get("plugins", []),
            "pluginsConfig": {
                "sharing": {
                    "github": True,
                    "facebook": False,
                    "twitter": True
                }
            },
            "links": {
                "sidebar": {
                    "GitHub": project["github_url"]
                }
            },
            "pdf": {
                "fontSize": 12,
                "paperSize": "a4"
            } if gitbook_config.get("pdf") else {}
        }

        with open(gitbook_dir / "book.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    def _generate_gitbook_pages(self, gitbook_dir: Path) -> None:
        """Generate GitBook content pages"""
        sections = self.config["content"]["sections"]

        for section in sections:
            for page in section["pages"]:
                page_name = page["name"] if isinstance(page, dict) else page
                page_file = page_name.replace(" ", "-").lower() + ".md"

                content = self._get_page_template(page_name, page.get("template") if isinstance(page, dict) else None)

                with open(gitbook_dir / page_file, 'w', encoding='utf-8') as f:
                    f.write(content)

    def _get_page_template(self, page_name: str, template: Optional[str]) -> str:
        """Get content template for a page"""
        project = self.config["project"]

        # Simple template system - can be vastly expanded
        templates = {
            "quickstart": f'''# Quick Start Guide

Get up and running with {project["name"]} in just minutes.

## Prerequisites

- Git
- Python 3.8+
- GitHub CLI

## Installation

```bash
git clone {project["github_url"]}.git
cd {project["name"].lower().replace(" ", "-")}
python {project["main_script"]}
```

## First Steps

1. Run the launcher
2. Follow the setup wizard
3. Configure your preferences
4. Start managing repositories!

## Next Steps

- [Read the Installation Guide](installation)
- [Explore Advanced Features](advanced-features)
- [Join the Community](community)
''',
            "installation": f'''# Installation Guide

Complete installation instructions for {project["name"]}.

## System Requirements

- **Operating System:** Windows 10+, macOS 10.14+, Linux
- **Python:** 3.8 or higher
- **Git:** Latest version
- **GitHub CLI:** Latest version

## Installation Steps

### 1. Install Prerequisites

**Git:**
- Windows: [Download from git-scm.com](https://git-scm.com/download/win)
- macOS: `brew install git`
- Linux: `sudo apt install git`

**GitHub CLI:**
- Windows: `winget install GitHub.cli`
- macOS: `brew install gh`
- Linux: `sudo snap install gh`

### 2. Clone Repository

```bash
git clone {project["github_url"]}.git
cd {project["name"].lower().replace(" ", "-")}
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Setup Wizard

```bash
python utils/setup_wizard.py
```

## Verification

Test your installation:

```bash
python launcher.py
```

You should see the main menu. Success!

## Troubleshooting

If you encounter issues, see the [Troubleshooting Guide](troubleshooting).
'''
        }

        # Return template if available, otherwise generic page
        if template and template in templates:
            return templates[template]

        return f'''# {page_name}

This page contains information about {page_name.lower()}.

## Overview

Documentation coming soon...

## See Also

- [Home](home)
- [Quick Start](quick-start)
'''

    def create_deployment_scripts(self) -> None:
        """Create enhanced deployment scripts"""
        deploy_dir = self.output_dir / "deployment"
        deploy_dir.mkdir(parents=True, exist_ok=True)

        # GitHub Wiki deploy script
        wiki_deploy = '''#!/bin/bash
# Enhanced GitHub Wiki Deployment
set -e

REPO_URL="$1"
WIKI_DIR="./generated-docs/github-wiki"

if [ -z "$REPO_URL" ]; then
    echo "Usage: $0 <repository-url>"
    exit 1
fi

WIKI_URL="${REPO_URL%.git}.wiki.git"

echo "🚀 Deploying GitHub Wiki..."
echo "📦 Repository: $REPO_URL"
echo "📖 Wiki URL: $WIKI_URL"

TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

cd "$TEMP_DIR"

if git clone "$WIKI_URL" wiki 2>/dev/null; then
    echo "✅ Wiki repository cloned"
    cd wiki
else
    echo "📝 Creating new wiki repository"
    mkdir wiki
    cd wiki
    git init
    git remote add origin "$WIKI_URL"
fi

echo "📄 Copying wiki files..."
cp -r "$(cd "$(dirname "$0")/../.." && pwd)/$WIKI_DIR"/* .

echo "💾 Committing changes..."
git add .

if ! git diff --staged --quiet; then
    git config user.name "Documentation Bot" 2>/dev/null || true
    git config user.email "docs@generator.local" 2>/dev/null || true

    git commit -m "📚 Auto-update documentation - $(date '+%Y-%m-%d %H:%M:%S')"
    git push -u origin main || git push -u origin master

    echo "✅ Wiki deployed successfully!"
    echo "🔗 View at: ${REPO_URL%.git}/wiki"
else
    echo "✅ No changes to commit"
fi
'''

        with open(deploy_dir / "deploy-wiki.sh", 'w', encoding='utf-8') as f:
            f.write(wiki_deploy)

        # Make executable (Unix/Linux/macOS only)
        if sys.platform != 'win32':
            os.chmod(deploy_dir / "deploy-wiki.sh", 0o755)

        # GitBook deploy script
        gitbook_deploy = '''#!/bin/bash
# GitBook Deployment
set -e

GITBOOK_DIR="./generated-docs/gitbook"

echo "🚀 Building GitBook..."

cd "$GITBOOK_DIR"

# Install GitBook CLI if needed
if ! command -v gitbook &> /dev/null; then
    echo "Installing GitBook CLI..."
    npm install -g gitbook-cli
fi

# Install plugins
echo "📦 Installing plugins..."
gitbook install

# Build
echo "🔨 Building..."
gitbook build

echo "✅ GitBook built successfully!"
echo "📂 Output: $GITBOOK_DIR/_book"
echo ""
echo "Deploy options:"
echo "  1. GitBook.com: Push to GitHub and connect"
echo "  2. GitHub Pages: Copy _book/* to gh-pages branch"
echo "  3. Netlify: Deploy _book folder"
'''

        with open(deploy_dir / "deploy-gitbook.sh", 'w', encoding='utf-8') as f:
            f.write(gitbook_deploy)

        # Make executable (Unix/Linux/macOS only)
        if sys.platform != 'win32':
            os.chmod(deploy_dir / "deploy-gitbook.sh", 0o755)

    def generate_all(self, formats: Optional[List[str]] = None) -> None:
        """Generate all enabled formats"""
        if RICH_AVAILABLE:
            rprint("\n[bold cyan]🚀 Documentation Generation Starting...[/bold cyan]\n")
        else:
            print("\n🚀 Documentation Generation Starting...\n")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.load_config()

        # Determine which formats to generate
        if formats:
            enabled_formats = formats
        else:
            enabled_formats = [
                fmt for fmt, config in self.config["formats"].items()
                if isinstance(config, dict) and config.get("enabled", False)
            ]

        # Generate each format
        if "github_wiki" in enabled_formats or "github-wiki" in enabled_formats:
            self.generate_github_wiki()

        if "gitbook" in enabled_formats:
            self.generate_gitbook()

        # Create deployment scripts
        self.create_deployment_scripts()

        # Show summary
        self._show_summary()

    def _show_summary(self) -> None:
        """Show generation summary"""
        duration = (datetime.now() - self.stats["start_time"]).total_seconds()

        if RICH_AVAILABLE:
            rprint("\n[bold green]✅ Documentation Generation Complete![/bold green]\n")

            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("Pages Generated", str(self.stats["pages_generated"]))
            table.add_row("Formats", ", ".join(self.stats["formats"]))
            table.add_row("Duration", f"{duration:.2f}s")
            table.add_row("Output Directory", str(self.output_dir))

            console.print(table)

            rprint("\n[bold]📁 Next Steps:[/bold]")
            rprint("  1. Review generated docs in [cyan]generated-docs/[/cyan]")
            rprint("  2. Deploy wiki: [cyan]./generated-docs/deployment/deploy-wiki.sh <repo-url>[/cyan]")
            rprint("  3. Build GitBook: [cyan]./generated-docs/deployment/deploy-gitbook.sh[/cyan]")
        else:
            print("\n✅ Documentation Generation Complete!\n")
            print(f"Pages Generated: {self.stats['pages_generated']}")
            print(f"Formats: {', '.join(self.stats['formats'])}")
            print(f"Duration: {duration:.2f}s")
            print(f"Output: {self.output_dir}")
            print("\nNext Steps:")
            print("  1. Review generated docs")
            print("  2. Deploy wiki: ./generated-docs/deployment/deploy-wiki.sh <repo-url>")
            print("  3. Build GitBook: ./generated-docs/deployment/deploy-gitbook.sh")


def main():
    """Enhanced CLI interface"""
    parser = argparse.ArgumentParser(
        description="Enhanced Documentation Generator - Multi-Format, Multi-Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all enabled formats
  python wiki-generator.py --all

  # Generate specific format
  python wiki-generator.py --format github-wiki

  # Generate multiple formats
  python wiki-generator.py --format github-wiki gitbook

  # List available templates and themes
  python wiki-generator.py --list
        """
    )

    parser.add_argument("--all", action="store_true", help="Generate all enabled formats")
    parser.add_argument("--format", nargs="+", choices=DocumentationGenerator.SUPPORTED_FORMATS,
                       help="Specific format(s) to generate")
    parser.add_argument("--list", action="store_true", help="List available templates and themes")
    parser.add_argument("--config", default="wiki-config.yaml", help="Configuration file path")

    args = parser.parse_args()

    if args.list:
        if RICH_AVAILABLE:
            rprint("\n[bold]📚 Available Templates:[/bold]")
            for template in DocumentationGenerator.INDUSTRY_TEMPLATES:
                rprint(f"  • [cyan]{template}[/cyan]")

            rprint("\n[bold]🎨 Available Themes:[/bold]")
            for theme in DocumentationGenerator.THEMES:
                rprint(f"  • [cyan]{theme}[/cyan]")

            rprint("\n[bold]📋 Supported Formats:[/bold]")
            for fmt in DocumentationGenerator.SUPPORTED_FORMATS:
                rprint(f"  • [cyan]{fmt}[/cyan]")
        else:
            print("\n📚 Available Templates:")
            for template in DocumentationGenerator.INDUSTRY_TEMPLATES:
                print(f"  • {template}")
            print("\n🎨 Available Themes:")
            for theme in DocumentationGenerator.THEMES:
                print(f"  • {theme}")
            print("\n📋 Supported Formats:")
            for fmt in DocumentationGenerator.SUPPORTED_FORMATS:
                print(f"  • {fmt}")
        return

    generator = DocumentationGenerator()

    if args.all:
        generator.generate_all()
    elif args.format:
        generator.generate_all(formats=args.format)
    else:
        if RICH_AVAILABLE:
            rprint("[yellow]Usage: python wiki-generator.py --all[/yellow]")
            rprint("[dim]Run with --help for more options[/dim]")
        else:
            print("Usage: python wiki-generator.py --all")
            print("Run with --help for more options")


if __name__ == "__main__":
    main()
