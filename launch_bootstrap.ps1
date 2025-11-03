# SCARIFY Bootstrap Launcher - Interactive Menu
# Simple menu interface for the bootstrap script

function Show-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "    🔥 SCARIFY BOOTSTRAP LAUNCHER 🔥" -ForegroundColor Red
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  Select an option:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [1] Quick Test (Setup Only - No Videos)" -ForegroundColor White
    Write-Host "  [2] Generate 1 Test Video" -ForegroundColor White
    Write-Host "  [3] Generate 5 Videos" -ForegroundColor White
    Write-Host "  [4] Generate 10 Videos" -ForegroundColor White
    Write-Host "  [5] Full Deployment (Setup + 5 Videos)" -ForegroundColor White
    Write-Host "  [6] Custom Configuration" -ForegroundColor White
    Write-Host "  [0] Exit" -ForegroundColor Gray
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
}

function Show-ArchetypeMenu {
    Write-Host ""
    Write-Host "Select Archetype:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [1] Mystic (Spiritual, Ethereal)" -ForegroundColor Magenta
    Write-Host "  [2] Rebel (Revolutionary, Gritty)" -ForegroundColor Red
    Write-Host "  [3] Sage (Wisdom, Knowledge)" -ForegroundColor Blue
    Write-Host "  [4] Hero (Inspirational, Courageous)" -ForegroundColor Yellow
    Write-Host "  [5] Guardian (Protective, Strong)" -ForegroundColor Green
    Write-Host ""
    
    $choice = Read-Host "Enter choice (1-5)"
    
    switch ($choice) {
        "1" { return "Mystic" }
        "2" { return "Rebel" }
        "3" { return "Sage" }
        "4" { return "Hero" }
        "5" { return "Guardian" }
        default { return "Mystic" }
    }
}

function Run-Bootstrap {
    param(
        [int]$VideoCount = 0,
        [string]$Archetype = "Mystic",
        [switch]$QuickTest,
        [switch]$FullDeploy
    )
    
    $scriptPath = Join-Path $PSScriptRoot "scarify_bootstrap.ps1"
    
    if (-not (Test-Path $scriptPath)) {
        Write-Host ""
        Write-Host "❌ Error: scarify_bootstrap.ps1 not found!" -ForegroundColor Red
        Write-Host "   Expected location: $scriptPath" -ForegroundColor Gray
        Write-Host ""
        Read-Host "Press Enter to exit"
        return
    }
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "    🚀 LAUNCHING BOOTSTRAP" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    $args = @()
    
    if ($QuickTest) {
        $args += "-QuickTest"
        Write-Host "Mode: Quick Test (No Videos)" -ForegroundColor Yellow
    } else {
        if ($VideoCount -gt 0) {
            $args += "-VideoCount", $VideoCount
            Write-Host "Video Count: $VideoCount" -ForegroundColor White
        }
        $args += "-Archetype", $Archetype
        Write-Host "Archetype: $Archetype" -ForegroundColor Magenta
    }
    
    if ($FullDeploy) {
        $args += "-FullDeploy"
        Write-Host "Full Deploy: Enabled" -ForegroundColor Green
    }
    
    Write-Host ""
    Write-Host "Press Ctrl+C to cancel, or" -ForegroundColor Gray
    Read-Host "Press Enter to continue"
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    try {
        & $scriptPath @args
        
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "    ✅ BOOTSTRAP COMPLETED" -ForegroundColor Green
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
    } catch {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "    ❌ BOOTSTRAP FAILED" -ForegroundColor Red
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Error: $_" -ForegroundColor Red
        Write-Host ""
    }
    
    Read-Host "Press Enter to return to menu"
}

# Main loop
do {
    Show-Menu
    $choice = Read-Host "Enter your choice (0-6)"
    
    switch ($choice) {
        "1" {
            Run-Bootstrap -QuickTest
        }
        "2" {
            $archetype = Show-ArchetypeMenu
            Run-Bootstrap -VideoCount 1 -Archetype $archetype
        }
        "3" {
            $archetype = Show-ArchetypeMenu
            Run-Bootstrap -VideoCount 5 -Archetype $archetype
        }
        "4" {
            $archetype = Show-ArchetypeMenu
            Run-Bootstrap -VideoCount 10 -Archetype $archetype
        }
        "5" {
            $archetype = Show-ArchetypeMenu
            Run-Bootstrap -VideoCount 5 -Archetype $archetype -FullDeploy
        }
        "6" {
            Write-Host ""
            Write-Host "Custom Configuration" -ForegroundColor Yellow
            Write-Host ""
            
            $archetype = Show-ArchetypeMenu
            
            Write-Host ""
            $count = Read-Host "Enter number of videos to generate (1-100)"
            try {
                $count = [int]$count
                if ($count -lt 1) { $count = 1 }
                if ($count -gt 100) { $count = 100 }
            } catch {
                $count = 1
            }
            
            Write-Host ""
            $fullDeploy = Read-Host "Enable full deploy? (y/n)"
            
            if ($fullDeploy -eq 'y' -or $fullDeploy -eq 'Y') {
                Run-Bootstrap -VideoCount $count -Archetype $archetype -FullDeploy
            } else {
                Run-Bootstrap -VideoCount $count -Archetype $archetype
            }
        }
        "0" {
            Write-Host ""
            Write-Host "Goodbye! 👋" -ForegroundColor Cyan
            Write-Host ""
            break
        }
        default {
            Write-Host ""
            Write-Host "❌ Invalid choice. Please select 0-6." -ForegroundColor Red
            Start-Sleep -Seconds 2
        }
    }
} while ($choice -ne "0")

