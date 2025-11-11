param(
    [string]$RepoPath = "F:\AI_Oracle_Root",
    [string]$LogFile = "F:\AI_Oracle_Root\Logs\Automation\auto_git_push.log",
    [switch]$DryRun
)

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$timestamp] $Message"
    Write-Output $entry
    if ($LogFile) {
        $entry | Out-File -FilePath $LogFile -Append -Encoding UTF8
    }
}

if (-not (Test-Path -Path $RepoPath)) {
    Write-Log "Repo path '$RepoPath' not found."
    exit 1
}

try {
    Push-Location -Path $RepoPath

    git rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "Directory is not a git repository."
        throw "Not a git repo"
    }

    $branch = (git rev-parse --abbrev-ref HEAD).Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($branch)) {
        Write-Log "Unable to determine current branch."
        throw "branch lookup failed"
    }

    if ($branch -eq 'HEAD') {
        $symbolicRaw = git symbolic-ref --short HEAD 2>$null
        if ($LASTEXITCODE -eq 0 -and -not [string]::IsNullOrWhiteSpace($symbolicRaw)) {
            $branch = $symbolicRaw.Trim()
        }
    }

    Write-Log "Syncing branch '$branch' with origin."

    $fetchOutput = git fetch origin $branch 2>&1
    if ($fetchOutput) { $fetchOutput | ForEach-Object { Write-Log $_ } }
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git fetch failed."
        throw "git fetch failed"
    }

    $behindRaw = git rev-list --count "$branch..origin/$branch" 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($behindRaw)) {
        Write-Log "Unable to compare with origin/$branch."
        throw "divergence check failed"
    }
    $behindCount = [int]$behindRaw

    $aheadRaw = git rev-list --count "origin/$branch..$branch" 2>$null
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($aheadRaw)) {
        $aheadCount = 0
    } else {
        $aheadCount = [int]$aheadRaw
    }

    if ($behindCount -gt 0) {
        Write-Log "Branch is behind origin/$branch by $behindCount commit(s). Manual sync required; aborting auto push."
        exit 0
    }

    if ($aheadCount -gt 0) {
        Write-Log "Branch is ahead of origin/$branch by $aheadCount commit(s)."
    }

    $status = git status --porcelain
    if ($LASTEXITCODE -ne 0) {
        Write-Log "Failed to check git status."
        throw "git status failed"
    }

    if ([string]::IsNullOrWhiteSpace($status)) {
        Write-Log "No changes detected after sync. Exiting."
        exit 0
    }

    $statusLines = $status -split "`n" | Where-Object { $_.Trim() -ne "" }
    Write-Log ("Detected {0} changed path(s) on branch '{1}'." -f $statusLines.Count, $branch)

    if ($DryRun) {
        Write-Log "DryRun flag set. Skipping git add/commit/push."
        $preview = $statusLines | Select-Object -First 10
        if ($preview) {
            $summary = $preview -join ' '
            if ($statusLines.Count -gt 10) {
                $summary += ' ...'
            }
            Write-Log ("Status preview: {0}" -f $summary)
        }
        exit 0
    }

    $excludePatterns = @(
        '^Logs/',
        '^Backups/',
        '^backup/',
        '^Archive/',
        '^archive_cleanup/',
        '^tmp/',
        '^temp/',
        '^\.venv',
        '^venv'
    )

    $pathsToStage = @()
    foreach ($line in $statusLines) {
        if ($line.Length -lt 4) { continue }

        $path = $line.Substring(3)

        if ($line.StartsWith("R ") -or $line.StartsWith("C ")) {
            $parts = $path -split ' -> '
            if ($parts.Length -gt 0) {
                $path = $parts[-1]
            }
        }

        $path = $path.Trim()
        if ([string]::IsNullOrWhiteSpace($path)) { continue }

        $exclude = $false
        foreach ($pattern in $excludePatterns) {
            if ($path -match $pattern) {
                $exclude = $true
                break
            }
        }

        if (-not $exclude) {
            $pathsToStage += $path
        }
    }

    if ($pathsToStage.Count -eq 0) {
        Write-Log "Changes limited to excluded paths. Exiting."
        exit 0
    }

    Write-Log ("Staging {0} path(s)." -f $pathsToStage.Count)

    git add -- $pathsToStage
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git add failed."
        throw "git add failed"
    }

    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Log "No staged changes after add. Exiting."
        exit 0
    }

    $commitMessage = "auto-sync $(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss')"
    git commit -m $commitMessage
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git commit failed."
        throw "git commit failed"
    }

    $pushOutput = git push origin $branch 2>&1
    if ($pushOutput) { $pushOutput | ForEach-Object { Write-Log $_ } }
    if ($LASTEXITCODE -ne 0) {
        Write-Log "git push failed."
        throw "git push failed"
    }

    Write-Log "Auto push complete: $commitMessage"

} catch {
    Write-Log "Automation failed: $_"
    exit 1
} finally {
    Pop-Location -ErrorAction SilentlyContinue
}

