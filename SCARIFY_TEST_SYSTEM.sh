#!/bin/bash
# SCARIFY System Test Script

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "🧪 SCARIFY SYSTEM TEST"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "📋 Checking all scripts exist..."
echo ""

scripts=(
    "DUAL_STYLE_GENERATOR.py"
    "KLING_CLIENT.py"
    "KLING_CACHE.py"
    "SUBLIMINAL_AUDIO.py"
    "VIDEO_LAYOUT.py"
    "SCARIFY_COMPLETE.py"
)

missing=0
for script in "${scripts[@]}"; do
    if [ -f "/workspace/$script" ]; then
        echo "  ✅ $script"
    else
        echo "  ❌ $script (MISSING)"
        missing=$((missing + 1))
    fi
done

echo ""
if [ $missing -eq 0 ]; then
    echo "✅ All 6 scripts present!"
    echo ""
    echo "🚀 Ready to test! Run:"
    echo "   python /workspace/SCARIFY_COMPLETE.py"
else
    echo "❌ $missing script(s) missing!"
    echo ""
    echo "📝 Note: Some scripts may need to be created from templates"
    echo "   Check: /workspace/SHUTDOWN_SAVE_2025-12-04_04-34-58/"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
