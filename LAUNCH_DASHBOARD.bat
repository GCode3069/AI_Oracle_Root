@echo off
title SCARIFY Empire - Launch Dashboard
color 0A
cls

echo.
echo ========================================
echo    SCARIFY EMPIRE CONTROL CENTER
echo ========================================
echo.
echo Starting desktop dashboard...
echo.

cd /d "F:\AI_Oracle_Root\scarify"

REM Try pythonw first (no console window)
start /B pythonw SCARIFY_CONTROL_CENTER.pyw 2>nul

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Check if it started
tasklist /FI "IMAGENAME eq pythonw.exe" 2>NUL | find /I /N "pythonw.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Dashboard launched successfully!
    echo.
    echo The control center should be opening now...
    timeout /t 3
    exit
)

REM If pythonw failed, try python (with console)
echo Launching with console fallback...
python SCARIFY_CONTROL_CENTER.pyw


