#!/usr/bin/env python3
"""
ENQUEUE_FOR_PRODUCTION.py
Transform validated submission files into per-episode input files a production pipeline can consume.

- Looks in ./submissions for files authored by SUBMISSION_RECEIVER
- For each new submission, writes per-episode JSON files into ./core/production_inputs/
  e.g., core/production_inputs/LLM_EP30000.input.json
- Marks the submission entry in battle_data.json as 'enqueued'
- Does NOT call any external APIs or upload anything
"""
import json
import time
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
SUBMISSIONS_DIR = ROOT / "submissions"
INPUTS_DIR = ROOT / "core" / "production_inputs"
BATTLE_DATA = ROOT / "battle_data.json"

INPUTS_DIR.mkdir(parents=True, exist_ok=True)
if not BATTLE_DATA.exists():
    BATTLE_DATA.write_text(json.dumps({"runs": [], "proofs": [], "pending_submissions": [], "generated_at": datetime.utcnow().isoformat() + "Z"}, indent=2))

def load_battle_data():
    return json.loads(BATTLE_DATA.read_text(encoding="utf-8"))

def save_battle_data(data):
    BATTLE_DATA.write_text(json.dumps(data, indent=2), encoding="utf-8")

def process_submission_file(path: Path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    llm = payload["llm_name"]
    produced = []
    for s in payload["scripts"]:
        ep = int(s["episode"])
        inp = {
            "llm_name": llm,
            "episode": ep,
            "script": s["script"],
            "title": s["title"],
            "tags": s.get("tags", []),
            "notes": s.get("notes", ""),
            "satire_label": s.get("satire_label", False),
            "received_from_file": str(path),
            "enqueued_at": datetime.utcnow().isoformat() + "Z"
        }
        dest = INPUTS_DIR / f"{llm}_EP{ep}.input.json"
        dest.write_text(json.dumps(inp, indent=2), encoding="utf-8")
        produced.append(str(dest))
    # update battle_data.json pending -> enqueued
    data = load_battle_data()
    # find matching pending entry by file path
    for e in data.get("pending_submissions", []):
        if e.get("file") == str(path):
            e["status"] = "enqueued"
            e["enqueued_at"] = datetime.utcnow().isoformat() + "Z"
    save_battle_data(data)
    return produced

def main():
    submissions = sorted(SUBMISSIONS_DIR.glob("*.json"))
    all_produced = []
    for sub in submissions:
        produced = process_submission_file(sub)
        all_produced.extend(produced)
    print(json.dumps({"ok": True, "produced_inputs": all_produced, "count": len(all_produced)}, indent=2))

if __name__ == "__main__":
    main()


