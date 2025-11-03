# ============================================================================
# DROPBOX MOBILE CONTROL - NO SERVER, NO BOT, NO COMPLEXITY
# ============================================================================

Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host "#                                                                             #" -ForegroundColor Green
Write-Host "#         📁 DROPBOX MOBILE CONTROL - SIMPLEST METHOD 📁                     #" -ForegroundColor Green
Write-Host "#                                                                             #" -ForegroundColor Green
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""
Write-Host "NO SERVER. NO BOT. NO NETWORK ISSUES. JUST FILE SYNC." -ForegroundColor Yellow
Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""

# Create mobile_commands folder
$commandsFolder = "F:\AI_Oracle_Root\scarify\mobile_commands"
if (-not (Test-Path $commandsFolder)) {
    New-Item -Path $commandsFolder -ItemType Directory -Force | Out-Null
}

Write-Host "[1/2] Command folder created: $commandsFolder`n" -ForegroundColor Green

# Create example command files
$exampleCmd = @"
GENERATE 5 ChatGPT
"@

$exampleIdea = @"
IDEA: Make videos about crypto crash with aggressive CTR hooks
"@

$exampleCmd | Out-File "$commandsFolder\_EXAMPLE_generate.cmd.txt" -Encoding UTF8
$exampleIdea | Out-File "$commandsFolder\_EXAMPLE_idea.cmd.txt" -Encoding UTF8

Write-Host "[2/2] Example files created`n" -ForegroundColor Green

Write-Host "###############################################################################" -ForegroundColor Green
Write-Host "#                                                                             #" -ForegroundColor Green
Write-Host "#                         ✅ SETUP COMPLETE ✅                                #" -ForegroundColor Green
Write-Host "#                                                                             #" -ForegroundColor Green
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""
Write-Host "FOLDER: $commandsFolder`n" -ForegroundColor Cyan
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  OPTION A: Dropbox Sync (Recommended)" -ForegroundColor Cyan
Write-Host "    1. Install Dropbox on PC (if not installed)" -ForegroundColor White
Write-Host "    2. Move folder to Dropbox:" -ForegroundColor White
Write-Host "       → Drag 'mobile_commands' to Dropbox folder" -ForegroundColor Gray
Write-Host "    3. Install Dropbox on iPhone" -ForegroundColor White
Write-Host "    4. Navigate to folder on iPhone" -ForegroundColor White
Write-Host "    5. Create file with command, sync happens automatically`n" -ForegroundColor White
Write-Host "  OPTION B: OneDrive/iCloud (Alternative)" -ForegroundColor Cyan
Write-Host "    → Same process, just use OneDrive or iCloud instead`n" -ForegroundColor White
Write-Host "  OPTION C: Manual Transfer (Works Right Now)" -ForegroundColor Cyan
Write-Host "    → Use iPhone Notes, copy command" -ForegroundColor White
Write-Host "    → Text or email yourself" -ForegroundColor White
Write-Host "    → Paste into text file in this folder`n" -ForegroundColor White
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""
Write-Host "TO START WATCHER:" -ForegroundColor Yellow
Write-Host "  .\WATCH_MOBILE_COMMANDS.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "WATCHER WILL:" -ForegroundColor Yellow
Write-Host "  → Check folder every 10 seconds" -ForegroundColor White
Write-Host "  → Execute any .cmd.txt files" -ForegroundColor White
Write-Host "  → Generate videos automatically" -ForegroundColor White
Write-Host "  → Move processed files to archive`n" -ForegroundColor White
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""
Write-Host "COMMAND FORMAT (in .cmd.txt file):" -ForegroundColor Yellow
Write-Host ""
Write-Host "  GENERATE 10 ChatGPT" -ForegroundColor Cyan
Write-Host "  GENERATE 20 Cursor" -ForegroundColor Cyan
Write-Host "  IDEA: Your idea text here" -ForegroundColor Cyan
Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Green
Write-Host ""
Write-Host "Ready! Start watcher and create command files from iPhone." -ForegroundColor Yellow
Write-Host ""


