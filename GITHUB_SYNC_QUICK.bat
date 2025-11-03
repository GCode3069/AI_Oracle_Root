@echo off
REM Quick GitHub Sync - One-Click Repository Update
REM Syncs Scarify Empire to GCode3069/AI_Oracle_Root

color 0B
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║           GITHUB SYNC - Update AI_Oracle_Root Repo              ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo.
echo [INFO] Syncing to: https://github.com/GCode3069/AI_Oracle_Root
echo [INFO] This will update your repository with ALL latest files
echo.
echo Press Ctrl+C to cancel, or
pause

cd /d "F:\AI_Oracle_Root\scarify"

echo.
echo [STEP 1/5] Running comprehensive sync...
echo.
pwsh -ExecutionPolicy Bypass -File SYNC_EVERYTHING_TO_GITHUB.ps1

if errorlevel 1 (
    echo.
    echo ❌ Sync failed! Check errors above.
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║                    ✓ GITHUB SYNC COMPLETE!                      ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🎉 Your repository is now up-to-date!
echo 🔗 View at: https://github.com/GCode3069/AI_Oracle_Root
echo.
pause

