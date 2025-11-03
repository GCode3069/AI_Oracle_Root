@echo off
REM ═══════════════════════════════════════════════════════════════
REM   SCARIFY EMPIRE - AUTO DEPLOYMENT
REM   One command = Complete setup!
REM ═══════════════════════════════════════════════════════════════

color 0B
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              🤖 SCARIFY EMPIRE - AUTO DEPLOY 🤖                  ║
echo ║                                                                  ║
echo ║           Complete Automated Setup & Configuration              ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo.

cd /d "%~dp0"

echo 🚀 Starting self-deployment agent...
echo.
timeout /t 2 /nobreak >nul

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo.
    echo Please install Python 3.8+ from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH"!
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

REM Run the self-deployment script
python SELF_DEPLOY.py

if errorlevel 1 (
    echo.
    echo ❌ Deployment failed!
    echo.
    echo Check the error messages above and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              ✅ AUTO DEPLOYMENT COMPLETE! ✅                     ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 🎯 Your empire is ready!
echo.
echo Next step: LAUNCH_EMPIRE.bat
echo.
pause

