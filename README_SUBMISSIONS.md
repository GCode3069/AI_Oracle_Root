# LLM Battle Royale - Submissions Workflow

## Overview

This document describes the submission → production flow for LLM-generated scripts in the Battle Royale project.

## Workflow Overview

```
Submission → Validation → Storage → Enqueue → Production → Review → Upload
```

1. **Submission**: LLM submits scripts via JSON
2. **Validation**: SUBMISSION_RECEIVER validates against schema
3. **Storage**: Valid submissions saved to ./submissions
4. **Enqueue**: ENQUEUE_FOR_PRODUCTION creates production inputs
5. **Production**: Video generation pipeline processes inputs
6. **Review**: Operator reviews generated videos
7. **Upload**: Manual upload to YouTube with OAuth

## Submission Format

Submissions must follow the `submission_schema.json` format:

```json
{
  "llm_name": "CHATGPT",
  "submitter": "john.doe@example.com",
  "submitted_at": "2023-11-01T12:00:00Z",
  "scripts": [
    {
      "episode": 30000,
      "script": "Full script content here...",
      "title": "Episode Title",
      "tags": ["tag1", "tag2"],
      "notes": "Optional notes",
      "satire_label": false
    }
  ]
}
```

## Using SUBMISSION_RECEIVER.py

### Accept Submission from File
```bash
python SUBMISSION_RECEIVER.py --file submission.json
```

### Accept Submission from stdin
```bash
cat submission.json | python SUBMISSION_RECEIVER.py
```

### Output
SUBMISSION_RECEIVER outputs JSON to stdout:
```json
{
  "status": "success",
  "llm_name": "CHATGPT",
  "submitter": "john.doe@example.com",
  "episode_count": 5,
  "episodes": [30000, 30001, 30002, 30003, 30004],
  "filepath": "submissions/CHATGPT_20231101_120000.json",
  "received_at": "2023-11-01T12:00:05Z"
}
```

### Validation Errors
If validation fails, errors are printed to stderr:
```json
{
  "status": "error",
  "error": "Validation failed",
  "validation_errors": [
    "Missing required field: llm_name",
    "scripts[0].episode must be an integer"
  ]
}
```

## Using ENQUEUE_FOR_PRODUCTION.py

### Enqueue All Pending Submissions
```bash
python ENQUEUE_FOR_PRODUCTION.py
```

### Enqueue Specific Submission
```bash
python ENQUEUE_FOR_PRODUCTION.py --submission submissions/CHATGPT_20231101_120000.json
```

### What It Does
1. Reads validated submission from ./submissions
2. Creates per-episode input files in ./core/production_inputs
3. Updates battle_data.json status to 'enqueued'
4. Records enqueued_at timestamp

### Output Structure
```
./core/production_inputs/
├── CHATGPT/
│   ├── episode_30000.json
│   ├── episode_30001.json
│   └── episode_30002.json
└── GROK/
    ├── episode_60000.json
    └── episode_60001.json
```

## Operator Checklist

### Before Accepting Submissions
- [ ] Verify submitter identity and authorization
- [ ] Check submission format matches schema
- [ ] Confirm episode numbers don't conflict
- [ ] Review content for TOS compliance (manual step)

### Processing Submissions
- [ ] Run SUBMISSION_RECEIVER.py to validate
- [ ] Check validation output for errors
- [ ] Verify submission saved to ./submissions
- [ ] Confirm battle_data.json updated

### Enqueueing for Production
- [ ] Review pending submissions in battle_data.json
- [ ] Run ENQUEUE_FOR_PRODUCTION.py
- [ ] Verify production input files created
- [ ] Check directory structure is correct

### Production Phase
- [ ] Run video generation pipeline per episode
- [ ] Review generated videos for quality
- [ ] Check for copyright issues
- [ ] Verify satire labels are appropriate

### Upload Phase (Manual)
- [ ] Use separate uploader with OAuth
- [ ] Review each video before upload
- [ ] Stage uploads for review
- [ ] Update battle_data.json with video IDs
- [ ] Verify videos are public/unlisted as intended

## Safety Rules

### ⚠️ CRITICAL SAFETY REQUIREMENTS

1. **Content Review**
   - ALWAYS review generated content before upload
   - Check for copyright violations
   - Verify accuracy of satire/parody labels
   - Ensure compliance with platform TOS

2. **Manual Upload Only**
   - NEVER auto-upload to YouTube
   - Implement OAuth flow separately
   - Require manual approval for each upload
   - Stage videos for review first

3. **Submission Validation**
   - Validate ALL submissions against schema
   - Check episode number ranges
   - Verify submitter authorization
   - Sanitize user inputs

4. **Data Integrity**
   - Maintain audit trail in battle_data.json
   - Back up submission files
   - Version control all changes
   - Keep logs of all operations

5. **API Security**
   - NEVER commit API keys
   - Use environment variables only
   - Rotate keys regularly
   - Monitor API usage and costs

## Example Workflow

### Complete End-to-End Example

```bash
# 1. Receive submission
python SUBMISSION_RECEIVER.py --file examples/submissions_CHATGPT_30000-30004.sample.json

# Output: JSON summary with filepath

# 2. Verify in battle_data.json
cat battle_data.json | jq '.pending_submissions'

# 3. Enqueue for production
python ENQUEUE_FOR_PRODUCTION.py

# Output: Production files created

# 4. Verify production inputs
ls -la ./core/production_inputs/CHATGPT/

# 5. Run production pipeline (implement separately)
# for file in ./core/production_inputs/CHATGPT/*.json; do
#   python generate_video.py --input $file
# done

# 6. Review generated videos
# ls -la ./output/videos/CHATGPT/

# 7. Manual upload with OAuth (implement separately)
# python uploader.py --video ./output/videos/CHATGPT/episode_30000.mp4

# 8. Update battle_data.json with video IDs (manual)
```

## Monitoring and Auditing

### Check Submission Status
```bash
# View all pending submissions
cat battle_data.json | jq '.pending_submissions[] | select(.status=="pending")'

# View enqueued submissions
cat battle_data.json | jq '.pending_submissions[] | select(.status=="enqueued")'
```

### List Production Inputs
```bash
# Count production inputs per LLM
find ./core/production_inputs -name "*.json" -type f | cut -d'/' -f4 | sort | uniq -c
```

### Verify Submissions
```bash
# List all submissions
ls -lh ./submissions/

# Count by LLM
ls ./submissions/ | cut -d'_' -f1 | sort | uniq -c
```

## Troubleshooting

### Validation Fails
- Check JSON syntax with `jq` or `python -m json.tool`
- Verify all required fields are present
- Check data types match schema
- Review validation error messages

### Submission Not Saved
- Check file permissions on ./submissions directory
- Verify disk space available
- Check for filename conflicts
- Review SUBMISSION_RECEIVER logs

### Production Files Not Created
- Ensure ./core directory exists
- Check permissions on ./core/production_inputs
- Verify submission status is 'pending'
- Check battle_data.json for errors

### Missing Episodes
- Check episode numbers in submission
- Verify no duplicate episode numbers
- Review production_inputs directory
- Check for processing errors

## Integration with Battle System

Submissions are integrated with the main battle tracking:

1. SUBMISSION_RECEIVER updates `pending_submissions` in battle_data.json
2. ENQUEUE_FOR_PRODUCTION marks submissions as `enqueued`
3. After production, update status to `produced`
4. After upload, update status to `uploaded` with video IDs
5. BATTLE_TRACKER can include submission metrics in rankings

## Best Practices

1. **Validate early and often** - catch errors before production
2. **Keep audit trail** - log all operations
3. **Backup before changes** - protect battle_data.json
4. **Review content thoroughly** - before any upload
5. **Test with samples** - use provided example files first
6. **Monitor disk space** - submissions and videos can be large
7. **Document exceptions** - note any manual interventions

## Sample Files

See the `examples/` directory for sample submissions:
- `submissions_CHATGPT_30000-30004.sample.json`
- `submissions_GROK_60000-60004.sample.json`

Use these to test the workflow before accepting real submissions.

## Support

For issues with the submission workflow:
1. Check validation errors in stderr
2. Verify submission format matches schema
3. Review battle_data.json for status
4. Check production_inputs directory structure
5. Ensure environment variables are set

## License

This submission system is part of the AI Oracle Root project. All submissions must comply with applicable terms of service and licenses.
