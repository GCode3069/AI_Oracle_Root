#!/usr/bin/env python3
"""
ENQUEUE_FOR_PRODUCTION.py - Production Queue Manager

Reads submission files from ./submissions, writes per-episode input files
into ./core/production_inputs (creating directories as needed), and updates
battle_data.json pending_submissions status to 'enqueued' with timestamp.

Does not call any external APIs - purely file-based queue management.

Usage:
  python ENQUEUE_FOR_PRODUCTION.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def load_battle_data():
    """Load battle_data.json."""
    battle_file = Path("battle_data.json")
    if not battle_file.exists():
        return {
            "runs": [],
            "proofs": [],
            "pending_submissions": [],
            "llm_summary": {},
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
    
    with open(battle_file, "r") as f:
        return json.load(f)


def save_battle_data(data):
    """Save battle_data.json with updated timestamp."""
    data["generated_at"] = datetime.utcnow().isoformat() + "Z"
    with open("battle_data.json", "w") as f:
        json.dump(data, f, indent=2)


def get_pending_submissions():
    """Get list of submission files from ./submissions directory."""
    submissions_dir = Path("submissions")
    if not submissions_dir.exists():
        return []
    
    return list(submissions_dir.glob("submission_*.json"))


def create_production_input(llm_name, episode_num, script_data):
    """Create per-episode production input file."""
    production_dir = Path("core/production_inputs")
    production_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{llm_name}_ep{episode_num:05d}.json"
    filepath = production_dir / filename
    
    # Create production input structure
    production_input = {
        "llm_name": llm_name,
        "episode": episode_num,
        "title": script_data.get("title"),
        "script": script_data.get("script"),
        "tags": script_data.get("tags", []),
        "notes": script_data.get("notes", ""),
        "satire_label": script_data.get("satire_label", False),
        "enqueued_at": datetime.utcnow().isoformat() + "Z",
        "status": "queued"
    }
    
    with open(filepath, "w") as f:
        json.dump(production_input, f, indent=2)
    
    return str(filepath)


def process_submission_file(submission_path):
    """Process a single submission file."""
    with open(submission_path, "r") as f:
        submission_data = json.load(f)
    
    llm_name = submission_data.get("llm_name")
    scripts = submission_data.get("scripts", [])
    
    production_files = []
    
    for script in scripts:
        episode_num = script.get("episode")
        production_file = create_production_input(llm_name, episode_num, script)
        production_files.append(production_file)
    
    return production_files


def update_submission_status(battle_data, submission_path, production_files):
    """Update pending submission status to 'enqueued'."""
    submission_path_str = str(submission_path)
    
    for pending in battle_data.get("pending_submissions", []):
        if pending.get("filepath") == submission_path_str:
            pending["status"] = "enqueued"
            pending["enqueued_at"] = datetime.utcnow().isoformat() + "Z"
            pending["production_files"] = production_files
            break


def main():
    print("=" * 60)
    print("LLM BATTLE ROYALE - PRODUCTION QUEUE MANAGER")
    print("=" * 60)
    
    # Load battle data
    battle_data = load_battle_data()
    
    # Get pending submissions
    submission_files = get_pending_submissions()
    
    if not submission_files:
        print("\n⚠️  No submission files found in ./submissions")
        print("Run SUBMISSION_RECEIVER.py first to receive submissions.")
        return
    
    print(f"\n📂 Found {len(submission_files)} submission file(s)")
    
    total_enqueued = 0
    
    # Process each submission
    for submission_path in submission_files:
        print(f"\n📝 Processing: {submission_path.name}")
        
        try:
            production_files = process_submission_file(submission_path)
            update_submission_status(battle_data, submission_path, production_files)
            
            print(f"  ✅ Created {len(production_files)} production input(s)")
            for pf in production_files:
                print(f"     - {Path(pf).name}")
            
            total_enqueued += len(production_files)
            
        except Exception as e:
            print(f"  ❌ Error processing {submission_path.name}: {e}")
            continue
    
    # Save updated battle data
    save_battle_data(battle_data)
    
    print("\n" + "=" * 60)
    print(f"✅ ENQUEUE COMPLETE")
    print(f"   Total episodes enqueued: {total_enqueued}")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review production inputs in ./core/production_inputs")
    print("2. Run production pipeline on queued episodes")
    print("3. Review generated videos before upload")
    print("4. Update battle_data.json with production results")


if __name__ == "__main__":
    main()
