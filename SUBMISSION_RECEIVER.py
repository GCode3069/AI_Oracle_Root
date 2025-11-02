#!/usr/bin/env python3
"""
SUBMISSION_RECEIVER.py - Validates and saves LLM script submissions

This script validates incoming submission JSON using simple validation
(no external jsonschema dependency), saves to ./submissions with timestamped
filename, and records pending submission in battle_data.json.

Usage:
  python SUBMISSION_RECEIVER.py --file submission.json
  cat submission.json | python SUBMISSION_RECEIVER.py
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


VALID_LLMS = ["ChatGPT", "Claude", "Gemini", "Grok", "Llama"]


def validate_submission(data):
    """Validate submission structure without external jsonschema library."""
    errors = []
    
    # Check required top-level fields
    if "llm_name" not in data:
        errors.append("Missing required field: llm_name")
    elif data["llm_name"] not in VALID_LLMS:
        errors.append(f"Invalid llm_name. Must be one of: {', '.join(VALID_LLMS)}")
    
    if "scripts" not in data:
        errors.append("Missing required field: scripts")
    elif not isinstance(data["scripts"], list):
        errors.append("Field 'scripts' must be an array")
    elif len(data["scripts"]) == 0:
        errors.append("Field 'scripts' must contain at least one item")
    else:
        # Validate each script
        for idx, script in enumerate(data["scripts"]):
            if not isinstance(script, dict):
                errors.append(f"Script at index {idx} must be an object")
                continue
            
            # Check required script fields
            if "episode" not in script:
                errors.append(f"Script at index {idx}: Missing required field 'episode'")
            elif not isinstance(script["episode"], int) or script["episode"] < 1:
                errors.append(f"Script at index {idx}: 'episode' must be an integer >= 1")
            
            if "script" not in script:
                errors.append(f"Script at index {idx}: Missing required field 'script'")
            elif not isinstance(script["script"], str) or len(script["script"]) == 0:
                errors.append(f"Script at index {idx}: 'script' must be a non-empty string")
            
            if "title" not in script:
                errors.append(f"Script at index {idx}: Missing required field 'title'")
            elif not isinstance(script["title"], str) or len(script["title"]) == 0:
                errors.append(f"Script at index {idx}: 'title' must be a non-empty string")
            elif len(script["title"]) > 100:
                errors.append(f"Script at index {idx}: 'title' must be <= 100 characters")
            
            # Validate optional fields
            if "tags" in script:
                if not isinstance(script["tags"], list):
                    errors.append(f"Script at index {idx}: 'tags' must be an array")
                elif len(script["tags"]) > 10:
                    errors.append(f"Script at index {idx}: 'tags' must have <= 10 items")
            
            if "satire_label" in script and not isinstance(script["satire_label"], bool):
                errors.append(f"Script at index {idx}: 'satire_label' must be a boolean")
    
    return errors


def save_submission(data):
    """Save submission to ./submissions with timestamped filename."""
    submissions_dir = Path("submissions")
    submissions_dir.mkdir(exist_ok=True)
    
    llm_name = data.get("llm_name", "unknown")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"submission_{llm_name}_{timestamp}.json"
    filepath = submissions_dir / filename
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    return str(filepath)


def record_pending_submission(llm_name, filepath, script_count):
    """Record pending submission in battle_data.json."""
    battle_file = Path("battle_data.json")
    
    # Load or create battle data
    if battle_file.exists():
        with open(battle_file, "r") as f:
            battle_data = json.load(f)
    else:
        battle_data = {
            "runs": [],
            "proofs": [],
            "pending_submissions": [],
            "llm_summary": {},
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }
    
    # Add pending submission record
    pending_record = {
        "llm_name": llm_name,
        "filepath": filepath,
        "script_count": script_count,
        "status": "pending",
        "received_at": datetime.utcnow().isoformat() + "Z"
    }
    
    battle_data["pending_submissions"].append(pending_record)
    battle_data["generated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Save battle data
    with open(battle_file, "w") as f:
        json.dump(battle_data, f, indent=2)
    
    return pending_record


def main():
    parser = argparse.ArgumentParser(
        description="LLM Battle Royale Submission Receiver"
    )
    parser.add_argument("--file", help="Path to submission JSON file")
    
    args = parser.parse_args()
    
    # Read input
    if args.file:
        with open(args.file, "r") as f:
            data = json.load(f)
    else:
        # Read from stdin
        data = json.load(sys.stdin)
    
    # Validate submission
    errors = validate_submission(data)
    
    if errors:
        result = {
            "status": "error",
            "errors": errors,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        print(json.dumps(result, indent=2))
        sys.exit(1)
    
    # Save submission
    filepath = save_submission(data)
    
    # Record in battle_data.json
    llm_name = data["llm_name"]
    script_count = len(data["scripts"])
    pending_record = record_pending_submission(llm_name, filepath, script_count)
    
    # Output success summary
    result = {
        "status": "success",
        "llm_name": llm_name,
        "script_count": script_count,
        "saved_to": filepath,
        "pending_record": pending_record,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
