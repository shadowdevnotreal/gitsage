#!/usr/bin/env python3
"""
Automated Wiki & GitBook Generator System
=========================================
Automatically generates GitHub wikis, GitBooks, and documentation sites from templates.
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

class WikiGenerator:
    """Automated wiki and documentation generator"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.config = {}
        self.templates_dir = self.project_root / "wiki-templates"
        self.output_dir = self.project_root / "generated-docs"
        
    def load_config(self, config_file: str = "wiki-config.yaml"):
        """Load project configuration"""
        config_path = self.project_root / config_file
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        else:
            # Generate default config
            self.config = self.generate_default_config()
            self.save_config(config_file)
            
        return self.config
    
    def generate_default_config(self) -> Dict[str, Any]:
        """Generate default configuration"""
        return {
            "project": {
                "name": "GitHub Repository Manager",
                "description": "A comprehensive tool for managing GitHub repositories",
                "version": "1.0.0",
                "author": "Repository Manager Contributors",
                "license": "MIT",
                "github_url": "https://github.com/user/github-repo-manager",
                "main_script": "delete-repo.sh",
                "primary_feature": "Interactive Repository Deletion"
            },
            "documentation": {
                "wiki_enabled": True,
                "gitbook_enabled": True,
                "github_pages": True,
                "api_docs": False
            },
            "wiki": {
                "sidebar": True,
                "search": True,
                "auto_nav": True,
                "custom_css": True
            },
            "gitbook": {
                "theme": "default",
                "plugins": ["search", "sharing", "fontsettings", "theme-api"],
                "structure": "auto"
            },
            "content": {
                "sections": [
                    {
                        "title": "Getting Started",
                        "pages": ["Home", "Quick-Start-Guide", "Installation"]
                    },
                    {
                        "title": "User Guides",
                        "pages": ["Deletion-Script-Guide", "Advanced-Features", "Platform-Guides"]
                    },
                    {
                        "title": "Technical",
                        "pages": ["System-Architecture", "API-Reference", "Contributing"]
                    },
                    {
                        "title": "Support",
                        "pages": ["Troubleshooting", "FAQ", "Community"]
                    }
                ]
            }
        }
    
    def save_config(self, config_file: str = "wiki-config.yaml"):
        """Save configuration to file"""
        config_path = self.project_root / config_file
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Configuration saved to {config_file}")
    
    def create_wiki_structure(self):
        """Create complete wiki file structure"""
        wiki_dir = self.output_dir / "wiki"
        wiki_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate all wiki pages
        self.generate_wiki_home(wiki_dir)
        self.generate_wiki_sidebar(wiki_dir)
        self.generate_user_guides(wiki_dir)
        self.generate_technical_docs(wiki_dir)
        self.generate_support_docs(wiki_dir)
        
        print(f"✅ Wiki structure created in {wiki_dir}")
        return wiki_dir
    
    def generate_wiki_home(self, wiki_dir: Path):
        """Generate wiki home page"""
        project = self.config["project"]
        
        content = f'''# Welcome to {project["name"]} Wiki

> {project["description"]}

## 🚀 Quick Navigation

### 📖 **Getting Started**
- **[Quick Start Guide](Quick-Start-Guide)** - Get up and running in 5 minutes
- **[Installation Guide](Installation)** - Complete setup instructions
- **[System Requirements](System-Requirements)** - Prerequisites and compatibility

### 🛠️ **User Guides**
- **[{project["primary_feature"]} Guide]({project["primary_feature"].replace(" ", "-")}-Guide)** - Main feature documentation
- **[Advanced Features](Advanced-Features)** - Power user functionality
- **[Platform-Specific Guides](Platform-Guides)** - Windows, macOS, Linux instructions

### 🧠 **Technical Documentation**
- **[System Architecture](System-Architecture)** - How everything works
- **[API Reference](API-Reference)** - Integration and automation
- **[Contributing Guide](Contributing)** - Development and contribution

### 🆘 **Support & Community**
- **[Troubleshooting](Troubleshooting)** - Common issues and solutions
- **[FAQ](FAQ)** - Frequently asked questions
- **[Community](Community)** - Getting help and contributing

## 📊 **Project Stats**

| Metric | Value |
|--------|-------|
| **Version** | {project["version"]} |
| **License** | {project["license"]} |
| **Platform Support** | Windows, macOS, Linux |
| **Main Language** | Bash/Python |

## 🔗 **Quick Links**

- **[GitHub Repository]({project["github_url"]})** - Source code and releases
- **[Download Latest Release]({project["github_url"]}/releases/latest)** - Get started now
- **[Report Issues]({project["github_url"]}/issues)** - Bug reports and feature requests
- **[Discussions]({project["github_url"]}/discussions)** - Community discussions

## 📝 **Latest Updates**

This wiki is automatically generated and kept in sync with the project documentation. For the latest changes, see the [CHANGELOG]({project["github_url"]}/blob/main/CHANGELOG.md).

---

**⚠️ Important**: Always ensure you have backups before performing destructive operations.

**Need help?** Check out our [Troubleshooting Guide](Troubleshooting) or [open an issue]({project["github_url"]}/issues).
'''
        
        with open(wiki_dir / "Home.md", 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_wiki_sidebar(self, wiki_dir: Path):
        """Generate wiki sidebar navigation"""
        sections = self.config["content"]["sections"]
        
        sidebar_content = "## 📚 Documentation\n\n"
        
        for section in sections:
            sidebar_content += f"### {section['title']}\n"
            for page in section['pages']:
                # Convert page names to proper titles
                title = page.replace('-', ' ').replace('_', ' ')
                sidebar_content += f"- **[{title}]({page})**\n"
            sidebar_content += "\n"
        
        sidebar_content += """
## 🔗 External Links

- **[Main Repository](https://github.com/user/github-repo-manager)**
- **[Latest Release](https://github.com/user/github-repo-manager/releases/latest)**
- **[Issues](https://github.com/user/github-repo-manager/issues)**
- **[Discussions](https://github.com/user/github-repo-manager/discussions)**

## 📞 Quick Support

- **[Troubleshooting](Troubleshooting)**
- **[FAQ](FAQ)**
- **[Community Help](Community)**
"""
        
        with open(wiki_dir / "_Sidebar.md", 'w', encoding='utf-8') as f:
            f.write(sidebar_content)
    
    def generate_user_guides(self, wiki_dir: Path):
        """Generate user guide pages"""
        project = self.config["project"]
        
        # Quick Start Guide
        quick_start = f'''# Quick Start Guide

Get up and running with {project["name"]} in just a few minutes!

## 🚀 Installation

### Prerequisites
1. **Git** - [Download here](https://git-scm.com/)
2. **GitHub CLI** - [Download here](https://cli.github.com/)
3. **Python 3.6+** - [Download here](https://python.org/)

### Quick Install
```bash
# Clone the repository
git clone {project["github_url"]}.git
cd {project["name"].lower().replace(" ", "-")}

# Run the launcher
python launcher.py
```

## 🎯 First Steps

1. **Choose Your Interface**
   - Option 1: `🗑️ DELETE REPOSITORY` - Original deletion script
   - Option 2: `🔧 Advanced Features` - Enhanced functionality

2. **Select a Repository**
   - Browse your repository list
   - View repository details
   - Choose operation type

3. **Confirm Operations**
   - Read all safety prompts carefully
   - Confirm destructive operations
   - Monitor progress and results

## ⚡ Quick Examples

### Delete a Repository
```bash
# Run the main script
./delete-repo.sh

# Or use the launcher
python launcher.py
# Choose option 1: "🗑️ DELETE REPOSITORY"
```

### Reset Git History
1. Launch any interface
2. Select "Reset Git History"
3. Choose repository and commit message
4. Confirm the operation

## 🔗 Next Steps

- **[Advanced Features](Advanced-Features)** - Explore more functionality
- **[Platform Guides](Platform-Guides)** - OS-specific instructions
- **[Safety Guide](Safety-Guide)** - Best practices and safety tips
'''
        
        with open(wiki_dir / "Quick-Start-Guide.md", 'w', encoding='utf-8') as f:
            f.write(quick_start)
    
    def generate_technical_docs(self, wiki_dir: Path):
        """Generate technical documentation"""
        
        # System Architecture
        architecture = '''# System Architecture & Logic

Understanding how the GitHub Repository Manager system works.

## 🏗️ Overall Architecture

### Progressive Enhancement Design
```
Simple → Complex
Basic User → Power User  
Single Script → Full Suite
```

The system uses a **progressive complexity** approach:
1. **Entry Level**: Standalone deletion script
2. **Intermediate**: Enhanced versions with more features
3. **Advanced**: Full GUI and multi-platform support
4. **Expert**: Direct script execution and automation

## 🔄 Component Relationships

### Central Hub Pattern
```
           launcher.py (Universal Detector)
                    ↙️        ↓        ↘️
        delete-repo.sh    Enhanced     GUI/CLI
        (Original)        Versions     Versions
              ↓              ↓            ↓
        Single Purpose   Multi-Feature  Full Suite
```

### Design Philosophy
1. **Autonomous scripts** - Each works independently
2. **Shared safety logic** - Consistent protection across all versions
3. **Progressive disclosure** - Show complexity only when needed
4. **Platform adaptation** - Best experience for each environment

## 🛡️ Safety Architecture

### Multi-Layer Safety Pattern
```
User Intent → Validation → Confirmation → Execution → Verification
     ↓             ↓            ↓           ↓            ↓
  What do you   Does repo    Are you     Perform      Did it
    want?       exist?       sure?       action       work?
```

This architecture ensures the system is **safe by default**, **grows with users**, and **adapts to different environments** while maintaining consistency across all interfaces.
'''
        
        with open(wiki_dir / "System-Architecture.md", 'w', encoding='utf-8') as f:
            f.write(architecture)
    
    def generate_support_docs(self, wiki_dir: Path):
        """Generate support documentation"""
        
        # Troubleshooting guide
        troubleshooting = '''# Troubleshooting Guide

Common issues and solutions for GitHub Repository Manager.

## 🚨 Common Issues

### "Command not found" Errors

#### Git not found
**Solutions**:
```bash
# Windows: Download from https://git-scm.com/download/win
# macOS: brew install git
# Linux: sudo apt install git
```

#### GitHub CLI not found
**Solutions**:
```bash
# Windows: winget install GitHub.cli
# macOS: brew install gh  
# Linux: sudo snap install gh
```

### Authentication Issues

#### GitHub CLI not authenticated
**Solutions**:
```bash
gh auth login
# Follow prompts for web authentication
```

## 🆘 Getting More Help

- **[GitHub Issues](https://github.com/user/repo/issues)** - Bug reports
- **[GitHub Discussions](https://github.com/user/repo/discussions)** - Community help
'''
        
        with open(wiki_dir / "Troubleshooting.md", 'w', encoding='utf-8') as f:
            f.write(troubleshooting)
    
    def create_deployment_scripts(self):
        """Create deployment automation scripts"""
        deploy_dir = self.output_dir / "deployment"
        deploy_dir.mkdir(parents=True, exist_ok=True)
        
        # GitHub Wiki deployment script
        wiki_deploy = '''#!/bin/bash
# GitHub Wiki Deployment Script
set -e

REPO_URL="$1"
WIKI_DIR="./generated-docs/wiki"

if [ -z "$REPO_URL" ]; then
    echo "Usage: $0 <repository-url>"
    exit 1
fi

WIKI_URL="${REPO_URL%.git}.wiki.git"

echo "🚀 Deploying Wiki to GitHub..."
echo "Repository: $REPO_URL"
echo "Wiki URL: $WIKI_URL"

# Create temporary directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

cd "$TEMP_DIR"

# Clone or initialize wiki
if git clone "$WIKI_URL" wiki 2>/dev/null; then
    echo "✅ Wiki repository cloned"
    cd wiki
else
    echo "📝 Initializing new wiki repository"
    mkdir wiki
    cd wiki
    git init
    git remote add origin "$WIKI_URL"
fi

# Copy wiki files
echo "📄 Copying wiki files..."
cp -r "$(cd "$(dirname "$0")/../.." && pwd)/$WIKI_DIR"/* .

# Commit and push
echo "💾 Committing changes..."
git add .

if ! git diff --staged --quiet; then
    git config user.name "Wiki Generator" 2>/dev/null || true
    git config user.email "wiki@generator.local" 2>/dev/null || true
    
    git commit -m "Auto-update wiki documentation $(date '+%Y-%m-%d %H:%M:%S')"
    git push -u origin main || git push -u origin master
    
    echo "✅ Wiki deployed successfully!"
else
    echo "✅ No changes to commit"
fi

echo "🔗 View your wiki at: ${REPO_URL%.git}/wiki"
'''
        
        with open(deploy_dir / "deploy-wiki.sh", 'w', encoding='utf-8') as f:
            f.write(wiki_deploy)
        
        os.chmod(deploy_dir / "deploy-wiki.sh", 0o755)
        
        # Complete setup script
        setup_script = '''#!/bin/bash
# Complete Documentation Setup
set -e

REPO_URL="$1"

if [ -z "$REPO_URL" ]; then
    echo "Usage: $0 <repository-url>"
    echo "Example: $0 https://github.com/user/repo.git"
    exit 1
fi

echo "🚀 Complete Documentation Setup"
echo "Repository: $REPO_URL"

# Generate documentation
echo "📝 Generating documentation..."
python wiki-generator.py --all

echo "📖 Deploying Wiki..."
./generated-docs/deployment/deploy-wiki.sh "$REPO_URL"

echo "🎉 Documentation setup complete!"
echo "📖 Wiki: ${REPO_URL%.git}/wiki"
'''
        
        with open(deploy_dir / "setup-docs.sh", 'w', encoding='utf-8') as f:
            f.write(setup_script)
            
        os.chmod(deploy_dir / "setup-docs.sh", 0o755)
        
        print(f"✅ Deployment scripts created in {deploy_dir}")
    
    def generate_all(self):
        """Generate all documentation formats"""
        print("🚀 Starting documentation generation...")
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.load_config()
        
        if self.config["documentation"]["wiki_enabled"]:
            self.create_wiki_structure()
        
        self.create_deployment_scripts()
        
        print(f"\n✅ Documentation generation complete!")
        print(f"📁 Output directory: {self.output_dir}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Automated Wiki & GitBook Generator")
    parser.add_argument("--all", action="store_true", help="Generate all formats")
    parser.add_argument("--wiki-only", action="store_true", help="Generate wiki only")
    
    args = parser.parse_args()
    
    generator = WikiGenerator()
    
    if args.all or args.wiki_only:
        generator.generate_all()
    else:
        print("🚀 Automated Wiki & GitBook Generator")
        print("Usage: python wiki-generator.py --all")

if __name__ == "__main__":
    main()
