#!/usr/bin/env python3
"""
SUBMISSION_RECEIVER.py
Validates and saves LLM script submissions for the Battle Royale project.

This script validates incoming submission JSON against the submission schema,
saves submissions to ./submissions directory with timestamped filenames,
and records pending submissions in battle_data.json.

Usage:
    python SUBMISSION_RECEIVER.py --file submission.json
    cat submission.json | python SUBMISSION_RECEIVER.py

Validation includes:
    - Required fields presence
    - Field types and formats
    - Episode number ranges
    - Script content validation

Output:
    - Saves to ./submissions/<llm_name>_<timestamp>.json
    - Updates battle_data.json with pending submission record
    - Prints JSON summary to stdout
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BATTLE_DATA_PATH = 'battle_data.json'
SUBMISSIONS_DIR = 'submissions'
SCHEMA_PATH = 'submission_schema.json'


def load_battle_data():
    """Load current battle data from JSON file."""
    path = Path(BATTLE_DATA_PATH)
    if not path.exists():
        return {
            'runs': [],
            'proofs': {},
            'pending_submissions': [],
            'llm_summary': {},
            'generated_at': None
        }
    
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"ERROR: Failed to load {BATTLE_DATA_PATH}: {e}", file=sys.stderr)
        sys.exit(1)


def save_battle_data(data):
    """Save battle data to JSON file."""
    data['generated_at'] = datetime.now(timezone.utc).isoformat()
    path = Path(BATTLE_DATA_PATH)
    path.write_text(json.dumps(data, indent=2))


def validate_submission(submission):
    """Validate submission structure and content (simple validation without jsonschema)."""
    errors = []
    
    # Check required top-level fields
    required_fields = ['llm_name', 'scripts', 'submitter', 'submitted_at']
    for field in required_fields:
        if field not in submission:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Validate llm_name
    if not isinstance(submission['llm_name'], str) or not submission['llm_name'].strip():
        errors.append("llm_name must be a non-empty string")
    
    # Validate scripts array
    if not isinstance(submission['scripts'], list):
        errors.append("scripts must be an array")
    elif len(submission['scripts']) == 0:
        errors.append("scripts array must not be empty")
    else:
        # Validate each script entry
        for i, script in enumerate(submission['scripts']):
            if not isinstance(script, dict):
                errors.append(f"scripts[{i}] must be an object")
                continue
            
            # Check required script fields
            script_required = ['episode', 'script', 'title']
            for field in script_required:
                if field not in script:
                    errors.append(f"scripts[{i}] missing required field: {field}")
            
            # Validate episode number
            if 'episode' in script:
                if not isinstance(script['episode'], int):
                    errors.append(f"scripts[{i}].episode must be an integer")
                elif script['episode'] < 0:
                    errors.append(f"scripts[{i}].episode must be non-negative")
            
            # Validate script content
            if 'script' in script:
                if not isinstance(script['script'], str) or not script['script'].strip():
                    errors.append(f"scripts[{i}].script must be a non-empty string")
            
            # Validate title
            if 'title' in script:
                if not isinstance(script['title'], str) or not script['title'].strip():
                    errors.append(f"scripts[{i}].title must be a non-empty string")
            
            # Validate optional fields
            if 'tags' in script and not isinstance(script['tags'], list):
                errors.append(f"scripts[{i}].tags must be an array")
            
            if 'satire_label' in script and not isinstance(script['satire_label'], bool):
                errors.append(f"scripts[{i}].satire_label must be a boolean")
    
    # Validate submitter
    if not isinstance(submission['submitter'], str) or not submission['submitter'].strip():
        errors.append("submitter must be a non-empty string")
    
    # Validate submitted_at (should be ISO format)
    if not isinstance(submission['submitted_at'], str):
        errors.append("submitted_at must be a string (ISO 8601 format)")
    
    return len(errors) == 0, errors


def save_submission(submission):
    """Save submission to submissions directory."""
    # Create submissions directory if it doesn't exist
    submissions_dir = Path(SUBMISSIONS_DIR)
    submissions_dir.mkdir(exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    llm_name = submission['llm_name'].replace(' ', '_').upper()
    filename = f"{llm_name}_{timestamp}.json"
    
    filepath = submissions_dir / filename
    filepath.write_text(json.dumps(submission, indent=2))
    
    return str(filepath)


def record_pending_submission(battle_data, submission, filepath):
    """Record pending submission in battle_data.json."""
    timestamp = datetime.now(timezone.utc).isoformat()
    
    pending_record = {
        'llm_name': submission['llm_name'],
        'submitter': submission['submitter'],
        'submitted_at': submission['submitted_at'],
        'received_at': timestamp,
        'filepath': filepath,
        'episode_count': len(submission['scripts']),
        'episodes': [s['episode'] for s in submission['scripts']],
        'status': 'pending'
    }
    
    battle_data['pending_submissions'].append(pending_record)


def print_summary(submission, filepath):
    """Print JSON summary to stdout."""
    summary = {
        'status': 'success',
        'llm_name': submission['llm_name'],
        'submitter': submission['submitter'],
        'episode_count': len(submission['scripts']),
        'episodes': [s['episode'] for s in submission['scripts']],
        'filepath': filepath,
        'received_at': datetime.now(timezone.utc).isoformat()
    }
    
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description='LLM Battle Royale Submission Receiver'
    )
    parser.add_argument('--file', help='Path to submission JSON file (or read from stdin)')
    
    args = parser.parse_args()
    
    # Read submission
    if args.file:
        try:
            submission = json.loads(Path(args.file).read_text())
        except Exception as e:
            print(json.dumps({
                'status': 'error',
                'error': f'Failed to read file: {e}'
            }), file=sys.stderr)
            sys.exit(1)
    else:
        try:
            submission = json.load(sys.stdin)
        except Exception as e:
            print(json.dumps({
                'status': 'error',
                'error': f'Failed to parse JSON from stdin: {e}'
            }), file=sys.stderr)
            sys.exit(1)
    
    # Validate submission
    valid, errors = validate_submission(submission)
    
    if not valid:
        print(json.dumps({
            'status': 'error',
            'error': 'Validation failed',
            'validation_errors': errors
        }), file=sys.stderr)
        sys.exit(1)
    
    # Save submission
    filepath = save_submission(submission)
    
    # Load and update battle data
    battle_data = load_battle_data()
    record_pending_submission(battle_data, submission, filepath)
    save_battle_data(battle_data)
    
    # Print summary
    print_summary(submission, filepath)
    
    return 0


if __name__ == '__main__':
    exit(main())
