@echo off
REM Launch Scarify Empire Control Center Dashboard

echo ========================================
echo  Scarify Empire - Control Center
echo ========================================
echo.

cd /d "%~dp0"

echo Starting Control Center Dashboard...
echo.

pythonw SCARIFY_CONTROL_CENTER.pyw

if errorlevel 1 (
    echo.
    echo Error launching Control Center!
    echo Make sure Python is installed.
    echo.
    pause
)
