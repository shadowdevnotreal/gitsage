#Requires -Version 5.1
<#
.SYNOPSIS
    GitSage Interactive Repository Deletion Tool (PowerShell)

.DESCRIPTION
    Safely delete GitHub repositories with multiple confirmations and safety checks.
    Handles both local and remote cleanup with comprehensive verification.

.PARAMETER Repository
    Repository name in format "owner/repo" (optional - will prompt if not provided)

.PARAMETER SkipBackup
    Skip creating backup before deletion (not recommended)

.EXAMPLE
    .\Delete-Repository.ps1
    Interactive mode - prompts for all inputs

.EXAMPLE
    .\Delete-Repository.ps1 -Repository "username/myrepo"
    Delete specific repository with prompts

.NOTES
    Author: GitSage Contributors
    Requires: Git, GitHub CLI (gh)
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [string]$Repository,

    [Parameter(Mandatory=$false)]
    [switch]$SkipBackup
)

# Color functions
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
        [ValidateSet("INFO", "SUCCESS", "WARNING", "ERROR", "QUESTION")]
        [string]$Status = "INFO"
    )

    $colorMap = @{
        "INFO" = "Blue"
        "SUCCESS" = "Green"
        "WARNING" = "Yellow"
        "ERROR" = "Red"
        "QUESTION" = "Magenta"
    }

    $color = $colorMap[$Status]
    Write-ColorOutput "[$Status] " $color -NoNewline
    Write-Host $Message
}

# Check prerequisites
function Test-Prerequisites {
    Write-StatusMessage "Checking prerequisites..." "INFO"

    $missingTools = @()

    # Check Git
    try {
        $null = git --version 2>$null
        Write-StatusMessage "✓ Git is installed" "SUCCESS"
    } catch {
        $missingTools += "Git"
        Write-StatusMessage "✗ Git is not installed" "ERROR"
    }

    # Check GitHub CLI
    try {
        $null = gh --version 2>$null
        Write-StatusMessage "✓ GitHub CLI is installed" "SUCCESS"

        # Check authentication
        $authStatus = gh auth status 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ GitHub CLI is authenticated" "SUCCESS"
        } else {
            Write-StatusMessage "✗ GitHub CLI is not authenticated. Run: gh auth login" "ERROR"
            $missingTools += "GitHub CLI Authentication"
        }
    } catch {
        $missingTools += "GitHub CLI"
        Write-StatusMessage "✗ GitHub CLI is not installed" "ERROR"
    }

    if ($missingTools.Count -gt 0) {
        Write-Host ""
        Write-StatusMessage "Missing required tools: $($missingTools -join ', ')" "ERROR"
        Write-StatusMessage "Please install missing tools and try again." "ERROR"
        exit 1
    }

    Write-Host ""
}

# Get repository information
function Get-RepositoryInfo {
    param([string]$RepoName)

    Write-StatusMessage "Fetching repository information..." "INFO"

    try {
        $repoJson = gh repo view $RepoName --json name,owner,description,isPrivate,createdAt,pushedAt,url 2>$null | ConvertFrom-Json

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "Repository not found or inaccessible: $RepoName" "ERROR"
            return $null
        }

        return $repoJson
    } catch {
        Write-StatusMessage "Error fetching repository: $_" "ERROR"
        return $null
    }
}

# Display repository information
function Show-RepositoryInfo {
    param($RepoInfo)

    Write-Header "Repository Information"

    Write-ColorOutput "Name: " "Yellow" -NoNewline
    Write-Host "$($RepoInfo.owner.login)/$($RepoInfo.name)"

    Write-ColorOutput "Description: " "Yellow" -NoNewline
    Write-Host $(if ($RepoInfo.description) { $RepoInfo.description } else { "No description" })

    Write-ColorOutput "Visibility: " "Yellow" -NoNewline
    Write-Host $(if ($RepoInfo.isPrivate) { "Private" } else { "Public" })

    Write-ColorOutput "Created: " "Yellow" -NoNewline
    Write-Host $RepoInfo.createdAt

    Write-ColorOutput "Last Push: " "Yellow" -NoNewline
    Write-Host $RepoInfo.pushedAt

    Write-ColorOutput "URL: " "Yellow" -NoNewline
    Write-Host $RepoInfo.url

    Write-Host ""
}

# Create backup
function New-RepositoryBackup {
    param(
        [string]$RepoName,
        [string]$LocalPath
    )

    if ($SkipBackup) {
        Write-StatusMessage "Skipping backup as requested" "WARNING"
        return $true
    }

    Write-StatusMessage "Creating backup before deletion..." "INFO"

    $backupDir = Join-Path $env:USERPROFILE ".gitsage\backups"
    if (-not (Test-Path $backupDir)) {
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    }

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $safeRepoName = $RepoName -replace '[/\\]', '_'
    $backupFile = Join-Path $backupDir "${safeRepoName}_${timestamp}.zip"

    try {
        Write-StatusMessage "Compressing repository to: $backupFile" "INFO"
        Compress-Archive -Path "$LocalPath\*" -DestinationPath $backupFile -Force

        if (Test-Path $backupFile) {
            $backupSize = (Get-Item $backupFile).Length / 1MB
            Write-StatusMessage "✓ Backup created successfully (${backupSize:F2} MB)" "SUCCESS"
            Write-StatusMessage "  Backup location: $backupFile" "INFO"
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

# Check for uncommitted changes
function Test-UncommittedChanges {
    param([string]$LocalPath)

    if (-not (Test-Path $LocalPath)) {
        return $false
    }

    Push-Location $LocalPath
    try {
        $status = git status --porcelain 2>$null
        Pop-Location
        return ($null -ne $status -and $status.Trim() -ne "")
    } catch {
        Pop-Location
        return $false
    }
}

# Delete local repository
function Remove-LocalRepository {
    param([string]$LocalPath)

    if (-not (Test-Path $LocalPath)) {
        Write-StatusMessage "Local repository not found at: $LocalPath" "WARNING"
        return $true
    }

    Write-StatusMessage "Deleting local repository..." "WARNING"

    try {
        Remove-Item -Path $LocalPath -Recurse -Force

        if (-not (Test-Path $LocalPath)) {
            Write-StatusMessage "✓ Local repository deleted successfully" "SUCCESS"
            return $true
        } else {
            Write-StatusMessage "✗ Failed to delete local repository" "ERROR"
            return $false
        }
    } catch {
        Write-StatusMessage "✗ Error deleting local repository: $_" "ERROR"
        return $false
    }
}

# Delete remote repository
function Remove-RemoteRepository {
    param([string]$RepoName)

    Write-StatusMessage "Deleting remote repository on GitHub..." "WARNING"

    try {
        $result = gh repo delete $RepoName --yes 2>&1

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Remote repository deleted successfully" "SUCCESS"
            return $true
        } else {
            Write-StatusMessage "✗ Failed to delete remote repository: $result" "ERROR"
            return $false
        }
    } catch {
        Write-StatusMessage "✗ Error deleting remote repository: $_" "ERROR"
        return $false
    }
}

# Verify deletion
function Test-RepositoryDeleted {
    param([string]$RepoName)

    Write-StatusMessage "Verifying deletion..." "INFO"

    try {
        $null = gh repo view $RepoName 2>$null

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "✓ Repository deletion verified" "SUCCESS"
            return $true
        } else {
            Write-StatusMessage "✗ Repository still exists" "WARNING"
            return $false
        }
    } catch {
        # If error, likely deleted
        Write-StatusMessage "✓ Repository deletion verified" "SUCCESS"
        return $true
    }
}

# Get confirmation
function Get-UserConfirmation {
    param(
        [string]$Message,
        [string]$DefaultResponse = "N"
    )

    $prompt = if ($DefaultResponse -eq "Y") { "[Y/n]" } else { "[y/N]" }
    Write-ColorOutput "$Message $prompt " "Yellow" -NoNewline

    $response = Read-Host
    if ([string]::IsNullOrWhiteSpace($response)) {
        $response = $DefaultResponse
    }

    return $response -match '^[Yy]'
}

# Main execution
function Invoke-RepositoryDeletion {
    Write-Header "GitSage Repository Deletion Tool - PowerShell"

    # Check prerequisites
    Test-Prerequisites

    # Get repository name
    if ([string]::IsNullOrWhiteSpace($Repository)) {
        Write-Host "Enter repository name in format 'owner/repo'"
        Write-ColorOutput "Repository: " "Cyan" -NoNewline
        $Repository = Read-Host
    }

    if ([string]::IsNullOrWhiteSpace($Repository)) {
        Write-StatusMessage "Repository name is required" "ERROR"
        exit 1
    }

    # Get repository info
    $repoInfo = Get-RepositoryInfo -RepoName $Repository
    if ($null -eq $repoInfo) {
        exit 1
    }

    # Show repository info
    Show-RepositoryInfo -RepoInfo $repoInfo

    # Warning message
    Write-Header "⚠️  DANGER ZONE ⚠️"
    Write-StatusMessage "This action will PERMANENTLY DELETE the repository:" "WARNING"
    Write-StatusMessage "  Repository: $Repository" "WARNING"
    Write-StatusMessage "  This action CANNOT be undone!" "ERROR"
    Write-Host ""

    # Get local path
    $defaultPath = Join-Path (Get-Location) $repoInfo.name
    Write-ColorOutput "Local repository path [$defaultPath]: " "Cyan" -NoNewline
    $localPath = Read-Host
    if ([string]::IsNullOrWhiteSpace($localPath)) {
        $localPath = $defaultPath
    }

    # Check for uncommitted changes
    if (Test-Path $localPath) {
        if (Test-UncommittedChanges -LocalPath $localPath) {
            Write-StatusMessage "WARNING: Repository has uncommitted changes!" "ERROR"
            if (-not (Get-UserConfirmation "Delete anyway?")) {
                Write-StatusMessage "Deletion cancelled" "INFO"
                exit 0
            }
        }
    }

    # First confirmation
    if (-not (Get-UserConfirmation "Are you absolutely sure you want to delete '$Repository'?")) {
        Write-StatusMessage "Deletion cancelled" "INFO"
        exit 0
    }

    # Second confirmation
    Write-Host ""
    Write-StatusMessage "FINAL CONFIRMATION REQUIRED" "ERROR"
    Write-ColorOutput "Type the repository name '$Repository' to confirm: " "Red" -NoNewline
    $confirmation = Read-Host

    if ($confirmation -ne $Repository) {
        Write-StatusMessage "Repository name did not match. Deletion cancelled" "ERROR"
        exit 1
    }

    Write-Host ""
    Write-Header "Proceeding with Deletion"

    # Create backup
    if (Test-Path $localPath) {
        $backupSuccess = New-RepositoryBackup -RepoName $Repository -LocalPath $localPath
        if (-not $backupSuccess) {
            Write-StatusMessage "Backup failed. Continue anyway?" "WARNING"
            if (-not (Get-UserConfirmation "Continue without backup?" "N")) {
                Write-StatusMessage "Deletion cancelled" "INFO"
                exit 0
            }
        }
    }

    # Delete local repository
    $localSuccess = $true
    if (Test-Path $localPath) {
        $localSuccess = Remove-LocalRepository -LocalPath $localPath
    }

    # Delete remote repository
    $remoteSuccess = Remove-RemoteRepository -RepoName $Repository

    # Verify deletion
    Test-RepositoryDeleted -RepoName $Repository | Out-Null

    # Summary
    Write-Host ""
    Write-Header "Deletion Summary"

    if ($localSuccess) {
        Write-StatusMessage "✓ Local repository deleted" "SUCCESS"
    } else {
        Write-StatusMessage "✗ Local repository deletion failed or skipped" "WARNING"
    }

    if ($remoteSuccess) {
        Write-StatusMessage "✓ Remote repository deleted from GitHub" "SUCCESS"
    } else {
        Write-StatusMessage "✗ Remote repository deletion failed" "ERROR"
    }

    if ($localSuccess -and $remoteSuccess) {
        Write-Host ""
        Write-StatusMessage "Repository '$Repository' has been completely deleted" "SUCCESS"
    } else {
        Write-Host ""
        Write-StatusMessage "Deletion completed with errors - please review above" "WARNING"
    }
}

# Execute main function
try {
    Invoke-RepositoryDeletion
} catch {
    Write-StatusMessage "Unexpected error: $_" "ERROR"
    exit 1
}
