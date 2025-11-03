@echo off
echo ========================================
echo INSTALLING CURSOR MARKETPLACE TOOLS
echo ========================================
echo.

echo Installing Python optimization tools...
pip install --quiet rich progressbar2 pysnooper
echo.

echo Installing speed testing tools...
pip install --quiet blackbird memory-profiler
echo.

echo Done! Tools installed:
echo - Rich: Beautiful console output
echo - ProgressBar2: Visual progress tracking
echo - PySnooper: Advanced debugging
echo - Blackbird: Speed profiling
echo.

pause








