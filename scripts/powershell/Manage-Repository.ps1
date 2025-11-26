#Requires -Version 5.1
<#
.SYNOPSIS
    GitSage Repository Manager (PowerShell)

.DESCRIPTION
    Advanced repository management with Git and GitHub CLI operations.
    Interactive menu for common repository management tasks.

.EXAMPLE
    .\Manage-Repository.ps1
    Launch interactive repository manager

.NOTES
    Author: GitSage Contributors
    Requires: Git, GitHub CLI (gh)
#>

[CmdletBinding()]
param()

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
    $missingTools = @()

    try { $null = git --version 2>$null } catch { $missingTools += "Git" }
    try { $null = gh --version 2>$null } catch { $missingTools += "GitHub CLI" }

    if ($missingTools.Count -gt 0) {
        Write-StatusMessage "Missing required tools: $($missingTools -join ', ')" "ERROR"
        Write-StatusMessage "Please install missing tools and try again." "ERROR"
        exit 1
    }
}

# Menu functions
function Show-Menu {
    Write-Header "GitSage Repository Manager - PowerShell"

    Write-ColorOutput "Repository Operations:" "Yellow"
    Write-Host "  1. Clone Repository"
    Write-Host "  2. Create New Repository"
    Write-Host "  3. List Your Repositories"
    Write-Host "  4. Repository Status"
    Write-Host ""

    Write-ColorOutput "Git Operations:" "Yellow"
    Write-Host "  5. Commit Changes"
    Write-Host "  6. Push to Remote"
    Write-Host "  7. Pull from Remote"
    Write-Host "  8. Create Branch"
    Write-Host "  9. Switch Branch"
    Write-Host " 10. Merge Branch"
    Write-Host ""

    Write-ColorOutput "Advanced:" "Yellow"
    Write-Host " 11. Sync Fork"
    Write-Host " 12. Create Pull Request"
    Write-Host " 13. View Repository Issues"
    Write-Host ""

    Write-ColorOutput "Other:" "Yellow"
    Write-Host "  0. Exit"
    Write-Host ""

    Write-ColorOutput "Enter choice: " "Cyan" -NoNewline
    return Read-Host
}

# Clone repository
function Invoke-CloneRepository {
    Write-Header "Clone Repository"

    Write-ColorOutput "Enter repository (owner/repo or URL): " "Cyan" -NoNewline
    $repo = Read-Host

    if ([string]::IsNullOrWhiteSpace($repo)) {
        Write-StatusMessage "Repository name required" "ERROR"
        return
    }

    Write-StatusMessage "Cloning $repo..." "INFO"

    try {
        if ($repo -match "^https?://") {
            git clone $repo
        } else {
            gh repo clone $repo
        }

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Repository cloned successfully" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Clone failed" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Create repository
function New-GitHubRepository {
    Write-Header "Create New Repository"

    Write-ColorOutput "Repository name: " "Cyan" -NoNewline
    $repoName = Read-Host

    if ([string]::IsNullOrWhiteSpace($repoName)) {
        Write-StatusMessage "Repository name required" "ERROR"
        return
    }

    Write-ColorOutput "Description (optional): " "Cyan" -NoNewline
    $description = Read-Host

    Write-ColorOutput "Visibility (public/private) [public]: " "Cyan" -NoNewline
    $visibility = Read-Host
    if ([string]::IsNullOrWhiteSpace($visibility)) { $visibility = "public" }

    try {
        $args = @("repo", "create", $repoName, "--$visibility")
        if (-not [string]::IsNullOrWhiteSpace($description)) {
            $args += "--description", $description
        }

        & gh @args

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Repository '$repoName' created successfully" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Failed to create repository" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# List repositories
function Show-Repositories {
    Write-Header "Your Repositories"

    try {
        Write-StatusMessage "Fetching repositories..." "INFO"
        gh repo list --limit 20

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "✗ Failed to fetch repositories" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Repository status
function Show-RepositoryStatus {
    Write-Header "Repository Status"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    try {
        git status
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Commit changes
function Invoke-CommitChanges {
    Write-Header "Commit Changes"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    git status

    Write-Host ""
    Write-ColorOutput "Commit message: " "Cyan" -NoNewline
    $message = Read-Host

    if ([string]::IsNullOrWhiteSpace($message)) {
        Write-StatusMessage "Commit message required" "ERROR"
        return
    }

    try {
        git add .
        git commit -m $message

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Changes committed" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Commit failed" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Push to remote
function Invoke-PushToRemote {
    Write-Header "Push to Remote"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    try {
        $branch = git branch --show-current
        Write-StatusMessage "Pushing '$branch' to origin..." "INFO"

        git push origin $branch

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Pushed successfully" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Push failed" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Pull from remote
function Invoke-PullFromRemote {
    Write-Header "Pull from Remote"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    try {
        $branch = git branch --show-current
        Write-StatusMessage "Pulling '$branch' from origin..." "INFO"

        git pull origin $branch

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Pulled successfully" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Pull failed" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Create branch
function New-GitBranch {
    Write-Header "Create Branch"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    Write-ColorOutput "New branch name: " "Cyan" -NoNewline
    $branchName = Read-Host

    if ([string]::IsNullOrWhiteSpace($branchName)) {
        Write-StatusMessage "Branch name required" "ERROR"
        return
    }

    try {
        git checkout -b $branchName

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Branch '$branchName' created and checked out" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Failed to create branch" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Switch branch
function Switch-GitBranch {
    Write-Header "Switch Branch"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    Write-StatusMessage "Available branches:" "INFO"
    git branch -a

    Write-Host ""
    Write-ColorOutput "Branch name to switch to: " "Cyan" -NoNewline
    $branchName = Read-Host

    if ([string]::IsNullOrWhiteSpace($branchName)) {
        Write-StatusMessage "Branch name required" "ERROR"
        return
    }

    try {
        git checkout $branchName

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Switched to branch '$branchName'" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Failed to switch branch" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Merge branch
function Merge-GitBranch {
    Write-Header "Merge Branch"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    $currentBranch = git branch --show-current
    Write-StatusMessage "Current branch: $currentBranch" "INFO"

    Write-Host ""
    Write-StatusMessage "Available branches:" "INFO"
    git branch

    Write-Host ""
    Write-ColorOutput "Branch to merge into '$currentBranch': " "Cyan" -NoNewline
    $branchName = Read-Host

    if ([string]::IsNullOrWhiteSpace($branchName)) {
        Write-StatusMessage "Branch name required" "ERROR"
        return
    }

    try {
        git merge $branchName

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Merged '$branchName' into '$currentBranch'" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Merge failed - resolve conflicts manually" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Sync fork
function Sync-Fork {
    Write-Header "Sync Fork"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    try {
        Write-StatusMessage "Syncing fork with upstream..." "INFO"
        gh repo sync

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Fork synced successfully" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Sync failed" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Create pull request
function New-PullRequest {
    Write-Header "Create Pull Request"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    Write-ColorOutput "PR title: " "Cyan" -NoNewline
    $title = Read-Host

    if ([string]::IsNullOrWhiteSpace($title)) {
        Write-StatusMessage "Title required" "ERROR"
        return
    }

    Write-ColorOutput "PR description (optional): " "Cyan" -NoNewline
    $body = Read-Host

    try {
        $args = @("pr", "create", "--title", $title)
        if (-not [string]::IsNullOrWhiteSpace($body)) {
            $args += "--body", $body
        }

        & gh @args

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Pull request created" "SUCCESS"
        } else {
            Write-StatusMessage "✗ Failed to create PR" "ERROR"
        }
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# View issues
function Show-Issues {
    Write-Header "Repository Issues"

    if (-not (Test-Path ".git")) {
        Write-StatusMessage "Not a git repository" "ERROR"
        return
    }

    try {
        gh issue list --limit 20
    } catch {
        Write-StatusMessage "✗ Error: $_" "ERROR"
    }
}

# Main loop
function Start-RepositoryManager {
    Test-Prerequisites

    while ($true) {
        $choice = Show-Menu

        switch ($choice) {
            "1" { Invoke-CloneRepository }
            "2" { New-GitHubRepository }
            "3" { Show-Repositories }
            "4" { Show-RepositoryStatus }
            "5" { Invoke-CommitChanges }
            "6" { Invoke-PushToRemote }
            "7" { Invoke-PullFromRemote }
            "8" { New-GitBranch }
            "9" { Switch-GitBranch }
            "10" { Merge-GitBranch }
            "11" { Sync-Fork }
            "12" { New-PullRequest }
            "13" { Show-Issues }
            "0" {
                Write-StatusMessage "Thank you for using GitSage Repository Manager!" "SUCCESS"
                exit 0
            }
            default {
                Write-StatusMessage "Invalid choice" "ERROR"
            }
        }

        Write-Host ""
        Write-ColorOutput "Press Enter to continue..." "Yellow" -NoNewline
        Read-Host | Out-Null
    }
}

# Execute main function
try {
    Start-RepositoryManager
} catch {
    Write-StatusMessage "Unexpected error: $_" "ERROR"
    exit 1
}
