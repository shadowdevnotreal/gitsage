<#
.SYNOPSIS
    GitSage Wiki Generator - PowerShell Version
.DESCRIPTION
    Generate complete GitHub Wiki documentation with Table of Contents,
    beautiful formatting, and automated setup instructions.
.PARAMETER All
    Generate all wiki pages (default)
.PARAMETER Page
    Generate specific page (Home, Installation, Usage, API, Contributing, FAQ)
.PARAMETER ShowSetup
    Show GitHub Wiki setup instructions
.PARAMETER Output
    Output directory for wiki pages (default: wiki/)
.EXAMPLE
    .\Generate-Wiki.ps1 -All
    .\Generate-Wiki.ps1 -Page Home
    .\Generate-Wiki.ps1 -ShowSetup
#>

param(
    [switch]$All,
    [switch]$ShowSetup,
    [string]$Page,
    [string]$Output = ""  # Empty means use default output folder
)

# ============================================
# Output Folder Configuration
# ============================================
$DefaultOutputDir = ".\gitsage-output"
$WikiOutputDir = "$DefaultOutputDir\wiki"

# Create output directories
if (-not (Test-Path $DefaultOutputDir)) {
    New-Item -ItemType Directory -Path $DefaultOutputDir -Force | Out-Null
}
if (-not (Test-Path $WikiOutputDir)) {
    New-Item -ItemType Directory -Path $WikiOutputDir -Force | Out-Null
}

# Set default output path if not specified
if ([string]::IsNullOrEmpty($Output)) {
    $Output = $WikiOutputDir
}

# Color output functions
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success { param([string]$Message) Write-ColorOutput "[OK] $Message" "Green" }
function Write-Info { param([string]$Message) Write-ColorOutput "[>>] $Message" "Cyan" }
function Write-Warning { param([string]$Message) Write-ColorOutput "[WARN] $Message" "Yellow" }
function Write-Error { param([string]$Message) Write-ColorOutput "[FAIL] $Message" "Red" }

# Get GitHub repository info
function Get-GitHubInfo {
    try {
        $remoteUrl = git config --get remote.origin.url
        if ($remoteUrl -match "github.com[:/](.+)/(.+)\.git") {
            return @{
                Username = $matches[1]
                Repo = $matches[2]
                Url = "https://github.com/$($matches[1])/$($matches[2])"
            }
        }
    } catch {}

    return @{
        Username = "username"
        Repo = (Get-Item .).Name
        Url = "https://github.com/username/$((Get-Item .).Name)"
    }
}

# Show GitHub Wiki setup instructions
function Show-WikiSetupInstructions {
    $info = Get-GitHubInfo

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " [>>] GitHub Wiki Setup Instructions" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    Write-ColorOutput "Your wiki pages are ready! But first, enable Wiki in GitHub:" "Yellow"
    Write-Host ""

    Write-ColorOutput "Step 1: Go to Repository Settings" "White"
    Write-Host "  $($info.Url)/settings" -ForegroundColor Gray
    Write-Host ""

    Write-ColorOutput "Step 2: Scroll to 'Features' section" "White"
    Write-Host ""

    Write-ColorOutput "Step 3: Check the 'Wikis' checkbox" "White"
    Write-Host ""

    Write-ColorOutput "Step 4: Initialize Wiki" "White"
    Write-Host "  Go to: $($info.Url)/wiki" -ForegroundColor Gray
    Write-Host "  Click 'Create the first page'" -ForegroundColor Gray
    Write-Host "  Add any content and save (we'll replace it)" -ForegroundColor Gray
    Write-Host ""

    Write-ColorOutput "Step 5: Clone Wiki Repository" "White"
    Write-Host "  git clone $($info.Url).wiki.git" -ForegroundColor Gray
    Write-Host ""

    Write-ColorOutput "Step 6: Copy Generated Pages" "White"
    Write-Host "  Copy files from wiki/ to $($info.Repo).wiki/" -ForegroundColor Gray
    Write-Host ""

    Write-ColorOutput "Step 7: Commit and Push" "White"
    Write-Host "  cd $($info.Repo).wiki" -ForegroundColor Gray
    Write-Host "  git add ." -ForegroundColor Gray
    Write-Host "  git commit -m `"Update wiki pages`"" -ForegroundColor Gray
    Write-Host "  git push origin master" -ForegroundColor Gray
    Write-Host ""

    Write-Success "Once complete, your wiki will be live at: $($info.Url)/wiki"
    Write-Host ""
}

# Generate wiki page with footer
function New-WikiPage {
    param(
        [string]$Title,
        [string]$Content,
        [string]$Filename
    )

    $info = Get-GitHubInfo
    $year = (Get-Date).Year

    $footer = @"

---

## [>>] Navigation

- [Home](Home) - Project Overview
- [Installation](Installation) - Setup Guide
- [Usage](Usage) - How to Use
- [API Reference](API-Reference) - API Documentation
- [Contributing](Contributing) - Contribution Guide
- [FAQ](FAQ) - Frequently Asked Questions

---

## [!] Resources

- [GitHub Repository]($($info.Url))
- [Issues]($($info.Url)/issues)
- [Discussions]($($info.Url)/discussions)

---

_Last Updated: $(Get-Date -Format "yyyy-MM-dd") | $($info.Repo) © $year_
"@

    return $Content + $footer
}

# Generate Home page
function New-HomePage {
    $info = Get-GitHubInfo

    $content = @"
# Welcome to $($info.Repo) Wiki

> Your comprehensive guide to using $($info.Repo)

## [>>] Quick Start

Get started in under 5 minutes:

``````bash
# Clone the repository
git clone $($info.Url).git
cd $($info.Repo)

# Install dependencies
# (Add installation commands here)

# Run the project
# (Add run commands here)
``````

## [DOCS] Documentation

- **[Installation Guide](Installation)** - Complete setup instructions
- **[Usage Guide](Usage)** - How to use the project
- **[API Reference](API-Reference)** - Detailed API documentation
- **[Contributing](Contributing)** - How to contribute
- **[FAQ](FAQ)** - Common questions and answers

## [*] Features

- [*] Feature 1
- [*] Feature 2
- [*] Feature 3

## [!] Getting Help

Need assistance?

- [Open an issue]($($info.Url)/issues)
- [Start a discussion]($($info.Url)/discussions)
- Check the [FAQ](FAQ)
"@

    return New-WikiPage -Title "Home" -Content $content -Filename "Home.md"
}

# Generate Installation page
function New-InstallationPage {
    $info = Get-GitHubInfo

    $content = @"
# Installation Guide

## [PKG] Prerequisites

Before installing, ensure you have:

- **Git** - Version control
- **[Language/Runtime]** - Version X.X or higher
- **[Package Manager]** - (npm, pip, etc.)

## [>>] Installation Methods

### Method 1: Clone from GitHub

``````bash
git clone $($info.Url).git
cd $($info.Repo)
``````

### Method 2: Package Manager

``````bash
# Add installation command here
``````

## [ROCKET] Post-Installation

Verify installation:

``````bash
# Add verification command
``````

## [!] Troubleshooting

### Common Issues

**Issue 1: Description**
``````bash
# Solution
``````

**Issue 2: Description**
``````bash
# Solution
``````

## [>>] Next Steps

- Read the [Usage Guide](Usage)
- Explore [API Reference](API-Reference)
- Join our [Discussions]($($info.Url)/discussions)
"@

    return New-WikiPage -Title "Installation" -Content $content -Filename "Installation.md"
}

# Generate Usage page
function New-UsagePage {
    $content = @"
# Usage Guide

## [ROCKET] Basic Usage

### Getting Started

``````bash
# Basic command
command --help
``````

## [CODE] Examples

### Example 1: Basic Usage

``````bash
# Example command
``````

**Output:**
``````
# Expected output
``````

### Example 2: Advanced Usage

``````bash
# Advanced command
``````

## [TOOL] Configuration

### Configuration File

Create a config file:

``````yaml
# config.yml
key: value
``````

### Environment Variables

``````bash
export VAR_NAME=value
``````

## [*] Best Practices

1. **Do this** - Explanation
2. **Avoid that** - Explanation
3. **Consider this** - Explanation

## [!] Common Patterns

### Pattern 1

``````bash
# Example
``````

### Pattern 2

``````bash
# Example
``````
"@

    return New-WikiPage -Title "Usage" -Content $content -Filename "Usage.md"
}

# Generate API Reference page
function New-APIPage {
    $content = @"
# API Reference

## [CODE] Overview

This document provides a complete API reference.

## [TOOL] Core Functions

### Function 1

``````python
def function_name(param1, param2):
    """
    Description

    Args:
        param1: Description
        param2: Description

    Returns:
        Description
    """
``````

**Parameters:**
- `param1` (type) - Description
- `param2` (type) - Description

**Returns:** Return value description

**Example:**
``````python
result = function_name("value1", "value2")
``````

### Function 2

``````python
def another_function(arg):
    """Description"""
``````

## [PKG] Classes

### Class Name

``````python
class ClassName:
    """Class description"""

    def method1(self):
        """Method description"""
``````

**Methods:**
- `method1()` - Description

**Properties:**
- `property1` - Description

## [!] Error Handling

### Exception Types

- `CustomException` - When this happens
- `AnotherException` - When that happens
"@

    return New-WikiPage -Title "API Reference" -Content $content -Filename "API-Reference.md"
}

# Generate Contributing page
function New-ContributingPage {
    $info = Get-GitHubInfo

    $content = @"
# Contributing Guide

## [*] Welcome Contributors!

We love contributions! This guide will help you get started.

## [>>] Getting Started

### 1. Fork the Repository

Click the 'Fork' button at [$($info.Url)]($($info.Url))

### 2. Clone Your Fork

``````bash
git clone https://github.com/YOUR-USERNAME/$($info.Repo).git
cd $($info.Repo)
``````

### 3. Create a Branch

``````bash
git checkout -b feature/AmazingFeature
``````

## [CODE] Development Process

### Setup Development Environment

``````bash
# Install dependencies
# Add commands here

# Run tests
# Add test command
``````

### Code Style

- Follow existing code style
- Write clear comments
- Add tests for new features

### Commit Guidelines

``````bash
# Good commit messages
git commit -m "feat: Add amazing feature"
git commit -m "fix: Resolve bug in component"
git commit -m "docs: Update installation guide"
``````

**Commit Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring

## [ROCKET] Submitting Changes

### 1. Push to Your Fork

``````bash
git push origin feature/AmazingFeature
``````

### 2. Create Pull Request

- Go to [$($info.Url)/pulls]($($info.Url)/pulls)
- Click 'New Pull Request'
- Select your branch
- Fill in the template

### 3. Code Review

- Address reviewer feedback
- Keep discussion focused
- Be patient and respectful

## [!] Guidelines

### Do:
- [*] Write clear, descriptive PR titles
- [*] Add tests for new features
- [*] Update documentation
- [*] Follow code style

### Don't:
- [FAIL] Submit untested code
- [FAIL] Include unrelated changes
- [FAIL] Ignore review feedback

## [OK] Recognition

Contributors are listed in:
- README.md
- GitHub Contributors page
- Release notes

Thank you for contributing!
"@

    return New-WikiPage -Title "Contributing" -Content $content -Filename "Contributing.md"
}

# Generate FAQ page
function New-FAQPage {
    $info = Get-GitHubInfo

    $content = @"
# Frequently Asked Questions

## [!] General Questions

### What is this project?

[Add description]

### Who maintains this project?

[Add maintainer information]

### What license is this under?

[Add license information]

## [PKG] Installation Questions

### Q: Installation fails with error X

**A:** Try the following:
``````bash
# Solution steps
``````

### Q: Which version should I install?

**A:** We recommend the latest stable release.

## [CODE] Usage Questions

### Q: How do I do X?

**A:** See the [Usage Guide](Usage) section on X.

### Q: Can I use this for Y?

**A:** Yes/No, because...

## [TOOL] Technical Questions

### Q: What are the system requirements?

**A:**
- OS: Windows/Mac/Linux
- RAM: X GB
- Disk: Y GB

### Q: Is this production-ready?

**A:** [Add status information]

## [*] Troubleshooting

### Q: Error message "X"

**A:** This usually means...

**Solution:**
``````bash
# Fix command
``````

### Q: Performance is slow

**A:** Check these:
1. [Thing to check]
2. [Another thing]
3. [One more thing]

## [>>] Contributing Questions

### Q: How can I contribute?

**A:** See our [Contributing Guide](Contributing)!

### Q: I found a bug, what now?

**A:** [Open an issue]($($info.Url)/issues) with:
- Description
- Steps to reproduce
- Expected vs actual behavior
- System information

## [!] Still Have Questions?

- [Open an issue]($($info.Url)/issues)
- [Start a discussion]($($info.Url)/discussions)
- Check [existing issues]($($info.Url)/issues?q=is%3Aissue)
"@

    return New-WikiPage -Title "FAQ" -Content $content -Filename "FAQ.md"
}

# Generate all wiki pages
function New-AllWikiPages {
    param([string]$OutputDir)

    # Create output directory
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir | Out-Null
    }

    Write-Info "Generating wiki pages in $OutputDir/"
    Write-Host ""

    # Generate pages
    $pages = @{
        "Home.md" = New-HomePage
        "Installation.md" = New-InstallationPage
        "Usage.md" = New-UsagePage
        "API-Reference.md" = New-APIPage
        "Contributing.md" = New-ContributingPage
        "FAQ.md" = New-FAQPage
    }

    $totalPages = 0
    $totalChars = 0

    foreach ($filename in $pages.Keys) {
        $filepath = Join-Path $OutputDir $filename
        $content = $pages[$filename]
        $content | Out-File -FilePath $filepath -Encoding UTF8

        $lineCount = ($content -split "`n").Count
        $charCount = $content.Length

        Write-Success "$filename"
        Write-Host "  $lineCount lines, $charCount characters" -ForegroundColor Gray

        $totalPages++
        $totalChars += $charCount
    }

    Write-Host ""
    Write-Success "Generated $totalPages wiki pages ($totalChars total characters)"
    Write-Host ""
    Write-ColorOutput "[>>] Next Steps:" "Cyan"
    Write-Host "  1. Review generated pages in $OutputDir/" -ForegroundColor Gray
    Write-Host "  2. Customize content for your project" -ForegroundColor Gray
    Write-Host "  3. Enable GitHub Wiki (run with -ShowSetup)" -ForegroundColor Gray
    Write-Host "  4. Deploy pages to your wiki" -ForegroundColor Gray
    Write-Host ""
}

# Main execution
if ($ShowSetup) {
    Show-WikiSetupInstructions
}
elseif ($Page) {
    Write-Info "Generating $Page page..."

    $content = switch ($Page) {
        "Home" { New-HomePage }
        "Installation" { New-InstallationPage }
        "Usage" { New-UsagePage }
        "API" { New-APIPage }
        "API-Reference" { New-APIPage }
        "Contributing" { New-ContributingPage }
        "FAQ" { New-FAQPage }
        default {
            Write-Error "Unknown page: $Page"
            Write-Host ""
            Write-Host "Available pages: Home, Installation, Usage, API, Contributing, FAQ" -ForegroundColor Gray
            Write-Host ""
            exit 1
        }
    }

    $filename = "$Page.md"
    $filepath = Join-Path $Output $filename

    if (-not (Test-Path $Output)) {
        New-Item -ItemType Directory -Path $Output | Out-Null
    }

    $content | Out-File -FilePath $filepath -Encoding UTF8
    Write-Success "Generated $filepath"
    Write-Host ""
}
elseif ($All -or (-not $ShowSetup -and -not $Page)) {
    New-AllWikiPages -OutputDir $Output
}
else {
    Write-Error "No mode specified. Use -All, -Page <name>, or -ShowSetup"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\Generate-Wiki.ps1 -All" -ForegroundColor Gray
    Write-Host "  .\Generate-Wiki.ps1 -Page Home" -ForegroundColor Gray
    Write-Host "  .\Generate-Wiki.ps1 -ShowSetup" -ForegroundColor Gray
    Write-Host ""
}
