# Launch ABRAHAM STUDIO Desktop App
Write-Host ""
Write-Host "Launching ABRAHAM STUDIO..." -ForegroundColor Cyan
Write-Host ""

$studioFile = "ABRAHAM_STUDIO (1).pyw"

if (Test-Path $studioFile) {
    # Launch with pythonw (no console window for GUI apps)
    Start-Process pythonw.exe -ArgumentList "`"$studioFile`"" -NoNewWindow
    
    Write-Host "[OK] ABRAHAM STUDIO launched!" -ForegroundColor Green
    Write-Host ""
    Write-Host "The desktop app window should open shortly." -ForegroundColor Yellow
} else {
    Write-Host "[ERROR] Studio file not found: $studioFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected location:" -ForegroundColor Yellow
    Write-Host "  $(Resolve-Path .)\$studioFile" -ForegroundColor White
}

