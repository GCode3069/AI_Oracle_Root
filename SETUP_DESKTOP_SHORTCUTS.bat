@echo off
REM Create desktop shortcuts - One click setup!

color 0B
cls

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              🖥️  DESKTOP SHORTCUT CREATOR 🖥️                    ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo Creating desktop shortcuts...
echo.

pwsh -ExecutionPolicy Bypass -File CREATE_DESKTOP_SHORTCUTS.ps1

if errorlevel 1 (
    echo.
    echo ⚠️  PowerShell script failed. Trying fallback method...
    echo.
    
    REM Create simple batch launcher on desktop
    set DESKTOP=%USERPROFILE%\Desktop
    
    echo @echo off > "%DESKTOP%\Scarify Empire.bat"
    echo cd /d "%~dp0" >> "%DESKTOP%\Scarify Empire.bat"
    echo call "%CD%\LAUNCH_EMPIRE.bat" >> "%DESKTOP%\Scarify Empire.bat"
    
    echo ✅ Created: Scarify Empire.bat on desktop
)

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              ✅ DESKTOP SHORTCUTS CREATED! ✅                    ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Check your desktop for new shortcuts!
echo.
pause

