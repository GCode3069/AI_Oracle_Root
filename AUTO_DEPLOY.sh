#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#   SCARIFY EMPIRE - AUTO DEPLOYMENT (Linux/Mac)
#   One command = Complete setup!
# ═══════════════════════════════════════════════════════════════

clear

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              🤖 SCARIFY EMPIRE - AUTO DEPLOY 🤖                  ║"
echo "║                                                                  ║"
echo "║           Complete Automated Setup & Configuration              ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo ""

cd "$(dirname "$0")"

echo "🚀 Starting self-deployment agent..."
echo ""
sleep 2

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python is not installed!"
    echo ""
    echo "Please install Python 3.8+ with:"
    echo "  sudo apt install python3 python3-pip    # Ubuntu/Debian"
    echo "  sudo yum install python3 python3-pip    # RedHat/CentOS"
    echo "  brew install python3                    # macOS"
    echo ""
    exit 1
fi

echo "✅ Python found!"
echo ""

# Make this script executable
chmod +x "$0"

# Run the self-deployment script
$PYTHON_CMD SELF_DEPLOY.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Deployment failed!"
    echo ""
    echo "Check the error messages above and try again."
    echo ""
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              ✅ AUTO DEPLOYMENT COMPLETE! ✅                     ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 Your empire is ready!"
echo ""
echo "Next step: ./LAUNCH_EMPIRE.sh"
echo ""

