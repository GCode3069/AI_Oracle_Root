param([int]$Count = 50)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"

Write-Host ""
Write-Host "🔥 ABRAHAM HORROR - SCARY EDITION" -ForegroundColor Red
Write-Host ("=" * 70)
Write-Host ""

# Create dirs
$dirs = @("audio", "videos", "youtube_ready", "temp")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null }
}

# Install dependencies
pip install --quiet requests beautifulsoup4 lxml 2>&1 | Out-Null

# Run existing Python script
Write-Host "🚀 GENERATING $Count SCARY VIDEOS..." -ForegroundColor Yellow
Write-Host ""
cd $ROOT
python abraham.py $Count

Write-Host ""
Write-Host "✅ DONE!" -ForegroundColor Green
Start-Process explorer.exe -ArgumentList "$ROOT\youtube_ready"

