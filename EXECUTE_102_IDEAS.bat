@echo off
title SCARIFY - 102 Horror Ideas Production
color 0C
cls

echo.
echo ========================================
echo   SCARIFY - 102 IDEAS PRODUCTION
echo ========================================
echo.
echo This will generate videos from your
echo 102 unique horror ideas database.
echo.
echo NO MORE REPETITIVE CONTENT!
echo.
echo ========================================
echo.
echo Choose production mode:
echo.
echo 1. TEST (10 videos)
echo 2. BATCH 1 (Ideas 1-50)
echo 3. BATCH 2 (Ideas 51-100)
echo 4. FULL RUN (All 102)
echo 5. CUSTOM
echo.
set /p choice="Enter choice (1-5): "

cd /d "F:\AI_Oracle_Root\scarify"

if "%choice%"=="1" (
    echo.
    echo Generating 10 test videos...
    powershell -ExecutionPolicy Bypass -File MASS_PRODUCE_102_IDEAS.ps1 -BatchSize 10 -StartFrom 1
)

if "%choice%"=="2" (
    echo.
    echo Generating batch 1 (Ideas 1-50)...
    powershell -ExecutionPolicy Bypass -File MASS_PRODUCE_102_IDEAS.ps1 -BatchSize 50 -StartFrom 1
)

if "%choice%"=="3" (
    echo.
    echo Generating batch 2 (Ideas 51-100)...
    powershell -ExecutionPolicy Bypass -File MASS_PRODUCE_102_IDEAS.ps1 -BatchSize 50 -StartFrom 51
)

if "%choice%"=="4" (
    echo.
    echo Generating ALL 102 ideas...
    powershell -ExecutionPolicy Bypass -File MASS_PRODUCE_102_IDEAS.ps1 -BatchSize 102 -StartFrom 1
)

if "%choice%"=="5" (
    echo.
    set /p custom_count="How many videos? "
    set /p custom_start="Start from idea #? "
    powershell -ExecutionPolicy Bypass -File MASS_PRODUCE_102_IDEAS.ps1 -BatchSize %custom_count% -StartFrom %custom_start%
)

echo.
echo ========================================
echo   Production Complete!
echo ========================================
echo.
pause


