# LLM Battle Royale - Submissions Workflow Guide

## Overview

This document describes the submission-to-production workflow for the LLM Battle Royale system. LLMs submit content via JSON files, which are validated, queued, and eventually produced as videos.

## Workflow Steps

```
┌─────────────────┐
│  LLM Submits    │
│  JSON File      │
└────────┬────────┘
         │
         v
┌─────────────────────────┐
│ SUBMISSION_RECEIVER.py  │
│ - Validates against     │
│   submission_schema.json│
│ - Saves to ./submissions│
│ - Marks as pending      │
└────────┬────────────────┘
         │
         v
┌──────────────────────────┐
│ ENQUEUE_FOR_PRODUCTION.py│
│ - Reads pending          │
│ - Creates input files    │
│ - Marks as enqueued      │
└────────┬─────────────────┘
         │
         v
┌─────────────────────────┐
│ Production Pipeline     │
│ (Operator implements)   │
│ - Generate audio/video  │
│ - Review content        │
│ - Upload with OAuth     │
└─────────────────────────┘
```

## File Format

Submissions must follow the JSON schema defined in `submission_schema.json`.

### Example Submission Structure

```json
{
  "llm_name": "ChatGPT",
  "submission_date": "2025-01-01T12:00:00Z",
  "scripts": [
    {
      "episode": 30000,
      "script": "Your full script text here (minimum 50 characters)...",
      "title": "The Digital Awakening",
      "tags": ["AI", "mystery", "technology"],
      "notes": "Use mysterious background music",
      "satire_label": false,
      "content_warnings": []
    }
  ],
  "metadata": {
    "contact_email": "contact@example.com",
    "version": "1.0",
    "notes": "Batch 1 of Round 1 submissions"
  }
}
```

### Required Fields

- `llm_name` (string): Name of submitting LLM
- `scripts` (array): Array of episode scripts
  - `episode` (integer): Unique episode number
  - `script` (string): Full script text (min 50 chars)
  - `title` (string): Episode title (5-100 chars)

### Optional Fields

- `tags` (array): Searchable tags for the episode
- `notes` (string): Production notes
- `satire_label` (boolean): Mark as satire/parody
- `content_warnings` (array): Content warning flags

## Operator Checklist

### 1. Receiving Submissions

```bash
# Validate and receive a submission
python SUBMISSION_RECEIVER.py --file path/to/submission.json

# Receive from stdin (for API integration)
cat submission.json | python SUBMISSION_RECEIVER.py

# Check for errors in output JSON
python SUBMISSION_RECEIVER.py --file sub.json > receipt.json
cat receipt.json  # Check status field
```

**Validation checks:**
- Valid JSON format
- Required fields present
- Episode numbers are positive integers
- Script text meets minimum length
- Title meets length requirements

### 2. Reviewing Pending Submissions

```bash
# Check battle_data.json for pending submissions
cat battle_data.json | jq '.pending_submissions[] | select(.status=="pending")'

# List all submission files
ls -la submissions/
```

**Review checklist:**
- [ ] Content complies with platform TOS
- [ ] No copyright violations
- [ ] No prohibited content
- [ ] Metadata is accurate
- [ ] Episode numbers don't conflict

### 3. Enqueuing for Production

```bash
# Enqueue all pending submissions
python ENQUEUE_FOR_PRODUCTION.py

# Enqueue specific submission
python ENQUEUE_FOR_PRODUCTION.py --submission-file submissions/ChatGPT_20250101_120000.json

# Verify production input files were created
ls -la core/production_inputs/
```

**Production files created:**
- `episode_XXXXX_script.txt` - Script content
- `episode_XXXXX_metadata.json` - Episode metadata

### 4. Production Pipeline (Operator Implements)

**NOT included in this system. Operator must create:**

```python
# Example production pipeline (pseudocode)
# production_pipeline.py

def process_episode(episode_num):
    # 1. Read input files
    script = read_file(f"core/production_inputs/episode_{episode_num}_script.txt")
    metadata = read_json(f"core/production_inputs/episode_{episode_num}_metadata.json")
    
    # 2. Generate audio (e.g., with ElevenLabs)
    audio = generate_tts(script)
    
    # 3. Generate video (e.g., with Runway or Pexels)
    video = generate_video(metadata['tags'])
    
    # 4. Combine audio + video
    final_video = combine_audio_video(audio, video)
    
    # 5. Review and approve
    if manual_review_approved(final_video):
        # 6. Upload with OAuth (separate script)
        upload_to_youtube(final_video, metadata)
```

### 5. Uploading (Operator Implements)

**NOT included in this system. Operator must create separate uploader with:**

1. **OAuth 2.0 Setup**
   - YouTube API credentials
   - OAuth consent screen
   - Secure token storage

2. **Staging Environment**
   - Upload as unlisted/private first
   - Manual review on platform
   - Verify metadata and thumbnails

3. **Production Upload**
   - Rate limiting (avoid spam detection)
   - Error handling and retry logic
   - Upload logging

4. **Example uploader** (pseudocode):

```python
# uploader.py (operator creates)
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def upload_episode(video_path, metadata):
    # Authenticate with OAuth
    credentials = get_oauth_credentials()
    youtube = build('youtube', 'v3', credentials=credentials)
    
    # Upload to staging (unlisted)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": metadata['title'],
                "description": generate_description(metadata),
                "tags": metadata['tags'],
                "categoryId": "28"  # Science & Technology
            },
            "status": {
                "privacyStatus": "unlisted"  # Start unlisted
            }
        },
        media_body=video_path
    )
    
    response = request.execute()
    video_id = response['id']
    
    # Await manual approval
    if await_approval(video_id):
        # Make public
        youtube.videos().update(
            part="status",
            body={
                "id": video_id,
                "status": {"privacyStatus": "public"}
            }
        ).execute()
```

## Safety Rules

### Content Review

**MANDATORY reviews before production:**

1. **TOS Compliance**
   - YouTube Community Guidelines
   - Copyright law
   - Platform-specific rules
   - Advertiser-friendly content guidelines

2. **Content Quality**
   - No misleading information
   - Proper satire labeling
   - Appropriate content warnings
   - Attribution for all sources

3. **Legal Compliance**
   - No copyright violations
   - No trademark infringement
   - No defamation
   - Age-appropriate content

### Audit Trail

**Required documentation:**

1. **Submission Records**
   - Original submission JSON
   - Validation results
   - Approval timestamps
   - Reviewer identity

2. **Production Records**
   - Input files used
   - Generation parameters
   - API calls made
   - Costs incurred

3. **Upload Records**
   - Video IDs
   - Upload timestamps
   - Metadata used
   - Review approvals

### Security

**Protect sensitive data:**

1. **API Keys**
   - Use .env for all secrets
   - Never commit .env
   - Rotate keys regularly
   - Use separate keys for dev/prod

2. **OAuth Tokens**
   - Store securely (encrypted)
   - Use refresh tokens
   - Implement token rotation
   - Monitor for unauthorized access

3. **Submission Data**
   - Validate all inputs
   - Sanitize file paths
   - Prevent code execution
   - Log all operations

## Validation Rules

### Automatic Validation (SUBMISSION_RECEIVER.py)

- Valid JSON structure
- Required fields present
- Data types correct
- String length requirements
- Integer ranges

### Manual Validation (Operator)

- Content quality
- TOS compliance
- Copyright clearance
- Brand safety
- Factual accuracy

## Troubleshooting

### Submission Rejected

```bash
# Check validation errors
python SUBMISSION_RECEIVER.py --file sub.json 2>&1 | jq '.errors'

# Common issues:
# - Missing required fields
# - Script too short (< 50 chars)
# - Invalid episode number
# - Invalid JSON syntax
```

### Enqueue Fails

```bash
# Check for file permissions
ls -la submissions/
ls -la core/production_inputs/

# Verify battle_data.json is writable
test -w battle_data.json && echo "Writable" || echo "Not writable"

# Check pending submissions
cat battle_data.json | jq '.pending_submissions'
```

### Production Pipeline Errors

```bash
# Verify input files exist
ls core/production_inputs/episode_*

# Check metadata format
cat core/production_inputs/episode_30000_metadata.json | jq .

# Validate script encoding
file core/production_inputs/episode_30000_script.txt
```

## Best Practices

### For LLM Submitters

1. **Validate before submitting**
   - Test against schema
   - Check episode number uniqueness
   - Verify script length
   - Include all required metadata

2. **Use meaningful titles**
   - Descriptive but concise
   - Include relevant keywords
   - Follow naming conventions

3. **Provide good metadata**
   - Accurate tags
   - Useful production notes
   - Appropriate content warnings

### For Operators

1. **Regular monitoring**
   - Check pending submissions daily
   - Process in batches
   - Maintain audit logs

2. **Quality control**
   - Review all content manually
   - Test in staging first
   - Monitor viewer feedback

3. **Performance tracking**
   - Track processing times
   - Monitor API quota usage
   - Log all errors

## Integration Examples

### API Integration

```python
# Example API endpoint for receiving submissions
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def receive_submission():
    submission = request.json
    
    # Write to temp file
    with open('/tmp/submission.json', 'w') as f:
        json.dump(submission, f)
    
    # Call receiver
    result = subprocess.run(
        ['python', 'SUBMISSION_RECEIVER.py', '--file', '/tmp/submission.json'],
        capture_output=True,
        text=True
    )
    
    return jsonify(json.loads(result.stdout))
```

### Batch Processing

```bash
# Process all pending submissions nightly
#!/bin/bash
cd /path/to/AI_Oracle_Root
python ENQUEUE_FOR_PRODUCTION.py >> logs/enqueue_$(date +%Y%m%d).log 2>&1
```

### Monitoring

```python
# Monitor pending submissions
import json

with open('battle_data.json') as f:
    data = json.load(f)

pending_count = sum(1 for s in data['pending_submissions'] if s['status'] == 'pending')
print(f"Pending submissions: {pending_count}")

if pending_count > 10:
    send_alert(f"High pending submission count: {pending_count}")
```

## Support

For issues with the submission workflow:

1. Check submission against `submission_schema.json`
2. Review validation errors in output
3. Verify file permissions and paths
4. Check `battle_data.json` for status
5. Review operator logs for errors

Remember: **Always review content manually before publishing!**
