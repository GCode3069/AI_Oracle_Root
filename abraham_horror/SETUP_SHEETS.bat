@echo off
title Google Sheets Setup - One Click
color 0A

cd /d "F:\AI_Oracle_Root\scarify\abraham_horror"

echo.
echo ========================================
echo   GOOGLE SHEETS AUTOMATIC SETUP
echo ========================================
echo.
echo   This will guide you through:
echo   1. Downloading service account key
echo   2. Setting up credentials
echo   3. Sharing your Google Sheet
echo   4. Testing the connection
echo.
echo ========================================
echo.

powershell -ExecutionPolicy Bypass -File "SETUP_SHEETS_AUTOMATIC.ps1"

echo.
pause




