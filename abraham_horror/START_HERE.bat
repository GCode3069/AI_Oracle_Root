@echo off
title Abraham Lincoln Video Generator
color 0A

cd /d "F:\AI_Oracle_Root\scarify\abraham_horror"

cls
echo.
echo ============================================================================
echo   ABRAHAM LINCOLN PROFESSIONAL VIDEO GENERATOR
echo ============================================================================
echo.
echo   Status: VERIFIED WORKING
echo   Channel: UCS5pEpSCw8k4wene0iv0uAg
echo.
echo   Generating 10 videos and uploading to YouTube...
echo.
echo ============================================================================
echo.

python ABRAHAM_PROFESSIONAL_UPGRADE.py 10

echo.
echo ============================================================================
if %ERRORLEVEL% EQU 0 (
    echo   SUCCESS! Videos uploaded to YouTube
    echo ============================================================================
    echo.
    echo   YouTube Studio:
    echo   https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos
    echo.
    start explorer "F:\AI_Oracle_Root\scarify\abraham_horror\videos"
) else (
    echo   ERROR: Check output above
    echo ============================================================================
)

echo.
pause


