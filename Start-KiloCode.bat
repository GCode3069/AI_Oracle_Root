@echo off
REM Kilo Code Quick Launcher for zED IDE Environment
REM This script provides fast access to Kilo AI agent

title Kilo Code AI Agent - zED Workspace

echo.
echo ========================================
echo    KILO CODE - AI CODING ASSISTANT
echo ========================================
echo.
echo [1] Start Kilo CLI (Interactive Chat)
echo [2] Launch VS Code + Kilo Extension
echo [3] Run Kilo Diagnostics
echo [4] Show Free Models List
echo [5] Create Project Context File
echo [6] Update Kilo to Latest Version
echo [7] View Quick Start Guide
echo [8] Exit
echo.

:CHOICE
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto START_CLI
if "%choice%"=="2" goto START_VSCODE
if "%choice%"=="3" goto DIAGNOSE
if "%choice%"=="4" goto SHOW_MODELS
if "%choice%"=="5" goto CREATE_CONTEXT
if "%choice%"=="6" goto UPDATE_KILO
if "%choice%"=="7" goto VIEW_GUIDE
if "%choice%"=="8" goto EXIT
goto CHOICE

:START_CLI
echo.
echo Starting Kilo CLI...
echo Type /help for commands, /models to switch models
echo.
kilo
goto END

:START_VSCODE
echo.
echo Launching VS Code with Kilo extension...
if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" (
    start "" "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
) else if exist "%ProgramFiles%\Microsoft VS Code\Code.exe" (
    start "" "%ProgramFiles%\Microsoft VS Code\Code.exe"
) else (
    echo ERROR: VS Code not found. Install from https://code.visualstudio.com/
    pause
)
goto END

:DIAGNOSE
echo.
echo Running Kilo Integration Diagnostics...
powershell -Command ".\Kilo-Utils.ps1" -NoProfile -Command "Test-KiloIntegration"
pause
goto END

:SHOW_MODELS
echo.
echo ========================================
echo    AVAILABLE FREE MODELS (256K Context)
echo ========================================
echo.
echo 1. inclusionAI Ling-2.6-1T (RECOMMENDED)
echo    - Context: 262,144 tokens
echo    - Code Rank: #9, Debug Rank: #3
echo    - Cost: FREE
echo    - Use: /model inclusionai/ling-2.6-1t:free
echo.
echo 2. Tencent Hy3 Preview
echo    - Context: 262,144 tokens
echo    - Code Rank: #17
echo    - Cost: FREE
echo    - Use: /model tencent/hy3-preview:free
echo.
echo 3. NVIDIA Nemotron 3 Super
echo    - Context: 262,144 tokens
echo    - Code Rank: #85
echo    - Cost: FREE
echo    - Use: /model nvidia/nemotron-3-super-120b-a12b:free
echo.
echo 4. StepFun Step 3.5 Flash
echo    - Context: 262,144 tokens
echo    - Cost: $0.10/1M tokens input, $0.30/1M output
echo    - Use: /model stepfun/step-3.5-flash
echo.
echo Leaderboard: https://kilo.ai/models
echo.
pause
goto END

:CREATE_CONTEXT
echo.
echo Creating project context file...
powershell -Command ".\Kilo-Utils.ps1" -NoProfile -Command "New-KiloProjectContext"
pause
goto END

:UPDATE_KILO
echo.
echo Updating Kilo CLI...
powershell -Command ".\Kilo-Utils.ps1" -NoProfile -Command "Update-Kilo"
pause
goto END

:VIEW_GUIDE
echo.
echo Opening Quick Start Guide...
if exist ".\KILO_QUICKSTART.md" (
    notepad .\KILO_QUICKSTART.md
) else (
    echo Guide not found. Run Setup-KiloCode.ps1 first.
    pause
)
goto END

:EXIT
echo.
echo Exiting Kilo Code Launcher...
exit /b 0

:END
echo.
pause
