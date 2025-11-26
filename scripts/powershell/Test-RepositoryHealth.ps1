<#
.SYNOPSIS
    GitSage Repository Health Checker - PowerShell Version
.DESCRIPTION
    Analyze repository health with 13 comprehensive checks,
    gamified beautification scoring with 5 levels and achievements.
.PARAMETER Full
    Show full detailed report
.PARAMETER Quick
    Show quick summary only
.PARAMETER Beauty
    Show beautification score and achievements
.EXAMPLE
    .\Test-RepositoryHealth.ps1
    .\Test-RepositoryHealth.ps1 -Full
    .\Test-RepositoryHealth.ps1 -Beauty
#>

param(
    [switch]$Full,
    [switch]$Quick,
    [switch]$Beauty
)

# Color output functions
function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success { param([string]$Message) Write-ColorOutput $Message "Green" }
function Write-Info { param([string]$Message) Write-ColorOutput $Message "Cyan" }
function Write-Warning { param([string]$Message) Write-ColorOutput $Message "Yellow" }
function Write-Error { param([string]$Message) Write-ColorOutput $Message "Red" }

# Health check functions
function Test-ReadmeExists {
    $score = 0
    $maxScore = 15
    $status = "[FAIL]"
    $message = ""
    $quickWin = $false
    $critical = $false

    if (Test-Path "README.md") {
        $content = Get-Content "README.md" -Raw
        $length = $content.Length

        if ($length -lt 200) {
            $score = 5
            $status = "[WARN]"
            $message = "README exists but is too short (< 200 chars)"
            $quickWin = $true
        } elseif ($length -lt 1000) {
            $score = 10
            $status = "[WARN]"
            $message = "README exists but could be more comprehensive"
            $quickWin = $true
        } else {
            $score = 15
            $status = "[OK]"
            $message = "README.md is comprehensive"
        }
    } else {
        $status = "[FAIL]"
        $message = "README.md is missing"
        $critical = $true
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = $quickWin
        Critical = $critical
        Why = "README is the first thing visitors see. A good README increases project adoption by 70%."
    }
}

function Test-LicenseExists {
    $score = 0
    $maxScore = 10
    $status = "[FAIL]"
    $message = ""

    if (Test-Path "LICENSE") {
        $score = 10
        $status = "[OK]"
        $message = "LICENSE file exists"
    } elseif (Test-Path "LICENSE.md") {
        $score = 10
        $status = "[OK]"
        $message = "LICENSE.md file exists"
    } elseif (Test-Path "LICENSE.txt") {
        $score = 10
        $status = "[OK]"
        $message = "LICENSE.txt file exists"
    } else {
        $message = "No LICENSE file found"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = $false
        Why = "LICENSE clarifies how others can use your code. 84% of developers won't use unlicensed code."
    }
}

function Test-GitignoreExists {
    $score = 0
    $maxScore = 8
    $status = "[FAIL]"
    $message = ""

    if (Test-Path ".gitignore") {
        $score = 8
        $status = "[OK]"
        $message = ".gitignore exists"
    } else {
        $message = ".gitignore is missing"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = ($score -eq 0)
        Why = ".gitignore prevents committing sensitive files, secrets, and build artifacts."
    }
}

function Test-ContributingExists {
    $score = 0
    $maxScore = 8
    $status = "[FAIL]"
    $message = ""

    if (Test-Path "CONTRIBUTING.md") {
        $score = 8
        $status = "[OK]"
        $message = "CONTRIBUTING.md exists"
    } else {
        $message = "CONTRIBUTING.md is missing"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = $false
        Why = "CONTRIBUTING.md helps new contributors get started. Projects with this get 3x more contributions."
    }
}

function Test-CIConfigured {
    $score = 0
    $maxScore = 10
    $status = "[FAIL]"
    $message = ""

    if (Test-Path ".github/workflows") {
        $workflowFiles = Get-ChildItem ".github/workflows" -Filter "*.yml" -ErrorAction SilentlyContinue
        if ($workflowFiles.Count -gt 0) {
            $score = 10
            $status = "[OK]"
            $message = "GitHub Actions configured ($($workflowFiles.Count) workflows)"
        }
    } elseif (Test-Path ".travis.yml") {
        $score = 10
        $status = "[OK]"
        $message = "Travis CI configured"
    } elseif (Test-Path ".circleci/config.yml") {
        $score = 10
        $status = "[OK]"
        $message = "CircleCI configured"
    } else {
        $message = "No CI/CD automation detected"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = $false
        Critical = $false
        Why = "CI/CD ensures code quality and catches bugs early. Reduces production issues by 50%."
    }
}

function Test-DescriptionExists {
    $score = 0
    $maxScore = 5
    $status = "[WARN]"
    $message = "Cannot verify (requires GitHub API)"

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = $true
        Critical = $false
        Why = "Repository description helps with discoverability in GitHub search."
    }
}

function Test-TopicsExist {
    $score = 0
    $maxScore = 5
    $status = "[WARN]"
    $message = "Cannot verify (requires GitHub API)"

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = $true
        Critical = $false
        Why = "Topics/tags help users find your project. Tagged repos get 5x more visibility."
    }
}

function Test-IssueTemplates {
    $score = 0
    $maxScore = 7
    $status = "[FAIL]"
    $message = ""

    $templates = @(
        ".github/ISSUE_TEMPLATE",
        ".github/ISSUE_TEMPLATE.md",
        ".github/ISSUE_TEMPLATE/bug_report.md"
    )

    $found = $false
    foreach ($template in $templates) {
        if (Test-Path $template) {
            $found = $true
            break
        }
    }

    if ($found) {
        $score = 7
        $status = "[OK]"
        $message = "Issue templates configured"
    } else {
        $message = "No issue templates found"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = $false
        Why = "Issue templates help users report bugs effectively. Saves 60% of triage time."
    }
}

function Test-PRTemplates {
    $score = 0
    $maxScore = 7
    $status = "[FAIL]"
    $message = ""

    $templates = @(
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/pull_request_template.md",
        "docs/PULL_REQUEST_TEMPLATE.md"
    )

    $found = $false
    foreach ($template in $templates) {
        if (Test-Path $template) {
            $found = $true
            break
        }
    }

    if ($found) {
        $score = 7
        $status = "[OK]"
        $message = "PR template exists"
    } else {
        $message = "No PR template found"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = $false
        Why = "PR templates ensure consistent code reviews. Improves review efficiency by 40%."
    }
}

function Test-ChangelogExists {
    $score = 0
    $maxScore = 7
    $status = "[FAIL]"
    $message = ""

    if (Test-Path "CHANGELOG.md") {
        $score = 7
        $status = "[OK]"
        $message = "CHANGELOG.md exists"
    } elseif (Test-Path "HISTORY.md") {
        $score = 7
        $status = "[OK]"
        $message = "HISTORY.md exists"
    } else {
        $message = "No changelog found"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = $false
        Why = "CHANGELOG helps users track changes and decide when to upgrade."
    }
}

function Test-CodeOfConduct {
    $score = 0
    $maxScore = 6
    $status = "[FAIL]"
    $message = ""

    if (Test-Path "CODE_OF_CONDUCT.md") {
        $score = 6
        $status = "[OK]"
        $message = "CODE_OF_CONDUCT.md exists"
    } else {
        $message = "CODE_OF_CONDUCT.md is missing"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = $false
        Why = "Code of Conduct creates a welcoming environment. Increases diverse contributions by 35%."
    }
}

function Test-SecurityPolicy {
    $score = 0
    $maxScore = 6
    $status = "[FAIL]"
    $message = ""

    if (Test-Path "SECURITY.md") {
        $score = 6
        $status = "[OK]"
        $message = "SECURITY.md exists"
    } elseif (Test-Path ".github/SECURITY.md") {
        $score = 6
        $status = "[OK]"
        $message = "SECURITY.md exists"
    } else {
        $message = "SECURITY.md is missing"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = $false
        Why = "SECURITY.md tells researchers how to report vulnerabilities responsibly."
    }
}

function Test-Documentation {
    $score = 0
    $maxScore = 6
    $status = "[FAIL]"
    $message = ""

    $docPaths = @("docs/", "documentation/", "wiki/")
    $found = $false

    foreach ($path in $docPaths) {
        if (Test-Path $path) {
            $found = $true
            break
        }
    }

    if ($found) {
        $score = 6
        $status = "[OK]"
        $message = "Documentation directory exists"
    } else {
        $message = "No documentation directory found"
    }

    return @{
        Score = $score
        MaxScore = $maxScore
        Status = $status
        Message = $message
        QuickWin = ($score -eq 0)
        Critical = $false
        Why = "Good documentation reduces support burden and increases adoption."
    }
}

# Beautification scoring
function Get-BeautificationScore {
    $categories = @{
        Documentation = 0
        Community = 0
        Automation = 0
        Code = 0
        Visual = 0
        Extras = 0
    }

    $maxScores = @{
        Documentation = 25
        Community = 20
        Automation = 20
        Code = 15
        Visual = 10
        Extras = 10
    }

    # Documentation (25 pts)
    if (Test-Path "README.md") { $categories.Documentation += 10 }
    if (Test-Path "CHANGELOG.md") { $categories.Documentation += 5 }
    if ((Test-Path "docs/") -or (Test-Path "wiki/")) { $categories.Documentation += 10 }

    # Community (20 pts)
    if (Test-Path "CONTRIBUTING.md") { $categories.Community += 7 }
    if (Test-Path "CODE_OF_CONDUCT.md") { $categories.Community += 6 }
    if (Test-Path "LICENSE") { $categories.Community += 7 }

    # Automation (20 pts)
    if (Test-Path ".github/workflows") { $categories.Automation += 10 }
    if (Test-Path ".github/ISSUE_TEMPLATE") { $categories.Automation += 5 }
    if (Test-Path ".github/PULL_REQUEST_TEMPLATE.md") { $categories.Automation += 5 }

    # Code Quality (15 pts)
    if (Test-Path ".gitignore") { $categories.Code += 5 }
    if (Test-Path "tests/") { $categories.Code += 5 }
    if ((Test-Path ".editorconfig") -or (Test-Path ".prettierrc")) { $categories.Code += 5 }

    # Visual (10 pts)
    if (Test-Path "README.md") {
        $readme = Get-Content "README.md" -Raw
        if ($readme -match "!\[.*\]\(.*\)") { $categories.Visual += 5 }  # Has images
        if ($readme -match "shields.io") { $categories.Visual += 5 }  # Has badges
    }

    # Extras (10 pts)
    if (Test-Path "SECURITY.md") { $categories.Extras += 5 }
    if (Test-Path "Dockerfile") { $categories.Extras += 5 }

    $totalScore = 0
    foreach ($score in $categories.Values) {
        $totalScore += $score
    }

    # Determine level
    $level = "BEGINNER"
    $levelDesc = "Just Getting Started"
    $levelColor = "Red"

    if ($totalScore -ge 95) {
        $level = "MASTER"
        $levelDesc = "Open Source Champion"
        $levelColor = "Magenta"
    } elseif ($totalScore -ge 80) {
        $level = "EXPERT"
        $levelDesc = "Production Ready"
        $levelColor = "Green"
    } elseif ($totalScore -ge 60) {
        $level = "ADVANCED"
        $levelDesc = "Looking Professional"
        $levelColor = "Cyan"
    } elseif ($totalScore -ge 30) {
        $level = "INTERMEDIATE"
        $levelDesc = "Building Momentum"
        $levelColor = "Yellow"
    }

    # Check achievements
    $achievements = @()

    if (Test-Path "README.md") { $achievements += "First Steps - Created README.md" }
    if (Test-Path "LICENSE") { $achievements += "Legally Sound - Added LICENSE" }
    if (Test-Path ".github/workflows") { $achievements += "Automation Master - Setup CI/CD" }
    if (Test-Path "CONTRIBUTING.md") { $achievements += "Community Builder - Added CONTRIBUTING.md" }
    if ((Test-Path "docs/") -or (Test-Path "wiki/")) { $achievements += "Documentation Champion - Created documentation" }
    if ($totalScore -ge 50) { $achievements += "Half Way There - Reached 50% score" }
    if ($totalScore -ge 80) { $achievements += "Production Ready - Reached 80% score" }
    if ($totalScore -eq 100) { $achievements += "Perfect Score - Achieved 100%!" }

    return @{
        TotalScore = $totalScore
        MaxScore = 100
        Categories = $categories
        MaxScores = $maxScores
        Level = $level
        LevelDesc = $levelDesc
        LevelColor = $levelColor
        Achievements = $achievements
    }
}

# Run all health checks
function Get-FullHealthReport {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " [HEALTH] Repository Health Check" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    $checks = @(
        @{Name="README.md"; Check=(Test-ReadmeExists)},
        @{Name="LICENSE"; Check=(Test-LicenseExists)},
        @{Name=".gitignore"; Check=(Test-GitignoreExists)},
        @{Name="CONTRIBUTING.md"; Check=(Test-ContributingExists)},
        @{Name="CI/CD"; Check=(Test-CIConfigured)},
        @{Name="Description"; Check=(Test-DescriptionExists)},
        @{Name="Topics"; Check=(Test-TopicsExist)},
        @{Name="Issue Templates"; Check=(Test-IssueTemplates)},
        @{Name="PR Template"; Check=(Test-PRTemplates)},
        @{Name="CHANGELOG.md"; Check=(Test-ChangelogExists)},
        @{Name="CODE_OF_CONDUCT.md"; Check=(Test-CodeOfConduct)},
        @{Name="SECURITY.md"; Check=(Test-SecurityPolicy)},
        @{Name="Documentation"; Check=(Test-Documentation)}
    )

    $totalScore = 0
    $maxScore = 0
    $quickWins = @()
    $criticalIssues = @()

    foreach ($item in $checks) {
        $check = $item.Check
        $totalScore += $check.Score
        $maxScore += $check.MaxScore

        $statusColor = switch ($check.Status) {
            "[OK]" { "Green" }
            "[WARN]" { "Yellow" }
            "[FAIL]" { "Red" }
            default { "White" }
        }

        Write-Host "  $($check.Status) " -ForegroundColor $statusColor -NoNewline
        Write-Host "$($item.Name): $($check.Message)"

        if ($Full) {
            Write-Host "      [!] $($check.Why)" -ForegroundColor Gray
        }

        if ($check.QuickWin) {
            $quickWins += "$($item.Name) - $($check.Message)"
        }

        if ($check.Critical) {
            $criticalIssues += "$($item.Name) - $($check.Message)"
        }
    }

    Write-Host ""
    $percentage = [math]::Round($totalScore / $maxScore * 100, 1)
    $scoreColor = if ($totalScore -ge 80) { "Green" } elseif ($totalScore -ge 60) { "Yellow" } else { "Red" }

    Write-Host "Overall Score: $totalScore/$maxScore ($percentage%)" -ForegroundColor $scoreColor
    Write-Host ""

    # Quick wins
    if ($quickWins.Count -gt 0) {
        Write-Host "[ROCKET] Quick Wins (< 5 min):" -ForegroundColor Green
        foreach ($win in $quickWins | Select-Object -First 3) {
            Write-Host "  [>>] $win" -ForegroundColor Gray
        }
        Write-Host ""
    }

    # Critical issues
    if ($criticalIssues.Count -gt 0) {
        Write-Host "[!] Critical Issues:" -ForegroundColor Red
        foreach ($issue in $criticalIssues) {
            Write-Host "  [FAIL] $issue" -ForegroundColor Gray
        }
        Write-Host ""
    }
}

# Show beautification report
function Show-BeautificationReport {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " [*] Repository Beautification Score" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    $beauty = Get-BeautificationScore

    Write-Host "Overall Score: $($beauty.TotalScore)/$($beauty.MaxScore) ($([math]::Round($beauty.TotalScore))%)" -ForegroundColor $beauty.LevelColor
    Write-Host "Level: [$($beauty.Level)] $($beauty.LevelDesc)" -ForegroundColor $beauty.LevelColor
    Write-Host ""

    Write-Host "[STATS] Category Breakdown:" -ForegroundColor Cyan
    foreach ($category in $beauty.Categories.Keys) {
        $score = $beauty.Categories[$category]
        $max = $beauty.MaxScores[$category]
        $pct = if ($max -gt 0) { [math]::Round($score / $max * 100) } else { 0 }

        $barLength = [math]::Floor($pct / 5)
        $bar = "#" * $barLength + "-" * (20 - $barLength)

        Write-Host ("  {0,-15} [{1}] {2}/{3}" -f $category, $bar, $score, $max)
    }

    Write-Host ""

    # Achievements
    if ($beauty.Achievements.Count -gt 0) {
        Write-Host "[TROPHY] Achievements Unlocked ($($beauty.Achievements.Count)):" -ForegroundColor Yellow
        foreach ($achievement in $beauty.Achievements) {
            Write-Host "  [*] $achievement" -ForegroundColor Gray
        }
        Write-Host ""
    }

    # Next steps
    Write-Host "[>>] Next Steps to Level Up:" -ForegroundColor Cyan
    if (-not (Test-Path "README.md")) {
        Write-Host "  1. Create comprehensive README.md" -ForegroundColor Gray
    }
    if (-not (Test-Path "LICENSE")) {
        Write-Host "  2. Add LICENSE file" -ForegroundColor Gray
    }
    if (-not (Test-Path ".github/workflows")) {
        Write-Host "  3. Setup GitHub Actions CI/CD" -ForegroundColor Gray
    }
    if (-not (Test-Path "CONTRIBUTING.md")) {
        Write-Host "  4. Add CONTRIBUTING.md" -ForegroundColor Gray
    }
    Write-Host ""
}

# Main execution
if ($Beauty) {
    Show-BeautificationReport
}
elseif ($Quick) {
    $beauty = Get-BeautificationScore
    Write-Host ""
    Write-Host "Repository Score: $($beauty.TotalScore)/100" -ForegroundColor $beauty.LevelColor
    Write-Host "Level: $($beauty.Level)" -ForegroundColor $beauty.LevelColor
    Write-Host ""
}
elseif ($Full) {
    Get-FullHealthReport
    Write-Host ""
    Show-BeautificationReport
}
else {
    # Default: Both reports
    Get-FullHealthReport
    Write-Host ""
    Show-BeautificationReport
}
