@echo off
title ABRAHAM STUDIO Web Server
echo.
echo ================================================================
echo    ABRAHAM STUDIO - WEB SERVER FOR IPHONE
echo ================================================================
echo.

echo Installing dependencies...
pip install flask flask-cors -q

echo.
echo Starting web server...
echo.
echo MOBILE ACCESS:
echo   http://[YOUR_IP]:5000
echo.
echo Find your IP address:
ipconfig | findstr IPv4

echo.
echo ================================================================
echo    Server starting...
echo ================================================================
echo.
echo Press Ctrl+C to stop
echo.

python STUDIO_WEB_SERVER.py

pause







