#!/usr/bin/env python3
"""
BATTLE_TRACKER_ELIMINATION_ROUNDS.py - Elimination Logic Tracker

Reads battle_data.json, computes totals per LLM, applies elimination logic,
and writes elimination.json with rankings and eliminated LLMs per phase.

Usage:
  python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase 1
  python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase 2 --eliminate 2
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def load_battle_data():
    """Load battle_data.json."""
    battle_file = Path("battle_data.json")
    if not battle_file.exists():
        print("❌ battle_data.json not found. Run BATTLE_CTR_INTEGRATION.py first.")
        sys.exit(1)
    
    with open(battle_file, "r") as f:
        return json.load(f)


def compute_llm_totals(battle_data):
    """Compute totals per LLM from battle_data."""
    llm_stats = {}
    
    # Count runs per LLM
    for run in battle_data.get("runs", []):
        if run.get("dry_run"):
            continue  # Skip dry runs
        
        llm = run.get("llm")
        if llm not in llm_stats:
            llm_stats[llm] = {
                "total_runs": 0,
                "total_videos": 0,
                "rounds": set()
            }
        
        llm_stats[llm]["total_runs"] += 1
        llm_stats[llm]["total_videos"] += run.get("videos", 0)
        llm_stats[llm]["rounds"].add(run.get("round"))
    
    # Count proofs per LLM
    for proof in battle_data.get("proofs", []):
        llm = proof.get("llm")
        if llm in llm_stats:
            if "total_proofs" not in llm_stats[llm]:
                llm_stats[llm]["total_proofs"] = 0
            llm_stats[llm]["total_proofs"] += 1
    
    # Convert sets to lists for JSON serialization
    for llm in llm_stats:
        llm_stats[llm]["rounds"] = sorted(list(llm_stats[llm]["rounds"]))
    
    return llm_stats


def rank_llms(llm_stats):
    """Rank LLMs by total videos generated (descending)."""
    ranked = []
    for llm, stats in llm_stats.items():
        ranked.append({
            "llm": llm,
            "total_videos": stats.get("total_videos", 0),
            "total_proofs": stats.get("total_proofs", 0),
            "rounds_participated": len(stats.get("rounds", []))
        })
    
    ranked.sort(key=lambda x: x["total_videos"], reverse=True)
    
    # Add ranks
    for idx, item in enumerate(ranked):
        item["rank"] = idx + 1
    
    return ranked


def apply_elimination(ranked_llms, eliminate_count):
    """Apply elimination logic - eliminate bottom N LLMs."""
    if eliminate_count <= 0:
        return []
    
    # Sort by rank (descending) to get bottom performers
    sorted_by_rank = sorted(ranked_llms, key=lambda x: x["rank"], reverse=True)
    eliminated = sorted_by_rank[:eliminate_count]
    
    return [llm["llm"] for llm in eliminated]


def save_elimination_data(phase, ranked_llms, eliminated, llm_stats):
    """Save elimination.json with phase results."""
    elimination_file = Path("elimination.json")
    
    # Load existing data or create new
    if elimination_file.exists():
        with open(elimination_file, "r") as f:
            data = json.load(f)
    else:
        data = {"phases": []}
    
    # Add this phase
    phase_data = {
        "phase": phase,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "rankings": ranked_llms,
        "eliminated": eliminated,
        "llm_stats": llm_stats
    }
    
    # Update or append
    phase_exists = False
    for idx, p in enumerate(data["phases"]):
        if p.get("phase") == phase:
            data["phases"][idx] = phase_data
            phase_exists = True
            break
    
    if not phase_exists:
        data["phases"].append(phase_data)
    
    # Sort phases
    data["phases"].sort(key=lambda x: x["phase"])
    
    with open(elimination_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved elimination.json (Phase {phase})")


def main():
    parser = argparse.ArgumentParser(
        description="LLM Battle Royale Elimination Tracker"
    )
    parser.add_argument("--phase", type=int, required=True, help="Battle phase/round")
    parser.add_argument("--eliminate", type=int, default=0, help="Number of LLMs to eliminate")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LLM BATTLE ROYALE ELIMINATION TRACKER")
    print("=" * 60)
    print(f"Phase: {args.phase}")
    print(f"Eliminate: {args.eliminate} LLMs")
    print("=" * 60)
    
    # Load battle data
    battle_data = load_battle_data()
    
    # Compute LLM stats
    llm_stats = compute_llm_totals(battle_data)
    print(f"\n📊 LLM Statistics:")
    for llm, stats in llm_stats.items():
        print(f"  {llm}: {stats['total_videos']} videos, {stats.get('total_proofs', 0)} proofs")
    
    # Rank LLMs
    ranked_llms = rank_llms(llm_stats)
    print(f"\n🏆 Rankings:")
    for item in ranked_llms:
        print(f"  #{item['rank']} {item['llm']}: {item['total_videos']} videos")
    
    # Apply elimination
    eliminated = []
    if args.eliminate > 0:
        eliminated = apply_elimination(ranked_llms, args.eliminate)
        print(f"\n❌ Eliminated ({len(eliminated)}):")
        for llm in eliminated:
            print(f"  - {llm}")
    
    # Save elimination data
    save_elimination_data(args.phase, ranked_llms, eliminated, llm_stats)
    
    print("\n" + "=" * 60)
    print("✅ ELIMINATION TRACKING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
