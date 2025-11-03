# LLM Battle Royale - Quick Start Guide

## Overview

The LLM Battle Royale system orchestrates content generation from multiple LLM-driven generator scripts, tracks performance across battle rounds, and manages the elimination process.

## Quick Start

### 1. Initial Setup

```bash
# Run bootstrap script (creates directories and placeholders)
pwsh BATTLE_BOOTSTRAP.ps1

# Copy environment template and populate with your API keys
cp .env.example .env
# Edit .env with your actual credentials (NEVER commit this file)
```

### 2. Generate Content for a Battle Round

```bash
# Dry run (no actual generation)
python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --videos 5 --dry-run

# Production run
python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --videos 5 --start 30000
python BATTLE_CTR_INTEGRATION.py --llm GROK --round 1 --videos 5 --start 60000
python BATTLE_CTR_INTEGRATION.py --llm Claude --round 1 --videos 5 --start 90000
```

### 3. Track Statistics and Eliminations

```bash
# Track current statistics (no eliminations)
python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase round1

# Track and eliminate lowest performers
python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase round2 --eliminate
```

### 4. Review and Upload

**IMPORTANT**: This system does NOT upload to YouTube automatically.

1. Review `battle_data.json` for generated content details
2. Review `elimination.json` for elimination decisions
3. Manually review all generated content for compliance
4. Implement separate uploader script with OAuth 2.0
5. Use staging environment before production upload

## File Structure

```
AI_Oracle_Root/
├── BATTLE_CTR_INTEGRATION.py      # Main orchestrator
├── BATTLE_TRACKER_ELIMINATION_ROUNDS.py  # Tracker & eliminator
├── battle_data.json                # Battle statistics and runs
├── elimination.json                # Elimination results (generated)
├── .env.example                    # Environment variables template
├── .env                            # Your actual secrets (DO NOT COMMIT)
├── BATTLE_BOOTSTRAP.ps1            # Setup script
├── core/
│   └── production_inputs/          # Generated content staging
├── submissions/                    # LLM submission files
└── examples/                       # Example submission files
```

## Safety & Terms of Service

### ⚠️ Critical Reminders

1. **NO AUTOMATIC UPLOADS**: These scripts do NOT upload to YouTube automatically
2. **MANUAL REVIEW REQUIRED**: Operator must review ALL content before publishing
3. **TOS COMPLIANCE**: Ensure all content complies with:
   - YouTube Terms of Service
   - Community Guidelines
   - Copyright law
   - Platform-specific rules

4. **SECRETS MANAGEMENT**:
   - Use `.env` for all API keys and credentials
   - NEVER commit `.env` to version control
   - Use OAuth 2.0 for YouTube uploads (separate script)
   - Store OAuth tokens securely

5. **PROOF SYSTEM**:
   - Maintain auditable proof of content generation
   - Document all content sources and attributions
   - Keep records of review and approval process

## Uploader Implementation (Operator TODO)

The battle system intentionally does NOT include an uploader. Operator must implement separately:

1. **OAuth 2.0 Setup**:
   - Register app with YouTube API
   - Obtain client secrets
   - Implement OAuth flow
   - Securely store refresh tokens

2. **Staging Environment**:
   - Upload to private/unlisted first
   - Review on actual platform
   - Verify metadata, thumbnails, descriptions
   - Check for any TOS issues

3. **Production Upload**:
   - Use rate limiting (avoid spam detection)
   - Implement retry logic with exponential backoff
   - Log all upload attempts
   - Monitor for API quota limits

4. **Example Uploader Structure** (pseudocode):
   ```python
   # uploader.py (operator creates separately)
   from google_auth_oauthlib.flow import InstalledAppFlow
   from googleapiclient.discovery import build
   
   def upload_to_youtube(video_path, metadata):
       # 1. Authenticate with OAuth 2.0
       # 2. Read metadata from battle_data.json
       # 3. Upload to staging (unlisted)
       # 4. Await manual approval
       # 5. Update to public if approved
       # 6. Record proof in battle_data.json
       pass
   ```

## Proof Expectations

Each generated piece of content should have:

1. **Metadata Proof**:
   - Episode number
   - LLM source
   - Round number
   - Generation timestamp
   - Generator script version

2. **Content Proof**:
   - Script text file
   - Generated audio file (if applicable)
   - Generated video file
   - Thumbnail image
   - Metadata (title, description, tags)

3. **Compliance Proof**:
   - Review checklist completed
   - TOS compliance verified
   - Attribution documented
   - Approval signature/timestamp

4. **Upload Proof** (after manual upload):
   - YouTube video ID
   - Upload timestamp
   - Final metadata used
   - Staging review notes

## Troubleshooting

### Generator Script Not Found
```bash
# Check GENERATORS mapping in BATTLE_CTR_INTEGRATION.py
# Ensure generator scripts exist in 1_Script_Engine/
```

### Battle Data Missing
```bash
# Initialize with:
python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --videos 1 --dry-run
```

### Environment Variables Not Loading
```bash
# Ensure .env file exists and is in the correct location
# Check .env.example for required variable names
```

## Advanced Usage

### Custom Elimination Logic

Edit `BATTLE_TRACKER_ELIMINATION_ROUNDS.py` function `determine_eliminations()` to implement custom rules:

```python
def determine_eliminations(stats, phase, auto_eliminate=False):
    # Custom logic here
    # Example: eliminate based on engagement rate, not just episode count
    pass
```

### Multiple Rounds in One Command

```bash
# Use shell scripting for batch operations
for llm in ChatGPT GROK Claude Gemini; do
    python BATTLE_CTR_INTEGRATION.py --llm $llm --round 1 --videos 5
done
```

### Dry Run Testing

Always test with `--dry-run` before production:

```bash
python BATTLE_CTR_INTEGRATION.py --llm ChatGPT --round 1 --videos 100 --dry-run
# Review output, then run without --dry-run
```

## Contact & Support

For issues with the battle system:
1. Check `battle_data.json` for error logs
2. Review generator script output
3. Verify environment variables in `.env`
4. Consult repository documentation

Remember: **Always review content manually before publishing!**
