@echo off
echo ==============================================
echo ABRAHAM LINCOLN - ULTIMATE FINAL EDITION
echo ==============================================
echo.

cd /d "F:\AI_Oracle_Root\scarify"

if not exist "ABRAHAM_ULTIMATE_FINAL.py" (
    echo ERROR: ABRAHAM_ULTIMATE_FINAL.py not found!
    pause
    exit /b 1
)

echo Generating videos...
echo.

python ABRAHAM_ULTIMATE_FINAL.py 50

echo.
echo Done!
pause







