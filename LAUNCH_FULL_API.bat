@echo off
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║ ABRAHAM LINCOLN - FULL API (OPTIMIZED)                            ║
echo ║ Choose mode:                                                       ║
echo ║ 1. WITH B-roll (better quality, slower)                            ║
echo ║ 2. WITHOUT B-roll (faster)                                         ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
choice /C 12 /N /M "Select mode (1 or 2): "

if errorlevel 2 goto fast
if errorlevel 1 goto quality

:quality
powershell -ExecutionPolicy Bypass -File ".\BOOTSTRAP_ABE_FULL_API.ps1" -Videos 10
goto end

:fast
powershell -ExecutionPolicy Bypass -File ".\BOOTSTRAP_ABE_FULL_API.ps1" -Videos 10 -SkipBroll
goto end

:end
pause


