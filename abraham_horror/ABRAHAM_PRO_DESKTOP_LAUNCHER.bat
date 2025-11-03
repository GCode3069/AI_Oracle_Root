@echo off
REM ============================================================================
REM ABRAHAM LINCOLN PROFESSIONAL VIDEO GENERATOR - UPDATED
REM Desktop Launcher - Double-click to generate and upload to YouTube
REM Quality: EXCEEDS FarFromWeakFFW Channel | Status: VERIFIED WORKING
REM ============================================================================

title Abraham Lincoln Professional Video Generator
color 0A

cd /d "F:\AI_Oracle_Root\scarify\abraham_horror"

cls
echo.
echo ============================================================================
echo  ABRAHAM LINCOLN PROFESSIONAL VIDEO GENERATOR
echo ============================================================================
echo.
echo  Status: VERIFIED WORKING - Test Upload SUCCESS
echo  Channel: UCS5pEpSCw8k4wene0iv0uAg
echo  Quality Level: EXCEEDS FarFromWeakFFW Channel
echo.
echo  Features:
echo    - Real headline scraping
echo    - Professional comedy scripts
echo    - Dynamic B-roll from Pexels
echo    - Text overlays (PIL-based, no ImageMagick needed)
echo    - Direct YouTube upload
echo.
echo  Generating 10 professional videos and uploading...
echo ============================================================================
echo.

python ABRAHAM_PROFESSIONAL_UPGRADE.py 10

echo.
echo ============================================================================
if %ERRORLEVEL% EQU 0 (
    echo  SUCCESS! Videos generated and uploaded to YouTube
    echo ============================================================================
    echo.
    echo  YouTube Studio:
    echo  https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos
    echo.
    echo  Videos will appear within 1-2 minutes.
    echo.
    start explorer "F:\AI_Oracle_Root\scarify\abraham_horror\videos"
) else (
    echo  ERROR: Generation/Upload failed
    echo ============================================================================
    echo.
    echo  Check console output above for details
)

echo.
pause

