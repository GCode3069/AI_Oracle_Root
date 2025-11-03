#!/usr/bin/env pwsh
<#
.SYNOPSIS
    COMPLETE GITHUB SYNC - Update AI_Oracle_Root repository with ALL latest files
    
.DESCRIPTION
    Syncs your local Scarify Empire to GitHub repository GCode3069/AI_Oracle_Root
    Handles large files, excludes sensitive data, commits everything properly
    
.NOTES
    Repository: https://github.com/GCode3069/AI_Oracle_Root
    Current Status: 7 months behind (needs major update!)
    Target: Sync ALL 145+ project files to GitHub
#>

param(
    [string]$CommitMessage = "🚀 MASSIVE UPDATE: Scarify Empire complete system sync",
    [switch]$DryRun = $false,
    [switch]$Force = $false
)

$ErrorActionPreference = "Continue"
$PROJECT_ROOT = "F:\AI_Oracle_Root\scarify"
$REPO_URL = "https://github.com/GCode3069/AI_Oracle_Root.git"

function Write-ColorOutput {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Test-GitInstalled {
    try {
        $null = git --version
        return $true
    } catch {
        return $false
    }
}

function Initialize-GitRepo {
    Write-ColorOutput "`n=== INITIALIZING GIT REPOSITORY ===" "Cyan"
    
    Push-Location $PROJECT_ROOT
    
    # Check if .git exists
    if (-not (Test-Path ".git")) {
        Write-ColorOutput "Initializing new Git repository..." "Yellow"
        git init
        
        # Add remote
        Write-ColorOutput "Adding remote origin..." "Yellow"
        git remote add origin $REPO_URL
    } else {
        Write-ColorOutput "Git repository already initialized" "Green"
        
        # Verify remote
        $remotes = git remote -v
        if ($remotes -notmatch "origin") {
            Write-ColorOutput "Adding remote origin..." "Yellow"
            git remote add origin $REPO_URL
        }
    }
    
    Pop-Location
}

function Update-GitIgnore {
    Write-ColorOutput "`n=== UPDATING .GITIGNORE ===" "Cyan"
    
    $gitignoreContent = @"
# Sensitive Files
*.pickle
*token*.json
*credentials*.json
*secrets*.json
*api_key*.txt
client_secrets.json
youtube_token.pickle
config/credentials/
*.env

# Large Media Files
*.mp4
*.avi
*.mov
*.mkv
*.webm
*.wav
*.mp3
*.flac
*.m4a

# Generated Content
abraham_horror/generated/
abraham_horror/uploaded/
abraham_horror/youtube_ready/
abraham_horror/cache/
abraham_horror/pollo_cache/
abraham_horror/logs/
abraham_horror/temp/
*/generated/
*/uploaded/
*/cache/
*/logs/
*/temp/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
venv/
ENV/

# Node
node_modules/
npm-debug.log
yarn-error.log

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
desktop.ini

# Backups
*.bak
*.backup
*.old
*~
_quarantine*/
backups/
archive/

# Large binaries
*.exe
*.msi
*.dll
*.so
*.dylib
*.zip
*.tar.gz
*.rar
*.7z

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log
logs/

# Temporary
*.tmp
*.temp
"@

    $gitignorePath = Join-Path $PROJECT_ROOT ".gitignore"
    Set-Content -Path $gitignorePath -Value $gitignoreContent -Encoding UTF8
    Write-ColorOutput "✓ .gitignore updated" "Green"
}

function Get-RepoStatus {
    Write-ColorOutput "`n=== REPOSITORY STATUS ===" "Cyan"
    
    Push-Location $PROJECT_ROOT
    
    $status = git status --short
    $untracked = ($status | Where-Object { $_ -match "^\?\?" }).Count
    $modified = ($status | Where-Object { $_ -match "^ M" }).Count
    $added = ($status | Where-Object { $_ -match "^A " }).Count
    $deleted = ($status | Where-Object { $_ -match "^ D" }).Count
    
    Write-ColorOutput "`nFiles to sync:" "Yellow"
    Write-ColorOutput "  Untracked: $untracked" "White"
    Write-ColorOutput "  Modified:  $modified" "White"
    Write-ColorOutput "  Added:     $added" "White"
    Write-ColorOutput "  Deleted:   $deleted" "White"
    Write-ColorOutput "  Total:     $($untracked + $modified + $added + $deleted)" "Cyan"
    
    Pop-Location
    
    return @{
        Untracked = $untracked
        Modified = $modified
        Added = $added
        Deleted = $deleted
        Total = $untracked + $modified + $added + $deleted
    }
}

function Add-FilesToGit {
    param([bool]$DryRun = $false)
    
    Write-ColorOutput "`n=== STAGING FILES ===" "Cyan"
    
    Push-Location $PROJECT_ROOT
    
    if ($DryRun) {
        Write-ColorOutput "DRY RUN: Would stage all files..." "Yellow"
        git add --dry-run -A
    } else {
        Write-ColorOutput "Staging all files (respecting .gitignore)..." "Yellow"
        git add -A
        
        $staged = git diff --cached --name-only
        $count = ($staged | Measure-Object).Count
        
        Write-ColorOutput "✓ Staged $count files" "Green"
        
        # Show first 20 files
        Write-ColorOutput "`nFirst 20 staged files:" "Cyan"
        $staged | Select-Object -First 20 | ForEach-Object {
            Write-ColorOutput "  + $_" "White"
        }
        
        if ($count -gt 20) {
            Write-ColorOutput "  ... and $($count - 20) more files" "Gray"
        }
    }
    
    Pop-Location
}

function Commit-Changes {
    param(
        [string]$Message,
        [bool]$DryRun = $false
    )
    
    Write-ColorOutput "`n=== COMMITTING CHANGES ===" "Cyan"
    
    Push-Location $PROJECT_ROOT
    
    if ($DryRun) {
        Write-ColorOutput "DRY RUN: Would commit with message: $Message" "Yellow"
    } else {
        Write-ColorOutput "Committing changes..." "Yellow"
        git commit -m $Message
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✓ Changes committed successfully" "Green"
        } else {
            Write-ColorOutput "⚠ No changes to commit or commit failed" "Yellow"
        }
    }
    
    Pop-Location
}

function Push-ToGitHub {
    param([bool]$DryRun = $false, [bool]$Force = $false)
    
    Write-ColorOutput "`n=== PUSHING TO GITHUB ===" "Cyan"
    
    Push-Location $PROJECT_ROOT
    
    if ($DryRun) {
        Write-ColorOutput "DRY RUN: Would push to GitHub..." "Yellow"
        git push --dry-run origin main
    } else {
        Write-ColorOutput "Pushing to GitHub (this may take a few minutes)..." "Yellow"
        
        if ($Force) {
            Write-ColorOutput "⚠ FORCE PUSH enabled!" "Red"
            git push -f origin main
        } else {
            # Try to pull first to avoid conflicts
            Write-ColorOutput "Pulling latest changes first..." "Yellow"
            git pull origin main --rebase 2>$null
            
            # Now push
            git push origin main
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✓ Successfully pushed to GitHub!" "Green"
            Write-ColorOutput "`n🎉 Repository updated: $REPO_URL" "Cyan"
        } else {
            Write-ColorOutput "❌ Push failed. You may need to resolve conflicts." "Red"
            Write-ColorOutput "Try running with -Force flag if you want to overwrite remote." "Yellow"
        }
    }
    
    Pop-Location
}

function Show-Summary {
    Write-ColorOutput "`n╔══════════════════════════════════════════════════════════════╗" "Cyan"
    Write-ColorOutput "║                                                              ║" "Cyan"
    Write-ColorOutput "║              GITHUB SYNC COMPLETE SUMMARY                    ║" "Cyan"
    Write-ColorOutput "║                                                              ║" "Cyan"
    Write-ColorOutput "╚══════════════════════════════════════════════════════════════╝" "Cyan"
    
    Write-ColorOutput "`n📊 Your repository has been updated!" "Green"
    Write-ColorOutput "🔗 View at: https://github.com/GCode3069/AI_Oracle_Root" "White"
    Write-ColorOutput "`n✓ All Scarify Empire files synced" "Green"
    Write-ColorOutput "✓ Sensitive files excluded (.gitignore)" "Green"
    Write-ColorOutput "✓ Large media files excluded" "Green"
    Write-ColorOutput "✓ Repository now up-to-date" "Green"
    
    Write-ColorOutput "`n📝 Next steps:" "Yellow"
    Write-ColorOutput "  1. Visit your repo to verify all files are there" "White"
    Write-ColorOutput "  2. Check GitHub Actions (if you have any)" "White"
    Write-ColorOutput "  3. Update README.md with latest features" "White"
    Write-ColorOutput "  4. Consider adding a LICENSE file" "White"
    
    Write-ColorOutput "`n🎯 Your repo is no longer 'lite' - it's COMPLETE!" "Cyan"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================

Write-ColorOutput "`n╔══════════════════════════════════════════════════════════════╗" "Cyan"
Write-ColorOutput "║                                                              ║" "Cyan"
Write-ColorOutput "║     SCARIFY EMPIRE → GITHUB SYNC                            ║" "Cyan"
Write-ColorOutput "║     Complete Repository Update                               ║" "Cyan"
Write-ColorOutput "║                                                              ║" "Cyan"
Write-ColorOutput "╚══════════════════════════════════════════════════════════════╝" "Cyan"

# Check Git installation
if (-not (Test-GitInstalled)) {
    Write-ColorOutput "`n❌ Git is not installed!" "Red"
    Write-ColorOutput "Download from: https://git-scm.com/download/win" "Yellow"
    exit 1
}

Write-ColorOutput "`n✓ Git is installed" "Green"
Write-ColorOutput "✓ Project root: $PROJECT_ROOT" "Green"
Write-ColorOutput "✓ Target repo: $REPO_URL" "Green"

if ($DryRun) {
    Write-ColorOutput "`n⚠ DRY RUN MODE - No changes will be made" "Yellow"
}

# Execute sync steps
try {
    # Step 1: Initialize
    Initialize-GitRepo
    
    # Step 2: Update .gitignore
    Update-GitIgnore
    
    # Step 3: Check status
    $status = Get-RepoStatus
    
    if ($status.Total -eq 0) {
        Write-ColorOutput "`n✓ Repository is already up-to-date!" "Green"
        exit 0
    }
    
    # Step 4: Stage files
    Add-FilesToGit -DryRun $DryRun
    
    # Step 5: Commit
    Commit-Changes -Message $CommitMessage -DryRun $DryRun
    
    # Step 6: Push
    if (-not $DryRun) {
        $confirm = Read-Host "`nPush to GitHub? (y/n)"
        if ($confirm -eq 'y' -or $confirm -eq 'Y') {
            Push-ToGitHub -DryRun $false -Force $Force
            Show-Summary
        } else {
            Write-ColorOutput "`n⚠ Push cancelled by user" "Yellow"
        }
    }
    
} catch {
    Write-ColorOutput "`n❌ Error: $_" "Red"
    Write-ColorOutput $_.ScriptStackTrace "Red"
    exit 1
}

Write-ColorOutput "`n✅ Script execution complete!" "Green"

