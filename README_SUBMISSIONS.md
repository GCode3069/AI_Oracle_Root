# LLM Battle Royale - Submissions Workflow

## Overview

The submissions workflow enables LLMs to submit scripts for video production through a safe, auditable pipeline. All submissions are validated, tracked, and queued for manual review before production.

## Workflow Steps

### 1. Submission Reception

LLMs or operators submit scripts via JSON payload:

```bash
# From file
python SUBMISSION_RECEIVER.py --file my_submission.json

# From stdin (for API integration)
cat my_submission.json | python SUBMISSION_RECEIVER.py
```

**What happens:**
- Validates JSON structure against submission_schema.json
- Saves to `./submissions` with timestamp
- Records in `battle_data.json` as pending
- Returns JSON summary to stdout

### 2. Queue for Production

Operator enqueues validated submissions for production:

```bash
python ENQUEUE_FOR_PRODUCTION.py
```

**What happens:**
- Scans `./submissions` for new submissions
- Creates per-episode input files in `./core/production_inputs`
- Updates `battle_data.json` status to "enqueued"
- Reports summary of queued episodes

### 3. Video Production

Operator runs production pipeline (separate from this workflow):

```bash
# Example - operator implements production pipeline
python produce_video.py --input ./core/production_inputs/chatgpt_episode_30001.json
```

### 4. Review and Upload

Operator manually reviews and uploads:

1. Review generated video
2. Verify metadata and tags
3. Check TOS compliance
4. Upload to YouTube (unlisted/private first)
5. Review on platform
6. Make public if approved

## Submission Format

See `submission_schema.json` for complete schema. Example:

```json
{
  "llm_name": "chatgpt",
  "scripts": [
    {
      "episode": 30001,
      "script": "Welcome to AI Oracle...",
      "title": "AI Oracle Episode 30001",
      "tags": ["AI", "technology", "oracle"],
      "satire_label": false,
      "notes": "Production note here"
    }
  ]
}
```

### Required Fields

- `llm_name`: String, LLM identifier
- `scripts`: Array of episode objects
  - `episode`: Integer, episode number
  - `script`: String, full voiceover script
  - `title`: String, YouTube title (max 100 chars)

### Optional Fields

- `tags`: Array of strings (max 30 tags)
- `satire_label`: Boolean, requires satire disclaimer
- `notes`: String, production notes

## Operator Checklist

### Before Accepting Submissions

- [ ] Submission validation is working
- [ ] `./submissions` directory exists
- [ ] `battle_data.json` is initialized
- [ ] `.gitignore` excludes submission files

### After Receiving Submissions

- [ ] Review submission JSON for quality
- [ ] Verify episode numbers don't conflict
- [ ] Check script content for TOS compliance
- [ ] Validate tags are appropriate
- [ ] Confirm satire labels where needed

### Before Production

- [ ] Run `ENQUEUE_FOR_PRODUCTION.py`
- [ ] Verify production input files created
- [ ] Review `battle_data.json` status updates
- [ ] Confirm no secrets in submission files

### During Production

- [ ] Generate videos with proper attribution
- [ ] Add satire disclaimers where flagged
- [ ] Include proper credits and sources
- [ ] Test video quality before upload

### Before Upload

- [ ] Review each video completely
- [ ] Verify metadata accuracy
- [ ] Check TOS compliance
- [ ] Upload as unlisted/private first
- [ ] Review on YouTube platform

## Safety Rules

### Critical Security

⚠️ **No auto-upload to YouTube**
- All uploads are manual
- Operator reviews every video
- OAuth required, never commit credentials

⚠️ **Validate all submissions**
- Check for malicious content
- Verify TOS compliance
- Review tags and metadata
- Confirm episode numbering

⚠️ **Track everything**
- All submissions logged in battle_data.json
- Per-episode audit trail
- Timestamps for all operations
- Status tracking through pipeline

### Content Guidelines

- Include satire/parody labels where appropriate
- Add proper attribution for media sources
- Verify fair use compliance
- Check copyright restrictions
- Review community guidelines

## Directory Structure

```
.
├── submissions/              # Received submissions (gitignored)
│   └── submission_chatgpt_20231201_120000.json
├── core/
│   └── production_inputs/    # Per-episode production files (gitignored)
│       └── chatgpt_episode_30001.json
├── battle_data.json          # Central tracking database
└── submission_schema.json    # Validation schema
```

## Example Workflow

```bash
# 1. Receive submission
python SUBMISSION_RECEIVER.py --file examples/submissions_CHATGPT_30000-30004.sample.json

# 2. Review submission (manual step)
cat submissions/submission_chatgpt_*.json

# 3. Enqueue for production
python ENQUEUE_FOR_PRODUCTION.py

# 4. Produce videos (operator implements)
# python produce_video.py --input ./core/production_inputs/chatgpt_episode_30001.json

# 5. Review and upload (manual, OAuth required)
# Review video, then upload to YouTube with proper staging
```

## Troubleshooting

### Validation Errors

```bash
# Check submission format
cat my_submission.json | python -m json.tool

# Validate against schema manually
python SUBMISSION_RECEIVER.py --file my_submission.json
```

### Missing Files

```bash
# Create directories
mkdir -p submissions core/production_inputs

# Initialize battle_data.json if missing
echo '{"runs":[],"proofs":[],"pending_submissions":[],"llm_summary":{},"generated_at":null}' > battle_data.json
```

### Status Tracking

```bash
# Check pending submissions
cat battle_data.json | python -m json.tool | grep -A 10 pending_submissions

# View production inputs
ls -la core/production_inputs/
```

## API Integration (Future)

For automated submission pipelines:

```python
import requests
import json

submission = {
    "llm_name": "chatgpt",
    "scripts": [...]
}

# Submit via API (operator implements endpoint)
response = requests.post(
    "https://api.example.com/submit",
    json=submission,
    headers={"Authorization": "Bearer TOKEN"}
)
```

## Support

- Review `README_BATTLE.md` for orchestration details
- Check `submission_schema.json` for format specification
- Examine example files in `examples/` directory
- Verify `battle_data.json` for submission status

## License and Compliance

All submissions must:
- Comply with platform Terms of Service
- Include proper attribution
- Respect copyright and fair use
- Contain appropriate content warnings
- Follow community guidelines
