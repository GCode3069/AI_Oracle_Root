@echo off
REM ============================================================================
REM QUICK LAUNCHER - BATTLE CHALLENGE DEPLOYMENT
REM ============================================================================

echo.
echo ###############################################################################
echo #                                                                             #
echo #              BATTLE CHALLENGE - QUICK DEPLOY                                #
echo #                                                                             #
echo ###############################################################################
echo.
echo [1] Round 1 - 5 videos (Test Mode)
echo [2] Round 1 - 10 videos (Aggressive)
echo [3] Full Competition - 12 rounds x 5 videos (60 total)
echo [4] Full Competition - 12 rounds x 10 videos (120 total)
echo [5] Custom
echo [0] Exit
echo.
echo ###############################################################################
echo.

set /p choice="Select option (0-5): "

if "%choice%"=="1" (
    powershell -ExecutionPolicy Bypass -File DEPLOY_CHALLENGE_NOW.ps1 -Round 1 -VideosPerRound 5 -StartEpisode 20000
    goto end
)

if "%choice%"=="2" (
    powershell -ExecutionPolicy Bypass -File DEPLOY_CHALLENGE_NOW.ps1 -Round 1 -VideosPerRound 10 -StartEpisode 20000
    goto end
)

if "%choice%"=="3" (
    powershell -ExecutionPolicy Bypass -File DEPLOY_CHALLENGE_NOW.ps1 -FullCompetition -VideosPerRound 5 -StartEpisode 20000
    goto end
)

if "%choice%"=="4" (
    powershell -ExecutionPolicy Bypass -File DEPLOY_CHALLENGE_NOW.ps1 -FullCompetition -VideosPerRound 10 -StartEpisode 20000
    goto end
)

if "%choice%"=="5" (
    echo.
    set /p round="Enter round number (1-12): "
    set /p videos="Enter videos per round: "
    set /p episode="Enter starting episode number: "
    powershell -ExecutionPolicy Bypass -File DEPLOY_CHALLENGE_NOW.ps1 -Round %round% -VideosPerRound %videos% -StartEpisode %episode%
    goto end
)

if "%choice%"=="0" (
    echo.
    echo Exiting...
    goto end
)

echo.
echo Invalid option!
pause
goto end

:end
echo.
pause


