# Start of Save_Scarify_Bats_And_Setup.ps1
param(
  [string]$RepoRoot = (Get-Location).Path,
  [switch]$InstallDeps,
  [switch]$RunFull,
  [switch]$SkipConfirm,
  [int]$TestCount = 3,
  [int]$TestDuration = 30,
  [int]$TestDelay = 5,
  [int]$UploadDelayBetween = 5
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Repo root: $RepoRoot"

# Ensure repo root exists
if (-not (Test-Path $RepoRoot)) {
  Write-Host "Repo root does not exist. Creating: $RepoRoot"
  New-Item -ItemType Directory -Path $RepoRoot | Out-Null
}

Push-Location $RepoRoot

# Fix Git safe.directory for drives that don't record ownership
try {
  if (Get-Command git -ErrorAction SilentlyContinue) {
    if (Test-Path (Join-Path $RepoRoot ".git")) {
      try {
        git rev-parse --is-inside-work-tree > $null 2>&1
      } catch {
        Write-Host "Configuring git safe.directory for $RepoRoot"
        git config --global --add safe.directory $RepoRoot
      }
    }
  }
} catch {
  Write-Host "Skipping git safe.directory step: $($_.Exception.Message)"
}

# Helper paths/URLs
$batchScriptPath = Join-Path $RepoRoot "batch_launch_first_batch.ps1"
$findCredsPath = Join-Path $RepoRoot "Find-YouTubeCredentials.ps1"
$batPath = Join-Path $RepoRoot "run_scarify.bat"
$reqPath = Join-Path $RepoRoot "requirements.txt"
$scarifyCliPath = Join-Path $RepoRoot "scarify_cli.py"
$scarifyCliUrl = "https://raw.githubusercontent.com/GCode3069/AI_Oracle_Root/main/scarify_cli.py"

# Download scarify_cli.py if missing
if (-not (Test-Path $scarifyCliPath)) {
  Write-Host "scarify_cli.py not found — attempting download..."
  try {
    Invoke-WebRequest -Uri $scarifyCliUrl -OutFile $scarifyCliPath -UseBasicParsing -ErrorAction Stop
    Write-Host "Downloaded scarify_cli.py"
  } catch {
    Write-Host "Failed to download scarify_cli.py: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "Please place scarify_cli.py into $RepoRoot and re-run this script."
  }
} else {
  Write-Host "scarify_cli.py already present."
}

# Write batch launcher if missing
$batchContent = @'
param(
  [int]$Count = 3,
  [int]$Duration = 45,
  [int]$DelayBetween = 5
)

if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
  Write-Host "Virtualenv not found. Create and activate .venv first." -ForegroundColor Red
  exit 1
}

$venvScripts = Join-Path (Get-Location) ".venv\Scripts"
$env:PATH = "$venvScripts;$env:PATH"

Write-Host "Starting batch: Count=$Count, Duration=$Duration sec" -ForegroundColor Cyan

for ($i = 1; $i -le $Count; $i++) {
  $title = "SCARIFY Transmission Batch $i - $(Get-Date -Format yyyyMMdd_HHmmss)"
  Write-Host "`n=== Generating video $i/$Count: $title ===" -ForegroundColor Yellow

  python .\scarify_cli.py generate --duration $Duration --theme "batch_$i"
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Generation failed for item $i. Aborting batch." -ForegroundColor Red
    exit 1
  }

  $outdir = Join-Path (Get-Location) "scarify\Output\YouTubeReady"
  if (-not (Test-Path $outdir)) {
    Write-Host "Output dir not found: $outdir" -ForegroundColor Red
    exit 1
  }

  $video = Get-ChildItem $outdir -Filter "SCARIFY_*.mp4" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if (-not $video) {
    Write-Host "No generated video found after generation step." -ForegroundColor Red
    exit 1
  }

  Write-Host "Uploading: $($video.FullName) (if credentials are present)" -ForegroundColor Cyan

  python .\scarify_cli.py upload --video-path $video.FullName --title $title --auto-find

  if ($LASTEXITCODE -ne 0) {
    Write-Host "Upload failed for $($video.Name). Continuing to next item." -ForegroundColor Red
  } else {
    Write-Host "Uploaded: $title" -ForegroundColor Green
  }

  Start-Sleep -Seconds $DelayBetween
}

Write-Host "`nBatch complete." -ForegroundColor Green
'@ 

if (-not (Test-Path $batchScriptPath)) {
  $batchContent | Out-File -FilePath $batchScriptPath -Encoding UTF8
  Write-Host "Wrote $batchScriptPath"
} else {
  Write-Host "$batchScriptPath already exists (skipping)."
}

# Write Find-YouTubeCredentials.ps1 (safe preview) if missing
$findCredsContent = @'
Write-Host "🔍 SEARCHING FOR YOUTUBE CREDENTIALS..." -ForegroundColor Cyan

$searchPatterns = @("client_secrets.json","client_secret*.json","credentials.json","youtube_credentials.json","api_keys.json","google_api.json")
$searchDirs = @(".",".\credentials",".\scarify",".\scarify\youtube_upload",".\scarify\youtube_upload\credentials",".\scarify\config",".\config",".\api")

$found = @()
foreach ($d in $searchDirs) {
  if (Test-Path $d) {
    foreach ($p in $searchPatterns) {
      $files = Get-ChildItem -Path $d -Filter $p -Recurse -ErrorAction SilentlyContinue -File
      if ($files) { $found += $files }
    }
  }
}

$found = $found | Sort-Object FullName -Unique
if ($found.Count -gt 0) {
  Write-Host "`n✅ FOUND:" -ForegroundColor Green
  foreach ($f in $found) {
    Write-Host "  $($f.FullName)"
  }
} else {
  Write-Host "`n❌ No credential files found." -ForegroundColor Red
}
'@ 

if (-not (Test-Path $findCredsPath)) {
  $findCredsContent | Out-File -FilePath $findCredsPath -Encoding UTF8
  Write-Host "Wrote $findCredsPath"
} else {
  Write-Host "$findCredsPath already exists (skipping)."
} 

# Write run_scarify.bat if missing
$batContent = @'
@echo off
chcp 65001 >nul
title SCARIFY AI Oracle CLI
call .venv\Scripts\activate.bat
python scarify_cli.py %*
pause
'@
if (-not (Test-Path $batPath)) {
  $batContent | Out-File -FilePath $batPath -Encoding ASCII
  Write-Host "Wrote $batPath"
}

# Write requirements.txt if missing
$reqContent = @'
typer>=0.9.0
google-api-python-client>=2.108.0
google-auth-httplib2>=0.1.0
google-auth-oauthlib>=1.0.0
gtts>=2.3.0
ffmpeg-python>=0.2.0
pillow>=10.0.0
requests>=2.31.0
moviepy>=1.0.3
numpy
opencv-python
'@
if (-not (Test-Path $reqPath)) {
  $reqContent | Out-File -FilePath $reqPath -Encoding UTF8
  Write-Host "Wrote $reqPath"
}

# Create venv if missing
$venvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
  Write-Host "Creating virtual environment..."
  python -m venv .venv
} else {
  Write-Host "Virtual environment already exists."
}

# Install dependencies into venv if requested
if ($InstallDeps) {
  Write-Host "Installing dependencies into venv..."
  & $venvPython -m pip install --upgrade pip
  & $venvPython -m pip install -r $reqPath
  Write-Host "Dependencies installed."
}

# Run credential finder
Write-Host "`nRunning credential search..."
& pwsh -NoProfile -ExecutionPolicy Bypass -File $findCredsPath

# Safe generate-only test
Write-Host "`n🧪 Running safe generate-only test..."
for ($i=1; $i -le $TestCount; $i++) {
  Write-Host "Generating test video $i/$TestCount..."
  python .\scarify_cli.py generate --duration $TestDuration --theme "test_$i"
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Generation failed at item $i" -ForegroundColor Red
    break
  } else {
    Write-Host "Test $i generation done." -ForegroundColor Green
  }
  Start-Sleep -Seconds $TestDelay
}

# Decide about uploads
$credPathStandard = Join-Path $RepoRoot "credentials\client_secrets.json"
$hasCred = Test-Path $credPathStandard

if ($hasCred) {
  Write-Host "`n✅ Found credentials at $credPathStandard" -ForegroundColor Green
} else {
  Write-Host "`n⚠️  No credentials at $credPathStandard" -ForegroundColor Yellow
}

if ($RunFull -or $hasCred) {
  $doUpload = $false
  if ($SkipConfirm) {
    $doUpload = $true
  } else {
    $ans = Read-Host "Attempt to upload generated videos now? (y/n)"
    if ($ans -eq 'y') { $doUpload = $true }
  }

  if ($doUpload) {
    $outdir = Join-Path (Get-Location) "scarify\Output\YouTubeReady"
    if (-not (Test-Path $outdir)) {
      Write-Host "No output directory found: $outdir" -ForegroundColor Red
    } else {
      $videos = Get-ChildItem $outdir -Filter "SCARIFY_*.mp4" -File | Sort-Object LastWriteTime -Descending
      foreach ($v in $videos) {
        Write-Host "Uploading $($v.Name) ..." -ForegroundColor Cyan
        python .\scarify_cli.py upload --video-path $v.FullName --title "SCARIFY Batch Upload $($v.BaseName)" --auto-find
        if ($LASTEXITCODE -ne 0) {
          Write-Host "Upload failed for $($v.Name)." -ForegroundColor Red
        } else {
          Write-Host "Uploaded $($v.Name)" -ForegroundColor Green
        }
        Start-Sleep -Seconds $UploadDelayBetween
      }
    }
  }
}

Pop-Location
Write-Host "Setup script finished."