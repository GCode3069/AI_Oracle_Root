# LLM Battle Royale - Battle System Documentation

## Overview

The LLM Battle Royale system coordinates video generation, tracking, and elimination rounds for a competitive showcase between different Large Language Models (LLMs).

## Quick Start

### 1. Initial Setup

```bash
# Copy environment template and populate with your API keys
cp .env.example .env
# Edit .env with your actual API keys (NEVER commit this file)

# Verify environment setup
python BATTLE_CTR_INTEGRATION.py --help
```

### 2. Run a Battle Round (Dry-Run First!)

Always test with dry-run before actual generation:

```bash
# Dry-run to verify configuration
python BATTLE_CTR_INTEGRATION.py \
  --llm CHATGPT \
  --round 1 \
  --videos 5 \
  --start 30000 \
  --dry-run

# If dry-run succeeds, run actual generation
python BATTLE_CTR_INTEGRATION.py \
  --llm CHATGPT \
  --round 1 \
  --videos 5 \
  --start 30000
```

### 3. Track Performance and Apply Eliminations

```bash
# View current rankings (no elimination)
python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase 1

# Apply elimination logic
python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase 1 --eliminate
```

## System Components

### BATTLE_CTR_INTEGRATION.py
**Purpose**: Orchestrates video generation workflow for each LLM

**Features**:
- Maps LLM names to generator scripts
- Validates environment variables
- Updates battle_data.json with generation metadata
- Records per-video proof hashes for audit trail
- **Does NOT upload to YouTube** - operator responsibility

**Usage**:
```bash
python BATTLE_CTR_INTEGRATION.py \
  --llm <LLM_NAME> \
  --round <ROUND_NUMBER> \
  --videos <COUNT> \
  --start <EPISODE_NUMBER> \
  [--dry-run]
```

### BATTLE_TRACKER_ELIMINATION_ROUNDS.py
**Purpose**: Computes performance metrics and applies elimination logic

**Features**:
- Reads battle_data.json
- Ranks LLMs by performance metrics
- Applies phase-appropriate elimination rules
- Writes elimination.json

**Usage**:
```bash
python BATTLE_TRACKER_ELIMINATION_ROUNDS.py \
  --phase <PHASE_NUMBER> \
  [--eliminate] \
  [--eliminate-count <NUMBER>]
```

## Data Files

### battle_data.json
Central tracking file containing:
- `runs`: All generation runs with timestamps and proofs
- `proofs`: Per-video proof hashes for audit
- `pending_submissions`: Submissions awaiting production
- `llm_summary`: Aggregated metrics per LLM

### elimination.json
Elimination tracking file containing:
- `phases`: Results per elimination phase
- `eliminated`: List of eliminated LLMs
- `remaining`: Currently active LLMs

## Generator Scripts

Generator scripts must be implemented per LLM and placed in the `generators/` directory:

- `generators/chatgpt_generator.py`
- `generators/grok_generator.py`
- `generators/claude_generator.py`
- `generators/gemini_generator.py`
- `generators/llama_generator.py`

**Generator Requirements**:
- Accept `--start` and `--count` arguments
- Generate videos for specified episode range
- Output videos to consistent directory structure
- Return 0 exit code on success

**Example Generator Interface**:
```python
# generators/chatgpt_generator.py
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start', type=int, required=True)
    parser.add_argument('--count', type=int, required=True)
    args = parser.parse_args()
    
    for i in range(args.count):
        episode = args.start + i
        # Generate video for episode
        generate_video(episode)

if __name__ == '__main__':
    main()
```

## Safety and TOS Compliance

### ⚠️ CRITICAL SAFETY RULES

1. **Never Auto-Upload to YouTube**
   - All uploads must be manual with human review
   - Implement OAuth flow separately
   - Stage videos for review before publishing

2. **Environment Variables**
   - NEVER commit .env with real API keys
   - Use .env.example as template only
   - Keep API keys secure and rotate regularly

3. **Content Review**
   - Review all generated content before upload
   - Ensure compliance with YouTube TOS
   - Verify satire/parody labels are appropriate
   - Check for copyright issues

4. **Proof and Evidence**
   - Maintain audit trail in battle_data.json
   - Keep proof hashes for all generated videos
   - Document all elimination decisions
   - Track timestamps for all operations

5. **API Rate Limits**
   - Respect all API provider rate limits
   - Implement backoff and retry logic
   - Monitor API usage and costs

## Wiring the Uploader

The orchestration system does NOT include YouTube upload functionality by design. You must implement this separately:

### Upload Workflow
1. Generate videos using BATTLE_CTR_INTEGRATION.py
2. Review videos locally
3. Use separate uploader script with OAuth
4. Manually approve each upload
5. Update battle_data.json with YouTube video IDs

### Recommended Uploader Structure
```python
# uploader.py (implement separately)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def upload_video(video_path, title, description):
    # Implement OAuth flow
    # Request manual approval
    # Upload to YouTube
    # Return video ID
    pass
```

## Proofs and Evidence

### Proof Hash System
Each video generation creates a proof hash:
```
SHA256(llm_name:round:episode:timestamp)[:16]
```

Stored in battle_data.json under `proofs` key:
```json
{
  "proofs": {
    "CHATGPT:30000": "a1b2c3d4e5f6g7h8",
    "GROK:60000": "9i8h7g6f5e4d3c2b"
  }
}
```

### Evidence Requirements
- Timestamp of generation
- LLM identifier
- Episode number
- Round number
- Proof hash
- Generator script version (if tracked)

## Troubleshooting

### Environment Issues
```bash
# Check which variables are missing
python -c "import os; print([v for v in ['ELEVENLABS_API_KEY', 'PEXELS_API_KEY'] if not os.getenv(v)])"
```

### Generator Not Found
- Ensure generator script exists in `generators/` directory
- Make script executable: `chmod +x generators/chatgpt_generator.py`
- Verify GENERATORS mapping in BATTLE_CTR_INTEGRATION.py

### Battle Data Corruption
- Keep backups of battle_data.json
- Validate JSON structure before committing changes
- Use version control for tracking changes

## Best Practices

1. **Always use dry-run first** to test configuration
2. **Commit battle_data.json regularly** to track progress
3. **Back up elimination.json** before applying eliminations
4. **Document all manual interventions** in git commit messages
5. **Review generated videos** before any public release
6. **Rotate API keys** periodically for security
7. **Monitor costs** for all API services

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review battle_data.json for errors
3. Verify environment variables are set
4. Check generator script logs

## License

This orchestration system is part of the AI Oracle Root project. Ensure all generated content complies with applicable licenses and terms of service.
