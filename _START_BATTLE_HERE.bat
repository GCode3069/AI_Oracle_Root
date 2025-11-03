@echo off
REM Quick launcher for LLM Battle Royale after reset

cd /d F:\AI_Oracle_Root\scarify

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║        🏆 LLM BATTLE ROYALE - QUICK LAUNCHER 🏆                       ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo [1] TEST MODE - Verify systems working
echo [2] START COMPETITION - Full battle launch
echo [3] READ INSTRUCTIONS - Open quick start guide
echo [4] EXIT
echo.

set /p choice="Select option (1-4): "

if "%choice%"=="1" (
    echo.
    echo [LAUNCHING TEST MODE...]
    powershell -ExecutionPolicy Bypass -File "LAUNCH_BATTLE_AFTER_RESET.ps1" -TestMode
    pause
) else if "%choice%"=="2" (
    echo.
    set /p llmname="Enter your LLM name (e.g., Claude-Sonnet-4): "
    set /p videocount="Enter number of videos to generate (e.g., 50): "
    echo.
    echo [LAUNCHING COMPETITION...]
    echo   Competitor: %llmname%
    echo   Videos: %videocount%
    echo.
    powershell -ExecutionPolicy Bypass -File "LAUNCH_BATTLE_AFTER_RESET.ps1" -LLMName "%llmname%" -VideoCount %videocount%
    pause
) else if "%choice%"=="3" (
    echo.
    echo [OPENING QUICK START GUIDE...]
    start BATTLE_QUICK_START_AFTER_RESET.txt
    pause
) else (
    echo.
    echo Exiting...
    exit /b
)



