@echo off
echo ============================================================
echo LINCOLN'S WARNING SYSTEM - QUICK START
echo ============================================================
echo.
echo Setting up...
pip install requests beautifulsoup4 lxml pillow qrcode
echo.
echo Enter your ElevenLabs API key:
set /p ELEVENLABS_KEY="API Key: "
setx ELEVENLABS_API_KEY "%ELEVENLABS_KEY%"
echo.
echo ============================================================
echo GENERATING YOUR FIRST VIDEO
echo ============================================================
echo.
set EPISODE_NUM=1000
python abraham_MAX_HEADROOM.py 1
echo.
echo ============================================================
echo DONE! Check the uploaded/ folder for your video!
echo ============================================================
pause
