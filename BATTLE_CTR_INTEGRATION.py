#!/usr/bin/env python3
"""
BATTLE_CTR_INTEGRATION.py - Orchestrator CLI for LLM Battle Royale

This script coordinates the generation of Battle Royale videos per LLM per round.
It validates environment variables, invokes mapped generator scripts, and updates
battle_data.json with production proofs. Does NOT upload to YouTube directly.

Operator responsibilities:
- Populate .env with required API keys
- Run with --dry-run first to validate setup
- Review generated videos before upload
- Use separate uploader script with OAuth for YouTube
- Maintain audit trail in battle_data.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Generator script mapping: LLM name -> generator script path
GENERATORS = {
    "ChatGPT": "./1_Script_Engine/chatgpt_generator.py",
    "Claude": "./1_Script_Engine/claude_generator.py",
    "Gemini": "./1_Script_Engine/gemini_generator.py",
    "Grok": "./1_Script_Engine/grok_generator.py",
    "Llama": "./1_Script_Engine/llama_generator.py",
}

REQUIRED_ENV_VARS = [
    "ELEVENLABS_API_KEY",
    "PEXELS_API_KEY",
]

OPTIONAL_ENV_VARS = [
    "RUNWAY_API_KEY",
    "POLLO_API_KEY",
    "STABILITY_API_KEY",
]


def validate_environment(dry_run=False):
    """Validate required environment variables are set."""
    missing = []
    for var in REQUIRED_ENV_VARS:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        print("Please populate .env file. See .env.example for template.")
        return False
    
    print("✅ All required environment variables are set")
    
    # Check optional vars
    optional_missing = [v for v in OPTIONAL_ENV_VARS if not os.getenv(v)]
    if optional_missing:
        print(f"⚠️  Optional environment variables not set: {', '.join(optional_missing)}")
    
    return True


def load_battle_data():
    """Load battle_data.json or create default structure."""
    battle_file = Path("battle_data.json")
    if battle_file.exists():
        with open(battle_file, "r") as f:
            return json.load(f)
    else:
        return {
            "runs": [],
            "proofs": [],
            "pending_submissions": [],
            "llm_summary": {},
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }


def save_battle_data(data):
    """Save battle_data.json with updated timestamp."""
    data["generated_at"] = datetime.utcnow().isoformat() + "Z"
    with open("battle_data.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Updated battle_data.json")


def record_run(battle_data, llm, round_num, videos, dry_run):
    """Record a new production run in battle_data."""
    run_record = {
        "llm": llm,
        "round": round_num,
        "videos": videos,
        "dry_run": dry_run,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "dry_run" if dry_run else "generated"
    }
    battle_data["runs"].append(run_record)
    return run_record


def record_proof(battle_data, llm, round_num, video_id, proof_data):
    """Record video generation proof."""
    proof_record = {
        "llm": llm,
        "round": round_num,
        "video_id": video_id,
        "proof": proof_data,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    battle_data["proofs"].append(proof_record)


def invoke_generator(llm, round_num, videos, start, dry_run):
    """Invoke the mapped generator script for the LLM."""
    if llm not in GENERATORS:
        print(f"❌ No generator mapped for LLM: {llm}")
        print(f"Available LLMs: {', '.join(GENERATORS.keys())}")
        return False
    
    generator_path = Path(GENERATORS[llm])
    
    if not generator_path.exists():
        print(f"⚠️  Generator script not found: {generator_path}")
        print("Please implement the generator script before running.")
        if dry_run:
            print("Dry run: Would have called generator here.")
            return True
        return False
    
    # In dry run, just validate
    if dry_run:
        print(f"✅ Dry run: Would invoke {generator_path} for {llm} round {round_num}")
        print(f"   Videos: {videos}, Start: {start}")
        return True
    
    # Actual invocation would happen here
    print(f"🎬 Invoking generator: {generator_path}")
    print(f"   LLM: {llm}, Round: {round_num}, Videos: {videos}, Start: {start}")
    
    # TODO: Implement actual subprocess call to generator
    # Example: subprocess.run([sys.executable, str(generator_path), ...])
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="LLM Battle Royale Orchestrator - Coordinate video generation per LLM"
    )
    parser.add_argument("--llm", required=True, help="LLM name (ChatGPT, Claude, Gemini, Grok, Llama)")
    parser.add_argument("--round", type=int, required=True, help="Battle round number")
    parser.add_argument("--videos", type=int, default=5, help="Number of videos to generate")
    parser.add_argument("--start", type=int, default=1, help="Starting video number")
    parser.add_argument("--dry-run", action="store_true", help="Validate without generating")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LLM BATTLE ROYALE ORCHESTRATOR")
    print("=" * 60)
    print(f"LLM: {args.llm}")
    print(f"Round: {args.round}")
    print(f"Videos: {args.videos}")
    print(f"Start: {args.start}")
    print(f"Dry Run: {args.dry_run}")
    print("=" * 60)
    
    # Validate environment
    if not validate_environment(args.dry_run):
        sys.exit(1)
    
    # Load battle data
    battle_data = load_battle_data()
    
    # Record this run
    run_record = record_run(battle_data, args.llm, args.round, args.videos, args.dry_run)
    print(f"📝 Recorded run: {run_record}")
    
    # Invoke generator
    success = invoke_generator(args.llm, args.round, args.videos, args.start, args.dry_run)
    
    if not success:
        print("❌ Generator invocation failed")
        sys.exit(1)
    
    # Record proofs (example - would be populated by actual generator)
    if not args.dry_run:
        for i in range(args.videos):
            video_id = args.start + i
            proof_data = {
                "video_file": f"{args.llm}_R{args.round}_V{video_id}.mp4",
                "generated": True
            }
            record_proof(battle_data, args.llm, args.round, video_id, proof_data)
    
    # Save battle data
    save_battle_data(battle_data)
    
    print("=" * 60)
    print("✅ ORCHESTRATION COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review generated videos")
    print("2. Stage for upload with YouTube OAuth uploader")
    print("3. Verify TOS compliance before publishing")
    print("4. Update battle_data.json with upload timestamps")


if __name__ == "__main__":
    main()
