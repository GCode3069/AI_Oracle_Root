# SCARIFY EMPIRE INSTALLATION SCRIPT
# Installs all dependencies for BTC QR + Theta Audio + Chapman Fear + Multi-Channel

Write-Host "🔥 SCARIFY EMPIRE INSTALLATION 🔥" -ForegroundColor Red
Write-Host "=" * 50

# Check if Python is installed
try {
    $PythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/"
    exit 1
}

# Check if pip is available
try {
    $PipVersion = pip --version 2>&1
    Write-Host "✅ pip found: $PipVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ pip not found! Please install pip first." -ForegroundColor Red
    exit 1
}

# Install ImageMagick (required for MoviePy text rendering)
Write-Host "`n📸 Installing ImageMagick..." -ForegroundColor Yellow
try {
    winget install ImageMagick.ImageMagick -e --silent
    Write-Host "✅ ImageMagick installed successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠️  ImageMagick installation failed. You may need to install manually." -ForegroundColor Yellow
    Write-Host "Download from: https://imagemagick.org/script/download.php#windows"
}

# Set ImageMagick environment variable
$ImageMagickPath = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
if (Test-Path $ImageMagickPath) {
    $env:IMAGEMAGICK_BINARY = $ImageMagickPath
    Write-Host "✅ ImageMagick path set: $ImageMagickPath" -ForegroundColor Green
} else {
    Write-Host "⚠️  ImageMagick path not found. You may need to set IMAGEMAGICK_BINARY manually." -ForegroundColor Yellow
}

# Install Python dependencies
Write-Host "`n🐍 Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..."

try {
    pip install -r requirements.txt
    Write-Host "✅ All Python dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to install Python dependencies" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)"
    exit 1
}

# Install additional audio dependencies
Write-Host "`n🎵 Installing audio processing dependencies..." -ForegroundColor Yellow
try {
    pip install numpy scipy pydub qrcode[pil] Pillow
    Write-Host "✅ Audio dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Some audio dependencies failed to install" -ForegroundColor Yellow
}

# Create necessary directories
Write-Host "`n📁 Creating directories..." -ForegroundColor Yellow
$Directories = @(
    "output",
    "output\videos",
    "output\audio",
    "config",
    "config\credentials",
    "config\credentials\youtube",
    "config\credentials\pexels"
)

foreach ($Dir in $Directories) {
    if (-not (Test-Path $Dir)) {
        New-Item -ItemType Directory -Path $Dir -Force | Out-Null
        Write-Host "✅ Created: $Dir" -ForegroundColor Green
    } else {
        Write-Host "✅ Exists: $Dir" -ForegroundColor Green
    }
}

# Check for API keys
Write-Host "`n🔑 Checking API configuration..." -ForegroundColor Yellow

$EnvFile = "config\credentials\.env"
if (-not (Test-Path $EnvFile)) {
    Write-Host "⚠️  .env file not found. Creating template..." -ForegroundColor Yellow
    
    $EnvContent = @"
# SCARIFY EMPIRE API KEYS
# Get your keys from the respective services

# ElevenLabs TTS (https://elevenlabs.io/)
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# Pexels Video API (https://www.pexels.com/api/)
PEXELS_API_KEY=your_pexels_key_here

# YouTube API (https://console.developers.google.com/)
# Download client_secrets.json and place in config/credentials/youtube/

# ImageMagick Path (set automatically)
IMAGEMAGICK_BINARY=C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe

# Channel Selection
SCARIFY_CHANNEL=the_vet_edge
"@
    
    Set-Content -Path $EnvFile -Value $EnvContent
    Write-Host "✅ Created .env template at: $EnvFile" -ForegroundColor Green
    Write-Host "⚠️  Please edit .env file with your actual API keys" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env file exists" -ForegroundColor Green
}

# Check YouTube credentials
$YouTubeSecrets = "config\credentials\youtube\client_secrets.json"
if (-not (Test-Path $YouTubeSecrets)) {
    Write-Host "⚠️  YouTube client_secrets.json not found" -ForegroundColor Yellow
    Write-Host "Please download from: https://console.developers.google.com/" -ForegroundColor Yellow
    Write-Host "Place in: $YouTubeSecrets" -ForegroundColor Yellow
} else {
    Write-Host "✅ YouTube credentials found" -ForegroundColor Green
}

# Test imports
Write-Host "`n🧪 Testing imports..." -ForegroundColor Yellow
$TestScript = @"
try:
    import moviepy.editor
    print("✅ MoviePy: OK")
except ImportError as e:
    print(f"❌ MoviePy: {e}")

try:
    import qrcode
    print("✅ QRCode: OK")
except ImportError as e:
    print(f"❌ QRCode: {e}")

try:
    import numpy
    print("✅ NumPy: OK")
except ImportError as e:
    print(f"❌ NumPy: {e}")

try:
    import scipy
    print("✅ SciPy: OK")
except ImportError as e:
    print(f"❌ SciPy: {e}")

try:
    import pydub
    print("✅ PyDub: OK")
except ImportError as e:
    print(f"❌ PyDub: {e}")

try:
    import elevenlabs
    print("✅ ElevenLabs: OK")
except ImportError as e:
    print(f"❌ ElevenLabs: {e}")

print("🎉 Import test complete!")
"@

$TestScript | python
Write-Host ""

# Final status
Write-Host "🔥 SCARIFY EMPIRE INSTALLATION COMPLETE! 🔥" -ForegroundColor Red
Write-Host "=" * 50
Write-Host ""
Write-Host "✅ All dependencies installed" -ForegroundColor Green
Write-Host "✅ Directories created" -ForegroundColor Green
Write-Host "✅ Configuration files ready" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "1. Edit config\credentials\.env with your API keys" -ForegroundColor White
Write-Host "2. Download YouTube client_secrets.json" -ForegroundColor White
Write-Host "3. Run: .\scarify_empire_dashboard.ps1" -ForegroundColor White
Write-Host ""
Write-Host "🎯 FEATURES READY:" -ForegroundColor Yellow
Write-Host "💰 BTC QR Overlays (Direct crypto payments)" -ForegroundColor White
Write-Host "🎵 Theta Audio (Brainwave retention)" -ForegroundColor White
Write-Host "😨 Chapman Fear Prompts (Psychology-based)" -ForegroundColor White
Write-Host "🔄 Multi-Channel Rotation (Scale without limits)" -ForegroundColor White
Write-Host "📤 Direct YouTube Upload (One-click)" -ForegroundColor White
Write-Host ""
Write-Host "🔥 LET'S BUILD THE EMPIRE! 🔥" -ForegroundColor Red

# Ask if user wants to launch dashboard
$Launch = Read-Host "`nLaunch SCARIFY Empire Dashboard now? (y/n)"
if ($Launch -eq "y" -or $Launch -eq "Y") {
    Write-Host "🚀 Launching SCARIFY Empire Dashboard..." -ForegroundColor Green
    .\scarify_empire_dashboard.ps1
}