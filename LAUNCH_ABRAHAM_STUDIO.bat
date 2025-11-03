@echo off
title ABRAHAM STUDIO - Launcher

echo.
echo ================================================================
echo    ABRAHAM STUDIO - Horror Video Generator
echo ================================================================
echo.

set STUDIO_PATH=F:\AI_Oracle_Root\scarify\abraham_studio\ABRAHAM_STUDIO.pyw

if not exist "%STUDIO_PATH%" (
    echo [ERROR] ABRAHAM_STUDIO.pyw not found!
    echo.
    echo Expected location:
    echo    %STUDIO_PATH%
    echo.
    echo Please download ABRAHAM_STUDIO.pyw and place it in:
    echo    F:\AI_Oracle_Root\scarify\abraham_studio\
    echo.
    pause
    exit /b 1
)

echo [+] Launching ABRAHAM STUDIO...
echo.
echo Features:
echo    - Region selection (10 regions)
echo    - Multi-language (EN/ES/PT/DE)
echo    - Batch control (1-50 videos)
echo    - Real Pexels stock footage
echo    - Professional ElevenLabs voice
echo    - Adult gore mode
echo    - Progress tracking
echo.

start "" pythonw.exe "%STUDIO_PATH%"

timeout /t 2 /nobreak >nul

echo [OK] ABRAHAM STUDIO launched!
echo.
echo The desktop app window should now be open.
echo.
echo HOW TO USE:
echo    1. Select your region
echo    2. Set batch count (e.g., 10)
echo    3. Click 'GENERATE VIDEOS'
echo    4. Wait for completion
echo    5. Upload from youtube_ready folder
echo.
echo Target: $15,000 from Halloween campaign
echo.
echo Press any key to close this window...
pause >nul
