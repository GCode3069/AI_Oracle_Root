#!/usr/bin/env python3
"""
ENQUEUE_FOR_PRODUCTION.py - LLM Battle Royale Production Queue Manager

This script reads submission files from ./submissions, writes per-episode input files
into ./core/production_inputs, and updates battle_data.json to mark submissions as
enqueued. It does NOT call external APIs or upload anything.

Usage:
    python ENQUEUE_FOR_PRODUCTION.py
    python ENQUEUE_FOR_PRODUCTION.py --submission-file submissions/ChatGPT_20250101_120000.json

Flow:
    1. Read pending submissions from ./submissions
    2. Parse each submission JSON
    3. Create per-episode input files in ./core/production_inputs
    4. Update battle_data.json status to "enqueued"
    5. Print summary

Safety:
    - Does NOT call external APIs
    - Does NOT upload or publish anything
    - Only creates local input files for production pipeline
    - Operator must manually run production pipeline
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


BATTLE_DATA_FILE = "battle_data.json"
SUBMISSIONS_DIR = "submissions"
PRODUCTION_INPUTS_DIR = "core/production_inputs"


def load_battle_data():
    """Load existing battle data."""
    if not os.path.exists(BATTLE_DATA_FILE):
        print(f"❌ Battle data file not found: {BATTLE_DATA_FILE}")
        sys.exit(1)
    
    with open(BATTLE_DATA_FILE, 'r') as f:
        return json.load(f)


def save_battle_data(data):
    """Save battle data to JSON file."""
    data["generated_at"] = datetime.utcnow().isoformat()
    with open(BATTLE_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_pending_submissions(battle_data, specific_file=None):
    """
    Get list of pending submissions to process.
    
    Args:
        battle_data: Battle data dictionary
        specific_file: If provided, only process this specific submission file
    
    Returns:
        List of pending submission entries
    """
    if specific_file:
        # Find the specific submission in pending list
        for sub in battle_data.get("pending_submissions", []):
            if sub["filename"] == os.path.basename(specific_file):
                if sub["status"] == "pending":
                    return [sub]
                else:
                    print(f"⚠️  Submission {specific_file} is not pending (status: {sub['status']})")
                    return []
        print(f"❌ Submission not found in pending list: {specific_file}")
        return []
    else:
        # Get all pending submissions
        return [sub for sub in battle_data.get("pending_submissions", [])
                if sub["status"] == "pending"]


def read_submission_file(filename):
    """Read submission JSON from file."""
    filepath = os.path.join(SUBMISSIONS_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"❌ Submission file not found: {filepath}")
        return None
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {filepath}: {e}")
        return None


def write_episode_input_files(submission):
    """
    Write per-episode input files to production_inputs directory.
    
    Returns list of created files.
    """
    # Ensure production inputs directory exists
    os.makedirs(PRODUCTION_INPUTS_DIR, exist_ok=True)
    
    created_files = []
    
    for script_data in submission["scripts"]:
        episode_num = script_data["episode"]
        
        # Write script text file
        script_filename = f"episode_{episode_num}_script.txt"
        script_filepath = os.path.join(PRODUCTION_INPUTS_DIR, script_filename)
        with open(script_filepath, 'w', encoding='utf-8') as f:
            f.write(script_data["script"])
        created_files.append(script_filename)
        
        # Write metadata JSON file
        metadata = {
            "episode": episode_num,
            "title": script_data["title"],
            "tags": script_data.get("tags", []),
            "llm_name": submission["llm_name"],
            "notes": script_data.get("notes", ""),
            "satire_label": script_data.get("satire_label", False),
            "content_warnings": script_data.get("content_warnings", []),
            "enqueued_at": datetime.utcnow().isoformat()
        }
        
        metadata_filename = f"episode_{episode_num}_metadata.json"
        metadata_filepath = os.path.join(PRODUCTION_INPUTS_DIR, metadata_filename)
        with open(metadata_filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        created_files.append(metadata_filename)
    
    return created_files


def update_submission_status(battle_data, filename, created_files):
    """Update submission status in battle_data.json to enqueued."""
    for sub in battle_data["pending_submissions"]:
        if sub["filename"] == filename:
            sub["status"] = "enqueued"
            sub["enqueued_at"] = datetime.utcnow().isoformat()
            sub["production_files"] = created_files
            break


def print_summary(processed_count, total_episodes, total_files):
    """Print processing summary."""
    print("\n" + "=" * 60)
    print("✅ ENQUEUE COMPLETE")
    print("=" * 60)
    print(f"Submissions processed: {processed_count}")
    print(f"Episodes queued: {total_episodes}")
    print(f"Production files created: {total_files}")
    print(f"Output directory: {PRODUCTION_INPUTS_DIR}")
    print("\n⚠️  NEXT STEPS:")
    print("1. Review production input files in core/production_inputs/")
    print("2. Run production pipeline (separate script)")
    print("3. Review generated content")
    print("4. Implement uploader with OAuth (separate script)")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Battle Royale Production Queue Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all pending submissions
  python ENQUEUE_FOR_PRODUCTION.py
  
  # Process specific submission file
  python ENQUEUE_FOR_PRODUCTION.py --submission-file submissions/ChatGPT_20250101_120000.json

Notes:
  - Reads submissions from ./submissions/
  - Writes to ./core/production_inputs/
  - Updates battle_data.json status to "enqueued"
  - Does NOT call external APIs or upload anything
        """
    )
    
    parser.add_argument("--submission-file", "-f",
                       help="Process specific submission file only")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎬 LLM Battle Royale - Production Queue Manager")
    print("=" * 60)
    
    # Load battle data
    battle_data = load_battle_data()
    
    # Get pending submissions
    pending = get_pending_submissions(battle_data, args.submission_file)
    
    if not pending:
        print("✅ No pending submissions to process")
        sys.exit(0)
    
    print(f"\n📋 Found {len(pending)} pending submission(s)")
    
    # Process each pending submission
    processed_count = 0
    total_episodes = 0
    total_files = 0
    
    for sub_entry in pending:
        filename = sub_entry["filename"]
        print(f"\n🔄 Processing: {filename}")
        
        # Read submission file
        submission = read_submission_file(filename)
        if not submission:
            print(f"⚠️  Skipping {filename} due to read error")
            continue
        
        # Write episode input files
        try:
            created_files = write_episode_input_files(submission)
            episode_count = len(submission["scripts"])
            
            print(f"  ✅ Created {len(created_files)} production files for {episode_count} episodes")
            
            # Update status
            update_submission_status(battle_data, filename, created_files)
            
            processed_count += 1
            total_episodes += episode_count
            total_files += len(created_files)
            
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
            continue
    
    # Save updated battle data
    if processed_count > 0:
        save_battle_data(battle_data)
        print(f"\n✅ Updated {BATTLE_DATA_FILE}")
    
    # Print summary
    print_summary(processed_count, total_episodes, total_files)


if __name__ == "__main__":
    main()
