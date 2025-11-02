#!/usr/bin/env python3
"""
SUBMISSION_RECEIVER.py

Validates incoming submission JSON using simple validation (no external jsonschema dependency).
Saves validated submissions to ./submissions with timestamped filename.
Records pending submission in battle_data.json.
Prints JSON summary to stdout for pipeline integration.

Usage:
    # From file
    python SUBMISSION_RECEIVER.py --file submission.json
    
    # From stdin
    cat submission.json | python SUBMISSION_RECEIVER.py

Validation:
    - Checks required fields: llm_name, scripts
    - Validates scripts array structure
    - Ensures episode numbers are integers
    - Verifies script text is non-empty
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def simple_validate_submission(data):
    """
    Simple validation without external jsonschema dependency.
    Returns (is_valid, error_message).
    """
    # Check top-level required fields
    if not isinstance(data, dict):
        return False, "Submission must be a JSON object"
    
    if "llm_name" not in data:
        return False, "Missing required field: llm_name"
    
    if not isinstance(data["llm_name"], str) or not data["llm_name"]:
        return False, "llm_name must be a non-empty string"
    
    if "scripts" not in data:
        return False, "Missing required field: scripts"
    
    if not isinstance(data["scripts"], list) or len(data["scripts"]) == 0:
        return False, "scripts must be a non-empty array"
    
    # Validate each script entry
    for i, script in enumerate(data["scripts"]):
        if not isinstance(script, dict):
            return False, f"scripts[{i}] must be an object"
        
        # Required fields in script
        required_fields = ["episode", "script", "title"]
        for field in required_fields:
            if field not in script:
                return False, f"scripts[{i}] missing required field: {field}"
        
        # Validate episode is integer
        if not isinstance(script["episode"], int):
            return False, f"scripts[{i}].episode must be an integer"
        
        if script["episode"] < 1:
            return False, f"scripts[{i}].episode must be >= 1"
        
        # Validate script text is non-empty
        if not isinstance(script["script"], str) or not script["script"].strip():
            return False, f"scripts[{i}].script must be a non-empty string"
        
        # Validate title is non-empty
        if not isinstance(script["title"], str) or not script["title"].strip():
            return False, f"scripts[{i}].title must be a non-empty string"
        
        # Optional fields validation
        if "tags" in script:
            if not isinstance(script["tags"], list):
                return False, f"scripts[{i}].tags must be an array"
            if len(script["tags"]) > 30:
                return False, f"scripts[{i}].tags exceeds maximum of 30 tags"
        
        if "satire_label" in script:
            if not isinstance(script["satire_label"], bool):
                return False, f"scripts[{i}].satire_label must be a boolean"
    
    return True, None


def save_submission(data):
    """Save submission to ./submissions with timestamped filename."""
    # Create submissions directory if it doesn't exist
    submissions_dir = Path("submissions")
    submissions_dir.mkdir(exist_ok=True)
    
    # Generate timestamped filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    llm_name = data["llm_name"].lower()
    filename = f"submission_{llm_name}_{timestamp}.json"
    filepath = submissions_dir / filename
    
    # Add timestamp to data
    data["received_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Save to file
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    return str(filepath)


def update_battle_data(data, filepath):
    """Record pending submission in battle_data.json."""
    battle_data_path = Path("battle_data.json")
    
    if battle_data_path.exists():
        with open(battle_data_path, "r") as f:
            battle_data = json.load(f)
    else:
        battle_data = {
            "runs": [],
            "proofs": [],
            "pending_submissions": [],
            "llm_summary": {},
            "generated_at": None
        }
    
    # Add pending submission entry
    pending_entry = {
        "llm": data["llm_name"],
        "episodes": [s["episode"] for s in data["scripts"]],
        "count": len(data["scripts"]),
        "filepath": filepath,
        "received_at": data.get("received_at"),
        "status": "pending"
    }
    
    battle_data["pending_submissions"].append(pending_entry)
    battle_data["generated_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Save battle data
    with open(battle_data_path, "w") as f:
        json.dump(battle_data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Battle Royale Submission Receiver",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--file", help="Path to submission JSON file")
    
    args = parser.parse_args()
    
    # Read input
    if args.file:
        try:
            with open(args.file, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(json.dumps({
                "status": "error",
                "error": f"File not found: {args.file}"
            }))
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "status": "error",
                "error": f"Invalid JSON: {str(e)}"
            }))
            sys.exit(1)
    else:
        # Read from stdin
        try:
            data = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "status": "error",
                "error": f"Invalid JSON from stdin: {str(e)}"
            }))
            sys.exit(1)
    
    # Validate submission
    is_valid, error_msg = simple_validate_submission(data)
    if not is_valid:
        print(json.dumps({
            "status": "error",
            "error": f"Validation failed: {error_msg}"
        }))
        sys.exit(1)
    
    # Save submission
    filepath = save_submission(data)
    
    # Update battle data
    update_battle_data(data, filepath)
    
    # Print success summary
    summary = {
        "status": "success",
        "llm": data["llm_name"],
        "episodes": len(data["scripts"]),
        "episode_numbers": [s["episode"] for s in data["scripts"]],
        "filepath": filepath,
        "received_at": data["received_at"]
    }
    
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
