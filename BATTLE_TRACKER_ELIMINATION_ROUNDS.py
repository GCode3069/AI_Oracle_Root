#!/usr/bin/env python3
"""
BATTLE_TRACKER_ELIMINATION_ROUNDS.py

Reads battle_data.json, computes totals per LLM, applies elimination logic,
and writes elimination.json. Supports different phases of battle royale.

Usage:
    python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase initial
    python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase quarterfinal --eliminate 2
    python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase final

Elimination Logic:
    - Computes total videos per LLM from battle_data.json
    - Applies elimination rules based on phase
    - Writes elimination.json with standings and eliminated LLMs
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


def load_battle_data():
    """Load battle_data.json."""
    battle_data_path = Path("battle_data.json")
    
    if not battle_data_path.exists():
        print("ERROR: battle_data.json not found. Run BATTLE_CTR_INTEGRATION.py first.")
        return None
    
    with open(battle_data_path, "r") as f:
        return json.load(f)


def compute_llm_totals(battle_data):
    """Compute total videos and rounds per LLM."""
    llm_stats = {}
    
    for run in battle_data.get("runs", []):
        llm = run["llm"]
        videos = run["videos"]
        round_num = run["round"]
        
        if llm not in llm_stats:
            llm_stats[llm] = {
                "total_videos": 0,
                "rounds": set(),
                "runs": []
            }
        
        llm_stats[llm]["total_videos"] += videos
        llm_stats[llm]["rounds"].add(round_num)
        llm_stats[llm]["runs"].append(run)
    
    # Convert sets to lists for JSON serialization
    for llm in llm_stats:
        llm_stats[llm]["rounds"] = sorted(list(llm_stats[llm]["rounds"]))
    
    return llm_stats


def apply_elimination_logic(llm_stats, phase, eliminate_count):
    """Apply elimination logic based on phase."""
    # Sort LLMs by total videos (descending)
    sorted_llms = sorted(
        llm_stats.items(),
        key=lambda x: x[1]["total_videos"],
        reverse=True
    )
    
    standings = []
    eliminated = []
    
    for rank, (llm, stats) in enumerate(sorted_llms, 1):
        entry = {
            "rank": rank,
            "llm": llm,
            "total_videos": stats["total_videos"],
            "rounds_participated": len(stats["rounds"]),
            "status": "active"
        }
        
        # Apply elimination based on phase
        if eliminate_count and rank > (len(sorted_llms) - eliminate_count):
            entry["status"] = "eliminated"
            entry["eliminated_in_phase"] = phase
            eliminated.append(entry)
        else:
            standings.append(entry)
    
    return standings + eliminated


def save_elimination_data(standings, phase):
    """Save elimination.json."""
    elimination_data = {
        "phase": phase,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "standings": standings,
        "total_llms": len(standings),
        "active_llms": len([s for s in standings if s["status"] == "active"]),
        "eliminated_llms": len([s for s in standings if s["status"] == "eliminated"])
    }
    
    with open("elimination.json", "w") as f:
        json.dump(elimination_data, f, indent=2)
    
    print(f"Elimination data saved: elimination.json")


def main():
    parser = argparse.ArgumentParser(
        description="LLM Battle Royale Elimination Tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--phase", required=True,
                        choices=["initial", "quarterfinal", "semifinal", "final"],
                        help="Battle phase")
    parser.add_argument("--eliminate", type=int, default=0,
                        help="Number of LLMs to eliminate (lowest scoring)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LLM BATTLE ROYALE ELIMINATION TRACKER")
    print("=" * 60)
    
    # Load battle data
    battle_data = load_battle_data()
    if not battle_data:
        return
    
    # Compute totals
    llm_stats = compute_llm_totals(battle_data)
    print(f"\nLLM Statistics ({len(llm_stats)} LLMs):")
    for llm, stats in sorted(llm_stats.items(), key=lambda x: x[1]["total_videos"], reverse=True):
        print(f"  {llm}: {stats['total_videos']} videos, {len(stats['rounds'])} rounds")
    
    # Apply elimination logic
    standings = apply_elimination_logic(llm_stats, args.phase, args.eliminate)
    
    print(f"\nPhase: {args.phase}")
    print(f"Eliminating: {args.eliminate} LLM(s)")
    print("\nStandings:")
    for entry in standings:
        status_marker = "❌" if entry["status"] == "eliminated" else "✓"
        print(f"  {status_marker} Rank {entry['rank']}: {entry['llm']} - {entry['total_videos']} videos")
    
    # Save elimination data
    save_elimination_data(standings, args.phase)
    
    print("=" * 60)
    print("SUCCESS: Elimination data saved")
    print("=" * 60)


if __name__ == "__main__":
    main()
