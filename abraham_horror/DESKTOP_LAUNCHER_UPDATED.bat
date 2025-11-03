@echo off
REM Updated Desktop Launcher - Uses Latest Working System
title Abraham Lincoln Professional Video Generator
color 0A

cd /d "F:\AI_Oracle_Root\scarify\abraham_horror"

cls
echo.
echo ============================================================================
echo   ABRAHAM LINCOLN PROFESSIONAL VIDEO GENERATOR
echo ============================================================================
echo.
echo   Status: VERIFIED WORKING - Test Upload SUCCESS
echo   Channel: UCS5pEpSCw8k4wene0iv0uAg
echo.
echo   Features:
echo     - Real headline scraping
echo     - Professional comedy scripts
echo     - Dynamic B-roll from Pexels
echo     - Text overlays (PIL-based)
echo     - Direct YouTube upload
echo.
echo   Generating 10 videos and uploading to YouTube...
echo.
echo ============================================================================
echo.

python ABRAHAM_PROFESSIONAL_UPGRADE.py 10

echo.
echo ============================================================================
if %ERRORLEVEL% EQU 0 (
    echo   SUCCESS! Videos generated and uploaded to YouTube
    echo ============================================================================
    echo.
    echo   YouTube Studio:
    echo   https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos
    echo.
    echo   Videos will appear within 1-2 minutes.
    echo.
    start explorer "F:\AI_Oracle_Root\scarify\abraham_horror\videos"
) else (
    echo   ERROR: Check output above for details
    echo ============================================================================
)

echo.
pause


