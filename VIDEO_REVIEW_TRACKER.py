#!/usr/bin/env python3
"""
VIDEO_REVIEW_TRACKER.py - Track uploaded videos for easy review

Creates a simple log of all uploaded videos with:
- Upload sequence number
- YouTube URL
- Episode number
- Timestamp
- Direct review link

Usage:
    python VIDEO_REVIEW_TRACKER.py --add <youtube_url> <episode_num>
    python VIDEO_REVIEW_TRACKER.py --list
    python VIDEO_REVIEW_TRACKER.py --last
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

TRACKER_FILE = Path("VIDEO_UPLOAD_LOG.json")

def load_tracker():
    """Load tracking data"""
    if TRACKER_FILE.exists():
        return json.loads(TRACKER_FILE.read_text())
    return {"uploads": [], "last_sequence": 0}

def save_tracker(data):
    """Save tracking data"""
    TRACKER_FILE.write_text(json.dumps(data, indent=2))

def add_upload(youtube_url: str, episode_num: int):
    """Add new upload to tracker"""
    data = load_tracker()
    
    sequence = data["last_sequence"] + 1
    
    entry = {
        "sequence": sequence,
        "episode": episode_num,
        "youtube_url": youtube_url,
        "uploaded_at": datetime.now().isoformat(),
        "review_status": "pending"
    }
    
    data["uploads"].append(entry)
    data["last_sequence"] = sequence
    save_tracker(data)
    
    print(f"\n[OK] TRACKED UPLOAD #{sequence}")
    print(f"Episode: #{episode_num}")
    print(f"URL: {youtube_url}")
    print(f"\nREVIEW THIS VIDEO:")
    print(f"Sequence: #{sequence}")
    print(f"Link: {youtube_url}\n")
    
    return entry

def list_uploads(limit=10):
    """List recent uploads"""
    data = load_tracker()
    uploads = data["uploads"][-limit:]
    
    print(f"\n{'='*80}")
    print(f"RECENT UPLOADS (Last {len(uploads)})")
    print(f"{'='*80}\n")
    
    for u in reversed(uploads):
        print(f"#{u['sequence']:03d} | Episode #{u['episode']} | {u['youtube_url']}")
        print(f"      Uploaded: {u['uploaded_at'][:19]}")
        print(f"      Status: {u.get('review_status', 'pending')}\n")

def get_last_upload():
    """Get most recent upload"""
    data = load_tracker()
    if not data["uploads"]:
        print("No uploads tracked yet")
        return None
    
    last = data["uploads"][-1]
    print(f"\n{'='*80}")
    print(f"LAST UPLOADED VIDEO")
    print(f"{'='*80}\n")
    print(f"Sequence: #{last['sequence']:03d}")
    print(f"Episode: #{last['episode']}")
    print(f"URL: {last['youtube_url']}")
    print(f"Uploaded: {last['uploaded_at'][:19]}")
    print(f"\n[REVIEW] {last['youtube_url']}\n")
    print(f"{'='*80}\n")
    
    return last

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Track YouTube uploads for review")
    parser.add_argument("--add", nargs=2, metavar=("URL", "EPISODE"), help="Add upload (url episode_num)")
    parser.add_argument("--list", action="store_true", help="List recent uploads")
    parser.add_argument("--last", action="store_true", help="Show last upload")
    
    args = parser.parse_args()
    
    if args.add:
        add_upload(args.add[0], int(args.add[1]))
    elif args.list:
        list_uploads()
    elif args.last:
        get_last_upload()
    else:
        parser.print_help()

