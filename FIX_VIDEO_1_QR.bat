@echo off
REM Quick fixer for Video 1 QR code issue

color 0E
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              🔧 FIX VIDEO 1 - ADD QR CODE 🔧                     ║
echo ║                                                                  ║
echo ║         Adding QR code matching Video 2 style                   ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 📍 Locating Video 1...
set "VIDEO1=Lincoln's DEEP DIVE_ Military Draft Return _ No. 23 USC Avoids Nebraska's U.mp4"

if not exist "%VIDEO1%" (
    echo ❌ Video 1 not found in current directory!
    echo.
    echo Searching subdirectories...
    for /r %%i in ("%VIDEO1%") do (
        if exist "%%i" (
            echo ✅ Found: %%i
            set "VIDEO1=%%i"
            goto :found
        )
    )
    echo.
    echo ❌ Could not find Video 1
    echo Please run this script from the directory containing the video
    echo Or manually run: python ADD_QR_TO_VIDEO.py "path\to\video1.mp4"
    echo.
    pause
    exit /b 1
)

:found
echo ✅ Found Video 1!
echo.

echo 🎨 Adding QR code (Video 2 style)...
echo    • White QR on black background
echo    • Bottom-right corner
echo    • 270x270px with border
echo    • Bitcoin donation link
echo.

python ADD_QR_TO_VIDEO.py "%VIDEO1%"

if errorlevel 1 (
    echo.
    echo ❌ Failed to add QR code!
    echo.
    echo Possible issues:
    echo   • moviepy not installed: pip install moviepy
    echo   • qrcode not installed: pip install qrcode[pil]
    echo   • FFmpeg not in PATH
    echo.
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              ✅ QR CODE ADDED SUCCESSFULLY! ✅                   ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo 📹 New video created with QR code!
echo.
echo 💡 Next steps:
echo    1. Preview the new video to verify QR placement
echo    2. Scan QR with your phone to test it works
echo    3. Upload to YouTube if satisfied
echo.
echo The updated video is in the same folder as the original.
echo Look for: *_with_qr.mp4
echo.
pause

