@echo off
chcp 65001 >nul
cd /d "F:\AI_Oracle_Root\scarify\abraham_horror"

echo ========================================================================
echo YOUTUBE STUDIO API CONNECTOR
echo ========================================================================
echo.
echo This script will:
echo   1. Connect to YouTube Studio via API
echo   2. Pull all analytics data
echo   3. Identify videos missing QR codes
echo   4. Generate comprehensive report
echo.
echo Press any key to start connection...
pause >nul

python YOUTUBE_ANALYTICS_CONNECTOR.py

if errorlevel 1 (
    echo.
    echo ERROR: Connection failed. Check credentials.
    pause
) else (
    echo.
    echo SUCCESS: Analysis complete!
    echo.
    echo Next steps:
    echo   - Check analytics_report_*.json for full data
    echo   - Run FIX_QR_CODES_BATCH.py to add QR codes
    echo.
    pause
)

