#Requires -Version 5.1
<#
.SYNOPSIS
    GitSage Git History Reset Tool (PowerShell)

.DESCRIPTION
    Reset Git history while keeping all files. Creates a fresh repository
    with a single initial commit containing all current files.

.PARAMETER Force
    Skip confirmations (use with caution)

.EXAMPLE
    .\Reset-GitHistory.ps1
    Interactive mode with safety prompts

.EXAMPLE
    .\Reset-GitHistory.ps1 -Force
    Reset without prompts (dangerous)

.NOTES
    Author: GitSage Contributors
    Requires: Git
    WARNING: This operation is IRREVERSIBLE
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

# Color output functions
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White",
        [switch]$NoNewline
    )

    if ($NoNewline) {
        Write-Host $Message -ForegroundColor $Color -NoNewline
    } else {
        Write-Host $Message -ForegroundColor $Color
    }
}

function Write-Header {
    param([string]$Title)

    $width = [Math]::Max(60, $Title.Length + 10)
    $separator = "=" * $width

    Write-Host ""
    Write-ColorOutput $separator "Cyan"
    Write-ColorOutput $Title.PadLeft(($width + $Title.Length) / 2).PadRight($width) "Cyan"
    Write-ColorOutput $separator "Cyan"
    Write-Host ""
}

function Write-StatusMessage {
    param(
        [string]$Message,
        [ValidateSet("INFO", "SUCCESS", "WARNING", "ERROR")]
        [string]$Status = "INFO"
    )

    $colorMap = @{
        "INFO" = "Blue"
        "SUCCESS" = "Green"
        "WARNING" = "Yellow"
        "ERROR" = "Red"
    }

    $color = $colorMap[$Status]
    Write-ColorOutput "[$Status] " $color -NoNewline
    Write-Host $Message
}

function Get-UserConfirmation {
    param(
        [string]$Message,
        [string]$DefaultResponse = "N"
    )

    if ($Force) { return $true }

    $prompt = if ($DefaultResponse -eq "Y") { "[Y/n]" } else { "[y/N]" }
    Write-ColorOutput "$Message $prompt " "Yellow" -NoNewline

    $response = Read-Host
    if ([string]::IsNullOrWhiteSpace($response)) {
        $response = $DefaultResponse
    }

    return $response -match '^[Yy]'
}

# Check if git repository
function Test-GitRepository {
    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        Write-StatusMessage "Please run this script from inside a git repository" "INFO"
        exit 1
    }
}

# Get current branch
function Get-CurrentBranch {
    try {
        $branch = git branch --show-current 2>$null
        if ([string]::IsNullOrWhiteSpace($branch)) {
            $branch = "main"
        }
        return $branch
    } catch {
        return "main"
    }
}

# Create backup
function New-RepositoryBackup {
    Write-StatusMessage "Creating backup before reset..." "INFO"

    $backupDir = Join-Path $env:USERPROFILE ".gitsage\history-backups"
    if (-not (Test-Path $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $repoName = (Get-Item -Path ".").Name
    $backupPath = Join-Path $backupDir "${repoName}_${timestamp}"

    try {
        # Create backup using git bundle
        Write-StatusMessage "Creating git bundle backup..." "INFO"
        $bundleFile = "${backupPath}.bundle"

        git bundle create $bundleFile --all 2>$null

        if ($LASTEXITCODE -eq 0 -and (Test-Path $bundleFile)) {
            $backupSize = (Get-Item $bundleFile).Length / 1MB
            Write-StatusMessage "✓ Backup created successfully (${backupSize:F2} MB)" "SUCCESS"
            Write-StatusMessage "  Backup location: $bundleFile" "INFO"
            Write-StatusMessage "  Restore with: git clone $bundleFile" "INFO"
            return $true
        } else {
            Write-StatusMessage "✗ Backup creation failed" "ERROR"
            return $false
        }
    } catch {
        Write-StatusMessage "✗ Error creating backup: $_" "ERROR"
        return $false
    }
}

# Count commits
function Get-CommitCount {
    try {
        $count = git rev-list --count HEAD 2>$null
        if ($LASTEXITCODE -eq 0) {
            return [int]$count
        }
        return 0
    } catch {
        return 0
    }
}

# Reset git history
function Reset-GitHistory {
    Write-Header "Git History Reset Tool - PowerShell"

    # Check prerequisites
    Test-GitRepository

    # Get current state
    $currentBranch = Get-CurrentBranch
    $commitCount = Get-CommitCount

    Write-StatusMessage "Current branch: $currentBranch" "INFO"
    Write-StatusMessage "Current commits: $commitCount" "INFO"
    Write-Host ""

    # Warning
    Write-Header "⚠️  DANGER ZONE ⚠️"
    Write-StatusMessage "This operation will:" "WARNING"
    Write-StatusMessage "  1. DELETE ALL commit history ($commitCount commits)" "ERROR"
    Write-StatusMessage "  2. Keep ALL current files unchanged" "INFO"
    Write-StatusMessage "  3. Create a NEW initial commit" "INFO"
    Write-StatusMessage "  4. Require FORCE PUSH to update remote" "WARNING"
    Write-Host ""
    Write-StatusMessage "This action is IRREVERSIBLE!" "ERROR"
    Write-Host ""

    # Confirmations
    if (-not (Get-UserConfirmation "Do you want to proceed with history reset?")) {
        Write-StatusMessage "Operation cancelled" "INFO"
        exit 0
    }

    Write-Host ""
    Write-StatusMessage "FINAL CONFIRMATION" "ERROR"
    Write-ColorOutput "Type 'RESET' to confirm: " "Red" -NoNewline
    if (-not $Force) {
        $confirmation = Read-Host
        if ($confirmation -ne "RESET") {
            Write-StatusMessage "Confirmation failed. Operation cancelled" "ERROR"
            exit 1
        }
    }

    Write-Host ""
    Write-Header "Proceeding with History Reset"

    # Create backup
    $backupSuccess = New-RepositoryBackup
    if (-not $backupSuccess) {
        Write-StatusMessage "Backup failed. Continue anyway?" "WARNING"
        if (-not (Get-UserConfirmation "Continue without backup?" "N")) {
            Write-StatusMessage "Operation cancelled" "INFO"
            exit 0
        }
    }

    # Reset history
    Write-StatusMessage "Resetting git history..." "INFO"

    try {
        # Step 1: Create orphan branch
        Write-StatusMessage "Step 1/5: Creating orphan branch..." "INFO"
        git checkout --orphan temp_reset_branch 2>$null

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "✗ Failed to create orphan branch" "ERROR"
            exit 1
        }

        # Step 2: Add all files
        Write-StatusMessage "Step 2/5: Adding all files..." "INFO"
        git add -A 2>$null

        # Step 3: Create initial commit
        Write-StatusMessage "Step 3/5: Creating initial commit..." "INFO"
        $commitMessage = "Initial commit - History reset on $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        git commit -m $commitMessage 2>$null

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "✗ Failed to create initial commit" "ERROR"
            exit 1
        }

        # Step 4: Delete old branch
        Write-StatusMessage "Step 4/5: Deleting old branch..." "INFO"
        git branch -D $currentBranch 2>$null

        # Step 5: Rename current branch
        Write-StatusMessage "Step 5/5: Renaming branch to $currentBranch..." "INFO"
        git branch -m $currentBranch 2>$null

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ History reset completed successfully!" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Branch rename failed" "ERROR"
            exit 1
        }

    } catch {
        Write-StatusMessage "✗ Error during reset: $_" "ERROR"
        exit 1
    }

    # Summary
    Write-Host ""
    Write-Header "Reset Complete"

    $newCommitCount = Get-CommitCount
    Write-StatusMessage "Old commits: $commitCount" "INFO"
    Write-StatusMessage "New commits: $newCommitCount" "SUCCESS"
    Write-StatusMessage "Branch: $currentBranch" "INFO"

    Write-Host ""
    Write-StatusMessage "Next steps:" "INFO"
    Write-StatusMessage "  1. Review your files: git status" "INFO"
    Write-StatusMessage "  2. Push to remote (FORCE): git push origin $currentBranch --force" "WARNING"
    Write-StatusMessage "     WARNING: This will overwrite remote history!" "ERROR"

    Write-Host ""
    Write-ColorOutput "Push to remote now? " "Yellow" -NoNewline
    if (-not $Force) {
        $pushNow = Read-Host
        if ($pushNow -match '^[Yy]') {
            Write-StatusMessage "Force pushing to origin/$currentBranch..." "WARNING"
            git push origin $currentBranch --force

            if ($LASTEXITCODE -eq 0) {
                Write-StatusMessage "✓ Pushed successfully" "SUCCESS"
            } else {
                Write-StatusMessage "✗ Push failed - please push manually later" "ERROR"
            }
        }
    }

    Write-Host ""
    Write-StatusMessage "History reset complete!" "SUCCESS"
}

# Execute main function
try {
    Reset-GitHistory
} catch {
    Write-StatusMessage "Unexpected error: $_" "ERROR"
    exit 1
}
