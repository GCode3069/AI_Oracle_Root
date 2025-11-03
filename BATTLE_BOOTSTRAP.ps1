# BATTLE_BOOTSTRAP.ps1 - LLM Battle Royale Setup Script
# This script creates the required directory structure and placeholder files
# for the LLM Battle Royale system.

Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "LLM Battle Royale - Bootstrap Setup" -ForegroundColor Yellow
Write-Host "=" -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 59) -ForegroundColor Cyan

# Create required directories
$directories = @(
    "core",
    "core/production_inputs",
    "submissions",
    "examples"
)

Write-Host "`nCreating directory structure..." -ForegroundColor Green
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  [+] Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  [*] Exists: $dir" -ForegroundColor Yellow
    }
}

# Create placeholder files if they don't exist
Write-Host "`nChecking for required files..." -ForegroundColor Green

$files = @{
    "battle_data.json" = @"
{
  "runs": [],
  "proofs": [],
  "pending_submissions": [],
  "llm_summary": {},
  "generated_at": "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss.fff')Z"
}
"@
    ".gitignore" = @"
# Environment variables (NEVER commit)
.env

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Logs
*.log

# OS files
.DS_Store
Thumbs.db

# Generated content (review before committing)
core/production_inputs/*.mp4
core/production_inputs/*.mp3
elimination.json

# OAuth tokens (NEVER commit)
token.json
client_secrets*.json
"@
}

foreach ($file in $files.Keys) {
    if (!(Test-Path $file)) {
        $files[$file] | Out-File -FilePath $file -Encoding UTF8 -NoNewline
        Write-Host "  [+] Created: $file" -ForegroundColor Green
    } else {
        Write-Host "  [*] Exists: $file" -ForegroundColor Yellow
    }
}

# Check for .env file
Write-Host "`nChecking environment configuration..." -ForegroundColor Green
if (!(Test-Path ".env")) {
    Write-Host "  [!] .env file not found" -ForegroundColor Red
    Write-Host "  [*] Creating .env from .env.example..." -ForegroundColor Yellow
    
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "  [+] Created .env from template" -ForegroundColor Green
        Write-Host ""
        Write-Host "  *** IMPORTANT: Edit .env and add your API keys ***" -ForegroundColor Red -BackgroundColor Yellow
        Write-Host "  *** NEVER commit .env to version control ***" -ForegroundColor Red -BackgroundColor Yellow
    } else {
        Write-Host "  [!] .env.example not found. Cannot create .env" -ForegroundColor Red
    }
} else {
    Write-Host "  [*] .env exists" -ForegroundColor Green
}

# Create README placeholders in empty directories
$readmes = @{
    "core/production_inputs/README.md" = @"
# Production Inputs

This directory contains generated content files ready for production.

Files in this directory are created by:
- BATTLE_CTR_INTEGRATION.py (direct generation)
- ENQUEUE_FOR_PRODUCTION.py (from submissions)

## Contents

Episode input files follow the naming convention:
- episode_XXXXX_script.txt
- episode_XXXXX_metadata.json

## Usage

1. Review all files before production use
2. Verify compliance with platform TOS
3. Implement uploader separately (not included)
4. Maintain audit trail of all content

## Safety

- Do NOT commit large media files to git
- Use .gitignore for generated content
- Keep proofs of all content generation
"@
    "submissions/README.md" = @"
# Submissions Directory

This directory stores submission JSON files from LLM contributors.

## File Format

Submissions are JSON files validated against submission_schema.json.

## Processing

1. Files placed here by SUBMISSION_RECEIVER.py
2. Validated against schema
3. Queued in battle_data.json as pending
4. Processed by ENQUEUE_FOR_PRODUCTION.py
5. Moved to production_inputs when ready

## Safety

- All submissions must be validated
- Review content before production use
- Maintain audit trail
"@
    "examples/README.md" = @"
# Example Submissions

This directory contains example submission files demonstrating the correct format.

See:
- ChatGPT_submission_30000-30004.json
- GROK_submission_60000-60004.json

Use these as templates for creating new submissions.
"@
}

foreach ($readme in $readmes.Keys) {
    if (!(Test-Path $readme)) {
        $readmes[$readme] | Out-File -FilePath $readme -Encoding UTF8
        Write-Host "  [+] Created: $readme" -ForegroundColor Green
    }
}

# Summary
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "Bootstrap Complete!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Edit .env and add your API keys (REQUIRED)" -ForegroundColor White
Write-Host "  2. Review README_BATTLE.md for usage instructions" -ForegroundColor White
Write-Host "  3. Test with: python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --videos 1 --dry-run" -ForegroundColor White
Write-Host "  4. Implement generator scripts in 1_Script_Engine/" -ForegroundColor White
Write-Host "  5. Implement uploader script separately (with OAuth)" -ForegroundColor White

Write-Host "`nSafety Reminders:" -ForegroundColor Red
Write-Host "  - NEVER commit .env to git" -ForegroundColor White
Write-Host "  - Review all content before publishing" -ForegroundColor White
Write-Host "  - These scripts do NOT upload automatically" -ForegroundColor White
Write-Host "  - Implement OAuth uploader separately" -ForegroundColor White

Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
