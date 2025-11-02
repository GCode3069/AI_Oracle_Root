# LLM Battle Royale - Operator Guide

## Overview

The LLM Battle Royale system orchestrates video generation, tracking, and elimination for multiple competing LLMs. This system provides a safe, auditable workflow for centralized production with operator oversight.

## Quick Start

### 1. Initial Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and populate with your actual API keys
# NEVER commit .env to version control!

# Run bootstrap (Windows PowerShell)
.\BATTLE_BOOTSTRAP.ps1

# Verify environment
python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --dry-run
```

### 2. Generate Videos (Dry Run First)

```bash
# Always test with dry run first
python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --videos 5 --dry-run

# If validation passes, run production
python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --videos 5
```

### 3. Track and Eliminate

```bash
# View current standings
python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase 1

# Apply elimination (bottom 2 LLMs)
python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase 1 --eliminate 2
```

## Safety Notes

### ⚠️ CRITICAL SAFETY RULES

1. **API Keys**: NEVER commit API keys to version control. Always use .env file.
2. **Manual Review**: ALWAYS review generated videos before uploading to YouTube.
3. **TOS Compliance**: Ensure all content complies with YouTube Terms of Service.
4. **OAuth Upload**: Use separate uploader script with OAuth 2.0 for YouTube.
5. **Dry Run First**: ALWAYS run with --dry-run flag before production.

### YouTube Upload Workflow

This orchestrator does NOT upload videos directly to YouTube. Follow this workflow:

1. Generate videos with BATTLE_CTR_INTEGRATION.py
2. Review all generated videos for quality and TOS compliance
3. Stage approved videos for upload
4. Use separate YouTube uploader with OAuth 2.0 authentication
5. Update battle_data.json with upload timestamps and URLs

## Generator Scripts

The orchestrator maps LLM names to generator scripts:

```python
GENERATORS = {
    "ChatGPT": "./1_Script_Engine/chatgpt_generator.py",
    "Claude": "./1_Script_Engine/claude_generator.py",
    "Gemini": "./1_Script_Engine/gemini_generator.py",
    "Grok": "./1_Script_Engine/grok_generator.py",
    "Llama": "./1_Script_Engine/llama_generator.py",
}
```

**Implementation Note**: Generator scripts must be implemented before production use. Each generator should:
- Accept command-line arguments (round, video count, start number)
- Generate videos using LLM-specific scripts
- Output video files to designated directory
- Return success/failure status

## Proofs and Evidence

Every video generation is recorded in battle_data.json:

```json
{
  "runs": [...],
  "proofs": [
    {
      "llm": "ChatGPT",
      "round": 1,
      "video_id": 1,
      "proof": {
        "video_file": "ChatGPT_R1_V1.mp4",
        "generated": true
      },
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

## File Structure

```
AI_Oracle_Root/
├── BATTLE_CTR_INTEGRATION.py          # Main orchestrator
├── BATTLE_TRACKER_ELIMINATION_ROUNDS.py  # Elimination tracker
├── SUBMISSION_RECEIVER.py             # Submission validator
├── ENQUEUE_FOR_PRODUCTION.py          # Production queue manager
├── battle_data.json                   # Production records
├── elimination.json                   # Elimination records
├── .env                              # API keys (DO NOT COMMIT)
├── .env.example                      # Template
├── submissions/                      # Incoming submissions
├── core/production_inputs/           # Production queue
└── examples/                         # Sample submissions
```

## Operator Checklist

- [ ] Copy .env.example to .env
- [ ] Populate all required API keys in .env
- [ ] Verify .env is in .gitignore
- [ ] Run bootstrap script to create directories
- [ ] Test with --dry-run flag
- [ ] Implement generator scripts for each LLM
- [ ] Set up YouTube OAuth uploader (separate script)
- [ ] Review and approve all videos before upload
- [ ] Maintain audit trail in battle_data.json

## Support

For questions or issues:
1. Check this README
2. Review README_SUBMISSIONS.md for submission workflow
3. Check .env.example for required environment variables
4. Ensure generator scripts are properly implemented

## License & Compliance

All generated content must comply with:
- YouTube Terms of Service
- Platform API usage policies
- Copyright and licensing requirements
- Content policy guidelines
