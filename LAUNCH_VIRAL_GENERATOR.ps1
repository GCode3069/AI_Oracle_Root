# ═══════════════════════════════════════════════════════════════════════════
# VIRAL OPTIMIZED GENERATOR - LAUNCHER
# Cross-platform viral content generator
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 5, [switch]$YouTubeOnly = $false)

$ErrorActionPreference = "Stop"
$ROOT = "F:\AI_Oracle_Root\scarify"

Write-Host ""
Write-Host "🔥 VIRAL OPTIMIZED GENERATOR - CROSS PLATFORM" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""
Write-Host "Features:"
Write-Host "  ✅ Algorithm-optimized titles & descriptions"
Write-Host "  ✅ Viral hooks and CTAs"
Write-Host "  ✅ YouTube + TikTok + Instagram ready"
Write-Host "  ✅ Max Headroom TV static effects"
Write-Host "  ✅ Real headlines + fear-based targeting"
Write-Host ""

# Check Python file
$pyFile = Join-Path $ROOT "VIRAL_OPTIMIZED_GENERATOR.py"
if (-not (Test-Path $pyFile)) {
    Write-Host "❌ VIRAL_OPTIMIZED_GENERATOR.py not found!" -ForegroundColor Red
    Write-Host "Expected: $pyFile" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found generator script" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Generating $Count viral-optimized video(s)..." -ForegroundColor Yellow
Write-Host ""

Set-Location $ROOT

if ($YouTubeOnly) {
    python VIRAL_OPTIMIZED_GENERATOR.py $Count
} else {
    python VIRAL_OPTIMIZED_GENERATOR.py $Count
}

Write-Host ""
Write-Host "✅ COMPLETE!" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Output locations:"
Write-Host "  • YouTube: abraham_horror\youtube_ready\"
Write-Host "  • TikTok:  abraham_horror\tiktok_ready\"
Write-Host "  • Instagram: abraham_horror\instagram_ready\"
Write-Host ""

# Open output folders
Start-Sleep -Seconds 2
Start-Process explorer.exe -ArgumentList (Join-Path $ROOT "abraham_horror\youtube_ready")







