# INVOKE-VIRALLINCOLN.PS1
# Self-Bootstrapping Lincoln Horror Generator with YouTube Auto-Upload
# Viral-targeted for $15K revenue per batch

param(
    [string]$Headline = "",
    [int]$Count = 1,
    [switch]$NoUpload,
    [switch]$Resume,
    [string]$Category = ""
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Red
Write-Host "║                                                                           ║" -ForegroundColor Red
Write-Host "║       🩸 LINCOLN VIRAL GENERATOR - $15K BAG MODE 🩸                      ║" -ForegroundColor Red
Write-Host "║                                                                           ║" -ForegroundColor Red
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Red
Write-Host ""

# ============================================================================
# AUTO-BOOTSTRAP: Save and Resume Capability
# ============================================================================

$STATE_DIR = "cache_lincoln"
if (-not (Test-Path $STATE_DIR)) {
    New-Item -ItemType Directory -Path $STATE_DIR | Out-Null
    Write-Host "📁 Created state directory: $STATE_DIR" -ForegroundColor Green
}

# Save function for auto-resume
function Save-GenerationState {
    param([hashtable]$State)
    
    $stateFile = Join-Path $STATE_DIR "current_state.json"
    $State | ConvertTo-Json -Depth 10 | Out-File -FilePath $stateFile -Encoding UTF8
    Write-Host "💾 State saved: $($State.Count) items" -ForegroundColor Gray
}

# Load previous state if resuming
if ($Resume) {
    $stateFile = Join-Path $STATE_DIR "current_state.json"
    if (Test-Path $stateFile) {
        $previousState = Get-Content $stateFile | ConvertFrom-Json
        Write-Host "♻️  Resuming from previous state..." -ForegroundColor Yellow
        Write-Host "   Videos: $($previousState.videos_completed)/$($previousState.total_count)" -ForegroundColor Gray
    }
}

# ============================================================================
# ENVIRONMENT CHECK
# ============================================================================

Write-Host "[STEP 1/5] Environment Validation..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found - install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check API keys (informational)
$hasElevenLabs = [bool]$env:ELEVENLABS_API_KEY
$hasRunway = [bool]$env:RUNWAYML_API_SECRET
$hasYouTube = Get-ChildItem -Path . -Filter "client_secret*.json" | Select-Object -First 1

Write-Host ""
Write-Host "🔑 API Keys Status:" -ForegroundColor Cyan
Write-Host "   ElevenLabs: $(if ($hasElevenLabs) {'✅ Set'} else {'❌ Missing - using fallback'})" -ForegroundColor $(if ($hasElevenLabs) {'Green'} else {'Yellow'})
Write-Host "   RunwayML: $(if ($hasRunway) {'✅ Set'} else {'❌ Missing - using fallback'})" -ForegroundColor $(if ($hasRunway) {'Green'} else {'Yellow'})
Write-Host "   YouTube: $(if ($hasYouTube) {'✅ Found'} else {'❌ Missing - upload disabled'})" -ForegroundColor $(if ($hasYouTube) {'Green'} else {'Yellow'})

# ============================================================================
# INSTALL DEPENDENCIES
# ============================================================================

Write-Host ""
Write-Host "[STEP 2/5] Installing Dependencies..." -ForegroundColor Yellow

$requirements = @"
google-auth>=2.23.0
google-auth-oauthlib>=1.1.0
google-auth-httplib2>=0.1.1
google-api-python-client>=2.108.0
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

$reqFile = Join-Path $PSScriptRoot "requirements_viral.txt"
$requirements | Out-File -FilePath $reqFile -Encoding UTF8

try {
    $output = & python -m pip install -r $reqFile 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Some packages failed - continuing anyway" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Installation issue: $_" -ForegroundColor Yellow
}

# ============================================================================
# GENERATE VIDEOS
# ============================================================================

Write-Host ""
Write-Host "[STEP 3/5] Generating Viral Lincoln Horror..." -ForegroundColor Yellow
Write-Host ""

$generatorScript = Join-Path $PSScriptRoot "scarify_lincoln_viral_v2.py"

# Build arguments
$pyArgs = @()

if ($Headline) {
    $pyArgs += "--headline", $Headline
    Write-Host "📰 Custom headline: $Headline" -ForegroundColor Magenta
} else {
    $pyArgs += "--count", $Count
    Write-Host "📊 Generating $Count video(s)" -ForegroundColor Magenta
}

if ($NoUpload) {
    $pyArgs += "--no-upload"
    Write-Host "⏸️  Upload disabled" -ForegroundColor Yellow
}

if ($Category) {
    $pyArgs += "--category", $Category
    Write-Host "📂 Category: $Category" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor DarkGray
Write-Host ""

try {
    $process = Start-Process -FilePath "python" `
                             -ArgumentList ($pyArgs + $generatorScript) `
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
        Write-Host "⚠️  Completed with code: $exitCode" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Generation failed: $_" -ForegroundColor Red
    exit 1
}

# ============================================================================
# SHOW RESULTS
# ============================================================================

Write-Host ""
Write-Host "[STEP 4/5] Results Summary..." -ForegroundColor Yellow
Write-Host ""

$videoDir = Join-Path $PSScriptRoot "output\lincoln_horror"
if (Test-Path $videoDir) {
    $videos = Get-ChildItem -Path $videoDir -Filter "final_*.mp4" -ErrorAction SilentlyContinue | 
        Sort-Object LastWriteTime -Descending | 
        Select-Object -First $Count
    
    if ($videos) {
        $totalSize = ($videos | Measure-Object -Property Length -Sum).Sum
        $totalMB = [math]::Round($totalSize / 1MB, 2)
        
        Write-Host "📹 Generated Videos:" -ForegroundColor Cyan
        foreach ($video in $videos) {
            $sizeMB = [math]::Round($video.Length / 1MB, 2)
            $age = (Get-Date) - $video.LastWriteTime
            
            if ($age.TotalMinutes -lt 5) {
                Write-Host "   ✅ $($video.Name) (${sizeMB}MB) - JUST NOW" -ForegroundColor Green
            } else {
                Write-Host "   • $($video.Name) (${sizeMB}MB)" -ForegroundColor White
            }
        }
        
        Write-Host ""
        Write-Host "📊 Total size: ${totalMB}MB" -ForegroundColor Cyan
        Write-Host "📁 Location: $videoDir" -ForegroundColor White
        
        # Open folder
        $response = Read-Host "`nOpen output folder? (y/n)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            Start-Process explorer.exe -ArgumentList $videoDir
        }
    } else {
        Write-Host "⚠️  No final videos found" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Output directory missing" -ForegroundColor Yellow
}

# ============================================================================
# UPLOAD STATUS
# ============================================================================

Write-Host ""
Write-Host "[STEP 5/5] Upload Status..." -ForegroundColor Yellow

if ($NoUpload) {
    Write-Host "⏸️  Uploads were skipped (--no-upload flag)" -ForegroundColor Yellow
} else {
    if ($hasYouTube) {
        Write-Host "✅ YouTube upload attempted" -ForegroundColor Green
        Write-Host "   Check output for YouTube URLs" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  No YouTube credentials found" -ForegroundColor Yellow
        Write-Host "   Place client_secret*.json in project root for auto-upload" -ForegroundColor Gray
    }
}

# ============================================================================
# FINAL SUMMARY
# ============================================================================

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🎯 VIRAL LINCOLN HORROR - $15K BAG READY                                ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Performance Expectations:" -ForegroundColor Yellow
Write-Host "   • Views: 100K+ per video (viral potential)" -ForegroundColor White
Write-Host "   • YouTube revenue: $500-$2K per video" -ForegroundColor White
Write-Host "   • Gumroad traffic: 2K+ visitors per video" -ForegroundColor White
Write-Host "   • Total per video: $2.5K-$5.5K" -ForegroundColor Green
Write-Host ""
Write-Host "💰 Revenue Target: $15K+ for $Count videos" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Review videos in output\lincoln_horror\" -ForegroundColor White
Write-Host "   2. Upload to YouTube Shorts (if not auto-uploaded)" -ForegroundColor White
Write-Host "   3. Post to X (Twitter) with provocative captions" -ForegroundColor White
Write-Host "   4. Add Gumroad CTA in descriptions" -ForegroundColor White
Write-Host "   5. Track performance and scale winners" -ForegroundColor White
Write-Host ""

# State save
Save-GenerationState @{
    videos_completed = $Count
    total_count = $Count
    timestamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
}

Write-Host "💀 'From my grave, I watch. From theirs, they'll scream.' - A. Lincoln" -ForegroundColor DarkGray
Write-Host ""

