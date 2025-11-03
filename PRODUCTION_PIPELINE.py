#!/usr/bin/env python3
"""
PRODUCTION PIPELINE - Processes submission input files and generates videos
Watches core/production_inputs/ and generates videos from submitted scripts
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Import our main video generation system
sys.path.insert(0, str(Path(__file__).parent))
from abraham_MAX_HEADROOM import (
    generate_voice, create_max_headroom_video, upload_to_youtube,
    BASE_DIR
)

INPUTS_DIR = Path("core/production_inputs")
BATTLE_DATA = Path("battle_data.json")

def process_input_file(input_path):
    """
    Process a single production input file
    
    Args:
        input_path: Path to .input.json file
    
    Returns:
        video_path or None
    """
    
    try:
        # Load input
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        llm_name = data['llm_name']
        episode = data['episode']
        script = data['script']
        title_suggestion = data['title']
        
        print(f"\n{'='*80}")
        print(f"  PROCESSING: {llm_name} - Episode #{episode}")
        print(f"{'='*80}\n")
        
        print(f"[1/4] Script: {script[:60]}...")
        
        # 1. Generate voice
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_path = BASE_DIR / "abraham_horror" / "audio" / f"{llm_name}_{episode}_{timestamp}.mp3"
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"[2/4] Generating voice...")
        if not generate_voice(script, audio_path):
            print(f"  [!] Voice generation failed")
            return None
        
        # 2. Create video
        print(f"[3/4] Creating video with VHS effects...")
        video_path = create_max_headroom_video(
            audio_path=audio_path,
            episode_num=episode,
            use_lipsync=False,  # Fast mode
            use_broll=True
        )
        
        if not video_path or not video_path.exists():
            print(f"  [!] Video creation failed")
            return None
        
        # 3. Upload to YouTube
        print(f"[4/4] Uploading to YouTube...")
        
        # Extract headline from title
        headline = title_suggestion.split(':')[1].split('#')[0].strip() if ':' in title_suggestion else "Submitted Content"
        
        youtube_url = upload_to_youtube(video_path, headline, episode)
        
        print(f"\n{'='*80}")
        print(f"  [OK] COMPLETE - {llm_name} Episode #{episode}")
        print(f"  Video: {video_path.name}")
        if youtube_url:
            print(f"  YouTube: {youtube_url}")
        print(f"{'='*80}\n")
        
        # 4. Log to battle data
        update_battle_data(llm_name, episode, video_path, youtube_url)
        
        # 5. Mark input as processed
        processed_path = input_path.with_suffix('.processed')
        input_path.rename(processed_path)
        
        return video_path
        
    except Exception as e:
        print(f"  [!] Error processing {input_path.name}: {e}")
        return None

def update_battle_data(llm_name, episode, video_path, youtube_url):
    """Update battle_data.json with production proof"""
    
    try:
        if BATTLE_DATA.exists():
            with open(BATTLE_DATA, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"runs": [], "proofs": [], "pending_submissions": []}
        
        proof = {
            "llm_name": llm_name,
            "episode": episode,
            "video_path": str(video_path),
            "youtube_url": youtube_url if youtube_url else "PENDING",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "revenue": 0  # Will be updated from analytics
        }
        
        data.setdefault("proofs", []).append(proof)
        
        with open(BATTLE_DATA, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    except Exception as e:
        print(f"  [!] Battle data update failed: {e}")

def process_all_inputs():
    """Process all pending input files"""
    
    if not INPUTS_DIR.exists():
        print("[!] No production_inputs directory found")
        return
    
    input_files = sorted(INPUTS_DIR.glob("*.input.json"))
    
    if not input_files:
        print("[!] No input files found in production queue")
        return
    
    print(f"\n{'='*80}")
    print(f"  PRODUCTION PIPELINE - PROCESSING {len(input_files)} INPUTS")
    print(f"{'='*80}\n")
    
    successful = 0
    failed = 0
    
    for input_file in input_files:
        result = process_input_file(input_file)
        if result:
            successful += 1
        else:
            failed += 1
    
    print(f"\n{'='*80}")
    print(f"  PRODUCTION COMPLETE")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Production Pipeline - Generate videos from submissions')
    parser.add_argument('--file', help='Process specific input file')
    parser.add_argument('--all', action='store_true', help='Process all pending inputs')
    
    args = parser.parse_args()
    
    if args.file:
        process_input_file(Path(args.file))
    elif args.all:
        process_all_inputs()
    else:
        process_all_inputs()  # Default: process all


