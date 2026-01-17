#!/bin/bash
# SCARIFY Channel Factory - Deployment Script

set -e

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║              🏭 SCARIFY CHANNEL FACTORY - DEPLOYMENT                        ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
python3 -c "import json, pathlib" 2>/dev/null && echo "✅ Core libraries available" || echo "⚠️  Core libraries missing"

# Check API keys (optional)
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not set (will use template fallback)"
else
    echo "✅ ANTHROPIC_API_KEY set"
fi

if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "⚠️  ELEVENLABS_API_KEY not set (audio generation will fail)"
else
    echo "✅ ELEVENLABS_API_KEY set"
fi

echo ""

# Setup channels
echo "🏭 Setting up default channels..."
python3 unified_pipeline.py --setup

echo ""
echo "📊 System status:"
python3 unified_pipeline.py --status

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Set API keys:"
echo "      export ANTHROPIC_API_KEY='your_key'"
echo "      export ELEVENLABS_API_KEY='your_key'"
echo ""
echo "   2. Generate test video:"
echo "      python3 unified_pipeline.py --channel horror_en_0 --topic 'Test' --generate 1"
echo ""
echo "   3. Generate batch:"
echo "      python3 unified_pipeline.py --generate 10"
echo ""
echo "   4. Start automated schedule:"
echo "      python3 production_scheduler.py --start-schedule"
echo ""
