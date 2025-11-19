# Complete Wiki & GitBook Generation Guide

Transform your GitHub repository into professional documentation in minutes!

## Overview

GitSage provides two powerful generators:
1. **Basic Wiki Generator** (`wiki-generator.py`) - Simple, fast wiki creation
2. **Enhanced Wiki Generator** (`wiki-generator-enhanced.py`) - Advanced features with GitBook support

Both create:
- ✅ GitHub Wiki pages
- ✅ GitBook-compatible documentation
- ✅ Markdown files ready for deployment
- ✅ Professional structure and navigation

---

## Quick Start (5 Minutes)

### 1. Configure Your Project

Edit `wiki-config.yaml`:

```yaml
project:
  name: "My Awesome Project"
  description: "A comprehensive tool for amazing things"
  version: "1.0.0"
  author: "Your Name"
  license: "MIT"
  github_url: "https://github.com/yourusername/your-repo"

content:
  sections:
    - title: "Getting Started"
      pages:
        - "Home"
        - "Installation"
        - "Quick Start"
    - title: "User Guide"
      pages:
        - "Features"
        - "Configuration"
        - "Examples"
    - title: "Advanced"
      pages:
        - "API Reference"
        - "Contributing"
        - "FAQ"
```

### 2. Generate Documentation

```bash
# Using enhanced generator (recommended)
python wiki-generator-enhanced.py

# OR using basic generator
python wiki-generator.py
```

### 3. Review Output

Check `generated-docs/` directory:
```
generated-docs/
├── Home.md                    # Main landing page
├── Installation.md
├── Quick-Start.md
├── Features.md
├── SUMMARY.md                 # GitBook structure
└── deployment/
    └── deploy-wiki.sh         # Deployment script
```

### 4. Deploy to GitHub Wiki

```bash
cd generated-docs/deployment
./deploy-wiki.sh https://github.com/yourusername/your-repo.git
```

---

## Configuration Reference

### Project Metadata

```yaml
project:
  name: "Project Name"           # Required
  description: "Project description"
  version: "1.0.0"               # Semantic versioning
  author: "Author Name"
  license: "MIT"                 # License type
  github_url: "https://..."      # Full GitHub URL
  main_script: "main.py"         # Entry point (optional)
  primary_feature: "Description" # Key feature (optional)
```

### Documentation Settings

```yaml
documentation:
  wiki_enabled: true            # Generate GitHub Wiki
  gitbook_enabled: true         # Generate GitBook structure
  github_pages: true            # GitHub Pages ready
  api_docs: false              # API documentation (future)
```

### Wiki Features

```yaml
wiki:
  sidebar: true                # Generate sidebar navigation
  search: true                 # Enable search functionality
  auto_nav: true               # Automatic navigation links
  custom_css: true             # Include custom styling
```

### GitBook Settings

```yaml
gitbook:
  theme: "default"             # GitBook theme
  plugins:                     # GitBook plugins
    - "search"
    - "sharing"
    - "fontsettings"
    - "theme-api"
  structure: "auto"            # Auto-generate structure
```

### Content Structure

```yaml
content:
  sections:
    - title: "Section Name"    # Section header
      pages:                   # List of pages
        - "Page-Name"          # Will create Page-Name.md
        - "Another-Page"
    - title: "Another Section"
      pages:
        - "More-Pages"
```

---

## Generator Comparison

| Feature | Basic Generator | Enhanced Generator |
|---------|----------------|-------------------|
| GitHub Wiki | ✅ Yes | ✅ Yes |
| GitBook Support | ❌ No | ✅ Yes |
| Custom Templates | ❌ No | ✅ Yes |
| Auto Navigation | ✅ Basic | ✅ Advanced |
| Deployment Script | ✅ Yes | ✅ Yes |
| Customization | ⚠️ Limited | ✅ Extensive |
| Speed | ⚡ Fastest | ⚡ Fast |
| Best For | Quick wikis | Professional docs |

**Recommendation:** Use Enhanced Generator for most projects.

---

## Enhanced Generator Features

### 1. Template System

The enhanced generator uses customizable templates:

```python
# Templates are built-in but can be customized
# Located in wiki-generator-enhanced.py

# Home page template
HOME_TEMPLATE = """
# {project_name}

{description}

## Features
- Feature 1
- Feature 2

## Quick Start
...
"""
```

### 2. Auto-Generated Content

**Home Page:**
- Project overview
- Key features
- Quick start guide
- Navigation links

**Installation Page:**
- Prerequisites
- Installation steps
- Platform-specific instructions
- Verification

**API Reference:**
- Module documentation
- Function references
- Usage examples

### 3. GitBook Integration

Creates `SUMMARY.md` for GitBook:

```markdown
# Summary

* [Home](Home.md)

## Getting Started
* [Installation](Installation.md)
* [Quick Start](Quick-Start.md)

## User Guide
* [Features](Features.md)
* [Configuration](Configuration.md)

## Advanced
* [API Reference](API-Reference.md)
```

### 4. Navigation System

**Sidebar Navigation:**
```markdown
## Navigation
- [Home](Home.md)
- [Installation](Installation.md)
- [Features](Features.md)
```

**Breadcrumbs:**
```markdown
Home > User Guide > Features
```

**Previous/Next Links:**
```markdown
← [Previous: Installation](Installation.md) | [Next: Configuration →](Configuration.md)
```

---

## Deployment Options

### Option 1: GitHub Wiki (Recommended)

```bash
# Generated deployment script
cd generated-docs/deployment
./deploy-wiki.sh https://github.com/user/repo.git

# Manual deployment
cd generated-docs
git init
git add .
git commit -m "Initialize wiki"
git remote add origin https://github.com/user/repo.wiki.git
git push -u origin master
```

### Option 2: GitBook

```bash
# Install GitBook CLI
npm install -g gitbook-cli

# Navigate to generated docs
cd generated-docs

# Initialize GitBook
gitbook init

# Serve locally
gitbook serve

# Build for deployment
gitbook build

# Output in _book/ directory
```

### Option 3: GitHub Pages

```bash
# Create gh-pages branch
git checkout -b gh-pages

# Copy generated docs
cp -r generated-docs/* .

# Commit and push
git add .
git commit -m "Deploy documentation"
git push origin gh-pages

# Enable in repository settings:
# Settings > Pages > Source: gh-pages branch
```

### Option 4: Custom Hosting

```bash
# Generated docs are static files
# Upload generated-docs/ to:
# - Netlify
# - Vercel
# - S3
# - Any static hosting
```

---

## Advanced Customization

### Custom Page Templates

Create your own templates by modifying the generator:

```python
# In wiki-generator-enhanced.py

CUSTOM_TEMPLATE = """
# {page_title}

{custom_content}

## Table of Contents
{toc}

## Content
{main_content}

## See Also
{related_links}
"""
```

### Adding Custom Pages

Add to `wiki-config.yaml`:

```yaml
content:
  sections:
    - title: "Custom Section"
      pages:
        - "Custom-Page"
```

Then create `templates/Custom-Page.md`:

```markdown
# Custom Page

Your custom content here.
```

### Styling and Themes

**GitHub Wiki CSS:**

Create `custom.css` in generated docs:

```css
/* Custom wiki styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.markdown-body {
    max-width: 900px;
    margin: 0 auto;
}

h1 {
    color: #0366d6;
    border-bottom: 2px solid #0366d6;
}
```

**GitBook Theme:**

Create `book.json`:

```json
{
  "title": "My Project Docs",
  "theme": "default",
  "plugins": [
    "search",
    "highlight",
    "sharing",
    "custom-css"
  ],
  "pluginsConfig": {
    "theme-default": {
      "showLevel": true
    }
  }
}
```

---

## Examples

### Example 1: Open Source Project

```yaml
project:
  name: "AwesomeLib"
  description: "A powerful library for awesome things"
  version: "2.1.0"
  author: "Open Source Contributors"
  license: "Apache 2.0"
  github_url: "https://github.com/org/awesomelib"

content:
  sections:
    - title: "Introduction"
      pages:
        - "Home"
        - "Why AwesomeLib"
        - "Installation"
    - title: "Getting Started"
      pages:
        - "Quick Start"
        - "Basic Usage"
        - "Examples"
    - title: "Documentation"
      pages:
        - "API Reference"
        - "Configuration"
        - "Advanced Topics"
    - title: "Community"
      pages:
        - "Contributing"
        - "Code of Conduct"
        - "FAQ"
        - "Changelog"
```

### Example 2: Personal Project

```yaml
project:
  name: "My Cool App"
  description: "An app that does cool things"
  version: "1.0.0"
  author: "Your Name"
  license: "MIT"
  github_url: "https://github.com/username/cool-app"

content:
  sections:
    - title: "Guide"
      pages:
        - "Home"
        - "Installation"
        - "How to Use"
        - "Tips and Tricks"
```

### Example 3: Documentation Only

```yaml
project:
  name: "Project Documentation"
  description: "Comprehensive documentation for our project"
  version: "1.0.0"

content:
  sections:
    - title: "Overview"
      pages:
        - "Home"
        - "Architecture"
    - title: "Guides"
      pages:
        - "User Guide"
        - "Admin Guide"
        - "Developer Guide"
    - title: "Reference"
      pages:
        - "API"
        - "CLI"
        - "Configuration"
```

---

## Troubleshooting

### Issue: Generated files are empty

**Solution:**
```bash
# Check wiki-config.yaml syntax
python -c "import yaml; yaml.safe_load(open('wiki-config.yaml'))"

# Validate configuration
python wiki-generator-enhanced.py --validate
```

### Issue: Deployment fails

**Solution:**
```bash
# Verify GitHub credentials
gh auth status

# Check repository access
gh repo view user/repo

# Manual deployment
cd generated-docs
git init
git add .
git commit -m "Initial wiki"
git push https://github.com/user/repo.wiki.git master
```

### Issue: GitBook won't build

**Solution:**
```bash
# Reinstall GitBook
npm uninstall -g gitbook-cli
npm install -g gitbook-cli

# Clear cache
rm -rf ~/.gitbook

# Try again
gitbook serve
```

### Issue: Links are broken

**Solution:**
- Use relative links: `[Link](Page.md)` not `[Link](/Page.md)`
- Match filename casing exactly
- Use hyphens in filenames: `Quick-Start.md` not `Quick Start.md`

---

## Best Practices

### Documentation Structure

✅ **DO:**
- Organize by user journey (Getting Started → Advanced)
- Keep pages focused and concise
- Use clear, descriptive titles
- Include code examples
- Add navigation links

❌ **DON'T:**
- Create overly long pages
- Use unclear page names
- Forget to update SUMMARY.md
- Mix concepts in single pages

### Content Guidelines

✅ **DO:**
- Write for your audience (novice, intermediate, expert)
- Use examples and screenshots
- Include troubleshooting sections
- Keep language simple and clear
- Update regularly

❌ **DON'T:**
- Assume knowledge
- Use jargon without explanation
- Forget to test examples
- Leave outdated information

### Maintenance

**Regular Updates:**
```bash
# Update documentation
cd your-project
python /path/to/gitsage/wiki-generator-enhanced.py

# Review changes
cd generated-docs
git diff

# Deploy updates
git add .
git commit -m "Update documentation"
git push
```

**Version Control:**
```bash
# Keep generated docs in version control
git add generated-docs/
git commit -m "Update documentation for v2.0"
```

---

## Integration with Development Workflow

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Auto-generate documentation before commits
python /path/to/gitsage/wiki-generator-enhanced.py

# Add generated docs
git add generated-docs/
```

### CI/CD Integration

**GitHub Actions:**

```yaml
name: Update Documentation
on:
  push:
    branches: [main]
    paths:
      - 'wiki-config.yaml'
      - 'README.md'

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate docs
        run: |
          pip install PyYAML rich
          python wiki-generator-enhanced.py
      - name: Deploy to wiki
        run: |
          cd generated-docs
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git init
          git add .
          git commit -m "Auto-update documentation"
          git push -f https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.wiki.git master
```

---

## Advanced Features

### Multi-Language Support

```yaml
content:
  languages:
    - en: "English"
    - es: "Español"
    - fr: "Français"

  sections:
    en:
      - title: "Getting Started"
        pages: ["Home", "Installation"]
    es:
      - title: "Comenzando"
        pages: ["Inicio", "Instalación"]
```

### Versioned Documentation

```bash
# Generate docs for specific version
python wiki-generator-enhanced.py --version 2.0

# Creates versioned structure
generated-docs/
├── v1.0/
├── v2.0/
└── latest/
```

### API Documentation Integration

```yaml
documentation:
  api_docs: true
  api_format: "openapi"  # or "swagger", "raml"
  api_file: "api-spec.yaml"
```

---

## Getting Help

**Common Questions:**

**Q: Can I use this for private repositories?**
A: Yes! Just authenticate with `gh auth login`.

**Q: How do I update existing documentation?**
A: Re-run the generator. It will overwrite files in `generated-docs/`.

**Q: Can I customize the templates?**
A: Yes! Edit the template strings in `wiki-generator-enhanced.py`.

**Q: Does this work with monorepos?**
A: Yes! Configure `wiki-config.yaml` for each project.

**Q: How do I add images?**
A: Place images in `generated-docs/images/` and reference: `![Alt](images/img.png)`

---

**You're now ready to create professional documentation for any project!** 📚

Next steps:
1. Configure `wiki-config.yaml` for your project
2. Run `python wiki-generator-enhanced.py`
3. Review generated docs in `generated-docs/`
4. Deploy to GitHub Wiki or GitBook

For more examples, see the `examples/` directory.
