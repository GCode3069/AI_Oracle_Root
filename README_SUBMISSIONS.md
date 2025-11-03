# Submissions → Production Flow (SCARIFY Battle)

## Purpose

- Let LLM participants submit scripts as JSON.
- Centralized producer (Cursor) runs a standardized production pipeline to ensure fairness.
- Submissions are validated, recorded, and enqueued for production. No LLM directly uploads.

## Files you have:

- `submission_schema.json` — schema to validate submissions
- `SUBMISSION_RECEIVER.py` — accepts a JSON submission, validates, and writes to `./submissions`
- `ENQUEUE_FOR_PRODUCTION.py` — converts submissions into `./core/production_inputs` per episode
- `battle_data.json` — central tracker (pending_submissions and proofs)
- Example submissions in `./submissions_*.sample.json`

## Quick operator workflow

1. LLM or their operator prepares a JSON following `submission_schema.json`.

2. Submit by calling:
   ```bash
   python SUBMISSION_RECEIVER.py --file path/to/submission.json
   ```

3. Operator runs:
   ```bash
   python ENQUEUE_FOR_PRODUCTION.py
   ```
   This writes per-episode files into `core/production_inputs/`

4. Production pipeline (Cursor) watches `core/production_inputs/` and:
   - consumes each input file
   - produces video and `out.json` with keys: `video_path`, `title`, `description`, `tags`, `duration_sec`
   - writes proof entries back to `battle_data.json` under "proofs"

5. Tracker reads `battle_data.json` for revenue/leaderboard calculations.

## Safety & compliance (must read)

- **DO NOT** include API keys or private credentials in submission payloads.
- Operator must stage uploads (private/unlisted) and review content before publishing.
- All satire/parody must be labeled where appropriate to reduce moderation risk.
- Do not post content that violates platform policies (harassment, hateful content, targeted harassment of real individuals).
- If you find previously exposed keys or secrets, rotate them immediately.

## Validation guidance for LLM authors

- Scripts should be short: 32–45 words (~12–15s narration).
- Include a strong hook in the first 3 seconds.
- Mark `"satire_label": true` when applicable.
- Provide suggested title and optional tags.

## Example Submission

```json
{
  "llm_name": "ChatGPT_4o",
  "contact": "operator: /F:/AI_Oracle_Root/scarify",
  "scripts": [
    {
      "episode": 30000,
      "script": "Stop scrolling. Governments hide things by fear. Today's headline shows them pocketing panic while you freeze. Now you see it. Support truth. Bitcoin below.",
      "title": "Lincoln's WARNING #30000: They Profit From Your Panic #Shorts",
      "tags": ["lincoln", "horror", "truth", "shorts"],
      "satire_label": true,
      "notes": "Hook first 3s: 'Stop scrolling.'"
    }
  ]
}
```

## Testing the System

```bash
# 1. Validate and receive submission
python SUBMISSION_RECEIVER.py --file submissions_CHATGPT_30000-30004.sample.json

# 2. Enqueue for production
python ENQUEUE_FOR_PRODUCTION.py

# 3. Check what was created
ls core/production_inputs/

# 4. Check battle_data.json
cat battle_data.json
```


