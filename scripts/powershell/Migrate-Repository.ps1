#Requires -Version 5.1
<#
.SYNOPSIS
    GitSage Repository Migration Tool (PowerShell)

.DESCRIPTION
    Migrate repositories between GitHub accounts or organizations.
    Supports simple and full migration modes with history preservation.

.PARAMETER Mode
    Migration mode: 'simple' (clone and push) or 'full' (mirror with all refs)

.PARAMETER Source
    Source repository (owner/repo format)

.PARAMETER Destination
    Destination repository (owner/repo format)

.EXAMPLE
    .\Migrate-Repository.ps1
    Interactive mode

.EXAMPLE
    .\Migrate-Repository.ps1 -Mode simple -Source "oldowner/repo" -Destination "newowner/repo"
    Simple migration with parameters

.NOTES
    Author: GitSage Contributors
    Requires: Git, GitHub CLI (gh)
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("simple", "full")]
    [string]$Mode,

    [Parameter(Mandatory=$false)]
    [string]$Source,

    [Parameter(Mandatory=$false)]
    [string]$Destination
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
    param([string]$Message)

    Write-ColorOutput "$Message [y/N] " "Yellow" -NoNewline
    $response = Read-Host
    return $response -match '^[Yy]'
}

# Check prerequisites
function Test-Prerequisites {
    Write-StatusMessage "Checking prerequisites..." "INFO"

    $missingTools = @()

    try {
        $null = git --version 2>$null
        Write-StatusMessage "✓ Git is installed" "SUCCESS"
    } catch {
        $missingTools += "Git"
        Write-StatusMessage "✗ Git is not installed" "ERROR"
    }

    try {
        $null = gh --version 2>$null
        Write-StatusMessage "✓ GitHub CLI is installed" "SUCCESS"

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
        exit 1
    }

    Write-Host ""
}

# Get repository info
function Get-RepositoryInfo {
    param([string]$RepoName)

    try {
        $repoJson = gh repo view $RepoName --json name,owner,url,isPrivate 2>$null | ConvertFrom-Json
        if ($LASTEXITCODE -ne 0) {
            return $null
        }
        return $repoJson
    } catch {
        return $null
    }
}

# Simple migration
function Invoke-SimpleMigration {
    param(
        [string]$SourceRepo,
        [string]$DestRepo
    )

    Write-Header "Simple Migration Mode"
    Write-StatusMessage "This mode clones the repository and pushes to new destination" "INFO"
    Write-Host ""

    $tempDir = Join-Path $env:TEMP "gitsage_migration_$(Get-Date -Format 'yyyyMMddHHmmss')"

    try {
        # Clone source
        Write-StatusMessage "Step 1/4: Cloning source repository..." "INFO"
        git clone "https://github.com/$SourceRepo" $tempDir 2>$null

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "✗ Failed to clone source repository" "ERROR"
            return $false
        }

        Push-Location $tempDir

        # Create destination
        Write-StatusMessage "Step 2/4: Creating destination repository..." "INFO"
        $destParts = $DestRepo -split '/'
        $destName = $destParts[1]

        gh repo create $DestRepo --private --confirm 2>$null

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "Repository might already exist, continuing..." "WARNING"
        }

        # Add new remote
        Write-StatusMessage "Step 3/4: Adding new remote..." "INFO"
        git remote add new-origin "https://github.com/$DestRepo" 2>$null

        # Push to new destination
        Write-StatusMessage "Step 4/4: Pushing to destination..." "INFO"
        git push new-origin --all 2>$null
        git push new-origin --tags 2>$null

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Migration completed successfully!" "SUCCESS"
            $success = $true
        } else {
            Write-StatusMessage "✗ Push to destination failed" "ERROR"
            $success = $false
        }

        Pop-Location

        # Cleanup
        Write-StatusMessage "Cleaning up temporary directory..." "INFO"
        Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

        return $success

    } catch {
        Write-StatusMessage "✗ Error during migration: $_" "ERROR"
        if (Test-Path $tempDir) {
            Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
        }
        return $false
    }
}

# Full migration (mirror)
function Invoke-FullMigration {
    param(
        [string]$SourceRepo,
        [string]$DestRepo
    )

    Write-Header "Full Migration Mode (Mirror)"
    Write-StatusMessage "This mode performs a complete mirror including all refs, branches, and tags" "INFO"
    Write-Host ""

    $tempDir = Join-Path $env:TEMP "gitsage_migration_$(Get-Date -Format 'yyyyMMddHHmmss')"

    try {
        # Mirror clone
        Write-StatusMessage "Step 1/5: Creating mirror clone..." "INFO"
        git clone --mirror "https://github.com/$SourceRepo" $tempDir 2>$null

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "✗ Failed to create mirror clone" "ERROR"
            return $false
        }

        Push-Location $tempDir

        # Create destination
        Write-StatusMessage "Step 2/5: Creating destination repository..." "INFO"
        gh repo create $DestRepo --private --confirm 2>$null

        if ($LASTEXITCODE -ne 0) {
            Write-StatusMessage "Repository might already exist, continuing..." "WARNING"
        }

        # Set new remote
        Write-StatusMessage "Step 3/5: Setting new remote..." "INFO"
        git remote set-url origin "https://github.com/$DestRepo" 2>$null

        # Mirror push
        Write-StatusMessage "Step 4/5: Pushing mirror to destination..." "INFO"
        git push --mirror 2>$null

        if ($LASTEXITCODE -eq 0) {
            Write-StatusMessage "✓ Mirror push completed!" "SUCCESS"
            $success = $true
        } else {
            Write-StatusMessage "✗ Mirror push failed" "ERROR"
            $success = $false
        }

        Pop-Location

        # Cleanup
        Write-StatusMessage "Step 5/5: Cleaning up..." "INFO"
        Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue

        return $success

    } catch {
        Write-StatusMessage "✗ Error during migration: $_" "ERROR"
        if (Test-Path $tempDir) {
            Remove-Item -Path $tempDir -Recurse -Force -ErrorAction SilentlyContinue
        }
        return $false
    }
}

# Main migration function
function Start-RepositoryMigration {
    Write-Header "GitSage Repository Migration Tool - PowerShell"

    Test-Prerequisites

    # Get mode
    if ([string]::IsNullOrWhiteSpace($Mode)) {
        Write-ColorOutput "Migration modes:" "Yellow"
        Write-Host "  1. Simple  - Clone and push (easier, faster)"
        Write-Host "  2. Full    - Complete mirror (all refs, branches, tags)"
        Write-Host ""
        Write-ColorOutput "Choose mode [1-2]: " "Cyan" -NoNewline
        $modeChoice = Read-Host

        $Mode = if ($modeChoice -eq "2") { "full" } else { "simple" }
    }

    Write-StatusMessage "Selected mode: $Mode" "INFO"
    Write-Host ""

    # Get source repository
    if ([string]::IsNullOrWhiteSpace($Source)) {
        Write-ColorOutput "Source repository (owner/repo): " "Cyan" -NoNewline
        $Source = Read-Host
    }

    if ([string]::IsNullOrWhiteSpace($Source)) {
        Write-StatusMessage "Source repository required" "ERROR"
        exit 1
    }

    # Verify source exists
    Write-StatusMessage "Verifying source repository..." "INFO"
    $sourceInfo = Get-RepositoryInfo -RepoName $Source
    if ($null -eq $sourceInfo) {
        Write-StatusMessage "Source repository not found or inaccessible: $Source" "ERROR"
        exit 1
    }

    Write-StatusMessage "✓ Source verified: $($sourceInfo.owner.login)/$($sourceInfo.name)" "SUCCESS"

    # Get destination repository
    if ([string]::IsNullOrWhiteSpace($Destination)) {
        Write-ColorOutput "Destination repository (owner/repo): " "Cyan" -NoNewline
        $Destination = Read-Host
    }

    if ([string]::IsNullOrWhiteSpace($Destination)) {
        Write-StatusMessage "Destination repository required" "ERROR"
        exit 1
    }

    # Check if destination exists
    Write-StatusMessage "Checking destination repository..." "INFO"
    $destInfo = Get-RepositoryInfo -RepoName $Destination
    if ($null -ne $destInfo) {
        Write-StatusMessage "WARNING: Destination repository already exists!" "WARNING"
        Write-StatusMessage "This will overwrite: $($destInfo.owner.login)/$($destInfo.name)" "WARNING"
        if (-not (Get-UserConfirmation "Continue and overwrite?")) {
            Write-StatusMessage "Migration cancelled" "INFO"
            exit 0
        }
    }

    # Confirm migration
    Write-Host ""
    Write-Header "Migration Summary"
    Write-ColorOutput "Mode: " "Yellow" -NoNewline
    Write-Host $Mode.ToUpper()
    Write-ColorOutput "From: " "Yellow" -NoNewline
    Write-Host $Source
    Write-ColorOutput "To:   " "Yellow" -NoNewline
    Write-Host $Destination
    Write-Host ""

    if (-not (Get-UserConfirmation "Proceed with migration?")) {
        Write-StatusMessage "Migration cancelled" "INFO"
        exit 0
    }

    Write-Host ""

    # Execute migration
    $success = if ($Mode -eq "full") {
        Invoke-FullMigration -SourceRepo $Source -DestRepo $Destination
    } else {
        Invoke-SimpleMigration -SourceRepo $Source -DestRepo $Destination
    }

    # Summary
    Write-Host ""
    Write-Header "Migration Summary"

    if ($success) {
        Write-StatusMessage "✓ Repository migrated successfully!" "SUCCESS"
        Write-StatusMessage "  Source: $Source" "INFO"
        Write-StatusMessage "  Destination: $Destination" "INFO"
        Write-StatusMessage "  New URL: https://github.com/$Destination" "INFO"

        Write-Host ""
        Write-StatusMessage "Next steps:" "INFO"
        Write-StatusMessage "  1. Verify the migrated repository" "INFO"
        Write-StatusMessage "  2. Update any CI/CD configurations" "INFO"
        Write-StatusMessage "  3. Update documentation and links" "INFO"
    } else {
        Write-StatusMessage "✗ Migration failed - please check errors above" "ERROR"
        exit 1
    }
}

# Execute main function
try {
    Start-RepositoryMigration
} catch {
    Write-StatusMessage "Unexpected error: $_" "ERROR"
    exit 1
}
