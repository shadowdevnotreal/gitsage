#
# GitSage Universal Installer for Windows
# ========================================
# PowerShell installation script with dependency checking
#

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("user", "system", "dev")]
    [string]$InstallType = "user"
)

# Requires PowerShell 5.0+
#Requires -Version 5.0

# Configuration
$GitSageDir = "$env:USERPROFILE\.gitsage"
$InstallDir = "$env:ProgramFiles\GitSage"
$RepoUrl = "https://github.com/shadowdevnotreal/gitsage.git"

# Colors (using Write-Host)
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[✓] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[✗] $Message" -ForegroundColor Red
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host ""
}

function Test-Command {
    param([string]$Command)
    $null = Get-Command $Command -ErrorAction SilentlyContinue
    return $?
}

# Main installation
Write-Header "GitSage Universal Installer v2.2.0"

Write-Info "Detected OS: Windows"
Write-Info "Installation type: $InstallType"
Write-Host ""

# Check if running from git repo
if (-not (Test-Path "pyproject.toml") -or -not (Test-Path "src\gitsage")) {
    Write-Error "This script must be run from the GitSage repository root"
    Write-Host "Please cd to the GitSage directory first"
    exit 1
}

########################################
# Check Prerequisites
########################################

Write-Header "Checking Prerequisites"

# Python
if (Test-Command python) {
    $PythonVersion = (python --version 2>&1).ToString().Split()[1]
    Write-Success "Python: $PythonVersion"

    # Check Python version >= 3.8
    $VersionParts = $PythonVersion.Split('.')
    $Major = [int]$VersionParts[0]
    $Minor = [int]$VersionParts[1]

    if ($Major -lt 3 -or ($Major -eq 3 -and $Minor -lt 8)) {
        Write-Error "Python 3.8+ is required (found $PythonVersion)"
        Write-Host "Download from: https://www.python.org/downloads/"
        exit 1
    }
} else {
    Write-Error "Python is not installed or not in PATH"
    Write-Host "Please install Python 3.8+ from: https://www.python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    exit 1
}

# Git
if (Test-Command git) {
    $GitVersion = (git --version).Split()[2]
    Write-Success "Git: $GitVersion"
} else {
    Write-Error "Git is not installed or not in PATH"
    Write-Host "Please install Git from: https://git-scm.com/download/win"
    Write-Host "Or use: winget install Git.Git"
    exit 1
}

# GitHub CLI
if (Test-Command gh) {
    $GhVersion = (gh --version).Split()[2]
    Write-Success "GitHub CLI: $GhVersion"

    # Check authentication
    $AuthStatus = gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "GitHub CLI: Authenticated"
    } else {
        Write-Warning "GitHub CLI: Not authenticated"
        Write-Host "  Run 'gh auth login' after installation"
    }
} else {
    Write-Warning "GitHub CLI (gh) is not installed"
    Write-Host "  Install with: winget install GitHub.cli"
    Write-Host "  GitHub CLI is optional but recommended"
}

# pip
if (Test-Command pip) {
    Write-Success "pip: Available"
} else {
    Write-Error "pip is not installed"
    Write-Host "Please reinstall Python with pip enabled"
    exit 1
}

Write-Host ""

########################################
# Installation Options
########################################

if ($InstallType -eq "") {
    Write-Header "Installation Options"

    Write-Host "Choose installation type:"
    Write-Host "  1. User Install (Recommended) - Install to $GitSageDir with virtual environment"
    Write-Host "  2. System Install - Install globally (requires admin)"
    Write-Host "  3. Development Install - Install in editable mode for development"
    Write-Host ""

    $Choice = Read-Host "Enter choice [1-3]"

    switch ($Choice) {
        "1" {
            $InstallType = "user"
            Write-Info "Selected: User Install"
        }
        "2" {
            $InstallType = "system"
            Write-Info "Selected: System Install"

            # Check if running as administrator
            $IsAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
            if (-not $IsAdmin) {
                Write-Error "System install requires administrator privileges"
                Write-Host "Please run PowerShell as Administrator"
                exit 1
            }
        }
        "3" {
            $InstallType = "dev"
            Write-Info "Selected: Development Install"
        }
        default {
            Write-Error "Invalid choice"
            exit 1
        }
    }

    Write-Host ""
}

########################################
# Create Directories
########################################

Write-Header "Creating Directories"

New-Item -ItemType Directory -Force -Path "$GitSageDir\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$GitSageDir\backups" | Out-Null
New-Item -ItemType Directory -Force -Path "$GitSageDir\config" | Out-Null

Write-Success "Created: $GitSageDir\"
Write-Success "Created: $GitSageDir\logs"
Write-Success "Created: $GitSageDir\backups"
Write-Success "Created: $GitSageDir\config"

########################################
# Install Python Package
########################################

Write-Header "Installing Python Package"

if ($InstallType -eq "user") {
    # Create virtual environment
    Write-Info "Creating virtual environment..."
    python -m venv "$GitSageDir\venv"
    Write-Success "Virtual environment created"

    # Activate venv
    & "$GitSageDir\venv\Scripts\Activate.ps1"

    # Upgrade pip
    Write-Info "Upgrading pip..."
    python -m pip install --upgrade pip --quiet

    # Install package
    Write-Info "Installing GitSage..."
    pip install -e . --quiet
    Write-Success "GitSage installed in virtual environment"

    # Create batch wrapper
    Write-Info "Creating launcher script..."
    $WrapperContent = @'
@echo off
set GITSAGE_VENV=%USERPROFILE%\.gitsage\venv
call "%GITSAGE_VENV%\Scripts\activate.bat"
python -m gitsage.cli.launcher %*
'@
    Set-Content -Path "$GitSageDir\gitsage.bat" -Value $WrapperContent
    Write-Success "Launcher script created"

    $InstallLocation = "$GitSageDir\gitsage.bat"

} elseif ($InstallType -eq "system") {
    # System-wide install
    Write-Info "Installing GitSage system-wide..."
    pip install -e .
    Write-Success "GitSage installed system-wide"
    $InstallLocation = "gitsage (in PATH)"

} else {
    # Development install
    Write-Info "Installing in development mode..."
    pip install -e ".[dev]"
    Write-Success "GitSage installed in development mode with dev dependencies"
    $InstallLocation = "gitsage (in PATH)"
}

########################################
# Create Configuration
########################################

Write-Header "Creating Configuration"

$ConfigPath = "$GitSageDir\config.yaml"
if (-not (Test-Path $ConfigPath)) {
    $ConfigContent = @"
# GitSage Configuration
# See docs for all available options

project:
  name: GitSage
  version: 2.3.0

backup:
  enabled: true
  backup_dir: $($GitSageDir -replace '\\', '/')/backups
  max_backups_per_repo: 10
  retention_days: 30

logging:
  level: INFO
  log_dir: $($GitSageDir -replace '\\', '/')/logs
  console_output: true
  file_output: true

security:
  require_confirmations: true
  backup_before_delete: true
"@
    Set-Content -Path $ConfigPath -Value $ConfigContent
    Write-Success "Created default configuration: $ConfigPath"
} else {
    Write-Info "Configuration file already exists"
}

########################################
# Setup PATH
########################################

Write-Header "Environment Configuration"

if ($InstallType -eq "user") {
    Write-Host ""
    $AddToPath = Read-Host "Add GitSage to user PATH? (Y/n)"

    if ($AddToPath -ne "n") {
        # Get current user PATH
        $UserPath = [Environment]::GetEnvironmentVariable("Path", "User")

        # Check if already in PATH
        if ($UserPath -notlike "*$GitSageDir*") {
            # Add to PATH
            $NewPath = "$GitSageDir;$UserPath"
            [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
            Write-Success "Added to user PATH"
            Write-Warning "Restart your shell for PATH changes to take effect"
        } else {
            Write-Info "GitSage is already in PATH"
        }
    }
}

########################################
# Completion
########################################

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Success "Installation Complete!"
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

Write-Host "GitSage has been installed successfully!" -ForegroundColor Green
Write-Host ""

if ($InstallType -eq "user") {
    Write-Host "To use GitSage:"
    Write-Host "  $InstallLocation" -ForegroundColor Green
    Write-Host ""
    Write-Host "Or simply run:"
    Write-Host "  gitsage" -ForegroundColor Cyan
    Write-Host "  (After restarting your shell)"
} elseif ($InstallType -eq "system") {
    Write-Host "GitSage is available system-wide:"
    Write-Host "  gitsage" -ForegroundColor Green
} else {
    Write-Host "GitSage is installed in development mode"
    Write-Host "  gitsage" -ForegroundColor Green
}

Write-Host ""
Write-Host "Quick start:"
Write-Host "  gitsage              # Launch interactive menu" -ForegroundColor Cyan
Write-Host "  gitsage --help       # Show help" -ForegroundColor Cyan
Write-Host "  python launcher.py   # Alternative launcher" -ForegroundColor Cyan
Write-Host ""

$GhAuthStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Don't forget to authenticate GitHub CLI:"
    Write-Host "  gh auth login" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "Documentation:"
Write-Host "  README.md"
Write-Host "  docs\"
Write-Host "  https://github.com/shadowdevnotreal/gitsage" -ForegroundColor Blue
Write-Host ""

Write-Success "Happy GitSaging! 🚀"
Write-Host ""
