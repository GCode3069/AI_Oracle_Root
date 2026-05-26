# 🚀 SCARIFY Pi Agent Integration

## Overview

Hybrid cost-optimized pipeline for SCARIFY Global Comedy Empire:

- **Stage 1:** Headline classification (Ollama local, FREE)
- **Stage 2:** Script generation (Groq, $0.40/1M tokens)
- **Stage 3:** Spirit refinement (Nous Hermes, $10 budget)
- **Stages 4-7:** Local rendering (FREE - Kokoro TTS, FFmpeg, Postiz)

## Cost Strategy

| Component | Cost | Used For |
|-----------|------|----------|
| Ollama Mistral | FREE | Classify headlines by importance (1-10) |
| Groq Mixtral | ~$0.001/script | Generate script templates |
| Nous Hermes | ~$0.05/script | Premium refinement (only high importance) |
| Kokoro TTS | FREE | Local voice synthesis (DirectML on GPU) |
| FFmpeg + LivePortrait | FREE | Video rendering |
| Postiz | Platform-dependent | Distribution |

## Expected Cost Per 100 Videos

```
Ollama (100):     $0.00
Groq (100):       $0.04
Nous (20):        $1.00
─────────────────
Total:            $1.04
Per video:        $0.010
```

## Files

- **empire_agent_core.ts** - Pi Agent setup with tools
- **cost_tracker.ts** - Real-time budget monitoring
- **batch_processor.ts** - Process 20+ headlines
- **PI_AGENT_INTEGRATION.md** - This file

## Setup

```bash
# Install dependencies
npm install @earendil-works/pi-agent-core @earendil-works/pi-ai

# Create .env with your API keys
GROQ_API_KEY=gsk_...
NOUS_API_KEY=sk_...
```

## Usage

```typescript
import BatchProcessor from "./scripts/batch_processor";

const processor = new BatchProcessor(20, 10.0);
const results = await processor.process([
  "Congress cuts social programs",
  "Tech billionaires donate $50M"
]);
processor.printResults();
```

## Budget Monitoring

The system automatically:
1. Classifies all headlines (free)
2. Generates scripts for all (cheap)
3. Refines only high-importance (budget-aware)
4. Stops refinements when budget exhausted

## Next Steps

1. Merge this branch to main
2. Install Pi dependencies
3. Configure API keys in .env
4. Run batch processor with your headlines
5. Monitor costs in real-time