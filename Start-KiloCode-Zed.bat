@echo off
REM Kilo Code Launcher for Zed Editor
REM Provides quick access to Kilo AI within Zed workflow

title Kilo Code - Zed Edition

echo.
echo ========================================
echo    KILO CODE FOR ZED EDITOR
echo ========================================
echo.
echo [1] Start Kilo Chat (Terminal)
echo [2] Open Zed with Kilo Panel
echo [3] Run Kilo Diagnostics
echo [4] Show Best Free Models (256K Context)
echo [5] Generate Project Context
echo [6] View Zed Integration Guide
echo [7] Update Kilo CLI
echo [8] Exit
echo.

:CHOICE
set /p choice="Select option (1-8): "

if "%choice%"=="1" goto START_CHAT
if "%choice%"=="2" goto START_ZED
if "%choice%"=="3" goto DIAGNOSE
if "%choice%"=="4" goto SHOW_MODELS
if "%choice%"=="5" goto CREATE_CONTEXT
if "%choice%"=="6" goto VIEW_GUIDE
if "%choice%"=="7" goto UPDATE_KILO
if "%choice%"=="8" goto EXIT
goto CHOICE

:START_CHAT
echo.
echo Starting Kilo in terminal...
echo Type /help for commands, /models to switch models
echo.
powershell -NoExit -Command "kilo"
goto END

:START_ZED
echo.
echo Launching Zed Editor...
echo Once open: Ctrl+` (terminal) then type 'kilo'
echo.

REM Try common Zed install locations
set zedPaths[0]=%LOCALAPPDATA%\Programs\Zed\zed.exe
set zedPaths[1]=%PROGRAMFILES%\Zed\zed.exe
set zedPaths[2]=%APPDATA%\Zed\zed.exe

for %%i in (0 1 2) do (
    if exist "!zedPaths[%%i]!" (
        start "" "!zedPaths[%%i]!"
        goto FOUND_ZED
    )
)

echo ERROR: Zed not found in standard locations.
echo Install from: https://zed.dev
pause
goto END

:FOUND_ZED
echo ✓ Zed launched
goto END

:DIAGNOSE
echo.
echo Running Kilo diagnostics...
powershell -Command "kilo --version"
powershell -Command "Get-Content $env:USERPROFILE\.config\kilo\config.json | ConvertFrom-Json | Select-Object model, agent"
pause
goto END

:SHOW_MODELS
echo.
echo ========================================
echo    BEST FREE MODELS FOR ZED (256K Context)
echo ========================================
echo.
echo 1. inclusionAI Ling-2.6-1T  [RECOMMENDED]
echo    Context: 262,144 tokens
echo    Rank:    #9 Code / #3 Debug
echo    Cost:    FREE
echo    Switch:  /model inclusionai/ling-2.6-1t:free
echo.
echo 2. Tencent Hy3 Preview
echo    Context: 262,144 tokens
echo    Rank:    #17 Code
echo    Cost:    FREE
echo    Switch:  /model tencent/hy3-preview:free
echo.
echo 3. NVIDIA Nemotron 3 Super
echo    Context: 262,144 tokens
echo    Rank:    #85 Code
echo    Cost:    FREE
echo    Switch:  /model nvidia/nemotron-3-super-120b-a12b:free
echo.
echo 4. StepFun Step 3.5 Flash
echo    Context: 262,144 tokens
echo    Rank:    #81 Code
echo    Cost:    $0.10/1M tokens
echo    Switch:  /model stepfun/step-3.5-flash
echo.
echo Live leaderboard: https://kilo.ai/models
echo.
pause
goto END

:CREATE_CONTEXT
echo.
echo Creating project context for current directory...
if exist "kilo_context.md" (
    echo File already exists. Overwrite? (Y/N)
    set /p overwrite=
    if /i not "%overwrite%"=="Y" goto END
)
powershell -Command "& {
    \$context = @'
# Project Context for Zed

**Generated:** $(Get-Date -Format 'yyyy-MM-dd')

## Overview
<!-- Describe your project -->

## Key Files
<!-- Kilo will auto-populate this -->

## Architecture
<!-- Add design notes -->

'@; \$context | Out-File -FilePath 'kilo_context.md' -Encoding UTF8; Write-Host '✓ Created kilo_context.md'}"
pause
goto END

:VIEW_GUIDE
echo.
echo Opening Zed integration guide...
if exist "KILO_FOR_ZED.md" (
    notepad KILO_FOR_ZED.md
) else (
    echo Guide not found. Run Setup-KiloCode-Zed.ps1 first.
    pause
)
goto END

:UPDATE_KILO
echo.
echo Updating Kilo CLI...
powershell -Command "npm update -g @kilocode/cli"
powershell -Command "kilo --version"
pause
goto END

:EXIT
echo.
echo Exiting Kilo Code Launcher...
exit /b 0

:END
echo.
pause
