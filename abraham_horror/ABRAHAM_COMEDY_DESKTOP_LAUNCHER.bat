@echo off
REM ============================================================================
REM ABRAHAM LINCOLN COMEDY SYSTEM
REM Desktop Launcher - Double-click to generate comedy videos
REM ============================================================================

title Abraham Lincoln Comedy Video Generator

cd /d "F:\AI_Oracle_Root\scarify\abraham_horror"

echo.
echo ============================================================================
echo  ABRAHAM LINCOLN COMEDY VIDEO GENERATOR
echo ============================================================================
echo.
echo  Generating 5 comedy videos with B-roll and professional editing...
echo ============================================================================
echo.

python ABRAHAM_COMEDY_YOUTUBE_COMPLETE.py 5

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================================================
    echo  SUCCESS! Videos generated and uploaded
    echo ============================================================================
    echo.
    echo  Videos: F:\AI_Oracle_Root\scarify\abraham_horror\videos\
    echo  YouTube: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg/videos
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


