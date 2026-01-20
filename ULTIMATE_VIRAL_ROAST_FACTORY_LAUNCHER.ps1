# ULTIMATE VIRAL ROAST FACTORY - LAUNCHER
# ========================================
# This is THE system that combines everything we built

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "    ULTIMATE VIRAL ROAST FACTORY" -ForegroundColor Yellow
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Combines EVERYTHING:" -ForegroundColor Green
Write-Host "  [+] Story-based visual storytelling (proven to work)"
Write-Host "  [+] GOAT comedy spirits (Carlin, Pryor, Chappelle, Burr, Patrice)"
Write-Host "  [+] Jimi Suave voice cloning"
Write-Host "  [+] Neuro-psychological optimization"
Write-Host "  [+] MCP agent coordination"
Write-Host "  [+] Multi-platform posting via Postiz"
Write-Host "  [+] Analytics tracking"
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Menu
Write-Host "What do you want to do?" -ForegroundColor Yellow
Write-Host ""
Write-Host "BASIC OPTIONS:" -ForegroundColor Cyan
Write-Host "1. Generate ONE viral roast (random GOAT)"
Write-Host "2. Generate ONE viral roast (choose GOAT)"
Write-Host "3. Generate SERIES of roasts (5 videos, all GOATs)"
Write-Host ""
Write-Host "GPU CLOUD OPTIONS:" -ForegroundColor Green
Write-Host "4. Generate with HIGH priority (HAMi local - fastest, free)"
Write-Host "5. Generate with MEDIUM priority (SkyPilot - auto-cheapest)"
Write-Host "6. Generate with LOW priority (Akash - cheapest cloud)"
Write-Host ""
Write-Host "ADVANCED:" -ForegroundColor Yellow
Write-Host "7. Generate and UPLOAD to platforms"
Write-Host "8. Check system status + GPU providers"
Write-Host "9. GPU Setup Guide"
Write-Host "0. Exit"
Write-Host ""

$choice = Read-Host "Enter choice (0-9)"

switch ($choice) {
    "1" {
        Write-Host "`nGenerating viral roast with random GOAT..." -ForegroundColor Green
        python ULTIMATE_VIRAL_ROAST_FACTORY.py
    }
    
    "2" {
        Write-Host "`nAvailable GOATs:" -ForegroundColor Yellow
        Write-Host "1. George Carlin (Systematic deconstruction)"
        Write-Host "2. Richard Pryor (Raw vulnerability)"
        Write-Host "3. Dave Chappelle (Cultural commentary)"
        Write-Host "4. Bill Burr (Angry rants)"
        Write-Host "5. Patrice O'Neal (Brutal honesty)"
        Write-Host ""
        
        $goat = Read-Host "Choose GOAT (1-5)"
        $spirits = @('carlin', 'pryor', 'chappelle', 'burr', 'patrice')
        $selected = $spirits[[int]$goat - 1]
        
        Write-Host "`nGenerating with $selected..." -ForegroundColor Green
        python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(); f.generate_viral_roast(spirit='$selected')"
    }
    
    "3" {
        Write-Host "`nGenerating series of 5 viral roasts..." -ForegroundColor Green
        python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(); f.generate_series(num_videos=5)"
    }
    
    "4" {
        Write-Host "`nGenerating with HIGH priority (HAMi local GPU)..." -ForegroundColor Green
        python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(use_gpu_cloud=True); r = f.generate_viral_roast(priority='high'); print(f'\nGPU: {r.get(\"gpu_provider\",\"N/A\")} | Cost: `${r.get(\"cost\",0):.4f} | Time: {r.get(\"render_time\",0):.1f}s')"
    }
    
    "5" {
        Write-Host "`nGenerating with MEDIUM priority (SkyPilot auto-routing)..." -ForegroundColor Green
        python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(use_gpu_cloud=True); r = f.generate_viral_roast(priority='medium'); print(f'\nGPU: {r.get(\"gpu_provider\",\"N/A\")} | Cost: `${r.get(\"cost\",0):.4f} | Time: {r.get(\"render_time\",0):.1f}s')"
    }
    
    "6" {
        Write-Host "`nGenerating with LOW priority (Akash P2P marketplace)..." -ForegroundColor Green
        python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(use_gpu_cloud=True); r = f.generate_viral_roast(priority='low'); print(f'\nGPU: {r.get(\"gpu_provider\",\"N/A\")} | Cost: `${r.get(\"cost\",0):.4f} | Time: {r.get(\"render_time\",0):.1f}s')"
    }
    
    "7" {
        Write-Host "`nGenerating and uploading to platforms..." -ForegroundColor Green
        Write-Host "WARNING: This requires MCP server and Postiz to be running" -ForegroundColor Yellow
        python -c "from ULTIMATE_VIRAL_ROAST_FACTORY import UltimateViralRoastFactory; f = UltimateViralRoastFactory(); f.generate_viral_roast(upload=True)"
    }
    
    "8" {
        Write-Host "`nChecking system status..." -ForegroundColor Green
        Write-Host ""
        Write-Host "CORE SYSTEM:" -ForegroundColor Cyan
        
        # Check Python
        $pythonVersion = python --version 2>&1
        Write-Host "  [Python] $pythonVersion" -ForegroundColor $(if ($LASTEXITCODE -eq 0) { "Green" } else { "Red" })
        
        # Check FFmpeg
        $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
        Write-Host "  [FFmpeg] $($ffmpegVersion -replace 'ffmpeg version ', '')" -ForegroundColor $(if ($LASTEXITCODE -eq 0) { "Green" } else { "Red" })
        
        # Check TTS
        python -c "from TTS.api import TTS; print('Available')" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [TTS] Available" -ForegroundColor Green
        } else {
            Write-Host "  [TTS] NOT AVAILABLE - Install: pip install TTS" -ForegroundColor Red
        }
        
        # Check Jimi voice
        if (Test-Path "scarify/voice_samples/jimi_enhanced/jimi_enhanced_full.wav") {
            Write-Host "  [Jimi Voice] Available" -ForegroundColor Green
        } else {
            Write-Host "  [Jimi Voice] NOT FOUND" -ForegroundColor Red
        }
        
        Write-Host ""
        Write-Host "GPU CLOUD PROVIDERS:" -ForegroundColor Yellow
        
        # Check HAMi
        kubectl version --client 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [HAMi Local] kubectl detected - run 'kubectl get nodes' to check" -ForegroundColor Green
        } else {
            Write-Host "  [HAMi Local] NOT CONFIGURED (optional - see GPU_CLOUD_SETUP_GUIDE.md)" -ForegroundColor Gray
        }
        
        # Check SkyPilot
        python -c "import sky; print('Installed')" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [SkyPilot] Installed - run 'sky check' to see configured clouds" -ForegroundColor Green
        } else {
            Write-Host "  [SkyPilot] NOT INSTALLED - Install: pip install skypilot[all]" -ForegroundColor Yellow
        }
        
        # Check Akash
        akash version 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [Akash] Installed" -ForegroundColor Green
        } else {
            Write-Host "  [Akash] NOT INSTALLED (optional - see GPU_CLOUD_SETUP_GUIDE.md)" -ForegroundColor Gray
        }
        
        Write-Host ""
        Write-Host "INTEGRATIONS:" -ForegroundColor Cyan
        
        # Check MCP
        try {
            $mcp = Invoke-WebRequest -Uri "http://localhost:8080/health" -TimeoutSec 2 -ErrorAction Stop
            Write-Host "  [MCP Server] Running" -ForegroundColor Green
        } catch {
            Write-Host "  [MCP Server] NOT RUNNING (optional)" -ForegroundColor Gray
        }
        
        Write-Host ""
        Write-Host "OUTPUT:" -ForegroundColor Cyan
        
        # Check output directory
        if (Test-Path "viral_roasts") {
            $count = (Get-ChildItem "viral_roasts/*.mp4" -ErrorAction SilentlyContinue).Count
            $totalSize = (Get-ChildItem "viral_roasts/*.mp4" -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
            Write-Host "  [Videos] $count generated ($($totalSize.ToString('0.00')) MB total)" -ForegroundColor Cyan
        } else {
            Write-Host "  [Videos] 0 generated" -ForegroundColor Gray
        }
        
        Write-Host ""
        Write-Host "================================================================" -ForegroundColor Green
        Write-Host "System check complete!" -ForegroundColor Green
        Write-Host "================================================================" -ForegroundColor Green
    }
    
    "9" {
        Write-Host "`nOpening GPU Setup Guide..." -ForegroundColor Green
        if (Test-Path "GPU_CLOUD_SETUP_GUIDE.md") {
            Start-Process "GPU_CLOUD_SETUP_GUIDE.md"
        } else {
            Write-Host "GPU_CLOUD_SETUP_GUIDE.md not found!" -ForegroundColor Red
        }
    }
    
    "0" {
        Write-Host "`nExiting..." -ForegroundColor Yellow
        exit
    }
    
    default {
        Write-Host "`nInvalid choice!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
