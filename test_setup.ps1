# SCARIFY Setup Verification Script
# Run this to check if everything is configured correctly

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  SCARIFY Setup Verification" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$AllGood = $true

# Check Python
Write-Host "[1/7] Checking Python..." -ForegroundColor Yellow
try {
    $PythonVersion = python --version 2>&1
    if ($PythonVersion -match "Python (\d+\.\d+)") {
        Write-Host "  ✅ Python found: $PythonVersion" -ForegroundColor Green
    } else {
        Write-Host "  ❌ Python not found or invalid version" -ForegroundColor Red
        $AllGood = $false
    }
} catch {
    Write-Host "  ❌ Python not installed" -ForegroundColor Red
    $AllGood = $false
}

# Check required files
Write-Host "[2/7] Checking required scripts..." -ForegroundColor Yellow
$RequiredFiles = @(
    "scarify_master.py",
    "audio_generator.py",
    "video_generator.py",
    "youtube_uploader.py",
    "scarify_launcher.ps1",
    "requirements.txt"
)

foreach ($File in $RequiredFiles) {
    if (Test-Path $File) {
        Write-Host "  ✅ $File" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $File missing" -ForegroundColor Red
        $AllGood = $false
    }
}

# Check output directories
Write-Host "[3/7] Checking output directories..." -ForegroundColor Yellow
$Dirs = @("output", "output\audio", "output\videos")
foreach ($Dir in $Dirs) {
    if (Test-Path $Dir) {
        Write-Host "  ✅ $Dir" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $Dir missing (will be created automatically)" -ForegroundColor Yellow
    }
}

# Check YouTube credentials folder
Write-Host "[4/7] Checking YouTube credentials..." -ForegroundColor Yellow
$CredsPath = "config\credentials\youtube"
if (Test-Path $CredsPath) {
    Write-Host "  ✅ Credentials folder exists" -ForegroundColor Green
    
    $ClientSecretsPath = Join-Path $CredsPath "client_secrets.json"
    if (Test-Path $ClientSecretsPath) {
        # Check if it's a real file or placeholder
        $Content = Get-Content $ClientSecretsPath -Raw
        if ($Content -match '"README"' -or $Content -match 'Place your') {
            Write-Host "  ⚠️  client_secrets.json is placeholder - needs real credentials" -ForegroundColor Yellow
            Write-Host "     See: YOUTUBE_SETUP_INSTRUCTIONS.md" -ForegroundColor Yellow
        } else {
            Write-Host "  ✅ client_secrets.json exists" -ForegroundColor Green
        }
    } else {
        Write-Host "  ❌ client_secrets.json missing" -ForegroundColor Red
        Write-Host "     See: YOUTUBE_SETUP_INSTRUCTIONS.md" -ForegroundColor Yellow
        $AllGood = $false
    }
} else {
    Write-Host "  ❌ Credentials folder missing" -ForegroundColor Red
    $AllGood = $false
}

# Check Python packages
Write-Host "[5/7] Checking Python packages..." -ForegroundColor Yellow
$RequiredPackages = @("moviepy", "requests", "python-dotenv")
foreach ($Package in $RequiredPackages) {
    $CheckPackage = python -c "import $($Package.Replace('-', '_'))" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ $Package" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $Package not installed" -ForegroundColor Red
        Write-Host "     Run: pip install -r requirements.txt" -ForegroundColor Yellow
        $AllGood = $false
    }
}

# Check Google API packages (for YouTube upload)
Write-Host "[6/7] Checking YouTube API packages..." -ForegroundColor Yellow
$GooglePackages = @("google.auth", "google_auth_oauthlib", "googleapiclient")
foreach ($Package in $GooglePackages) {
    $CheckPackage = python -c "import $($Package.Replace('-', '_').Replace('.', '_'))" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ $Package" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  $Package not installed (needed for YouTube upload)" -ForegroundColor Yellow
        Write-Host "     Run: pip install -r requirements.txt" -ForegroundColor Yellow
    }
}

# Check if desktop shortcut exists
Write-Host "[7/7] Checking desktop shortcut..." -ForegroundColor Yellow
$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $Desktop "SCARIFY Generator.lnk"
if (Test-Path $ShortcutPath) {
    Write-Host "  ✅ Desktop shortcut exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Desktop shortcut not created yet" -ForegroundColor Yellow
    Write-Host "     Run: .\create_desktop_shortcut.ps1" -ForegroundColor Yellow
}

# Final summary
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
if ($AllGood) {
    Write-Host "  ✅ SETUP COMPLETE!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Test video generation:" -ForegroundColor White
    Write-Host "     python scarify_master.py --count 1 --test" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Set up YouTube credentials (for upload):" -ForegroundColor White
    Write-Host "     See YOUTUBE_SETUP_INSTRUCTIONS.md" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. Create desktop shortcut:" -ForegroundColor White
    Write-Host "     .\create_desktop_shortcut.ps1" -ForegroundColor Gray
} else {
    Write-Host "  ⚠️  SETUP INCOMPLETE" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please fix the issues above." -ForegroundColor White
    Write-Host ""
    Write-Host "To install Python packages:" -ForegroundColor Cyan
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Gray
}
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

pause

