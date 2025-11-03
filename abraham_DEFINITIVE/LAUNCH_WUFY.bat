@echo off
echo ========================================
echo WUFY AGENT - SCARIFY BLITZKRIEG
echo 15 Channels | 72 Hours | $15K BTC Goal
echo ========================================
echo.

cd /d "F:\AI_Oracle_Root\scarify"

echo Installing Playwright...
pip install playwright -q

echo Installing browser...
python -m playwright install chromium

echo.
echo Starting WUFY agent...
echo.

python WUFY_AGENT.py test

pause

