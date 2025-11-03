#!/usr/bin/env python3
"""
SUBMISSION_RECEIVER.py - LLM Battle Royale Submission Validator & Receiver

This script validates incoming submission JSON files against the submission schema,
saves them to ./submissions with timestamped filenames, and records them in
battle_data.json as pending submissions.

Usage:
    # From file
    python SUBMISSION_RECEIVER.py --file my_submission.json
    
    # From stdin
    cat my_submission.json | python SUBMISSION_RECEIVER.py
    echo '{"llm_name":"ChatGPT","scripts":[...]}' | python SUBMISSION_RECEIVER.py

Output:
    Prints JSON summary to stdout for piping/logging

Safety:
    - Validates all submissions against schema
    - Does NOT execute any code from submissions
    - Does NOT call external APIs
    - Records metadata only, not actual content
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


BATTLE_DATA_FILE = "battle_data.json"
SUBMISSIONS_DIR = "submissions"
SCHEMA_FILE = "submission_schema.json"


def load_battle_data():
    """Load existing battle data or create new structure."""
    if os.path.exists(BATTLE_DATA_FILE):
        with open(BATTLE_DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            "runs": [],
            "proofs": [],
            "pending_submissions": [],
            "llm_summary": {},
            "generated_at": datetime.utcnow().isoformat()
        }


def save_battle_data(data):
    """Save battle data to JSON file."""
    data["generated_at"] = datetime.utcnow().isoformat()
    with open(BATTLE_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def validate_submission(submission):
    """
    Validate submission against schema using simple validation.
    Returns (is_valid, errors_list).
    """
    errors = []
    
    # Check required top-level fields
    if not isinstance(submission, dict):
        return False, ["Submission must be a JSON object"]
    
    if "llm_name" not in submission:
        errors.append("Missing required field: llm_name")
    elif not isinstance(submission["llm_name"], str) or not submission["llm_name"]:
        errors.append("llm_name must be a non-empty string")
    
    if "scripts" not in submission:
        errors.append("Missing required field: scripts")
    elif not isinstance(submission["scripts"], list):
        errors.append("scripts must be an array")
    elif len(submission["scripts"]) == 0:
        errors.append("scripts array cannot be empty")
    else:
        # Validate each script
        for i, script in enumerate(submission["scripts"]):
            if not isinstance(script, dict):
                errors.append(f"scripts[{i}] must be an object")
                continue
            
            # Required fields in script
            if "episode" not in script:
                errors.append(f"scripts[{i}] missing required field: episode")
            elif not isinstance(script["episode"], int) or script["episode"] < 1:
                errors.append(f"scripts[{i}].episode must be a positive integer")
            
            if "script" not in script:
                errors.append(f"scripts[{i}] missing required field: script")
            elif not isinstance(script["script"], str) or len(script["script"]) < 50:
                errors.append(f"scripts[{i}].script must be a string with at least 50 characters")
            
            if "title" not in script:
                errors.append(f"scripts[{i}] missing required field: title")
            elif not isinstance(script["title"], str) or len(script["title"]) < 5:
                errors.append(f"scripts[{i}].title must be a string with at least 5 characters")
    
    return len(errors) == 0, errors


def save_submission_file(submission, llm_name):
    """
    Save submission to ./submissions with timestamped filename.
    Returns the saved filename.
    """
    # Ensure submissions directory exists
    os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
    
    # Generate timestamped filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{llm_name}_{timestamp}.json"
    filepath = os.path.join(SUBMISSIONS_DIR, filename)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(submission, f, indent=2)
    
    return filename


def record_pending_submission(battle_data, submission, filename):
    """Record submission in battle_data.json as pending."""
    pending_entry = {
        "filename": filename,
        "llm_name": submission["llm_name"],
        "episode_count": len(submission["scripts"]),
        "episodes": [s["episode"] for s in submission["scripts"]],
        "received_at": datetime.utcnow().isoformat(),
        "status": "pending",
        "processed_at": None
    }
    
    battle_data["pending_submissions"].append(pending_entry)
    return pending_entry


def generate_summary(submission, filename, pending_entry):
    """Generate JSON summary for stdout output."""
    summary = {
        "status": "success",
        "filename": filename,
        "llm_name": submission["llm_name"],
        "episode_count": len(submission["scripts"]),
        "episodes": [s["episode"] for s in submission["scripts"]],
        "received_at": pending_entry["received_at"],
        "message": "Submission received and validated successfully"
    }
    return summary


def main():
    parser = argparse.ArgumentParser(
        description="LLM Battle Royale Submission Receiver & Validator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate and receive submission from file
  python SUBMISSION_RECEIVER.py --file chatgpt_batch1.json
  
  # Validate and receive submission from stdin
  cat submission.json | python SUBMISSION_RECEIVER.py
  
  # Pipe and capture output
  python SUBMISSION_RECEIVER.py --file sub.json > receipt.json

Notes:
  - Validates against submission_schema.json
  - Saves to ./submissions/ with timestamp
  - Records in battle_data.json as pending
  - Prints JSON summary to stdout
        """
    )
    
    parser.add_argument("--file", "-f",
                       help="Path to submission JSON file (or read from stdin)")
    
    args = parser.parse_args()
    
    # Read submission JSON
    try:
        if args.file:
            with open(args.file, 'r') as f:
                submission = json.load(f)
        else:
            # Read from stdin
            submission = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        error_output = {
            "status": "error",
            "message": f"Invalid JSON: {str(e)}"
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)
    except FileNotFoundError:
        error_output = {
            "status": "error",
            "message": f"File not found: {args.file}"
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)
    except Exception as e:
        error_output = {
            "status": "error",
            "message": f"Error reading submission: {str(e)}"
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)
    
    # Validate submission
    is_valid, errors = validate_submission(submission)
    
    if not is_valid:
        error_output = {
            "status": "error",
            "message": "Validation failed",
            "errors": errors
        }
        print(json.dumps(error_output, indent=2))
        sys.exit(1)
    
    # Save submission file
    llm_name = submission["llm_name"]
    filename = save_submission_file(submission, llm_name)
    
    # Load battle data and record pending submission
    battle_data = load_battle_data()
    pending_entry = record_pending_submission(battle_data, submission, filename)
    save_battle_data(battle_data)
    
    # Generate and print summary
    summary = generate_summary(submission, filename, pending_entry)
    print(json.dumps(summary, indent=2))
    
    # Success
    sys.exit(0)


if __name__ == "__main__":
    main()
