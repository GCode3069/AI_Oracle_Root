@echo off
cd /d "F:\AI_Oracle_Root\scarify"
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║ MASTER CONTROL DASHBOARD                                          ║
echo ║ Auto-Monitor, Analyze, Strategize, Execute                        ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo Channel: DissWhatImSayin (UCS5pEpSCw8k4wene0iv0uAg)
echo.
echo Options:
echo [1] Single optimization cycle
echo [2] Continuous monitoring (every 6 hours)
echo.
choice /C 12 /N /M "Select mode (1 or 2): "

if errorlevel 2 goto continuous
if errorlevel 1 goto single

:single
python MASTER_CONTROL_DASHBOARD.py
goto end

:continuous
echo.
echo Starting continuous monitoring...
echo Press Ctrl+C to stop
echo.
python MASTER_CONTROL_DASHBOARD.py --continuous
goto end

:end
pause


