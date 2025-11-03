@echo off
chcp 65001 >nul
cd /d "F:\AI_Oracle_Root\scarify"
echo.
echo ========================================================================
echo PRIORITY TASK EXECUTION
echo ========================================================================
echo.
echo This will:
echo   1. Fix QR codes in all generators
echo   2. Connect YouTube API for analytics
echo   3. Generate 12 new shorts WITH QR codes
echo.
echo ========================================================================
pause
echo.

echo.
echo [1/3] FIXING QR CODES IN ALL GENERATORS...
echo ========================================================================
cd abraham_horror
python -Xutf8 ADD_QR_TO_ALL_GENERATORS.py
if errorlevel 1 (
    echo ERROR: QR code patch failed
    pause
    exit /b 1
)
echo.
echo [OK] QR code patch complete
echo.
pause

echo.
echo [2/3] CONNECTING TO YOUTUBE API...
echo ========================================================================
cd ..
python -Xutf8 YOUTUBE_API_ANALYZER.py
if errorlevel 1 (
    echo ERROR: YouTube API connection failed
    echo.
    echo This is normal for first run. You need to:
    echo   1. Go to: https://console.cloud.google.com/
    echo   2. Enable YouTube Data API v3 and YouTube Analytics API
    echo   3. Create OAuth credentials
    echo   4. Download client_secrets.json
    echo   5. Place in: config/credentials/youtube/
    echo.
    pause
)
echo.
echo [OK] YouTube API connected
echo.
pause

echo.
echo [3/3] GENERATING 12 NEW SHORTS WITH QR CODES...
echo ========================================================================
cd abraham_horror
python -Xutf8 ULTIMATE_HORROR_GENERATOR.py 12
if errorlevel 1 (
    echo ERROR: Video generation failed
    pause
    exit /b 1
)
echo.
echo [OK] 12 new shorts generated with QR codes
echo.

echo.
echo ========================================================================
echo ALL PRIORITY TASKS COMPLETE
echo ========================================================================
echo.
echo Check your results:
echo   - New videos: abraham_horror\uploaded\
echo   - YouTube Studio: https://studio.youtube.com/channel/UCS5pEpSCw8k4wene0iv0uAg
echo   - Analytics report: youtube_analytics_*.json
echo.
echo Next: Delete old shorts without QR codes and keep the new ones!
echo.
pause

