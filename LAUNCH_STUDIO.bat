@echo off
title ABRAHAM STUDIO Launcher
echo.
echo ================================================================
echo    Launching ABRAHAM STUDIO...
echo ================================================================
echo.

pythonw.exe "ABRAHAM_STUDIO (1).pyw"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Studio launched!
    echo.
    echo The desktop app window should be open.
) else (
    echo.
    echo [ERROR] Failed to launch studio
    echo.
    pause
)







