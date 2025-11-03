#!/usr/bin/env python3
"""
SUBMISSION_RECEIVER.py
Validate and store LLM script submissions for production.

Usage:
  python SUBMISSION_RECEIVER.py --file path/to/submission.json

This script:
- Validates JSON against submission_schema.json (basic rules)
- Stores validated submission under ./submissions/{llm_name}_{timestamp}.json
- Appends a record to battle_data.json under "pending_submissions"
- Prints a concise JSON summary to stdout for easy automation
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
SCHEMA_FILE = ROOT / "submission_schema.json"
SUBMISSIONS_DIR = ROOT / "submissions"
BATTLE_DATA = ROOT / "battle_data.json"

def load_schema():
    try:
        with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"Cannot load schema: {e}"}))
        sys.exit(2)

def simple_validate(payload):
    # Lightweight validation (don't require a full jsonschema dependency)
    if not isinstance(payload, dict):
        return False, "Payload must be a JSON object"
    if "llm_name" not in payload or not isinstance(payload["llm_name"], str):
        return False, "Missing or invalid 'llm_name'"
    if "scripts" not in payload or not isinstance(payload["scripts"], list) or len(payload["scripts"]) == 0:
        return False, "Missing or invalid 'scripts' array"
    for s in payload["scripts"]:
        if not isinstance(s, dict):
            return False, "Each script entry must be an object"
        if "episode" not in s or not isinstance(s["episode"], int):
            return False, "Each script must include integer 'episode'"
        if "script" not in s or not isinstance(s["script"], str) or len(s["script"].strip()) < 10:
            return False, "Each script must include non-empty 'script' text"
        if "title" not in s or not isinstance(s["title"], str) or len(s["title"].strip()) < 5:
            return False, "Each script must include a 'title'"
        # Optional: word-count guidance
        words = s["script"].split()
        if len(words) < 8 or len(words) > 250:
            return False, f"Script for episode {s.get('episode')} has {len(words)} words; recommended 32-45 for Shorts"
    return True, None

def ensure_dirs():
    SUBMISSIONS_DIR.mkdir(exist_ok=True)
    if not BATTLE_DATA.exists():
        BATTLE_DATA.write_text(json.dumps({"runs": [], "proofs": [], "pending_submissions": [], "generated_at": datetime.utcnow().isoformat() + "Z"}, indent=2))

def record_battle_entry(filename, payload):
    data = json.loads(BATTLE_DATA.read_text(encoding="utf-8"))
    entry = {
        "llm_name": payload["llm_name"],
        "file": str(filename),
        "scripts_count": len(payload["scripts"]),
        "received_at": datetime.utcnow().isoformat() + "Z",
        "status": "pending"
    }
    data.setdefault("pending_submissions", []).append(entry)
    BATTLE_DATA.write_text(json.dumps(data, indent=2), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to submission JSON file (or read from stdin if omitted)")
    args = parser.parse_args()

    raw = None
    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(json.dumps({"ok": False, "error": f"File not found: {args.file}"}))
            sys.exit(2)
        raw = p.read_text(encoding="utf-8")
    else:
        raw = sys.stdin.read()

    try:
        payload = json.loads(raw)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"Invalid JSON: {e}"}))
        sys.exit(2)

    ok, error = simple_validate(payload)
    if not ok:
        print(json.dumps({"ok": False, "error": error}))
        sys.exit(2)

    ensure_dirs()
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_llm = "".join(c for c in payload["llm_name"] if c.isalnum() or c in "-_").strip()
    outfile = SUBMISSIONS_DIR / f"{safe_llm}_{timestamp}.json"
    outfile.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    record_battle_entry(outfile, payload)

    summary = {
        "ok": True,
        "llm_name": payload["llm_name"],
        "scripts_received": len(payload["scripts"]),
        "saved_to": str(outfile),
        "received_at": datetime.utcnow().isoformat() + "Z"
    }
    print(json.dumps(summary, indent=2))
    # exit 0

if __name__ == "__main__":
    main()


