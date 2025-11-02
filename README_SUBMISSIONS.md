# LLM Battle Royale - Submissions Workflow

## Overview

This document describes the complete workflow for receiving LLM script submissions, validating them, and enqueueing them for centralized production.

## Submission Flow

```
LLM Submits Script
      ↓
SUBMISSION_RECEIVER.py (validates & saves)
      ↓
./submissions/ (pending queue)
      ↓
ENQUEUE_FOR_PRODUCTION.py (creates production inputs)
      ↓
./core/production_inputs/ (production queue)
      ↓
Production Pipeline (generate videos)
      ↓
Review & Upload
```

## Components

### 1. SUBMISSION_RECEIVER.py

Validates incoming submission JSON and saves to ./submissions directory.

**Usage:**
```bash
# From file
python SUBMISSION_RECEIVER.py --file submission.json

# From stdin
cat submission.json | python SUBMISSION_RECEIVER.py
```

**Validation:**
- Checks required fields (llm_name, scripts)
- Validates LLM name against whitelist
- Ensures each script has episode, script, and title
- Validates optional fields (tags, satire_label, notes)
- Returns JSON with validation results

**Output:**
- Saves to `./submissions/submission_{LLM}_{timestamp}.json`
- Records in battle_data.json as pending submission
- Prints JSON summary to stdout

### 2. ENQUEUE_FOR_PRODUCTION.py

Reads submissions and creates per-episode production input files.

**Usage:**
```bash
python ENQUEUE_FOR_PRODUCTION.py
```

**Process:**
- Scans ./submissions for pending submissions
- Creates per-episode JSON files in ./core/production_inputs
- Updates battle_data.json status to 'enqueued'
- Does NOT call external APIs

**Output:**
- Creates `./core/production_inputs/{LLM}_ep{NNNNN}.json` per episode
- Updates battle_data.json with enqueued status

## Submission Schema

Submissions must follow this structure:

```json
{
  "llm_name": "ChatGPT",
  "scripts": [
    {
      "episode": 30001,
      "script": "Full script text here...",
      "title": "Episode Title",
      "tags": ["AI", "Mystery", "Tech"],
      "notes": "Optional production notes",
      "satire_label": false
    }
  ],
  "metadata": {
    "round": 1,
    "theme": "Tech Mystery"
  }
}
```

See `submission_schema.json` for complete schema definition.

## Operator Checklist

### Receiving Submissions

- [ ] Verify submission file exists
- [ ] Run SUBMISSION_RECEIVER.py to validate
- [ ] Check validation output for errors
- [ ] If valid, submission is saved to ./submissions
- [ ] Review submission content for TOS compliance
- [ ] Approve or reject submission

### Enqueueing for Production

- [ ] Review pending submissions in ./submissions
- [ ] Run ENQUEUE_FOR_PRODUCTION.py
- [ ] Verify production inputs created in ./core/production_inputs
- [ ] Check battle_data.json for updated status
- [ ] Proceed to production pipeline

### Production Pipeline

- [ ] Review production queue in ./core/production_inputs
- [ ] Run production pipeline on queued episodes
- [ ] Review generated videos for quality
- [ ] Check TOS compliance
- [ ] Stage approved videos for upload

### Upload to YouTube

- [ ] Use separate OAuth uploader script
- [ ] Upload only approved videos
- [ ] Update battle_data.json with upload timestamps
- [ ] Record YouTube video IDs

## Safety Rules

### ⚠️ CRITICAL SAFETY REQUIREMENTS

1. **Manual Review Required**: ALWAYS review submissions and generated videos before upload
2. **TOS Compliance**: Ensure all content complies with YouTube Terms of Service
3. **No Auto-Upload**: Never automatically upload to YouTube without review
4. **Audit Trail**: Maintain complete records in battle_data.json
5. **API Safety**: Never commit API keys to version control

### Content Guidelines

All submissions must:
- Comply with YouTube Community Guidelines
- Respect copyright and licensing
- Include accurate satire_label if applicable
- Avoid prohibited content (violence, hate speech, etc.)
- Be appropriate for intended audience

### Operator Responsibilities

The operator must:
- Review all submissions before production
- Verify TOS compliance before upload
- Maintain secure API credentials
- Keep audit trail in battle_data.json
- Follow manual review workflow
- Use OAuth 2.0 for YouTube uploads

## File Locations

```
./submissions/                     # Pending submissions
./core/production_inputs/          # Production queue
./battle_data.json                 # Central tracking database
./submission_schema.json           # Schema definition
./examples/                        # Sample submissions
```

## Example Workflow

### Step 1: Receive Submission

```bash
# Validate and save submission
python SUBMISSION_RECEIVER.py --file examples/submissions_CHATGPT_30000-30004.sample.json

# Output shows validation success and saved location
```

### Step 2: Review Submission

```bash
# Manually review the saved submission
cat submissions/submission_ChatGPT_20240101_120000.json

# Check for TOS compliance, quality, appropriateness
```

### Step 3: Enqueue for Production

```bash
# Create production inputs
python ENQUEUE_FOR_PRODUCTION.py

# Review created production inputs
ls -la core/production_inputs/
```

### Step 4: Production

```bash
# Run production pipeline (implementation-specific)
# This would use the files in ./core/production_inputs

# Review generated videos
```

### Step 5: Upload

```bash
# Use OAuth uploader (separate script, not included)
# Upload only after manual review and approval
```

## Troubleshooting

### Validation Errors

If SUBMISSION_RECEIVER.py reports errors:
1. Check the error messages in JSON output
2. Verify submission follows schema
3. Fix issues in submission file
4. Re-run validation

### Missing Files

If files are missing:
1. Run BATTLE_BOOTSTRAP.ps1 to create directories
2. Verify permissions on directories
3. Check that submission files are in ./submissions

### Status Tracking

Check submission status:
```bash
# View battle_data.json
cat battle_data.json | python -m json.tool
```

## Support

For issues or questions:
1. Review this document
2. Check README_BATTLE.md for system overview
3. Verify submission_schema.json for format requirements
4. Ensure all directories exist (run BATTLE_BOOTSTRAP.ps1)

## Compliance & Legal

All submissions and generated content must comply with:
- YouTube Terms of Service
- YouTube Community Guidelines
- Copyright law
- Platform API usage policies
- Applicable content regulations

The operator is responsible for ensuring compliance before upload.
