@echo off
echo ========================================================================
echo DISTRIBUTED WORKER SETUP - FOR OLDER LAPTOP
echo ========================================================================
echo.
echo This will set up your older laptop to help with video generation.
echo.
echo REQUIREMENTS:
echo   1. Python 3.10+ installed
echo   2. Network access to main PC
echo   3. FFmpeg installed
echo   4. At least 4GB RAM
echo.
echo SETUP STEPS:
echo   1. Copy this file to laptop
echo   2. Update network path in DISTRIBUTED_WORKER_SETUP.py
echo   3. Run this batch file
echo.
pause

echo.
echo [1/5] Installing required packages...
pip install --quiet pillow moviepy requests beautifulsoup4 qrcode google-auth google-auth-oauthlib google-api-python-client

echo.
echo [2/5] Creating work directories...
python -c "from pathlib import Path; [Path(d).mkdir(parents=True, exist_ok=True) for d in ['queue', 'processing', 'completed', 'failed', 'temp']]"

echo.
echo [3/5] Testing FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo    WARNING: FFmpeg not found! Install from https://ffmpeg.org/
) else (
    echo    OK: FFmpeg detected
)

echo.
echo [4/5] Testing network connection...
echo    Checking for main PC...
ping -n 1 MAIN_PC >nul 2>&1
if errorlevel 1 (
    echo    WARNING: Cannot reach main PC. Update network settings.
) else (
    echo    OK: Main PC reachable
)

echo.
echo [5/5] Setup complete!
echo.
echo ========================================================================
echo WORKER IS READY
echo ========================================================================
echo.
echo To start working:
echo   python DISTRIBUTED_WORKER_SETUP.py --mode worker
echo.
echo This laptop will:
echo   - Watch for tasks from main PC
echo   - Generate videos when tasks available
echo   - Report back when complete
echo.
echo Press any key to start worker now, or Ctrl+C to exit...
pause >nul

python DISTRIBUTED_WORKER_SETUP.py --mode worker

