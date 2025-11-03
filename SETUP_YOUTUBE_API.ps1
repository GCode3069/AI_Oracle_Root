# ═══════════════════════════════════════════════════════════════════════════
# YOUTUBE API SETUP - ONE-TIME CONFIGURATION
# Sets up authentication to auto-upload videos to your channel
# ═══════════════════════════════════════════════════════════════════════════

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "📺 YOUTUBE API SETUP - AUTO-UPLOAD CONFIGURATION 📺" -ForegroundColor Yellow
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

Write-Host "🎯 STEP-BY-STEP YOUTUBE API SETUP:" -ForegroundColor Cyan
Write-Host ""

Write-Host "1️⃣  GO TO GOOGLE CLOUD CONSOLE" -ForegroundColor Green
Write-Host "   https://console.cloud.google.com/" -ForegroundColor White
Write-Host "   - Click 'Select a project' → 'New Project'" -ForegroundColor Gray
Write-Host "   - Name: 'Abraham Studio'" -ForegroundColor Gray
Write-Host "   - Click 'Create'" -ForegroundColor Gray
Write-Host ""

Write-Host "2️⃣  ENABLE YOUTUBE DATA API" -ForegroundColor Green  
Write-Host "   - Click '≡' menu → 'APIs & Services' → 'Library'" -ForegroundColor White
Write-Host "   - Search: 'YouTube Data API v3'" -ForegroundColor Gray
Write-Host "   - Click on it → Click 'ENABLE'" -ForegroundColor Gray
Write-Host ""

Write-Host "3️⃣  CREATE OAUTH CREDENTIALS" -ForegroundColor Green
Write-Host "   - Click 'CREATE CREDENTIALS' → 'OAuth client ID'" -ForegroundColor White
Write-Host "   - If prompted, configure OAuth consent screen:" -ForegroundColor Gray
Write-Host "     • User Type: External" -ForegroundColor Gray
Write-Host "     • App name: Abraham Studio" -ForegroundColor Gray
Write-Host "     • User support email: your email" -ForegroundColor Gray
Write-Host "     • Developer email: your email" -ForegroundColor Gray
Write-Host "     • Click 'Save and Continue'" -ForegroundColor Gray
Write-Host "   - Application type: 'Desktop app'" -ForegroundColor White
Write-Host "   - Name: 'Abraham Desktop'" -ForegroundColor Gray
Write-Host "   - Click 'CREATE'" -ForegroundColor Gray
Write-Host ""

Write-Host "4️⃣  DOWNLOAD CREDENTIALS" -ForegroundColor Green
Write-Host "   - Click 'DOWNLOAD JSON'" -ForegroundColor White
Write-Host "   - Rename file to: client_secrets.json" -ForegroundColor Gray
Write-Host "   - Move file to: $ROOT\client_secrets.json" -ForegroundColor Gray
Write-Host ""

Write-Host "5️⃣  RUN THE SCRIPT" -ForegroundColor Green
Write-Host "   cd $ROOT" -ForegroundColor White
Write-Host "   python abe_animated_youtube.py 10" -ForegroundColor White
Write-Host ""

Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# Check if client_secrets.json exists
$clientSecrets = Join-Path $ROOT "client_secrets.json"
if (Test-Path $clientSecrets) {
    Write-Host "✅ client_secrets.json found!" -ForegroundColor Green
    Write-Host "🚀 Ready to run! Execute:" -ForegroundColor Yellow
    Write-Host "   python abe_animated_youtube.py 50" -ForegroundColor White
    Write-Host ""
    
    $run = Read-Host "Run now? (Y/N)"
    if ($run -eq "Y" -or $run -eq "y") {
        Set-Location $ROOT
        python abe_animated_youtube.py 10
    }
} else {
    Write-Host "⚠️  client_secrets.json NOT found" -ForegroundColor Yellow
    Write-Host "📋 Follow steps above to download it" -ForegroundColor Cyan
    Write-Host ""
    
    $open = Read-Host "Open Google Cloud Console? (Y/N)"
    if ($open -eq "Y" -or $open -eq "y") {
        Start-Process "https://console.cloud.google.com/"
    }
}

Write-Host ""
Write-Host "💡 TIPS:" -ForegroundColor Yellow
Write-Host "   - First run opens browser for authentication" -ForegroundColor Gray
Write-Host "   - Grant permissions to upload videos" -ForegroundColor Gray
Write-Host "   - Token saves for future uploads" -ForegroundColor Gray
Write-Host "   - Videos auto-upload to your channel" -ForegroundColor Gray
Write-Host ""
