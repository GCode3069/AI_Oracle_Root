# ============================================================================
# MOBILE COMMAND WATCHER - Works with iOS Shortcuts + iCloud
# ============================================================================

param(
    [string]$WatchFolder = "F:\AI_Oracle_Root\scarify\mobile_commands"
)

Write-Host ""
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host "#                                                                             #" -ForegroundColor Cyan
Write-Host "#           📱 MOBILE COMMAND WATCHER - iOS SHORTCUTS 📱                      #" -ForegroundColor Cyan
Write-Host "#                                                                             #" -ForegroundColor Cyan
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""
Write-Host "Watching folder: $WatchFolder" -ForegroundColor White
Write-Host ""
Write-Host "SETUP:" -ForegroundColor Yellow
Write-Host "  1. Sync this folder with iCloud Drive or Dropbox" -ForegroundColor White
Write-Host "  2. Create iOS Shortcut that writes command files here" -ForegroundColor White
Write-Host "  3. This watcher will execute commands automatically`n" -ForegroundColor White
Write-Host "COMMAND FORMAT (in .cmd.txt file):" -ForegroundColor Yellow
Write-Host "  GENERATE 10 ChatGPT" -ForegroundColor Cyan
Write-Host "  GENERATE 20 Cursor" -ForegroundColor Cyan
Write-Host "  GENERATE 5 Grok`n" -ForegroundColor Cyan
Write-Host "###############################################################################" -ForegroundColor Cyan
Write-Host ""

# Create folder if doesn't exist
if (-not (Test-Path $WatchFolder)) {
    New-Item -Path $WatchFolder -ItemType Directory -Force | Out-Null
    Write-Host "✅ Created watch folder`n" -ForegroundColor Green
}

Write-Host "🔄 Watching for commands (Ctrl+C to stop)...`n" -ForegroundColor Green

$iteration = 0
while ($true) {
    $iteration++
    
    # Check for command files
    $commands = Get-ChildItem "$WatchFolder\*.cmd.txt" -ErrorAction SilentlyContinue
    
    if ($commands) {
        foreach ($cmd in $commands) {
            $content = Get-Content $cmd.FullName -Raw
            $timestamp = Get-Date -Format "HH:mm:ss"
            
            Write-Host "[$timestamp] 📱 MOBILE COMMAND RECEIVED" -ForegroundColor Cyan
            Write-Host "  File: $($cmd.Name)" -ForegroundColor White
            Write-Host "  Content: $content" -ForegroundColor Gray
            
            # Parse command: GENERATE [COUNT] [STYLE]
            if ($content -match "GENERATE\s+(\d+)\s+(\w+)") {
                $count = $Matches[1]
                $style = $Matches[2].ToLower()
                
                Write-Host "  → Generating $count videos ($style style)" -ForegroundColor Green
                Write-Host ""
                
                # Map style to command
                $styleMap = @{
                    'chatgpt' = 'chatgpt_poetic'
                    'cursor' = 'cursor_consistent'
                    'grok' = 'grok_controversial'
                    'opus' = 'opus_sophisticated'
                }
                
                $fullStyle = $styleMap[$style]
                
                # Execute generation
                try {
                    Set-Location F:\AI_Oracle_Root\scarify
                    $result = python BATCH_MIXED_STRATEGY.py $count --start 80000
                    Write-Host "  ✅ Generation started`n" -ForegroundColor Green
                } catch {
                    Write-Host "  ❌ Error: $_`n" -ForegroundColor Red
                }
            }
            elseif ($content -match "IDEA:\s*(.+)") {
                $idea = $Matches[1]
                Write-Host "  💡 Idea saved: $idea" -ForegroundColor Yellow
                
                # Save to ideas file
                $ideasFile = "F:\AI_Oracle_Root\scarify\mobile_ideas.json"
                $ideas = @()
                if (Test-Path $ideasFile) {
                    $ideas = Get-Content $ideasFile -Raw | ConvertFrom-Json
                }
                $ideas += @{
                    idea = $idea
                    timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
                }
                $ideas | ConvertTo-Json | Set-Content $ideasFile
                Write-Host "  ✅ Saved to ideas queue`n" -ForegroundColor Green
            }
            else {
                Write-Host "  ❌ Unknown command format`n" -ForegroundColor Red
            }
            
            # Archive command (don't delete, for logging)
            $archiveName = "processed_$($cmd.Name)"
            Move-Item $cmd.FullName "$WatchFolder\$archiveName" -Force
        }
    }
    
    # Show heartbeat every 10 iterations (100 seconds)
    if ($iteration % 10 -eq 0) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] 💚 Watcher active (checked $iteration times)" -ForegroundColor DarkGreen
    }
    
    Start-Sleep -Seconds 10
}


