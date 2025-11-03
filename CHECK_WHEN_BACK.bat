@echo off
title SCARIFY - Check Deployment Status
color 0A
cls

echo.
echo ========================================
echo   SCARIFY - Deployment Status Check
echo ========================================
echo.
echo Checking what happened while you rested...
echo.

cd /d "F:\AI_Oracle_Root\scarify"

echo ========================================
echo VIDEO GENERATION:
echo ========================================
echo.

cd abraham_horror
for /f %%i in ('dir /b youtube_ready\*.mp4 2^>nul ^| find /c ".mp4"') do set video_count=%%i
echo Videos Generated: %video_count%
echo.

echo ========================================
echo YOUTUBE UPLOADS:
echo ========================================
echo.

cd ..
for /f %%i in ('dir /b upload_results_*.json 2^>nul ^| find /c ".json"') do set upload_count=%%i
echo Upload Batches: %upload_count%
echo.

if exist "upload_results_*.json" (
    echo Latest uploads:
    for /f "delims=" %%f in ('dir /b /o-d upload_results_*.json 2^>nul') do (
        echo   %%f
        goto :break
    )
    :break
)

echo.
echo ========================================
echo BITCOIN BALANCE:
echo ========================================
echo.

python check_balance.py

echo.
echo ========================================
echo ANALYTICS:
echo ========================================
echo.

python analytics_tracker.py report

echo.
echo ========================================
echo   Check Complete!
echo ========================================
echo.
echo View YouTube Studio:
echo https://studio.youtube.com
echo.
pause


