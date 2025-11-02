#!/usr/bin/env python3
"""
ENQUEUE_FOR_PRODUCTION.py
Enqueues validated submissions for production workflow.

This script reads validated submission files from ./submissions directory,
creates per-episode input files in ./core/production_inputs directory,
and updates battle_data.json to mark submissions as enqueued.

Does NOT call any external APIs - purely prepares local files for production.

Usage:
    python ENQUEUE_FOR_PRODUCTION.py
    python ENQUEUE_FOR_PRODUCTION.py --submission ./submissions/CHATGPT_20231101_120000.json

Workflow:
    1. Read submission files from ./submissions
    2. Create production input files in ./core/production_inputs
    3. Update battle_data.json pending_submissions status to 'enqueued'
    4. Record enqueued_at timestamp
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BATTLE_DATA_PATH = 'battle_data.json'
SUBMISSIONS_DIR = 'submissions'
PRODUCTION_INPUTS_DIR = 'core/production_inputs'


def load_battle_data():
    """Load current battle data from JSON file."""
    path = Path(BATTLE_DATA_PATH)
    if not path.exists():
        print(f"ERROR: {BATTLE_DATA_PATH} not found")
        return None
    
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"ERROR: Failed to load {BATTLE_DATA_PATH}: {e}")
        return None


def save_battle_data(data):
    """Save battle data to JSON file."""
    data['generated_at'] = datetime.now(timezone.utc).isoformat()
    path = Path(BATTLE_DATA_PATH)
    path.write_text(json.dumps(data, indent=2))


def get_pending_submissions(battle_data, specific_file=None):
    """Get pending submissions that need to be enqueued."""
    pending = battle_data.get('pending_submissions', [])
    
    if specific_file:
        # Filter to specific submission
        return [s for s in pending if s.get('filepath') == specific_file and s.get('status') == 'pending']
    
    # Return all pending submissions
    return [s for s in pending if s.get('status') == 'pending']


def load_submission_file(filepath):
    """Load submission JSON file."""
    try:
        return json.loads(Path(filepath).read_text())
    except Exception as e:
        print(f"ERROR: Failed to load {filepath}: {e}")
        return None


def create_production_input(script_entry, llm_name):
    """Create production input file for a single episode."""
    production_input = {
        'llm_name': llm_name,
        'episode': script_entry['episode'],
        'title': script_entry['title'],
        'script': script_entry['script'],
        'tags': script_entry.get('tags', []),
        'satire_label': script_entry.get('satire_label', False),
        'notes': script_entry.get('notes', ''),
        'created_at': datetime.now(timezone.utc).isoformat(),
        'status': 'ready_for_production'
    }
    
    return production_input


def save_production_input(production_input, llm_name, episode):
    """Save production input to file."""
    # Create directory structure
    production_dir = Path(PRODUCTION_INPUTS_DIR)
    production_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename
    llm_dir = production_dir / llm_name.upper()
    llm_dir.mkdir(exist_ok=True)
    
    filename = f"episode_{episode:05d}.json"
    filepath = llm_dir / filename
    
    filepath.write_text(json.dumps(production_input, indent=2))
    
    return str(filepath)


def enqueue_submission(submission_record, battle_data):
    """Enqueue a single submission for production."""
    filepath = submission_record.get('filepath')
    
    print(f"\nProcessing: {filepath}")
    
    # Load submission file
    submission = load_submission_file(filepath)
    if not submission:
        return False
    
    llm_name = submission['llm_name']
    scripts = submission['scripts']
    
    print(f"  LLM: {llm_name}")
    print(f"  Episodes: {len(scripts)}")
    
    # Create production inputs for each episode
    production_files = []
    for script in scripts:
        episode = script['episode']
        production_input = create_production_input(script, llm_name)
        prod_filepath = save_production_input(production_input, llm_name, episode)
        production_files.append(prod_filepath)
        print(f"    ✓ Created: {prod_filepath}")
    
    # Update submission status in battle_data
    timestamp = datetime.now(timezone.utc).isoformat()
    submission_record['status'] = 'enqueued'
    submission_record['enqueued_at'] = timestamp
    submission_record['production_files'] = production_files
    
    print(f"  ✓ Enqueued at {timestamp}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Enqueue submissions for production workflow'
    )
    parser.add_argument('--submission', help='Path to specific submission file (optional)')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("LLM BATTLE ROYALE - ENQUEUE FOR PRODUCTION")
    print("=" * 70)
    
    # Load battle data
    battle_data = load_battle_data()
    if not battle_data:
        return 1
    
    # Get pending submissions
    pending = get_pending_submissions(battle_data, args.submission)
    
    if not pending:
        if args.submission:
            print(f"\nNo pending submission found for: {args.submission}")
        else:
            print("\nNo pending submissions found")
        print("All submissions have been enqueued or there are no submissions yet")
        return 0
    
    print(f"\nFound {len(pending)} pending submission(s)")
    
    # Process each pending submission
    success_count = 0
    for submission_record in pending:
        if enqueue_submission(submission_record, battle_data):
            success_count += 1
    
    # Save updated battle data
    save_battle_data(battle_data)
    
    print("\n" + "=" * 70)
    print(f"✓ ENQUEUED {success_count}/{len(pending)} SUBMISSION(S)")
    print("=" * 70)
    print("\nNEXT STEPS:")
    print("1. Review production input files in ./core/production_inputs")
    print("2. Run video generation pipeline for each episode")
    print("3. Review generated videos before upload")
    print("4. Manually upload to YouTube with proper OAuth")
    
    return 0


if __name__ == '__main__':
    exit(main())
