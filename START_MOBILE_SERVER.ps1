# ============================================================================
# START MOBILE SERVER - Access from iPhone
# ============================================================================

Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host "#                                                                             #" -ForegroundColor Cyan
Write-Host "#           📱 MOBILE GENERATOR SERVER - iPHONE ACCESS 📱                     #" -ForegroundColor Cyan
Write-Host "#                                                                             #" -ForegroundColor Cyan
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""

# Get PC IP address
$ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"} | Select-Object -First 1).IPAddress

Write-Host "SETUP INSTRUCTIONS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Server will start on this PC" -ForegroundColor White
Write-Host "   IP Address: $ipAddress" -ForegroundColor Cyan
Write-Host "   Port: 5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. On your iPhone:" -ForegroundColor White
Write-Host "   → Open Safari" -ForegroundColor Gray
Write-Host "   → Go to: http://${ipAddress}:5000" -ForegroundColor Cyan
Write-Host "   → Bookmark it for quick access" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Features:" -ForegroundColor White
Write-Host "   ✅ Generate videos remotely" -ForegroundColor Green
Write-Host "   ✅ Capture ideas with voice-to-text" -ForegroundColor Green
Write-Host "   ✅ Select style, CTR level, batch count" -ForegroundColor Green
Write-Host "   ✅ Monitor stats in real-time" -ForegroundColor Green
Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
pip install flask flask-cors --quiet

Write-Host ""
Write-Host "Starting server..." -ForegroundColor Green
Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host "#  SERVER INFO:                                                               #" -ForegroundColor Cyan
Write-Host "#  PC IP: $ipAddress                                                          " -ForegroundColor Cyan
Write-Host "#  Port: 5000                                                                 #" -ForegroundColor Cyan
Write-Host "#  iPhone URL: http://${ipAddress}:5000                                       " -ForegroundColor Cyan
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""

# Copy HTML to static folder
$staticDir = "F:\AI_Oracle_Root\scarify\static"
New-Item -Path $staticDir -ItemType Directory -Force | Out-Null
Copy-Item "MOBILE_GENERATOR.html" -Destination "$staticDir\MOBILE_GENERATOR.html" -Force

# Start server
Set-Location F:\AI_Oracle_Root\scarify
python mobile_backend.py


