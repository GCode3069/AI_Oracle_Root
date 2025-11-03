@echo off
echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🎃 ABRAHAM HORROR - START                              ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo How many videos?
echo  1 = Quick test
echo  5 = Small batch  
echo 10 = Halloween campaign
echo.
set /p count="Enter number (1-10): "

powershell -ExecutionPolicy Bypass -File "DEPLOY_ABRAHAM.ps1" -Count %count%

echo.
echo ✅ Done! Check youtube_ready folder
pause

