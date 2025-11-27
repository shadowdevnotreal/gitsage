<#
.SYNOPSIS
    GitSage Main Launcher - PowerShell Version
.DESCRIPTION
    Universal launcher for all GitSage tools on Windows.
    Interactive menu for README generation, wiki creation, health checks, and more.
.PARAMETER Tool
    Specific tool to launch (readme, wiki, health, setup)
.PARAMETER Help
    Show help information
.EXAMPLE
    .\Launch-GitSage.ps1
    .\Launch-GitSage.ps1 -Tool readme
    .\Launch-GitSage.ps1 -Tool setup
#>

param(
    [string]$Tool,
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

# Show main header
function Show-MainHeader {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host " $PROJECT_NAME v$VERSION - PowerShell Edition" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
}

# Show help information
function Show-HelpInfo {
    Show-MainHeader

    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\Launch-GitSage.ps1 [OPTIONS]" -ForegroundColor Gray
    Write-Host ""

    Write-Host "Options:" -ForegroundColor White
    Write-Host "  -Tool <name>       Launch specific tool directly" -ForegroundColor Gray
    Write-Host "  -Help              Show this help message" -ForegroundColor Gray
    Write-Host ""

    Write-Host "Available Tools:" -ForegroundColor White
    Write-Host "  readme             Generate interactive README" -ForegroundColor Gray
    Write-Host "  wiki               Generate documentation wiki" -ForegroundColor Gray
    Write-Host "  health             Check repository health" -ForegroundColor Gray
    Write-Host "  setup              One-command repository setup" -ForegroundColor Gray
    Write-Host ""

    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\Launch-GitSage.ps1                    # Interactive menu" -ForegroundColor Gray
    Write-Host "  .\Launch-GitSage.ps1 -Tool readme       # Generate README" -ForegroundColor Gray
    Write-Host "  .\Launch-GitSage.ps1 -Tool setup        # Complete setup" -ForegroundColor Gray
    Write-Host ""

    Write-Host "Documentation:" -ForegroundColor White
    Write-Host "  README.md                               # Full documentation" -ForegroundColor Gray
    Write-Host "  docs/                                   # User guides" -ForegroundColor Gray
    Write-Host "  https://github.com/shadowdevnotreal/gitsage" -ForegroundColor Gray
    Write-Host ""
}

# Launch README generator
function Start-READMEGenerator {
    Write-Info "Launching README Generator..."
    Write-Host ""

    $scriptDir = Split-Path -Parent $PSCommandPath
    $readmeScript = Join-Path $scriptDir "Generate-ReadmeInteractive.ps1"

    if (Test-Path $readmeScript) {
        & $readmeScript -Interactive
    } else {
        Write-Error "README generator not found at: $readmeScript"
        Write-Host ""
    }
}

# Launch wiki generator
function Start-WikiGenerator {
    Write-Info "Launching Wiki Generator..."
    Write-Host ""

    $scriptDir = Split-Path -Parent $PSCommandPath
    $wikiScript = Join-Path $scriptDir "Generate-Wiki.ps1"

    if (Test-Path $wikiScript) {
        & $wikiScript -All
    } else {
        Write-Error "Wiki generator not found at: $wikiScript"
        Write-Host ""
    }
}

# Launch health checker
function Start-HealthChecker {
    Write-Info "Launching Health Checker..."
    Write-Host ""

    $scriptDir = Split-Path -Parent $PSCommandPath
    $healthScript = Join-Path $scriptDir "Test-RepositoryHealth.ps1"

    if (Test-Path $healthScript) {
        & $healthScript -Full
    } else {
        Write-Error "Health checker not found at: $healthScript"
        Write-Host ""
    }
}

# Launch setup wizard
function Start-SetupWizard {
    Write-Info "Launching Setup Wizard..."
    Write-Host ""

    $scriptDir = Split-Path -Parent $PSCommandPath
    $setupScript = Join-Path $scriptDir "Initialize-Repository.ps1"

    if (Test-Path $setupScript) {
        & $setupScript
    } else {
        Write-Error "Setup wizard not found at: $setupScript"
        Write-Host ""
    }
}

# Interactive menu
function Show-InteractiveMenu {
    Show-MainHeader

    Write-ColorOutput "Choose a tool:" "Cyan"
    Write-Host ""

    Write-Host "  1. README Generator      - Create professional README.md" -ForegroundColor Gray
    Write-Host "  2. Wiki Generator        - Generate documentation wiki" -ForegroundColor Gray
    Write-Host "  3. Health Checker        - Analyze repository health" -ForegroundColor Gray
    Write-Host "  4. Setup Wizard          - Complete repository setup" -ForegroundColor Gray
    Write-Host "  5. Help                  - Show help information" -ForegroundColor Gray
    Write-Host "  6. Exit                  - Exit GitSage" -ForegroundColor Gray
    Write-Host ""

    try {
        $choice = Read-Host "Enter choice [1-6]"

        switch ($choice) {
            "1" {
                Start-READMEGenerator
            }
            "2" {
                Start-WikiGenerator
            }
            "3" {
                Start-HealthChecker
            }
            "4" {
                Start-SetupWizard
            }
            "5" {
                Show-HelpInfo
                Read-Host "Press Enter to return to menu"
                Show-InteractiveMenu
            }
            "6" {
                Write-Host ""
                Write-Warning "Goodbye!"
                Write-Host ""
                exit 0
            }
            default {
                Write-Host ""
                Write-Error "Invalid choice: $choice"
                Write-Host ""
                Read-Host "Press Enter to try again"
                Show-InteractiveMenu
            }
        }
    }
    catch {
        Write-Host ""
        Write-Warning "Operation cancelled"
        Write-Host ""
        exit 0
    }
}

# Main execution
if ($Help) {
    Show-HelpInfo
    exit 0
}

if ($Tool) {
    # Direct tool launch
    switch ($Tool.ToLower()) {
        "readme" {
            Start-READMEGenerator
        }
        "wiki" {
            Start-WikiGenerator
        }
        "health" {
            Start-HealthChecker
        }
        "setup" {
            Start-SetupWizard
        }
        default {
            Write-Error "Unknown tool: $Tool"
            Write-Host ""
            Write-Host "Available tools: readme, wiki, health, setup" -ForegroundColor Gray
            Write-Host "Use -Help for more information" -ForegroundColor Gray
            Write-Host ""
            exit 1
        }
    }
}
else {
    # Interactive mode
    Show-InteractiveMenu
}
