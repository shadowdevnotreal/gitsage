<#
.SYNOPSIS
    GitSage One-Command Repository Setup - PowerShell Version
.DESCRIPTION
    Complete repository setup wizard in one command!
    Analyzes project, checks health, generates README and wiki.
.PARAMETER SkipREADME
    Skip README generation
.PARAMETER SkipWiki
    Skip wiki generation
.PARAMETER SkipHealth
    Skip health check
.EXAMPLE
    .\Initialize-Repository.ps1
    .\Initialize-Repository.ps1 -SkipWiki
#>

param(
    [switch]$SkipREADME,
    [switch]$SkipWiki,
    [switch]$SkipHealth
)

# Color output functions
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success { param([string]$Message) Write-ColorOutput "[OK] $Message" "Green" }
function Write-Info { param([string]$Message) Write-ColorOutput "[>>] $Message" "Cyan" }
function Write-Warning { param([string]$Message) Write-ColorOutput "[WARN] $Message" "Yellow" }
function Write-Error { param([string]$Message) Write-ColorOutput "[FAIL] $Message" "Red" }

function Show-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-StepHeader {
    param([string]$Step, [string]$Title)
    Write-Host ""
    Write-Host "[$Step] $Title" -ForegroundColor Yellow
    Write-Host ""
}

function Confirm-Action {
    param([string]$Message, [bool]$Default = $true)

    $choices = if ($Default) { "[Y/n]" } else { "[y/N]" }
    $response = Read-Host "$Message $choices"

    if ($response -eq "") {
        return $Default
    }

    return $response -match "^[Yy]"
}

# Main setup wizard
function Start-RepositorySetup {
    Show-Header "[>>] GitSage Repository Setup Wizard"

    Write-ColorOutput "Complete repository setup in one command!" "Gray"
    Write-Host ""

    # Step 1: Analyze Project
    Show-StepHeader "1/6" "Analyzing your project..."

    $scriptDir = Split-Path -Parent $PSCommandPath
    $analyzeScript = Join-Path $scriptDir "Generate-ReadmeInteractive.ps1"

    if (Test-Path $analyzeScript) {
        & $analyzeScript -Analyze
    } else {
        Write-Warning "Project analyzer not found, skipping..."
    }

    # Step 2: Health Check
    if (-not $SkipHealth) {
        Show-StepHeader "2/6" "Checking repository health..."

        $healthScript = Join-Path $scriptDir "Test-RepositoryHealth.ps1"

        if (Test-Path $healthScript) {
            & $healthScript
        } else {
            Write-Warning "Health checker not found, skipping..."
        }
    } else {
        Write-Info "[2/6] Health check skipped"
    }

    # Step 3: Generate README
    if (-not $SkipREADME) {
        Show-StepHeader "3/6" "Generate professional README?"

        if (Confirm-Action "Generate README.md now?" $true) {
            Write-Info "Launching README generator..."

            if (Test-Path $analyzeScript) {
                & $analyzeScript -Interactive
            } else {
                Write-Error "README generator not found at $analyzeScript"
            }
        } else {
            Write-Warning "README generation skipped"
        }
    } else {
        Write-Info "[3/6] README generation skipped"
    }

    # Step 4: Generate Wiki
    if (-not $SkipWiki) {
        Show-StepHeader "4/6" "Generate documentation wiki?"

        if (Confirm-Action "Generate wiki pages now?" $true) {
            Write-Info "Launching wiki generator..."

            $wikiScript = Join-Path $scriptDir "Generate-Wiki.ps1"

            if (Test-Path $wikiScript) {
                & $wikiScript -All
            } else {
                Write-Error "Wiki generator not found at $wikiScript"
            }
        } else {
            Write-Warning "Wiki generation skipped"
        }
    } else {
        Write-Info "[4/6] Wiki generation skipped"
    }

    # Step 5: GitHub Setup Checklist
    Show-StepHeader "5/6" "GitHub Setup Checklist"

    Write-ColorOutput "Please enable these features in your GitHub repository:" "Cyan"
    Write-Host ""
    Write-Host "  [ ] Enable Wiki (Settings -> Features -> Wikis)" -ForegroundColor Gray
    Write-Host "  [ ] Enable Issues (Settings -> Features -> Issues)" -ForegroundColor Gray
    Write-Host "  [ ] Enable Discussions (Settings -> Features -> Discussions)" -ForegroundColor Gray
    Write-Host "  [ ] Add repository description" -ForegroundColor Gray
    Write-Host "  [ ] Add 3-5 topics/tags" -ForegroundColor Gray
    Write-Host "  [ ] Add LICENSE file (if not exists)" -ForegroundColor Gray
    Write-Host "  [ ] Add repository social preview image" -ForegroundColor Gray
    Write-Host ""

    try {
        $remoteUrl = git config --get remote.origin.url
        if ($remoteUrl -match "github.com[:/](.+)/(.+)\.git") {
            $username = $matches[1]
            $repo = $matches[2]
            $repoUrl = "https://github.com/$username/$repo"

            Write-Info "Quick Links:"
            Write-Host "  Settings: $repoUrl/settings" -ForegroundColor Gray
            Write-Host "  Wiki: $repoUrl/wiki" -ForegroundColor Gray
            Write-Host "  Issues: $repoUrl/issues" -ForegroundColor Gray
        }
    } catch {}

    Write-Host ""
    Read-Host "Press Enter when ready to continue"

    # Step 6: Summary
    Show-StepHeader "6/6" "Setup Complete!"

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host " [OK] Repository Setup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""

    Write-ColorOutput "Your repository now has:" "White"
    Write-Host ""

    $hasREADME = Test-Path "README.md"
    $hasWiki = Test-Path "wiki/"
    $hasLICENSE = Test-Path "LICENSE"
    $hasCONTRIBUTING = Test-Path "CONTRIBUTING.md"
    $hasGitignore = Test-Path ".gitignore"

    if ($hasREADME) {
        Write-Host "  [OK] Professional README.md" -ForegroundColor Green
    } else {
        Write-Host "  [!] README.md (not created)" -ForegroundColor Yellow
    }

    if ($hasWiki) {
        Write-Host "  [OK] Complete documentation wiki" -ForegroundColor Green
    } else {
        Write-Host "  [!] Wiki pages (not created)" -ForegroundColor Yellow
    }

    if ($hasLICENSE) {
        Write-Host "  [OK] LICENSE file" -ForegroundColor Green
    }

    if ($hasCONTRIBUTING) {
        Write-Host "  [OK] CONTRIBUTING.md" -ForegroundColor Green
    }

    if ($hasGitignore) {
        Write-Host "  [OK] .gitignore" -ForegroundColor Green
    }

    Write-Host ""
    Write-ColorOutput "Next steps:" "Yellow"
    Write-Host ""
    Write-Host "  1. Review and commit changes" -ForegroundColor Gray
    Write-Host "     git add ." -ForegroundColor DarkGray
    Write-Host "     git commit -m 'docs: Setup repository with GitSage'" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  2. Enable GitHub features (see checklist above)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. Deploy wiki pages" -ForegroundColor Gray
    Write-Host "     git clone <repo>.wiki.git" -ForegroundColor DarkGray
    Write-Host "     cp wiki/* <repo>.wiki/" -ForegroundColor DarkGray
    Write-Host "     cd <repo>.wiki && git add . && git commit -m 'Update wiki' && git push" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  4. Share your awesome repository!" -ForegroundColor Gray
    Write-Host ""

    # Optional: Show beautification score
    Write-Host ""
    if (Confirm-Action "Show final beautification score?" $false) {
        $healthScript = Join-Path $scriptDir "Test-RepositoryHealth.ps1"
        if (Test-Path $healthScript) {
            & $healthScript -Beauty
        }
    }

    Write-Host ""
    Write-Success "Happy coding!"
    Write-Host ""
}

# Show quick help
function Show-QuickHelp {
    Write-Host ""
    Write-Host "GitSage Repository Setup Wizard" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage:" -ForegroundColor White
    Write-Host "  .\Initialize-Repository.ps1              # Full setup" -ForegroundColor Gray
    Write-Host "  .\Initialize-Repository.ps1 -SkipWiki    # Skip wiki generation" -ForegroundColor Gray
    Write-Host "  .\Initialize-Repository.ps1 -SkipREADME  # Skip README generation" -ForegroundColor Gray
    Write-Host ""
    Write-Host "This wizard will:" -ForegroundColor White
    Write-Host "  1. Analyze your project type" -ForegroundColor Gray
    Write-Host "  2. Check repository health" -ForegroundColor Gray
    Write-Host "  3. Generate professional README" -ForegroundColor Gray
    Write-Host "  4. Generate documentation wiki" -ForegroundColor Gray
    Write-Host "  5. Provide GitHub setup checklist" -ForegroundColor Gray
    Write-Host "  6. Show final beautification score" -ForegroundColor Gray
    Write-Host ""
}

# Main execution
if ($args -contains "--help" -or $args -contains "-h") {
    Show-QuickHelp
} else {
    Start-RepositorySetup
}
