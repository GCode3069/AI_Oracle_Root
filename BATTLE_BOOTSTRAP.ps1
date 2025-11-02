# LLM Battle Royale Bootstrap Script
# Creates placeholder directories and files for Battle Royale system
# Run this script once during initial setup

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan
Write-Host "LLM BATTLE ROYALE BOOTSTRAP" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 58) -ForegroundColor Cyan

# Create necessary directories
$directories = @(
    "submissions",
    "core",
    "core/production_inputs",
    "examples",
    "1_Script_Engine"
)

Write-Host "`nCreating directories..." -ForegroundColor Cyan
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  - Exists: $dir" -ForegroundColor Gray
    }
}

# Create placeholder generator scripts
Write-Host "`nCreating placeholder generator scripts..." -ForegroundColor Cyan
$generators = @(
    "chatgpt_generator.py",
    "claude_generator.py",
    "gemini_generator.py",
    "grok_generator.py",
    "llama_generator.py"
)

$placeholderContent = @"
#!/usr/bin/env python3
'''
Placeholder generator script.
Implement actual video generation logic here.
'''
import sys
print('TODO: Implement generator script')
sys.exit(1)
"@

foreach ($gen in $generators) {
    $genPath = "1_Script_Engine/$gen"
    if (-not (Test-Path $genPath)) {
        Set-Content -Path $genPath -Value $placeholderContent
        Write-Host "  ✓ Created placeholder: $genPath" -ForegroundColor Green
    } else {
        Write-Host "  - Exists: $genPath" -ForegroundColor Gray
    }
}

# Check for .env file
Write-Host "`nChecking environment configuration..." -ForegroundColor Cyan
if (-not (Test-Path ".env")) {
    Write-Host "  ⚠️  .env file not found" -ForegroundColor Yellow
    Write-Host "  ℹ️  Copy .env.example to .env and populate with your API keys" -ForegroundColor Cyan
    Write-Host "     Example: cp .env.example .env" -ForegroundColor Gray
} else {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
}

# Check for battle_data.json
if (Test-Path "battle_data.json") {
    Write-Host "  ✓ battle_data.json exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  battle_data.json not found (will be created on first run)" -ForegroundColor Yellow
}

# Instructions
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "NEXT STEPS" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create .env file from template:" -ForegroundColor White
Write-Host "   Copy-Item .env.example .env" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Edit .env and add your API keys:" -ForegroundColor White
Write-Host "   - ELEVENLABS_API_KEY" -ForegroundColor Gray
Write-Host "   - PEXELS_API_KEY" -ForegroundColor Gray
Write-Host "   - RUNWAY_API_KEY (optional)" -ForegroundColor Gray
Write-Host "   - POLLO_API_KEY (optional)" -ForegroundColor Gray
Write-Host "   - STABILITY_API_KEY (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. IMPORTANT: Never commit .env to version control!" -ForegroundColor Red
Write-Host "   Verify .env is in .gitignore" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Implement generator scripts in 1_Script_Engine/" -ForegroundColor White
Write-Host ""
Write-Host "5. Test with dry run:" -ForegroundColor White
Write-Host "   python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --dry-run" -ForegroundColor Gray
Write-Host ""
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host "Bootstrap complete!" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan
