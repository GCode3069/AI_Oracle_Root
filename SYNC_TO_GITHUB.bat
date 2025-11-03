@echo off
REM ═══════════════════════════════════════════════════════════════
REM   SCARIFY EMPIRE - GitHub Sync Script (Windows)
REM ═══════════════════════════════════════════════════════════════

color 0E
cls

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              📤 SYNCING TO GITHUB 📤                             ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

REM Check if this is a git repository
if not exist .git (
    echo ⚠️  Not a Git repository yet!
    echo.
    echo First-time setup:
    echo.
    set /p username="Enter your GitHub username: "
    echo.
    echo Initializing repository...
    git init
    git remote add origin https://github.com/!username!/scarify.git
    echo.
    echo ✅ Repository initialized!
    echo.
)

echo [1/5] 📊 Checking status...
git status
echo.

echo [2/5] ➕ Adding all files (respecting .gitignore)...
git add .
echo        ✅ Files staged!
echo.

echo [3/5] 💬 Creating commit...
set timestamp=%date% %time%
git commit -m "Update: %timestamp%"
echo        ✅ Commit created!
echo.

echo [4/5] 📤 Pushing to GitHub...
git push -u origin main 2>nul
if errorlevel 1 (
    echo.
    echo ⚠️  First time push? Try this:
    git branch -M main
    git push -u origin main
)
echo        ✅ Pushed to GitHub!
echo.

echo [5/5] ✅ Getting repository URL...
git remote get-url origin
echo.

echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║                                                                  ║
echo ║              ✅ GITHUB SYNC COMPLETE! ✅                         ║
echo ║                                                                  ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo Your code is now safely backed up on GitHub!
echo.
echo 🌐 View it at:
echo    https://github.com/YOUR_USERNAME/scarify
echo.
echo 💡 Next time, just run this script to sync!
echo.
pause

