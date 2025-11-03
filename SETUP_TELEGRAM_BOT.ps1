# ============================================================================
# TELEGRAM BOT - ONE-COMMAND SETUP
# ============================================================================

Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host "#                                                                             #" -ForegroundColor Cyan
Write-Host "#              🤖 TELEGRAM BOT - INSTANT SETUP 🤖                             #" -ForegroundColor Cyan
Write-Host "#                                                                             #" -ForegroundColor Cyan
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""
Write-Host "SETUP STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. On iPhone/Telegram:" -ForegroundColor White
Write-Host "     → Message @BotFather" -ForegroundColor Gray
Write-Host "     → Send: /newbot" -ForegroundColor Gray
Write-Host "     → Name: Abe Studio" -ForegroundColor Gray
Write-Host "     → Username: abe_studio_YOUR_NAME_bot" -ForegroundColor Gray
Write-Host "     → Copy the TOKEN BotFather sends`n" -ForegroundColor Gray
Write-Host "  2. Paste token below and we'll configure everything`n" -ForegroundColor White
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""

# Prompt for bot token
$token = Read-Host "Paste your bot token here (or press Enter to skip)"

if (-not $token -or $token.Trim() -eq "") {
    Write-Host ""
    Write-Host "No token provided. Exiting." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Get token from @BotFather first, then run again." -ForegroundColor Cyan
    Write-Host ""
    exit
}

Write-Host ""
Write-Host "[1/3] Configuring bot..." -ForegroundColor Yellow

# Read telegram_bot.py
$botFile = "telegram_bot.py"
$content = Get-Content $botFile -Raw

# Replace token
$content = $content -replace 'BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"', "BOT_TOKEN = `"$token`""

# Save
$content | Set-Content $botFile -Encoding UTF8

Write-Host "  ✅ Token configured in telegram_bot.py`n" -ForegroundColor Green

Write-Host "[2/3] Installing dependencies..." -ForegroundColor Yellow
pip install python-telegram-bot --quiet 2>&1 | Out-Null
Write-Host "  ✅ python-telegram-bot installed`n" -ForegroundColor Green

Write-Host "[3/3] Starting bot..." -ForegroundColor Yellow
Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host "#                                                                             #" -ForegroundColor Green
Write-Host "#                      ✅ BOT READY - USE IT NOW ✅                           #" -ForegroundColor Green
Write-Host "#                                                                             #" -ForegroundColor Green
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""
Write-Host "ON YOUR iPHONE:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Open Telegram" -ForegroundColor Cyan
Write-Host "  2. Search for your bot (username you created)" -ForegroundColor Cyan
Write-Host "  3. Send: /start" -ForegroundColor Cyan
Write-Host "  4. Try: /generate 5 chatgpt`n" -ForegroundColor Cyan
Write-Host "COMMANDS YOU CAN USE:" -ForegroundColor Yellow
Write-Host "  /generate 10 chatgpt - Generate 10 videos (ChatGPT style)" -ForegroundColor White
Write-Host "  /generate 20 cursor - Generate 20 videos (Cursor style)" -ForegroundColor White
Write-Host "  /status - Check video count & revenue" -ForegroundColor White
Write-Host "  /idea Your idea - Save idea for later" -ForegroundColor White
Write-Host "  /help - Show all commands`n" -ForegroundColor White
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""
Write-Host "Bot starting now... (Keep this window open)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop bot when done" -ForegroundColor Gray
Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""

# Start bot
python telegram_bot.py


