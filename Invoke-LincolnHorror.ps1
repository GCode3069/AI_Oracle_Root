# INVOKE-LINCOLNHORROR.PS1
# PowerShell wrapper for Lincoln Horror Generator
# Integrates with SCARIFY Bootstrap System

param(
    [Parameter(Position=0)]
    [string]$Headline = "",
    
    [int]$Count = 1,
    
    [switch]$SetupOnly,
    
    [switch]$TestRun
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║                                                                           ║" -ForegroundColor Red
Write-Host "║           🩸 ABRAHAM LINCOLN HORROR GENERATOR 🩸                          ║" -ForegroundColor Red
Write-Host "║                                                                           ║" -ForegroundColor Red
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

# ============================================================================
# STEP 1: ENVIRONMENT CHECK
# ============================================================================

Write-Host "[STEP 1/5] Checking Environment..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found - install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if generator script exists
$generatorScript = Join-Path $PSScriptRoot "scarify_lincoln_horror.py"
if (-not (Test-Path $generatorScript)) {
    Write-Host "❌ scarify_lincoln_horror.py not found!" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Generator script found" -ForegroundColor Green

# ============================================================================
# STEP 2: API KEYS CHECK
# ============================================================================

Write-Host ""
Write-Host "[STEP 2/5] Checking API Keys..." -ForegroundColor Yellow

$apiKeysNeeded = @(
    @{Name="ELEVENLABS_API_KEY"; Desc="ElevenLabs voice cloning"; Required=$false},
    @{Name="RUNWAYML_API_SECRET"; Desc="RunwayML video generation"; Required=$false},
    @{Name="ANTHROPIC_API_KEY"; Desc="Claude script generation"; Required=$false}
)

$hasAnyKey = $false
foreach ($key in $apiKeysNeeded) {
    $value = [Environment]::GetEnvironmentVariable($key.Name)
    if ($value) {
        Write-Host "✅ $($key.Name): Configured" -ForegroundColor Green
        $hasAnyKey = $true
    } else {
        if ($key.Required) {
            Write-Host "❌ $($key.Name): Missing (REQUIRED)" -ForegroundColor Red
        } else {
            Write-Host "⚠️  $($key.Name): Missing (will use fallback)" -ForegroundColor Yellow
        }
    }
}

if (-not $hasAnyKey) {
    Write-Host ""
    Write-Host "⚠️  WARNING: No API keys configured" -ForegroundColor Yellow
    Write-Host "   System will use fallback methods (gTTS + MoviePy)" -ForegroundColor Yellow
    Write-Host "   Results will be less impressive but still functional" -ForegroundColor Gray
    Write-Host ""
}

# ============================================================================
# STEP 3: INSTALL DEPENDENCIES
# ============================================================================

Write-Host ""
Write-Host "[STEP 3/5] Installing Dependencies..." -ForegroundColor Yellow

$lincolnRequirements = @"
# Lincoln Horror Generator Requirements
requests>=2.31.0
beautifulsoup4>=4.12.0
elevenlabs>=0.2.26
anthropic>=0.7.0
moviepy>=1.0.3
Pillow>=10.0.0
numpy>=1.24.0
gtts>=2.4.0
imageio>=2.31.0
imageio-ffmpeg>=0.4.9
"@

$reqFile = Join-Path $PSScriptRoot "requirements_lincoln.txt"
$lincolnRequirements | Out-File -FilePath $reqFile -Encoding UTF8

Write-Host "📦 Installing packages..." -ForegroundColor White

try {
    $output = & python -m pip install -r $reqFile 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Some packages may have failed" -ForegroundColor Yellow
        Write-Host "   Try manually: pip install -r requirements_lincoln.txt" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Installation failed: $_" -ForegroundColor Red
}

if ($SetupOnly) {
    Write-Host ""
    Write-Host "✅ Setup complete! Ready to generate Lincoln horror videos." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Set API keys (optional):" -ForegroundColor White
    Write-Host "     `$env:ELEVENLABS_API_KEY = 'your_key_here'" -ForegroundColor Gray
    Write-Host "     `$env:RUNWAYML_API_SECRET = 'your_key_here'" -ForegroundColor Gray
    Write-Host "     `$env:ANTHROPIC_API_KEY = 'your_key_here'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Generate video:" -ForegroundColor White
    Write-Host "     .\Invoke-LincolnHorror.ps1" -ForegroundColor Gray
    Write-Host ""
    exit 0
}

# ============================================================================
# STEP 4: GENERATE VIDEOS
# ============================================================================

Write-Host ""
Write-Host "[STEP 4/5] Generating Lincoln Horror Videos..." -ForegroundColor Yellow
Write-Host ""

$args = @($generatorScript)

if ($Headline) {
    $args += "--headline", $Headline
    Write-Host "📰 Custom headline: $Headline" -ForegroundColor Magenta
} else {
    $args += "--count", $Count
    Write-Host "📊 Generating $Count video(s)" -ForegroundColor Magenta
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor DarkGray
Write-Host ""

try {
    $process = Start-Process -FilePath "python" `
                             -ArgumentList $args `
                             -WorkingDirectory $PSScriptRoot `
                             -NoNewWindow `
                             -Wait `
                             -PassThru
    
    $exitCode = $process.ExitCode
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor DarkGray
    Write-Host ""
    
    if ($exitCode -eq 0) {
        Write-Host "✅ Generation complete!" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Generation completed with warnings (exit code: $exitCode)" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Generation failed: $_" -ForegroundColor Red
    exit 1
}

# ============================================================================
# STEP 5: SHOW RESULTS
# ============================================================================

Write-Host ""
Write-Host "[STEP 5/5] Results..." -ForegroundColor Yellow
Write-Host ""

$videoDir = Join-Path $PSScriptRoot "output\lincoln_horror"
if (Test-Path $videoDir) {
    $videos = Get-ChildItem -Path $videoDir -Filter "*.mp4" | Sort-Object LastWriteTime -Descending
    
    if ($videos) {
        Write-Host "📹 Generated Videos:" -ForegroundColor Cyan
        foreach ($video in $videos | Select-Object -First $Count) {
            $sizeMB = [math]::Round($video.Length / 1MB, 2)
            $age = (Get-Date) - $video.LastWriteTime
            
            if ($age.TotalMinutes -lt 5) {
                Write-Host "   ✓ $($video.Name) (${sizeMB}MB) - JUST CREATED" -ForegroundColor Green
            } else {
                Write-Host "   • $($video.Name) (${sizeMB}MB)" -ForegroundColor Gray
            }
        }
        
        Write-Host ""
        Write-Host "📁 Location: $videoDir" -ForegroundColor White
        
        # Offer to open folder
        $response = Read-Host "`nOpen output folder? (y/n)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            Start-Process explorer.exe -ArgumentList $videoDir
        }
    } else {
        Write-Host "⚠️  No videos found - check error messages above" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Output directory not created - generation may have failed" -ForegroundColor Yellow
}

# ============================================================================
# SUMMARY & NEXT STEPS
# ============================================================================

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  NEXT STEPS: UPLOAD & MONETIZE                                           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Review videos in output\lincoln_horror\" -ForegroundColor White
Write-Host "2. Upload to YouTube Shorts (vertical 9:16 format)" -ForegroundColor White
Write-Host "3. Post thread on X (Twitter) with video embed" -ForegroundColor White
Write-Host "4. Add Gumroad CTA in description" -ForegroundColor White
Write-Host "5. Track performance & iterate" -ForegroundColor White
Write-Host ""
Write-Host "💰 Expected conversion: +10-25% vs standard content" -ForegroundColor Green
Write-Host "🎯 Target: $50k+ purge with Lincoln horror niche" -ForegroundColor Green
Write-Host ""

Write-Host "Run again:" -ForegroundColor Yellow
Write-Host "  .\Invoke-LincolnHorror.ps1 -Count 5" -ForegroundColor Gray
Write-Host "  .\Invoke-LincolnHorror.ps1 -Headline 'Your custom headline'" -ForegroundColor Gray
Write-Host ""

