@echo off
REM Quick progress checker for mass generation

echo.
echo ###############################################################################
echo   CHECKING GENERATION PROGRESS
echo ###############################################################################
echo.

cd /d F:\AI_Oracle_Root\scarify\abraham_horror\uploaded

echo Latest 10 videos:
echo.
dir *.mp4 /o-d /b 2>nul | findstr /n "^" | findstr "^[1-9]:" | findstr /v "^1[0-9]:"

echo.
echo Total videos:
dir *.mp4 2>nul | find /c ".mp4"

echo.
echo Looking for test video (TEST_ChatGPT_30000):
dir *TEST*.mp4 2>nul | find /v ""

echo.
echo Looking for ChatGPT videos:
dir *ChatGPT*.mp4 2>nul | find /v ""

echo.
echo Looking for Grok videos:
dir *Grok*.mp4 2>nul | find /v ""

echo.
echo Looking for MIXED videos:
dir *MIXED*.mp4 2>nul | find /v ""

echo.
echo ###############################################################################
echo   Check again in a few minutes if videos are still generating
echo ###############################################################################
echo.

pause


