@echo off
REM ============================================================================
REM ABRAHAM LINCOLN PROFESSIONAL VIDEO GENERATOR - FIXED LAUNCHER
REM Double-click to generate videos and upload to YouTube
REM ============================================================================

title Abraham Lincoln Professional Video Generator

cd /d "F:\AI_Oracle_Root\scarify\abraham_horror"

echo.
echo ============================================================================
echo  ABRAHAM LINCOLN PROFESSIONAL VIDEO GENERATOR
echo ============================================================================
echo.
echo  Status: VERIFIED WORKING
echo  Test Upload: SUCCESS
echo.
echo  This will generate 10 videos and upload directly to YouTube
echo  Channel: UCS5pEpSCw8k4wene0iv0uAg
echo.
echo ============================================================================
echo.

python ABRAHAM_PROFESSIONAL_UPGRADE.py 10

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================================
    echo  SUCCESS! Videos generated and uploaded
    echo ============================================================================
    echo.
    echo  Check YouTube Studio:
    echo  https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos
    echo.
    explorer "F:\AI_Oracle_Root\scarify\abraham_horror\videos"
) else (
    echo.
    echo ============================================================================
    echo  ERROR: Generation failed
    echo ============================================================================
    echo.
    echo  Check console output above for details
)

echo.
pause


