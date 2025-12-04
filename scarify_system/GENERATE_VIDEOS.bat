@echo off
REM SCARIFY Video Generator - Windows Batch File
REM Quick launcher for SCARIFY video generation

cd /d D:\AI_Oracle_Projects\Active\Scripts

echo ============================================================
echo SCARIFY VIDEO GENERATOR
echo ============================================================
echo.

:menu
echo Select an option:
echo.
echo 1. Generate 1 test video
echo 2. Generate 10 videos
echo 3. Generate 25 videos (daily batch)
echo 4. Generate 50 videos (large batch)
echo 5. Test mode (mock, no API calls)
echo 6. View statistics
echo 7. Exit
echo.

set /p choice="Enter choice (1-7): "

if "%choice%"=="1" (
    echo Generating 1 test video...
    python run_batch.py 1
    goto end
)

if "%choice%"=="2" (
    echo Generating 10 videos...
    python run_batch.py 10
    goto end
)

if "%choice%"=="3" (
    echo Generating 25 videos (daily batch)...
    python run_batch.py 25
    goto end
)

if "%choice%"=="4" (
    echo.
    echo WARNING: This will generate 50 videos
    echo Estimated cost: $1.00 - $2.00
    set /p confirm="Continue? (Y/N): "
    if /i "%confirm%"=="Y" (
        python run_batch.py 50
    ) else (
        echo Cancelled.
    )
    goto end
)

if "%choice%"=="5" (
    echo Running in TEST MODE (no API calls)...
    python run_batch.py 5 --mock
    goto end
)

if "%choice%"=="6" (
    echo.
    echo ============================================================
    echo CACHE STATISTICS
    echo ============================================================
    python -c "from KLING_CACHE import KlingCache; c = KlingCache('D:/AI_Oracle_Projects/Assets/Kling_Cache'); s = c.get_stats(); print(f'\nCached videos: {s[\"total_entries\"]}'); print(f'Total reuses: {s[\"total_reuses\"]}'); print(f'Cost saved: ${s[\"cost_saved\"]:.2f}'); print(f'Cache size: {s[\"cache_size_mb\"]:.1f} MB')"
    echo.
    goto end
)

if "%choice%"=="7" (
    echo Goodbye!
    goto exit
)

echo Invalid choice. Please try again.
echo.
goto menu

:end
echo.
echo ============================================================
echo COMPLETE!
echo.
echo Output locations:
echo   WARNING videos: D:\AI_Oracle_Projects\Output\Generated\Winners\
echo   COMEDY videos:  D:\AI_Oracle_Projects\Output\Generated\Comedy\
echo ============================================================
echo.
pause
goto exit

:exit
