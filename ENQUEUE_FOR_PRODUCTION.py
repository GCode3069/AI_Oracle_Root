#!/usr/bin/env python3
"""
ENQUEUE_FOR_PRODUCTION.py

Reads submission files in ./submissions, writes per-episode input files
into ./core/production_inputs (creating directories as needed).
Updates battle_data.json pending_submissions status to 'enqueued' and
records enqueued_at timestamp.

Does NOT call any external APIs - purely file-based processing.

Usage:
    python ENQUEUE_FOR_PRODUCTION.py

Process:
    1. Scan ./submissions for JSON files
    2. For each submission, create per-episode input files
    3. Update battle_data.json with enqueued status
    4. Report summary of enqueued episodes
"""

import json
from datetime import datetime
from pathlib import Path


def load_submissions():
    """Load all submission files from ./submissions directory."""
    submissions_dir = Path("submissions")
    
    if not submissions_dir.exists():
        print("No submissions directory found")
        return []
    
    submission_files = list(submissions_dir.glob("submission_*.json"))
    
    submissions = []
    for filepath in submission_files:
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                data["_filepath"] = str(filepath)
                submissions.append(data)
        except Exception as e:
            print(f"Warning: Failed to load {filepath}: {e}")
    
    return submissions


def create_production_inputs(submission):
    """Create per-episode input files in ./core/production_inputs."""
    # Create directory structure
    production_dir = Path("core/production_inputs")
    production_dir.mkdir(parents=True, exist_ok=True)
    
    llm_name = submission["llm_name"]
    created_files = []
    
    for script_entry in submission["scripts"]:
        episode = script_entry["episode"]
        
        # Create production input file
        filename = f"{llm_name}_episode_{episode}.json"
        filepath = production_dir / filename
        
        # Prepare production input data
        production_input = {
            "llm": llm_name,
            "episode": episode,
            "script": script_entry["script"],
            "title": script_entry["title"],
            "tags": script_entry.get("tags", []),
            "satire_label": script_entry.get("satire_label", False),
            "notes": script_entry.get("notes", ""),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "status": "ready_for_production"
        }
        
        # Write to file
        with open(filepath, "w") as f:
            json.dump(production_input, f, indent=2)
        
        created_files.append(str(filepath))
    
    return created_files


def update_pending_submission_status(submission_filepath):
    """Update battle_data.json to mark submission as enqueued."""
    battle_data_path = Path("battle_data.json")
    
    if not battle_data_path.exists():
        print("Warning: battle_data.json not found")
        return
    
    with open(battle_data_path, "r") as f:
        battle_data = json.load(f)
    
    # Find and update the pending submission
    for pending in battle_data.get("pending_submissions", []):
        if pending.get("filepath") == submission_filepath:
            pending["status"] = "enqueued"
            pending["enqueued_at"] = datetime.utcnow().isoformat() + "Z"
            break
    
    battle_data["generated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Save updated battle data
    with open(battle_data_path, "w") as f:
        json.dump(battle_data, f, indent=2)


def main():
    print("=" * 60)
    print("LLM BATTLE ROYALE - ENQUEUE FOR PRODUCTION")
    print("=" * 60)
    print()
    
    # Load submissions
    submissions = load_submissions()
    
    if not submissions:
        print("No submissions found in ./submissions")
        return
    
    print(f"Found {len(submissions)} submission(s)")
    print()
    
    total_episodes = 0
    total_files = 0
    
    for submission in submissions:
        llm_name = submission["llm_name"]
        episode_count = len(submission["scripts"])
        filepath = submission.get("_filepath", "unknown")
        
        print(f"Processing: {llm_name} ({episode_count} episodes)")
        
        # Create production inputs
        created_files = create_production_inputs(submission)
        
        # Update status in battle_data.json
        update_pending_submission_status(filepath)
        
        total_episodes += episode_count
        total_files += len(created_files)
        
        print(f"  Created {len(created_files)} production input file(s)")
        for f in created_files:
            print(f"    - {f}")
        print()
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Submissions processed: {len(submissions)}")
    print(f"Total episodes enqueued: {total_episodes}")
    print(f"Production input files created: {total_files}")
    print()
    print("Next steps:")
    print("  1. Review production input files in ./core/production_inputs")
    print("  2. Run video production pipeline for each episode")
    print("  3. Review and stage videos before upload")
    print("  4. Manually upload to YouTube with proper OAuth")
    print("=" * 60)


if __name__ == "__main__":
    main()
