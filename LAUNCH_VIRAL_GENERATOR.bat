@echo off
title VIRAL OPTIMIZED GENERATOR
echo.
echo ================================================================
echo    VIRAL OPTIMIZED GENERATOR - CROSS PLATFORM
echo ================================================================
echo.

cd /d "F:\AI_Oracle_Root\scarify"

if "%1"=="" (
    set COUNT=5
) else (
    set COUNT=%1
)

echo Generating %COUNT% viral-optimized video(s)...
echo.

python VIRAL_OPTIMIZED_GENERATOR.py %COUNT%

echo.
echo ================================================================
echo    COMPLETE!
echo ================================================================
echo.

pause







