<#
.SYNOPSIS
    GitSage Universal Launcher - PowerShell Version
.DESCRIPTION
    Universal launcher for all GitSage tools on Windows.
    Supports both CLI and Web interface modes by calling the Python launcher.
.PARAMETER CLI
    Launch CLI interface directly
.PARAMETER Web
    Launch web interface directly
.PARAMETER SetupRepo
    Launch repository setup wizard directly
.PARAMETER Help
    Show help information
.EXAMPLE
    .\Launch-GitSage.ps1
    .\Launch-GitSage.ps1 -CLI
    .\Launch-GitSage.ps1 -Web
    .\Launch-GitSage.ps1 -SetupRepo
#>

param(
    [switch]$CLI,
    [switch]$Web,
    [switch]$SetupRepo,
    [switch]$Help
)

$VERSION = "2.3.0"
$PROJECT_NAME = "GitSage"

# Color output functions
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success { param([string]$Message) Write-ColorOutput $Message "Green" }
function Write-Info { param([string]$Message) Write-ColorOutput $Message "Cyan" }
function Write-Warning { param([string]$Message) Write-ColorOutput $Message "Yellow" }
function Write-Error { param([string]$Message) Write-ColorOutput $Message "Red" }

# Get script directory and locate launcher.py
$ScriptDir = Split-Path -Parent $PSCommandPath
$RootDir = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$LauncherPy = Join-Path $RootDir "launcher.py"

# Check if Python is available
function Test-PythonAvailable {
    try {
        $null = Get-Command python -ErrorAction Stop
        return $true
    }
    catch {
        try {
            $null = Get-Command python3 -ErrorAction Stop
            return $true
        }
        catch {
            return $false
        }
    }
}

# Get Python command (python or python3)
function Get-PythonCommand {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        return "python"
    }
    elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
        return "python3"
    }
    else {
        return $null
    }
}

# Show help information
function Show-HelpInfo {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host " $PROJECT_NAME v$VERSION - PowerShell Edition" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""

    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\Launch-GitSage.ps1 [OPTIONS]" -ForegroundColor Gray
    Write-Host ""

    Write-Host "Options:" -ForegroundColor White
    Write-Host "  -CLI               Launch CLI interface directly" -ForegroundColor Gray
    Write-Host "  -Web               Launch web interface directly" -ForegroundColor Gray
    Write-Host "  -SetupRepo         Launch repository setup wizard" -ForegroundColor Gray
    Write-Host "  -Help              Show this help message" -ForegroundColor Gray
    Write-Host ""

    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\Launch-GitSage.ps1                    # Interactive menu" -ForegroundColor Gray
    Write-Host "  .\Launch-GitSage.ps1 -CLI               # Launch CLI" -ForegroundColor Gray
    Write-Host "  .\Launch-GitSage.ps1 -Web               # Launch web interface" -ForegroundColor Gray
    Write-Host "  .\Launch-GitSage.ps1 -SetupRepo         # Setup wizard" -ForegroundColor Gray
    Write-Host ""

    Write-Host "Documentation:" -ForegroundColor White
    Write-Host "  README.md                               # Full documentation" -ForegroundColor Gray
    Write-Host "  docs/                                   # User guides" -ForegroundColor Gray
    Write-Host "  https://github.com/shadowdevnotreal/gitsage" -ForegroundColor Gray
    Write-Host ""
}

# Main execution
if ($Help) {
    Show-HelpInfo
    exit 0
}

# Check if Python is available
if (-not (Test-PythonAvailable)) {
    Write-Error "Python 3 is not installed or not in PATH"
    Write-Host ""
    Write-Host "Please install Python 3.8 or higher from:" -ForegroundColor Yellow
    Write-Host "  https://www.python.org/downloads/" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Check if launcher.py exists
if (-not (Test-Path $LauncherPy)) {
    Write-Error "launcher.py not found"
    Write-Host ""
    Write-Host "Expected location: $LauncherPy" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# Get Python command
$PythonCmd = Get-PythonCommand

# Launch with appropriate arguments
if ($CLI) {
    & $PythonCmd $LauncherPy --cli
}
elseif ($Web) {
    & $PythonCmd $LauncherPy --web
}
elseif ($SetupRepo) {
    & $PythonCmd $LauncherPy --setup-repo
}
else {
    # Interactive mode - no arguments
    & $PythonCmd $LauncherPy
}
