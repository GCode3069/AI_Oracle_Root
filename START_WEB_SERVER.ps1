# Start ABRAHAM STUDIO Web Server for iPhone Access
Write-Host ""
Write-Host "="*70 -ForegroundColor Cyan
Write-Host "ABRAHAM STUDIO - WEB SERVER" -ForegroundColor Yellow
Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""

# Check if Flask is installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import flask" 2>$null
    Write-Host "  [OK] Flask installed" -ForegroundColor Green
} catch {
    Write-Host "  [INSTALL] Installing Flask..." -ForegroundColor Yellow
    pip install flask flask-cors -q
    Write-Host "  [OK] Flask installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting web server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "MOBILE ACCESS:" -ForegroundColor Cyan
Write-Host "  http://[YOUR_IP]:5000" -ForegroundColor White
Write-Host ""
Write-Host "Finding your IP address..." -ForegroundColor Yellow

# Get IP address
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*" -and $_.IPAddress -notlike "169.254.*"} | Select-Object -First 1).IPAddress

if ($ip) {
    Write-Host "  [OK] Your IP: $ip" -ForegroundColor Green
    Write-Host ""
    Write-Host "iPhone Instructions:" -ForegroundColor Cyan
    Write-Host "  1. Make sure iPhone is on same WiFi network" -ForegroundColor White
    Write-Host "  2. Open Safari/Chrome on iPhone" -ForegroundColor White
    Write-Host "  3. Go to: http://$ip`:5000" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "  [WARN] Could not detect IP - use 'ipconfig' to find it" -ForegroundColor Yellow
}

Write-Host "="*70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop server" -ForegroundColor Yellow
Write-Host ""

# Start server
python STUDIO_WEB_SERVER.py







