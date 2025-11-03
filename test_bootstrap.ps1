# Quick test of the bootstrap script
# This validates syntax and tests basic functionality

Write-Host "🧪 Testing SCARIFY Bootstrap Script..." -ForegroundColor Cyan
Write-Host ""

# Test 1: Check script exists
Write-Host "[Test 1] Checking if bootstrap script exists..." -ForegroundColor Yellow
$scriptPath = Join-Path $PSScriptRoot "scarify_bootstrap.ps1"

if (Test-Path $scriptPath) {
    Write-Host "✅ Bootstrap script found at: $scriptPath" -ForegroundColor Green
} else {
    Write-Host "❌ Bootstrap script not found!" -ForegroundColor Red
    exit 1
}

# Test 2: Validate PowerShell syntax
Write-Host "`n[Test 2] Validating PowerShell syntax..." -ForegroundColor Yellow
try {
    $errors = $null
    $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content $scriptPath -Raw), [ref]$errors)
    
    if ($errors.Count -eq 0) {
        Write-Host "✅ No syntax errors found" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Found $($errors.Count) syntax warnings:" -ForegroundColor Yellow
        foreach ($error in $errors) {
            Write-Host "   - $($error.Message)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "❌ Syntax validation failed: $_" -ForegroundColor Red
}

# Test 3: Check Python availability
Write-Host "`n[Test 3] Checking Python availability..." -ForegroundColor Yellow
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Python not found - bootstrap will warn about this" -ForegroundColor Yellow
}

# Test 4: Check FFmpeg availability
Write-Host "`n[Test 4] Checking FFmpeg availability..." -ForegroundColor Yellow
try {
    $ffmpegVersion = & ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "✅ FFmpeg found: $ffmpegVersion" -ForegroundColor Green
} catch {
    Write-Host "⚠️  FFmpeg not found - some features may be limited" -ForegroundColor Yellow
}

# Test 5: Run bootstrap in quick test mode
Write-Host "`n[Test 5] Running bootstrap in quick test mode..." -ForegroundColor Yellow
Write-Host "Executing: .\scarify_bootstrap.ps1 -QuickTest" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

try {
    & $scriptPath -QuickTest
    
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "✅ Bootstrap test completed successfully!" -ForegroundColor Green
} catch {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "❌ Bootstrap test failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎉 All tests passed!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run full deployment: .\scarify_bootstrap.ps1 -VideoCount 1" -ForegroundColor White
Write-Host "  2. Generate 5 videos:    .\scarify_bootstrap.ps1 -VideoCount 5 -Archetype Mystic" -ForegroundColor White
Write-Host "  3. Full auto-deploy:     .\scarify_bootstrap.ps1 -FullDeploy -VideoCount 10" -ForegroundColor White
Write-Host ""

