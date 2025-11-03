@echo off
chcp 65001 >nul
cd /d "F:\AI_Oracle_Root\scarify\abraham_horror"
echo ========================================================================
echo PROJECT COGNITOHAZARD - AI Horror Series
echo COGNITIVE HAZE: The AI Horror Files
echo ========================================================================
echo.
echo Series: The Archivist's found audio logs
echo Format: 8+ minutes, glitchcore aesthetic
echo Features: Bitcoin QR code, multilingual triggers, analog horror
echo.
python -Xutf8 PROJECT_COGNITOHAZARD.py %*
if errorlevel 1 (
    echo.
    echo ERROR: Script failed. Check output above.
    pause
)


