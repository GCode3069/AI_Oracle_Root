@echo off
title SCARIFY - Create 15 Branded Channels
color 0C
cls

echo.
echo ========================================
echo   SCARIFY - Channel Creator
echo ========================================
echo.
echo This will create 15 uniformly branded
echo YouTube channels automatically.
echo.
echo You'll need:
echo   - 15 different Google accounts
echo   - 5-10 minutes per channel
echo   - Total time: ~90 minutes
echo.
echo ========================================
echo.
pause

cd /d "F:\AI_Oracle_Root\scarify"

echo.
echo Starting automatic channel creation...
echo.

python AUTO_CHANNEL_CREATOR.py create

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo View your channels:
echo   python AUTO_CHANNEL_CREATOR.py list
echo.
echo Start uploading:
echo   python MULTI_CHANNEL_UPLOADER.py abraham_horror/youtube_ready round-robin
echo.
pause


