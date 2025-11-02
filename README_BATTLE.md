# LLM Battle Royale - Orchestration Guide

## Overview

The LLM Battle Royale is a competition framework for generating and tracking AI-generated content across multiple LLM providers. This system provides safe, auditable workflows for script submission, production, and elimination tracking.

## Quick Start

1. **Setup Environment**
   ```bash
   # Copy environment template
   cp .env.example .env
   
   # Edit .env and add your API keys (NEVER commit this file)
   nano .env
   
   # Run bootstrap to create directories
   pwsh BATTLE_BOOTSTRAP.ps1
   ```

2. **Dry Run Test**
   ```bash
   # Test orchestrator without making API calls
   python BATTLE_CTR_INTEGRATION.py --llm chatgpt --round 1 --videos 5 --start 30000 --dry-run
   ```

3. **Generate Scripts**
   ```bash
   # Generate scripts for ChatGPT round 1
   python BATTLE_CTR_INTEGRATION.py --llm chatgpt --round 1 --videos 5 --start 30000
   
   # Generate scripts for Grok round 1
   python BATTLE_CTR_INTEGRATION.py --llm grok --round 1 --videos 5 --start 60000
   ```

4. **Track Elimination**
   ```bash
   # View current standings
   python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase initial
   
   # Eliminate bottom 2 LLMs
   python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase quarterfinal --eliminate 2
   ```

## Safety Notes

### Critical Security Rules

⚠️ **NEVER commit secrets to version control**
- Always use `.env` for API keys and credentials
- Add `.env` to `.gitignore`
- Use `.env.example` as a template only

⚠️ **No automatic uploads to YouTube**
- Scripts do NOT auto-upload to YouTube
- Operator must manually review and upload
- Use OAuth with proper staging environment
- Verify TOS compliance before upload

⚠️ **Manual review required**
- Review all generated scripts before production
- Verify content meets platform guidelines
- Check for satire labels and disclaimers
- Ensure proper attribution for media

## Wiring Generator Scripts

The orchestrator uses the `GENERATORS` mapping in `BATTLE_CTR_INTEGRATION.py`:

```python
GENERATORS = {
    "chatgpt": "scripts/generate_chatgpt_scripts.py",
    "grok": "scripts/generate_grok_scripts.py",
    "claude": "scripts/generate_claude_scripts.py",
    "gemini": "scripts/generate_gemini_scripts.py",
}
```

### Creating a Generator Script

Each generator script should:
1. Accept command-line arguments for episode range
2. Call the LLM API to generate scripts
3. Save scripts to standardized output format
4. Return success/failure status

Example generator template:
```python
#!/usr/bin/env python3
import argparse
import os

def generate_scripts(start_episode, count):
    # Call LLM API
    # Save scripts to output directory
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--count", type=int, required=True)
    args = parser.parse_args()
    generate_scripts(args.start, args.count)
```

## YouTube Uploader Integration

The uploader is intentionally separate from generation:

1. **Manual Review First**
   - Review all generated content
   - Verify metadata and tags
   - Check TOS compliance

2. **Staging Upload**
   - Upload as unlisted/private first
   - Review on YouTube platform
   - Make any necessary edits

3. **OAuth Setup Required**
   - Use YouTube Data API v3
   - Implement OAuth 2.0 flow
   - Store credentials securely (not in repo)

4. **Example Uploader Pattern**
   ```python
   # Operator implements separately
   python upload_to_youtube.py --video path/to/video.mp4 --metadata metadata.json --unlisted
   ```

## Proofs and Evidence

All operations are tracked in `battle_data.json`:

- **runs**: Each generation run with timestamps
- **proofs**: Per-video proof entries
- **pending_submissions**: Queue of submissions awaiting production
- **llm_summary**: Aggregated stats per LLM

Review proofs regularly to ensure audit trail integrity.

## Operator Checklist

Before each production run:

- [ ] Environment variables populated in `.env`
- [ ] Generator scripts tested and working
- [ ] Dry-run executed successfully
- [ ] Output directories created
- [ ] Review workflow documented
- [ ] Upload staging environment configured
- [ ] TOS compliance verified
- [ ] No secrets in version control

## Support

For issues or questions:
1. Review this README
2. Check `battle_data.json` for run history
3. Verify environment variables
4. Test with `--dry-run` flag

## License and Attribution

Ensure all generated content:
- Includes proper attribution for media sources
- Complies with platform Terms of Service
- Contains satire/parody labels where appropriate
- Respects copyright and fair use guidelines
