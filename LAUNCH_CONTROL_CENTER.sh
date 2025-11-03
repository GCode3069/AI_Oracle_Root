#!/bin/bash
# Launch Scarify Empire Control Center Dashboard (Linux/Mac)

echo "========================================"
echo " Scarify Empire - Control Center"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "Starting Control Center Dashboard..."
echo ""

if command -v python3 &> /dev/null; then
    python3 SCARIFY_CONTROL_CENTER.pyw &
elif command -v python &> /dev/null; then
    python SCARIFY_CONTROL_CENTER.pyw &
else
    echo "Error: Python not found!"
    echo "Please install Python 3.8+"
    exit 1
fi

echo "Control Center launched!"

