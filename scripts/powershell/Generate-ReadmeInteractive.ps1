<#
.SYNOPSIS
    GitSage Interactive README Generator - PowerShell Version
.DESCRIPTION
    Generate awesome README.md files with interactive wizard mode.
    Full feature parity with Python version!
.PARAMETER Interactive
    Launch interactive wizard mode
.PARAMETER Analyze
    Analyze project and show detected information
.PARAMETER HealthCheck
    Show repository health report
.EXAMPLE
    .\Generate-ReadmeInteractive.ps1 -Interactive
    .\Generate-ReadmeInteractive.ps1 -Analyze
    .\Generate-ReadmeInteractive.ps1 -HealthCheck
#>

param(
    [switch]$Interactive,
    [switch]$Analyze,
    [switch]$HealthCheck,
    [string]$Output = ""  # Empty means use default output folder
)

# ============================================
# Output Folder Configuration
# ============================================
$DefaultOutputDir = ".\gitsage-output"
$ReadmeOutputDir = "$DefaultOutputDir\readmes"

# Create output directories
if (-not (Test-Path $DefaultOutputDir)) {
    New-Item -ItemType Directory -Path $DefaultOutputDir -Force | Out-Null
}
if (-not (Test-Path $ReadmeOutputDir)) {
    New-Item -ItemType Directory -Path $ReadmeOutputDir -Force | Out-Null
}

# Set default output path if not specified
if ([string]::IsNullOrEmpty($Output)) {
    $Output = "$ReadmeOutputDir\README.md"
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

# Project detection function
function Get-ProjectType {
    $detectedType = "cli-tool"
    $languages = @{}
    $frameworks = @()

    # Detect languages
    if (Test-Path "package.json") {
        $detectedType = "npm-package"
        $languages["JavaScript"] = (Get-ChildItem -Recurse -Filter "*.js" | Measure-Object).Count
    }

    if ((Test-Path "setup.py") -or (Test-Path "pyproject.toml")) {
        $detectedType = "python-library"
        $languages["Python"] = (Get-ChildItem -Recurse -Filter "*.py" | Measure-Object).Count
    }

    if ((Test-Path "*.ipynb") -or (Test-Path "notebooks/*.ipynb")) {
        $detectedType = "data-science"
    }

    if (Test-Path "Dockerfile") {
        $frameworks += "Docker"
    }

    # Detect frameworks
    if (Test-Path "package.json") {
        $packageJson = Get-Content "package.json" | ConvertFrom-Json
        if ($packageJson.dependencies.react) { $frameworks += "React" }
        if ($packageJson.dependencies.vue) { $frameworks += "Vue" }
        if ($packageJson.dependencies.angular) { $frameworks += "Angular" }
    }

    return @{
        Type = $detectedType
        Languages = $languages
        Frameworks = $frameworks
    }
}

# Repository health check
function Get-RepositoryHealth {
    $score = 0
    $maxScore = 100
    $checks = @()

    # README check
    if (Test-Path "README.md") {
        $score += 15
        $checks += "[OK] README.md exists (+15 pts)"
    } else {
        $checks += "[FAIL] README.md missing (0 pts)"
    }

    # LICENSE check
    if (Test-Path "LICENSE") {
        $score += 10
        $checks += "[OK] LICENSE exists (+10 pts)"
    } else {
        $checks += "[WARN] LICENSE missing (0 pts)"
    }

    # .gitignore check
    if (Test-Path ".gitignore") {
        $score += 10
        $checks += "[OK] .gitignore exists (+10 pts)"
    } else {
        $checks += "[FAIL] .gitignore missing (0 pts)"
    }

    # CONTRIBUTING check
    if (Test-Path "CONTRIBUTING.md") {
        $score += 8
        $checks += "[OK] CONTRIBUTING.md exists (+8 pts)"
    } else {
        $checks += "[!] CONTRIBUTING.md missing (0 pts)"
    }

    # CI/CD check
    if (Test-Path ".github/workflows") {
        $score += 10
        $checks += "[OK] GitHub Actions configured (+10 pts)"
    } else {
        $checks += "[!] No CI/CD automation (0 pts)"
    }

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " [HEALTH] Repository Health Score" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Score: $score/$maxScore ($([math]::Round($score/$maxScore*100,1))%)" -ForegroundColor $(if($score -ge 80){"Green"}elseif($score -ge 60){"Yellow"}else{"Red"})
    Write-Host ""
    foreach ($check in $checks) {
        Write-Host "  $check"
    }
    Write-Host ""
}

# Interactive wizard
function Start-InteractiveWizard {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " [>>] README Generator - Interactive Wizard" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    # Detect project
    Write-ColorOutput "[SEARCH] Analyzing your codebase..." "Yellow"
    $detection = Get-ProjectType
    Write-Success "Detected: $($detection.Type)"
    if ($detection.Languages.Count -gt 0) {
        $langs = ($detection.Languages.Keys | Select-Object -First 3) -join ", "
        Write-Success "Languages: $langs"
    }

    # Get project info
    Write-Host ""
    Write-ColorOutput "[EDIT] Project Information" "Cyan"
    Write-Host ""

    $projectName = Read-Host "Project name [$((Get-Item .).Name)]"
    if (-not $projectName) { $projectName = (Get-Item .).Name }

    $tagline = Read-Host "Tagline [A $($detection.Type) for developers]"
    if (-not $tagline) { $tagline = "A $($detection.Type) for developers" }

    $description = Read-Host "Description [$projectName is a powerful $($detection.Type)]"
    if (-not $description) { $description = "$projectName is a powerful $($detection.Type)" }

    $version = Read-Host "Version [1.0.0]"
    if (-not $version) { $version = "1.0.0" }

    $author = Read-Host "Author name [Your Name]"
    if (-not $author) { $author = "Your Name" }

    # Get GitHub info
    try {
        $remoteUrl = git config --get remote.origin.url
        if ($remoteUrl -match "github.com[:/](.+)/(.+)\.git") {
            $username = $matches[1]
            $repo = $matches[2]
        } else {
            $username = "username"
            $repo = $projectName.ToLower().Replace(" ", "-")
        }
    } catch {
        $username = "username"
        $repo = $projectName.ToLower().Replace(" ", "-")
    }

    $githubUsername = Read-Host "GitHub username [$username]"
    if (-not $githubUsername) { $githubUsername = $username }

    $githubRepo = Read-Host "Repository name [$repo]"
    if (-not $githubRepo) { $githubRepo = $repo }

    # License
    Write-Host ""
    Write-Host "License: (1=MIT, 2=Apache-2.0, 3=GPL-3.0, 4=BSD-3-Clause)" -ForegroundColor Gray
    $licenseChoice = Read-Host "Choose license [1]"
    if (-not $licenseChoice) { $licenseChoice = "1" }

    $licenses = @{
        "1" = "MIT"
        "2" = "Apache-2.0"
        "3" = "GPL-3.0"
        "4" = "BSD-3-Clause"
    }
    $license = $licenses[$licenseChoice]

    # Generate README
    Write-Host ""
    Write-ColorOutput "[STYLE] Generating README.md..." "Cyan"

    $readme = @"
# $projectName

> $tagline

![License](https://img.shields.io/badge/license-$license-green)
![Version](https://img.shields.io/badge/version-$version-blue)
![Stars](https://img.shields.io/github/stars/$githubUsername/$githubRepo)
![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)

## [>>] Overview

$description

## [+] Features

- [+] Easy to use
- [ROCKET] Fast and efficient
- [PKG] Lightweight and portable
- [LOCK] Secure by design

## [PKG] Installation

### Using Git

``````bash
git clone https://github.com/$githubUsername/$githubRepo.git
cd $githubRepo
``````

## [ROCKET] Quick Start

``````bash
# Your quick start commands here
``````

## [CODE] Usage

``````
# Add usage examples here
``````

## [CONTRIB] Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Steps to Contribute

1. Fork the repository
2. Create your feature branch (``git checkout -b feature/AmazingFeature``)
3. Commit your changes (``git commit -m 'Add some AmazingFeature'``)
4. Push to the branch (``git push origin feature/AmazingFeature``)
5. Open a Pull Request

## [LICENSE] License

This project is licensed under the $license License - see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by $author © $((Get-Date).Year)
"@

    # Save README
    $readme | Out-File -FilePath $Output -Encoding UTF8

    Write-Host ""
    Write-Success "README generated: $Output"
    Write-Host "  $($readme.Length) characters" -ForegroundColor Gray
    Write-Host "  $(($readme -split "`n").Count) lines" -ForegroundColor Gray
    Write-Host ""
}

# Project analysis
function Show-ProjectAnalysis {
    $detection = Get-ProjectType

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " [EDIT] Project Analysis" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "[>>] Project Type: $($detection.Type)" -ForegroundColor Green
    Write-Host ""

    if ($detection.Languages.Count -gt 0) {
        Write-Host "Detected Languages:" -ForegroundColor Cyan
        foreach ($lang in $detection.Languages.GetEnumerator()) {
            Write-Host "  • $($lang.Key): $($lang.Value) files"
        }
        Write-Host ""
    }

    if ($detection.Frameworks.Count -gt 0) {
        Write-Host "[TOOL] Frameworks: $($detection.Frameworks -join ', ')" -ForegroundColor Cyan
        Write-Host ""
    }

    Write-Host "[!] Suggestions:" -ForegroundColor Yellow
    if (-not (Test-Path "README.md")) {
        Write-Host "  • Create README.md with project documentation"
    }
    if (-not (Test-Path "LICENSE")) {
        Write-Host "  • Add LICENSE file (choosealicense.com)"
    }
    if (-not (Test-Path ".gitignore")) {
        Write-Host "  • Add .gitignore to prevent committing unwanted files"
    }
    Write-Host ""
}

# Main execution
if ($HealthCheck) {
    Get-RepositoryHealth
}
elseif ($Analyze) {
    Show-ProjectAnalysis
}
elseif ($Interactive -or -not (Test-Path "readme-config.yaml")) {
    if (-not (Test-Path "readme-config.yaml") -and -not $Interactive) {
        Write-Warning "No config file found. Launching interactive wizard..."
        Write-Host ""
    }
    Start-InteractiveWizard
}
else {
    Write-Error "No mode specified. Use -Interactive, -Analyze, or -HealthCheck"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\Generate-ReadmeInteractive.ps1 -Interactive" -ForegroundColor Gray
    Write-Host "  .\Generate-ReadmeInteractive.ps1 -Analyze" -ForegroundColor Gray
    Write-Host "  .\Generate-ReadmeInteractive.ps1 -HealthCheck" -ForegroundColor Gray
    Write-Host ""
}
