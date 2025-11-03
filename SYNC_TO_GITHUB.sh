#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#   SCARIFY EMPIRE - GitHub Sync Script (Linux/Mac)
# ═══════════════════════════════════════════════════════════════

clear

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              📤 SYNCING TO GITHUB 📤                             ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

cd "$(dirname "$0")"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    echo ""
    echo "Install with:"
    echo "  sudo apt install git     # Ubuntu/Debian"
    echo "  sudo yum install git     # RedHat/CentOS"
    echo "  brew install git         # macOS"
    echo ""
    exit 1
fi

# Check if this is a git repository
if [ ! -d .git ]; then
    echo "⚠️  Not a Git repository yet!"
    echo ""
    echo "First-time setup:"
    echo ""
    read -p "Enter your GitHub username: " username
    echo ""
    echo "Initializing repository..."
    git init
    git remote add origin "https://github.com/$username/scarify.git"
    echo ""
    echo "✅ Repository initialized!"
    echo ""
fi

echo "[1/5] 📊 Checking status..."
git status
echo ""

echo "[2/5] ➕ Adding all files (respecting .gitignore)..."
git add .
echo "       ✅ Files staged!"
echo ""

echo "[3/5] 💬 Creating commit..."
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
git commit -m "Update: $timestamp"
echo "       ✅ Commit created!"
echo ""

echo "[4/5] 📤 Pushing to GitHub..."
git push -u origin main 2>/dev/null || {
    echo ""
    echo "⚠️  First time push? Trying with branch setup..."
    git branch -M main
    git push -u origin main
}
echo "       ✅ Pushed to GitHub!"
echo ""

echo "[5/5] ✅ Getting repository URL..."
git remote get-url origin
echo ""

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                                                                  ║"
echo "║              ✅ GITHUB SYNC COMPLETE! ✅                         ║"
echo "║                                                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Your code is now safely backed up on GitHub!"
echo ""
echo "🌐 View it at:"
echo "   https://github.com/YOUR_USERNAME/scarify"
echo ""
echo "💡 Next time, just run this script to sync!"
echo ""

