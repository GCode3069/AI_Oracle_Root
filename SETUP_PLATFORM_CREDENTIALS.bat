@echo off
title SCARIFY - Platform Credentials Setup
color 0A
cls

echo.
echo ================================================================
echo   MULTI-PLATFORM CREDENTIALS SETUP
echo ================================================================
echo.
echo This will guide you through setting up credentials for:
echo   [1] YouTube (already done)
echo   [2] TikTok
echo   [3] Instagram
echo   [4] Facebook
echo   [5] Twitter/X
echo   [6] Reddit
echo   [7] Telegram
echo.
echo You'll need to:
echo   - Create developer accounts
echo   - Get API keys
echo   - Store credentials securely
echo.
pause

cd /d "F:\AI_Oracle_Root\scarify"

REM Create directories
if not exist "config\platforms" mkdir config\platforms

echo.
echo ================================================================
echo   [1/6] YOUTUBE - Already Configured
echo ================================================================
echo.

if exist "config\credentials\youtube\client_secrets.json" (
    echo [OK] YouTube credentials found
) else (
    echo [WARN] YouTube credentials missing
    echo Get from: https://console.cloud.google.com
)

echo.
echo ================================================================
echo   [2/6] TIKTOK SETUP
echo ================================================================
echo.
echo TikTok doesn't have a public upload API yet.
echo We'll use browser automation (Playwright).
echo.
echo Setup steps:
echo   1. You'll login manually first time
echo   2. Session will be saved for future uploads
echo   3. Browser will open when you first upload
echo.
echo [READY] TikTok will use browser automation
pause

echo.
echo ================================================================
echo   [3/6] INSTAGRAM SETUP
echo ================================================================
echo.
echo Instagram setup:
echo.
echo [MANUAL] You'll login when first uploading
echo The script will save your session for future use.
echo.
echo Username/password will be requested at first upload.
echo.
pause

echo.
echo ================================================================
echo   [4/6] FACEBOOK SETUP
echo ================================================================
echo.
echo Facebook requires:
echo   1. Facebook Developer Account
echo   2. Create App at: https://developers.facebook.com
echo   3. Get App ID and App Secret
echo.
echo For now, we'll use browser automation (like TikTok).
echo.
echo [READY] Facebook will use browser automation
pause

echo.
echo ================================================================
echo   [5/6] TWITTER/X SETUP
echo ================================================================
echo.
echo Twitter API setup:
echo   1. Go to: https://developer.twitter.com
echo   2. Create project and app
echo   3. Get API Key, API Secret, Access Token, Access Secret
echo.

set /p twitter_key="Enter Twitter API Key (or press Enter to skip): "
set /p twitter_secret="Enter Twitter API Secret (or press Enter to skip): "
set /p twitter_access="Enter Twitter Access Token (or press Enter to skip): "
set /p twitter_access_secret="Enter Twitter Access Secret (or press Enter to skip): "

if not "%twitter_key%"=="" (
    echo { > config\platforms\twitter_credentials.json
    echo   "api_key": "%twitter_key%", >> config\platforms\twitter_credentials.json
    echo   "api_secret": "%twitter_secret%", >> config\platforms\twitter_credentials.json
    echo   "access_token": "%twitter_access%", >> config\platforms\twitter_credentials.json
    echo   "access_secret": "%twitter_access_secret%" >> config\platforms\twitter_credentials.json
    echo } >> config\platforms\twitter_credentials.json
    echo [OK] Twitter credentials saved
) else (
    echo [SKIP] Twitter - setup later
)

echo.
echo ================================================================
echo   [6/6] REDDIT SETUP
echo ================================================================
echo.
echo Reddit API setup:
echo   1. Go to: https://www.reddit.com/prefs/apps
echo   2. Create app (select "script" type)
echo   3. Get Client ID and Client Secret
echo.

set /p reddit_client="Enter Reddit Client ID (or press Enter to skip): "
set /p reddit_secret="Enter Reddit Client Secret (or press Enter to skip): "
set /p reddit_username="Enter Reddit Username (or press Enter to skip): "
set /p reddit_password="Enter Reddit Password (or press Enter to skip): "

if not "%reddit_client%"=="" (
    echo { > config\platforms\reddit_credentials.json
    echo   "client_id": "%reddit_client%", >> config\platforms\reddit_credentials.json
    echo   "client_secret": "%reddit_secret%", >> config\platforms\reddit_credentials.json
    echo   "user_agent": "SCARIFY_Bot/1.0", >> config\platforms\reddit_credentials.json
    echo   "username": "%reddit_username%", >> config\platforms\reddit_credentials.json
    echo   "password": "%reddit_password%" >> config\platforms\reddit_credentials.json
    echo } >> config\platforms\reddit_credentials.json
    echo [OK] Reddit credentials saved
) else (
    echo [SKIP] Reddit - setup later
)

echo.
echo ================================================================
echo   SETUP COMPLETE
echo ================================================================
echo.
echo Credential status:
echo   [OK] YouTube - Ready
echo   [OK] TikTok - Browser automation ready
echo   [OK] Instagram - Will login at first upload
echo   [OK] Facebook - Browser automation ready

if exist "config\platforms\twitter_credentials.json" (
    echo   [OK] Twitter - Credentials saved
) else (
    echo   [SKIP] Twitter - Not configured
)

if exist "config\platforms\reddit_credentials.json" (
    echo   [OK] Reddit - Credentials saved
) else (
    echo   [SKIP] Reddit - Not configured
)

echo.
echo ================================================================
echo   NEXT STEPS
echo ================================================================
echo.
echo Test with 1 video:
echo   python MULTI_PLATFORM_UPLOADER.py --test
echo.
echo Upload 5 videos:
echo   python MULTI_PLATFORM_UPLOADER.py --count 5
echo.
echo Upload all 111 videos to all platforms:
echo   python MULTI_PLATFORM_UPLOADER.py --count 111 --platforms all
echo.
echo Upload to specific platforms only:
echo   python MULTI_PLATFORM_UPLOADER.py --count 10 --platforms youtube tiktok instagram
echo.
pause

