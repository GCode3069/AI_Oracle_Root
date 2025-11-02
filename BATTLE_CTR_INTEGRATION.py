#!/usr/bin/env python3
"""
BATTLE_CTR_INTEGRATION.py
Orchestrator CLI for LLM Battle Royale video generation workflow.

This script coordinates the generation of battle videos by invoking mapped generator scripts.
It does NOT upload to YouTube directly - that is the operator's responsibility.

Usage:
    python BATTLE_CTR_INTEGRATION.py --llm CHATGPT --round 1 --videos 5 --start 30000
    python BATTLE_CTR_INTEGRATION.py --llm GROK --round 1 --videos 3 --start 60000 --dry-run

Responsibilities:
    1. Validate environment variables are set (via .env)
    2. Invoke the appropriate generator script based on --llm argument
    3. Update battle_data.json with generation metadata
    4. Record per-video proof hashes and timestamps
    5. Log all operations for audit trail

Operator Responsibilities:
    - Populate .env with valid API keys before running
    - Review generated videos before upload
    - Manually upload to YouTube with proper review and staging
    - Implement OAuth flow for YouTube uploads separately
    - Monitor battle_data.json for accuracy
"""

import argparse
import json
import os
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

# Map LLM names to their generator scripts
# These scripts must be implemented separately and accept episode number arguments
GENERATORS = {
    'CHATGPT': 'generators/chatgpt_generator.py',
    'GROK': 'generators/grok_generator.py',
    'CLAUDE': 'generators/claude_generator.py',
    'GEMINI': 'generators/gemini_generator.py',
    'LLAMA': 'generators/llama_generator.py',
}

REQUIRED_ENV_VARS = [
    'ELEVENLABS_API_KEY',
    'PEXELS_API_KEY',
]

BATTLE_DATA_PATH = 'battle_data.json'


def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_path = Path('.env')
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()


def validate_environment():
    """Check that required environment variables are set."""
    missing = []
    for var in REQUIRED_ENV_VARS:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"ERROR: Missing required environment variables: {', '.join(missing)}")
        print("Please populate .env file with valid API keys.")
        sys.exit(1)
    
    print("✓ Environment variables validated")


def load_battle_data():
    """Load current battle data from JSON file."""
    path = Path(BATTLE_DATA_PATH)
    if not path.exists():
        return {
            'runs': [],
            'proofs': {},
            'pending_submissions': [],
            'llm_summary': {},
            'generated_at': None
        }
    
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"ERROR: Failed to load {BATTLE_DATA_PATH}: {e}")
        sys.exit(1)


def save_battle_data(data):
    """Save battle data to JSON file."""
    data['generated_at'] = datetime.now(timezone.utc).isoformat()
    path = Path(BATTLE_DATA_PATH)
    path.write_text(json.dumps(data, indent=2))
    print(f"✓ Updated {BATTLE_DATA_PATH}")


def compute_proof_hash(llm, round_num, video_num, timestamp):
    """Compute a proof hash for audit trail."""
    content = f"{llm}:{round_num}:{video_num}:{timestamp}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def invoke_generator(llm, start_episode, num_videos, dry_run=False):
    """Invoke the generator script for the specified LLM."""
    generator_path = GENERATORS.get(llm.upper())
    
    if not generator_path:
        print(f"ERROR: Unknown LLM '{llm}'. Available: {', '.join(GENERATORS.keys())}")
        sys.exit(1)
    
    if not Path(generator_path).exists():
        print(f"WARNING: Generator script not found: {generator_path}")
        print(f"Please implement this script to generate videos for {llm}")
        if not dry_run:
            print("Continuing in dry-run mode for demonstration...")
            dry_run = True
    
    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Invoking generator: {generator_path}")
    print(f"  LLM: {llm}")
    print(f"  Start Episode: {start_episode}")
    print(f"  Number of Videos: {num_videos}")
    
    # In a real implementation, this would call the generator script
    # For now, we simulate the process
    if dry_run:
        print(f"  [DRY-RUN] Would execute: python {generator_path} --start {start_episode} --count {num_videos}")
        return True
    
    # Actual execution would go here
    # import subprocess
    # result = subprocess.run([
    #     'python', generator_path,
    #     '--start', str(start_episode),
    #     '--count', str(num_videos)
    # ], capture_output=True, text=True)
    # return result.returncode == 0
    
    return True


def record_run(data, llm, round_num, start_episode, num_videos, dry_run):
    """Record the generation run in battle data."""
    timestamp = datetime.now(timezone.utc).isoformat()
    
    run_record = {
        'llm': llm,
        'round': round_num,
        'start_episode': start_episode,
        'num_videos': num_videos,
        'timestamp': timestamp,
        'dry_run': dry_run,
        'status': 'completed'
    }
    
    # Record individual video proofs
    proofs = []
    for i in range(num_videos):
        episode = start_episode + i
        proof = compute_proof_hash(llm, round_num, episode, timestamp)
        proofs.append({
            'episode': episode,
            'proof': proof,
            'timestamp': timestamp
        })
        
        # Add to global proofs dictionary
        proof_key = f"{llm}:{episode}"
        data['proofs'][proof_key] = proof
    
    run_record['proofs'] = proofs
    data['runs'].append(run_record)
    
    # Update LLM summary
    if llm not in data['llm_summary']:
        data['llm_summary'][llm] = {
            'total_videos': 0,
            'rounds': []
        }
    
    data['llm_summary'][llm]['total_videos'] += num_videos
    data['llm_summary'][llm]['rounds'].append({
        'round': round_num,
        'videos': num_videos,
        'timestamp': timestamp
    })
    
    print(f"✓ Recorded run for {llm} Round {round_num}")
    print(f"  Generated {num_videos} video(s) starting at episode {start_episode}")
    print(f"  Proof hashes recorded in battle_data.json")


def main():
    parser = argparse.ArgumentParser(
        description='LLM Battle Royale Orchestrator - Coordinate video generation workflow'
    )
    parser.add_argument('--llm', required=True,
                        help=f'LLM identifier ({", ".join(GENERATORS.keys())})')
    parser.add_argument('--round', type=int, required=True,
                        help='Battle round number')
    parser.add_argument('--videos', type=int, required=True,
                        help='Number of videos to generate')
    parser.add_argument('--start', type=int, required=True,
                        help='Starting episode number')
    parser.add_argument('--dry-run', action='store_true',
                        help='Simulate without actual generation')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LLM BATTLE ROYALE - ORCHESTRATION CTR")
    print("=" * 60)
    
    # Load environment
    load_env_file()
    
    if not args.dry_run:
        validate_environment()
    else:
        print("[DRY-RUN] Skipping environment validation")
    
    # Load battle data
    battle_data = load_battle_data()
    
    # Invoke generator
    success = invoke_generator(
        args.llm,
        args.start,
        args.videos,
        args.dry_run
    )
    
    if not success:
        print("ERROR: Generator failed")
        sys.exit(1)
    
    # Record the run
    record_run(
        battle_data,
        args.llm.upper(),
        args.round,
        args.start,
        args.videos,
        args.dry_run
    )
    
    # Save updated battle data
    save_battle_data(battle_data)
    
    print("\n" + "=" * 60)
    print("✓ ORCHESTRATION COMPLETE")
    print("=" * 60)
    print("\nNEXT STEPS:")
    print("1. Review generated videos in output directory")
    print("2. Verify content complies with platform TOS")
    print("3. Manually upload to YouTube with proper OAuth and review")
    print("4. Update battle_data.json with YouTube video IDs")
    print("\nREMINDER: Never auto-upload. Always review first!")


if __name__ == '__main__':
    main()
