# SOVA TTS Installation Script
# Professional neural TTS for SCARIFY

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Installing SOVA TTS" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$SovaDir = "sova-tts"

# Check if already installed
if (Test-Path $SovaDir) {
    Write-Host "⚠️  SOVA TTS directory already exists" -ForegroundColor Yellow
    $Response = Read-Host "Reinstall? (y/n)"
    if ($Response -ne 'y' -and $Response -ne 'Y') {
        Write-Host "✅ Using existing installation" -ForegroundColor Green
        exit 0
    }
    Remove-Item -Recurse -Force $SovaDir
}

# Clone SOVA TTS repository
Write-Host "[1/4] Cloning SOVA TTS repository..." -ForegroundColor Yellow
try {
    git clone https://github.com/sovaai/sova-tts.git
    if ($LASTEXITCODE -ne 0) {
        throw "Git clone failed"
    }
    Write-Host "  ✅ Repository cloned" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Failed to clone repository" -ForegroundColor Red
    Write-Host "  Make sure Git is installed: https://git-scm.com/" -ForegroundColor Yellow
    pause
    exit 1
}

# Install SOVA dependencies
Write-Host "[2/4] Installing SOVA dependencies..." -ForegroundColor Yellow
Set-Location $SovaDir

if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ⚠️  Some dependencies may have failed" -ForegroundColor Yellow
    } else {
        Write-Host "  ✅ Dependencies installed" -ForegroundColor Green
    }
} else {
    Write-Host "  ⚠️  requirements.txt not found, installing common dependencies" -ForegroundColor Yellow
    pip install torch torchaudio numpy scipy librosa
}

Set-Location ..

# Download SOVA models (if needed)
Write-Host "[3/4] Checking for SOVA models..." -ForegroundColor Yellow
$ModelsDir = Join-Path $SovaDir "models"
if (-not (Test-Path $ModelsDir)) {
    Write-Host "  ⚠️  Models directory not found" -ForegroundColor Yellow
    Write-Host "  You may need to download models manually" -ForegroundColor Yellow
    Write-Host "  See: https://github.com/sovaai/sova-tts" -ForegroundColor Yellow
} else {
    Write-Host "  ✅ Models directory exists" -ForegroundColor Green
}

# Create wrapper script for easy integration
Write-Host "[4/4] Creating integration wrapper..." -ForegroundColor Yellow

$WrapperScript = @"
#!/usr/bin/env python3
"""
SOVA TTS Wrapper for SCARIFY
Simple interface for text-to-speech generation
"""
import sys
import os
from pathlib import Path

def generate_speech(text, output_path, voice='Matthew'):
    """Generate speech using SOVA TTS"""
    try:
        # Import SOVA TTS modules
        sys.path.insert(0, str(Path(__file__).parent))
        from synthesize import synthesize_text
        
        # Generate audio
        synthesize_text(
            text=text,
            output_path=output_path,
            speaker=voice
        )
        
        return os.path.exists(output_path)
    except Exception as e:
        print(f"SOVA TTS Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python run_sova_tts.py --text 'Your text' --output output.wav [--voice Matthew]")
        sys.exit(1)
    
    # Parse arguments
    args = {}
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == '--text' and i + 1 < len(sys.argv):
            args['text'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            args['output'] = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--voice' and i + 1 < len(sys.argv):
            args['voice'] = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    if 'text' not in args or 'output' not in args:
        print("Error: --text and --output are required")
        sys.exit(1)
    
    voice = args.get('voice', 'Matthew')
    
    success = generate_speech(args['text'], args['output'], voice)
    sys.exit(0 if success else 1)
"@

$WrapperPath = Join-Path $SovaDir "run_sova_tts.py"
Set-Content -Path $WrapperPath -Value $WrapperScript -Encoding UTF8
Write-Host "  ✅ Wrapper script created" -ForegroundColor Green

# Final summary
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  ✅ SOVA TTS Installation Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Test SOVA: python audio_generator.py 'Test audio' test_output.wav" -ForegroundColor White
Write-Host "2. If models are missing, download from: https://github.com/sovaai/sova-tts" -ForegroundColor White
Write-Host ""
Write-Host "SOVA will now be the PRIMARY audio generator!" -ForegroundColor Green
Write-Host "Fallback chain: SOVA → ElevenLabs → Windows TTS" -ForegroundColor Gray
Write-Host ""

pause

