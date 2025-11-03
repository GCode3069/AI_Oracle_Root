@echo off
title SCARIFY - Single Channel Test
color 0A
cls

echo.
echo ================================================================
echo   SCARIFY EMPIRE - SINGLE CHANNEL PROOF OF CONCEPT
echo ================================================================
echo.
echo This will TEST the full pipeline with 5 videos on 1 channel:
echo.
echo   [1] Check if videos exist
echo   [2] Authenticate YouTube API (Channel 1)
echo   [3] Upload 5 videos with optimized metadata
echo   [4] Validate Bitcoin + Rebel Kit embedding
echo   [5] Generate performance projections
echo.
echo If successful:
echo   - Proves pipeline works end-to-end
echo   - Validates YouTube API auth
echo   - Confirms metadata optimization
echo   - Ready for 111-video deployment
echo.
echo Time: ~3-5 minutes
echo.
pause

cd /d "F:\AI_Oracle_Root\scarify"

echo.
echo ================================================================
echo   CHECKING PREREQUISITES
echo ================================================================
echo.

echo [1/3] Checking for videos...
cd abraham_horror\youtube_ready
for /f %%i in ('dir /b *.mp4 2^>nul ^| find /c ".mp4"') do set video_count=%%i
cd ..\..

if %video_count% GTR 0 (
    echo   [OK] Found %video_count% videos
) else (
    echo   [ERROR] No videos found!
    echo.
    echo   Generate videos first:
    echo     python MASS_GENERATE_100_VIDEOS.py --total 5 --pollo 0
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Checking YouTube credentials...
if exist "config\credentials\youtube\client_secrets.json" (
    echo   [OK] Client secrets found
) else (
    echo   [ERROR] YouTube credentials missing!
    echo.
    echo   Download from: https://console.cloud.google.com
    echo   Save to: config\credentials\youtube\client_secrets.json
    echo.
    pause
    exit /b 1
)

echo.
echo [3/3] Checking Python dependencies...
python -c "import googleapiclient" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   [OK] Google API Client installed
) else (
    echo   [WARN] Installing Google API Client...
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
)

echo.
echo ================================================================
echo   RUNNING TEST
echo ================================================================
echo.

python TEST_SINGLE_CHANNEL_PROOF.py

echo.
echo ================================================================
echo   TEST COMPLETE
echo ================================================================
echo.

if exist "test_single_channel_results.json" (
    echo Results saved to: test_single_channel_results.json
    echo.
    echo Open this file to see:
    echo   - Video URLs
    echo   - Success/failure details
    echo   - Full deployment projections
    echo.
)

echo.
echo Next steps:
echo   [1] If test passed: Run EXECUTE_FULL_DEPLOYMENT.bat
echo   [2] If test had issues: Review errors and re-run
echo   [3] Check uploaded videos: https://studio.youtube.com
echo.
pause

