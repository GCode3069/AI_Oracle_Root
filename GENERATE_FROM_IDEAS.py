#!/usr/bin/env python3
"""
SCARIFY - Generate Videos from Horror Ideas Database
Uses the 102 horror ideas for varied, non-repetitive content
"""

import os, sys, json, random
from pathlib import Path

BASE_DIR = Path("F:/AI_Oracle_Root/scarify")
IDEAS_FILE = BASE_DIR / "horror_ideas_database.json"

# Import existing generator
sys.path.append(str(BASE_DIR / "abraham_horror"))

try:
    from ABRAHAM_PROFESSIONAL_UPGRADE import generate_professional_video
    GENERATOR_AVAILABLE = True
except:
    GENERATOR_AVAILABLE = False
    print("[WARNING] Professional generator not available")

def load_horror_ideas():
    """Load all 102 horror ideas"""
    if not IDEAS_FILE.exists():
        print(f"[ERROR] Ideas database not found: {IDEAS_FILE}")
        return []
    
    with open(IDEAS_FILE, 'r') as f:
        data = json.load(f)
    
    return data.get('horror_ideas', [])

def convert_idea_to_video(idea, use_lincoln=True):
    """Convert a horror idea into a video script"""
    
    title = idea['title']
    description = idea['description']
    script_base = idea['script']
    
    # Add Lincoln framing if requested
    if use_lincoln:
        lincoln_intro = [
            f"I am Abraham Lincoln. From beyond death, I warn you: {title}.",
            f"April 14, 1865. Booth's bullet showed me the future. {title}.",
            f"From Ford's Theatre, I speak: {title}. Listen or perish.",
            f"They killed me for truth. Now truth kills you. {title}.",
            f"Lincoln's ghost warns: {title}. The prophecy unfolds."
        ]
        
        intro = random.choice(lincoln_intro)
        full_script = f"{intro} {script_base} Support truth: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
    else:
        full_script = f"{script_base} Bitcoin: bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
    
    return {
        'title': title,
        'description': description,
        'script': full_script,
        'keywords': idea.get('keywords', ''),
        'theme': idea.get('theme', 'scarify'),
        'idea_id': idea['id']
    }

def generate_batch_from_ideas(count=50, start_id=1, use_lincoln=True):
    """Generate videos using horror ideas"""
    
    ideas = load_horror_ideas()
    
    if not ideas:
        print("[ERROR] No horror ideas available")
        return
    
    print(f"\n{'='*70}")
    print(f"GENERATING {count} VIDEOS FROM HORROR IDEAS")
    print(f"{'='*70}\n")
    print(f"Total Ideas Available: {len(ideas)}")
    print(f"Starting from ID: {start_id}")
    print(f"Lincoln Framing: {'ON' if use_lincoln else 'OFF'}")
    print(f"\n{'='*70}\n")
    
    # Filter ideas starting from start_id
    selected_ideas = [idea for idea in ideas if idea['id'] >= start_id][:count]
    
    if len(selected_ideas) < count:
        print(f"[WARNING] Only {len(selected_ideas)} ideas available from ID {start_id}")
        print(f"Looping back to use all 102 ideas...")
        
        # Loop if needed
        while len(selected_ideas) < count:
            selected_ideas.extend(ideas[:count - len(selected_ideas)])
    
    results = []
    
    for i, idea in enumerate(selected_ideas, 1):
        print(f"\n[{i}/{count}] Processing: {idea['title']}")
        
        video_data = convert_idea_to_video(idea, use_lincoln)
        
        print(f"  Theme: {video_data['theme']}")
        print(f"  Script: {video_data['script'][:100]}...")
        
        # Here you would call your actual video generator
        # For now, just save the metadata
        
        results.append({
            'idea_id': idea['id'],
            'title': idea['title'],
            'status': 'ready_for_generation',
            'video_data': video_data
        })
    
    # Save batch manifest
    manifest_file = BASE_DIR / f"batch_manifest_{start_id}_to_{start_id+count}.json"
    with open(manifest_file, 'w') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'count': len(results),
            'use_lincoln': use_lincoln,
            'results': results
        }, f, indent=2)
    
    print(f"\n{'='*70}")
    print(f"BATCH MANIFEST CREATED")
    print(f"{'='*70}\n")
    print(f"File: {manifest_file}")
    print(f"Videos: {len(results)}")
    print(f"\n{'='*70}\n")
    
    print(f"NEXT STEPS:")
    print(f"  1. Review manifest: {manifest_file.name}")
    print(f"  2. Generate videos: Use dashboard or CLI")
    print(f"  3. Upload to channels: python MULTI_CHANNEL_UPLOADER.py")
    print(f"\n{'='*70}\n")
    
    return results

if __name__ == "__main__":
    from datetime import datetime
    
    if len(sys.argv) < 2:
        print("""
SCARIFY - Horror Ideas Video Generator

Usage:
  python GENERATE_FROM_IDEAS.py <count> [start_id] [--no-lincoln]
  
Examples:
  python GENERATE_FROM_IDEAS.py 50          # Generate 50 videos from idea #1
  python GENERATE_FROM_IDEAS.py 25 26       # Generate 25 videos from idea #26
  python GENERATE_FROM_IDEAS.py 50 1 --no-lincoln  # Without Lincoln framing
  
Features:
  • Uses 102 unique horror ideas
  • Adds Lincoln framing by default
  • Prevents repetitive content
  • Assigns themes automatically
  • Integrates Bitcoin & product links
""")
    else:
        count = int(sys.argv[1])
        start_id = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        use_lincoln = '--no-lincoln' not in sys.argv
        
        generate_batch_from_ideas(count, start_id, use_lincoln)


