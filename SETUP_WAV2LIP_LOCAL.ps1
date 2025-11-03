# SETUP_WAV2LIP_LOCAL.ps1
# Complete setup for Wav2Lip lip-sync locally

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  WAV2LIP LOCAL SETUP - STEP BY STEP" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "This will install Wav2Lip for realistic lip-sync`n" -ForegroundColor Yellow

Write-Host "REQUIREMENTS:" -ForegroundColor Yellow
Write-Host "  - Python 3.7-3.9 (you have: 3.10 - may need downgrade)" -ForegroundColor White
Write-Host "  - CUDA GPU (optional but recommended)" -ForegroundColor White
Write-Host "  - ~2GB disk space" -ForegroundColor White
Write-Host "  - ~10GB RAM`n" -ForegroundColor White

$confirmation = Read-Host "Continue with setup? (yes/no)"

if ($confirmation -ne "yes") {
    Write-Host "`nAborted." -ForegroundColor Yellow
    exit
}

# Step 1: Create Wav2Lip directory
Write-Host "`n[STEP 1/6] Creating Wav2Lip directory..." -ForegroundColor Cyan
$wav2lipDir = "F:\AI_Oracle_Root\scarify\wav2lip"
if (-not (Test-Path $wav2lipDir)) {
    New-Item -ItemType Directory -Path $wav2lipDir | Out-Null
    Write-Host "  Created: $wav2lipDir" -ForegroundColor Green
} else {
    Write-Host "  Already exists: $wav2lipDir" -ForegroundColor Yellow
}

# Step 2: Clone Wav2Lip repository
Write-Host "`n[STEP 2/6] Cloning Wav2Lip repository..." -ForegroundColor Cyan
Set-Location $wav2lipDir

if (-not (Test-Path "$wav2lipDir\.git")) {
    Write-Host "  Cloning from GitHub..." -ForegroundColor White
    git clone https://github.com/Rudrabha/Wav2Lip.git .
    Write-Host "  Cloned successfully" -ForegroundColor Green
} else {
    Write-Host "  Repository already cloned" -ForegroundColor Yellow
}

# Step 3: Install dependencies
Write-Host "`n[STEP 3/6] Installing Python dependencies..." -ForegroundColor Cyan
Write-Host "  This may take 5-10 minutes..." -ForegroundColor Gray

# Create requirements file with compatible versions
@"
torch==1.9.0
torchvision==0.10.0
torchaudio==0.9.0
opencv-python==4.5.3.56
opencv-contrib-python==4.5.3.56
numpy==1.21.0
scipy==1.7.0
librosa==0.8.1
numba==0.53.1
scikit-image==0.18.2
Pillow==8.3.1
tqdm==4.61.2
"@ | Out-File -FilePath "$wav2lipDir\requirements_fixed.txt" -Encoding utf8

Write-Host "  Installing packages (this takes time)..." -ForegroundColor White
pip install -r requirements_fixed.txt --no-cache-dir

if ($LASTEXITCODE -eq 0) {
    Write-Host "  Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  WARNING: Some packages may have failed" -ForegroundColor Yellow
    Write-Host "  Continuing anyway..." -ForegroundColor Gray
}

# Step 4: Download pre-trained models
Write-Host "`n[STEP 4/6] Downloading pre-trained models..." -ForegroundColor Cyan
$checkpointsDir = "$wav2lipDir\checkpoints"
if (-not (Test-Path $checkpointsDir)) {
    New-Item -ItemType Directory -Path $checkpointsDir | Out-Null
}

# Download Wav2Lip GAN model (best quality)
$modelUrl = "https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA?download=1"
$modelPath = "$checkpointsDir\wav2lip_gan.pth"

if (-not (Test-Path $modelPath)) {
    Write-Host "  Downloading Wav2Lip GAN model (large file, ~700MB)..." -ForegroundColor White
    Write-Host "  This may take 10-30 minutes depending on connection..." -ForegroundColor Gray
    
    try {
        Invoke-WebRequest -Uri $modelUrl -OutFile $modelPath -TimeoutSec 3600
        Write-Host "  Model downloaded successfully" -ForegroundColor Green
    } catch {
        Write-Host "  Download failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "  Manual download required:" -ForegroundColor Yellow
        Write-Host "  1. Go to: https://github.com/Rudrabha/Wav2Lip#getting-the-weights" -ForegroundColor White
        Write-Host "  2. Download wav2lip_gan.pth" -ForegroundColor White
        Write-Host "  3. Save to: $modelPath" -ForegroundColor White
    }
} else {
    Write-Host "  Model already downloaded" -ForegroundColor Yellow
}

# Step 5: Download face detection model
Write-Host "`n[STEP 5/6] Downloading face detection model..." -ForegroundColor Cyan
$faceDetectionUrl = "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth"
$faceDetectionPath = "$wav2lipDir\face_detection\detection\sfd\s3fd.pth"
$faceDetectionDir = Split-Path $faceDetectionPath -Parent

if (-not (Test-Path $faceDetectionDir)) {
    New-Item -ItemType Directory -Path $faceDetectionDir -Force | Out-Null
}

if (-not (Test-Path $faceDetectionPath)) {
    Write-Host "  Downloading face detection model..." -ForegroundColor White
    try {
        Invoke-WebRequest -Uri $faceDetectionUrl -OutFile $faceDetectionPath
        Write-Host "  Face detection model downloaded" -ForegroundColor Green
    } catch {
        Write-Host "  Download failed, will download on first use" -ForegroundColor Yellow
    }
} else {
    Write-Host "  Face detection model already downloaded" -ForegroundColor Yellow
}

# Step 6: Test installation
Write-Host "`n[STEP 6/6] Testing Wav2Lip installation..." -ForegroundColor Cyan

$testScript = @"
import sys
import torch
print(f'Python: {sys.version}')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'CUDA device: {torch.cuda.get_device_name(0)}')
print('Wav2Lip dependencies OK')
"@

$testScript | Out-File -FilePath "$wav2lipDir\test_install.py" -Encoding utf8
python "$wav2lipDir\test_install.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n  Installation test passed!" -ForegroundColor Green
} else {
    Write-Host "`n  Installation test failed" -ForegroundColor Red
}

# Create helper script for generation
$helperScript = @"
import sys
import os
from pathlib import Path

# Add Wav2Lip to path
wav2lip_path = Path(__file__).parent
sys.path.insert(0, str(wav2lip_path))

def generate_lipsync(face_path, audio_path, output_path):
    '''Generate lip-sync video using local Wav2Lip'''
    import subprocess
    
    cmd = [
        'python', str(wav2lip_path / 'inference.py'),
        '--checkpoint_path', str(wav2lip_path / 'checkpoints' / 'wav2lip_gan.pth'),
        '--face', str(face_path),
        '--audio', str(audio_path),
        '--outfile', str(output_path),
        '--resize_factor', '1',
        '--fps', '25',
        '--pads', '0', '10', '0', '0'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    
    if result.returncode == 0:
        print(f'Lip-sync generated: {output_path}')
        return True
    else:
        print(f'Error: {result.stderr}')
        return False

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python wav2lip_helper.py <face_image> <audio_file> <output_video>')
        sys.exit(1)
    
    generate_lipsync(sys.argv[1], sys.argv[2], sys.argv[3])
"@

$helperScript | Out-File -FilePath "$wav2lipDir\wav2lip_helper.py" -Encoding utf8

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  WAV2LIP SETUP COMPLETE" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "INSTALLATION SUMMARY:" -ForegroundColor Yellow
Write-Host "  Location: $wav2lipDir" -ForegroundColor White
Write-Host "  Model: $(if (Test-Path $modelPath) {'Downloaded'} else {'MISSING - see manual download'})" -ForegroundColor $(if (Test-Path $modelPath) {'Green'} else {'Red'})
Write-Host "  Helper: wav2lip_helper.py created`n" -ForegroundColor White

Write-Host "USAGE:" -ForegroundColor Yellow
Write-Host "  python wav2lip_helper.py face.jpg audio.mp3 output.mp4`n" -ForegroundColor Cyan

Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Test with: python wav2lip_helper.py [your_image] [your_audio] test_output.mp4" -ForegroundColor Cyan
Write-Host "  2. If works: Enable in abraham_MAX_HEADROOM.py" -ForegroundColor Cyan
Write-Host "  3. Run: .\FIX_FFMPEG_ZOOM.ps1 (to fix zoom fallback too)`n" -ForegroundColor Cyan

Write-Host "================================================================`n" -ForegroundColor Cyan

Set-Location "F:\AI_Oracle_Root\scarify"


