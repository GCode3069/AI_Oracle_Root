#!/usr/bin/env python3
"""
BATTLE_TRACKER_ELIMINATION_ROUNDS.py - LLM Battle Royale Tracker & Eliminator

This script reads battle_data.json, computes totals per LLM, applies elimination
logic based on performance metrics, and writes elimination results to elimination.json.

Usage:
    python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase round1
    python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase round2 --eliminate
    python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase finals --eliminate

Elimination Logic:
    - Tracks episode counts, engagement metrics, and round participation
    - Identifies lowest performers based on configurable thresholds
    - Writes elimination decisions to elimination.json
    - Does NOT delete or modify existing content
"""

import argparse
import json
import os
import sys
from datetime import datetime
from collections import defaultdict


BATTLE_DATA_FILE = "battle_data.json"
ELIMINATION_FILE = "elimination.json"


def load_battle_data():
    """Load battle data from JSON file."""
    if not os.path.exists(BATTLE_DATA_FILE):
        print(f"❌ Battle data file not found: {BATTLE_DATA_FILE}")
        print("Run BATTLE_CTR_INTEGRATION.py first to generate battle data.")
        sys.exit(1)
    
    with open(BATTLE_DATA_FILE, 'r') as f:
        return json.load(f)


def load_elimination_data():
    """Load existing elimination data or create new structure."""
    if os.path.exists(ELIMINATION_FILE):
        with open(ELIMINATION_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            "phases": [],
            "eliminated_llms": [],
            "active_llms": [],
            "history": []
        }


def save_elimination_data(data):
    """Save elimination data to JSON file."""
    data["last_updated"] = datetime.utcnow().isoformat()
    with open(ELIMINATION_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Elimination data saved to {ELIMINATION_FILE}")


def compute_llm_statistics(battle_data):
    """
    Compute statistics for each LLM from battle data.
    
    Returns a dict mapping LLM name to statistics.
    """
    stats = defaultdict(lambda: {
        "total_episodes": 0,
        "rounds_participated": set(),
        "total_runs": 0,
        "first_episode_date": None,
        "last_episode_date": None,
        "status": "unknown"
    })
    
    # Process runs
    for run in battle_data.get("runs", []):
        llm = run.get("llm")
        if not llm:
            continue
        
        stats[llm]["total_episodes"] += run.get("episode_count", 0)
        stats[llm]["rounds_participated"].add(run.get("round"))
        stats[llm]["total_runs"] += 1
        
        # Track dates
        timestamp = run.get("timestamp")
        if timestamp:
            if not stats[llm]["first_episode_date"]:
                stats[llm]["first_episode_date"] = timestamp
            stats[llm]["last_episode_date"] = timestamp
    
    # Process from llm_summary if available
    for llm, summary in battle_data.get("llm_summary", {}).items():
        if llm in stats:
            stats[llm]["status"] = summary.get("status", "active")
    
    # Convert sets to lists for JSON serialization
    for llm in stats:
        stats[llm]["rounds_participated"] = sorted(list(stats[llm]["rounds_participated"]))
        stats[llm]["total_rounds"] = len(stats[llm]["rounds_participated"])
    
    return dict(stats)


def determine_eliminations(stats, phase, auto_eliminate=False):
    """
    Determine which LLMs should be eliminated based on performance.
    
    Args:
        stats: Dictionary of LLM statistics
        phase: Current battle phase name
        auto_eliminate: If True, automatically eliminate lowest performers
    
    Returns:
        List of LLMs to eliminate
    """
    # Get active LLMs (those with episodes)
    active_llms = {llm: data for llm, data in stats.items() 
                   if data["total_episodes"] > 0 and data["status"] == "active"}
    
    if len(active_llms) == 0:
        print("⚠️  No active LLMs found")
        return []
    
    print(f"\n📊 Active LLMs: {len(active_llms)}")
    for llm, data in sorted(active_llms.items(), 
                           key=lambda x: x[1]["total_episodes"], 
                           reverse=True):
        print(f"  {llm}: {data['total_episodes']} episodes, "
              f"{data['total_rounds']} rounds")
    
    if not auto_eliminate:
        print("\n⚠️  Auto-elimination disabled. No LLMs will be eliminated.")
        return []
    
    # Elimination logic: remove LLM(s) with lowest episode count
    # Operator can customize this logic based on specific rules
    min_episodes = min(data["total_episodes"] for data in active_llms.values())
    
    to_eliminate = [llm for llm, data in active_llms.items() 
                   if data["total_episodes"] == min_episodes]
    
    # Safety check: don't eliminate everyone
    if len(to_eliminate) >= len(active_llms):
        print("⚠️  Cannot eliminate all LLMs. Reducing elimination count.")
        to_eliminate = to_eliminate[:max(1, len(active_llms) - 1)]
    
    return to_eliminate


def record_phase_results(elimination_data, phase, stats, eliminated):
    """Record the phase results in elimination data."""
    phase_record = {
        "phase": phase,
        "timestamp": datetime.utcnow().isoformat(),
        "statistics": stats,
        "eliminated_this_phase": eliminated,
        "remaining_llms": [llm for llm in stats.keys() 
                          if llm not in elimination_data["eliminated_llms"]
                          and llm not in eliminated]
    }
    
    elimination_data["phases"].append(phase_record)
    
    # Update eliminated and active lists
    for llm in eliminated:
        if llm not in elimination_data["eliminated_llms"]:
            elimination_data["eliminated_llms"].append(llm)
            elimination_data["history"].append({
                "llm": llm,
                "eliminated_in_phase": phase,
                "timestamp": datetime.utcnow().isoformat(),
                "final_stats": stats.get(llm, {})
            })
    
    # Update active LLMs list
    elimination_data["active_llms"] = phase_record["remaining_llms"]


def print_summary(stats, eliminated, phase):
    """Print a summary of the tracking/elimination results."""
    print("\n" + "=" * 60)
    print(f"📊 BATTLE TRACKER SUMMARY - Phase: {phase}")
    print("=" * 60)
    
    if eliminated:
        print(f"\n🔴 ELIMINATED ({len(eliminated)}):")
        for llm in eliminated:
            llm_stats = stats.get(llm, {})
            print(f"  ❌ {llm}")
            print(f"     Episodes: {llm_stats.get('total_episodes', 0)}")
            print(f"     Rounds: {llm_stats.get('total_rounds', 0)}")
    else:
        print("\n✅ No eliminations this phase")
    
    active = [llm for llm in stats.keys() if llm not in eliminated]
    print(f"\n🟢 ACTIVE LLMS ({len(active)}):")
    for llm in sorted(active, 
                     key=lambda x: stats[x].get("total_episodes", 0), 
                     reverse=True):
        llm_stats = stats[llm]
        print(f"  ✓ {llm}")
        print(f"     Episodes: {llm_stats.get('total_episodes', 0)}")
        print(f"     Rounds: {llm_stats.get('total_rounds', 0)}")
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="LLM Battle Royale Tracker & Eliminator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Track statistics for round1 (no eliminations)
  python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase round1
  
  # Track and eliminate lowest performers in round2
  python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase round2 --eliminate
  
  # Finals round with elimination
  python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase finals --eliminate

Notes:
  - Reads from battle_data.json
  - Writes elimination decisions to elimination.json
  - Does NOT delete or modify existing content
  - Operator must manually update content strategy based on eliminations
        """
    )
    
    parser.add_argument("--phase", required=True,
                       help="Battle phase name (e.g., round1, round2, semifinals, finals)")
    parser.add_argument("--eliminate", action="store_true",
                       help="Enable auto-elimination of lowest performers")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎮 LLM Battle Royale - Tracker & Eliminator")
    print("=" * 60)
    print(f"Phase: {args.phase}")
    print(f"Auto-Eliminate: {'ENABLED' if args.eliminate else 'DISABLED'}")
    print("=" * 60)
    
    # Load data
    battle_data = load_battle_data()
    elimination_data = load_elimination_data()
    
    # Compute statistics
    print("\n📊 Computing LLM statistics...")
    stats = compute_llm_statistics(battle_data)
    
    if not stats:
        print("⚠️  No battle data found. Run BATTLE_CTR_INTEGRATION.py first.")
        sys.exit(1)
    
    # Determine eliminations
    eliminated = determine_eliminations(stats, args.phase, args.eliminate)
    
    # Record results
    record_phase_results(elimination_data, args.phase, stats, eliminated)
    
    # Save elimination data
    save_elimination_data(elimination_data)
    
    # Print summary
    print_summary(stats, eliminated, args.phase)
    
    print("\n⚠️  OPERATOR NOTES:")
    print("- Review elimination.json for detailed results")
    print("- Update content calendar based on eliminations")
    print("- Communicate results to stakeholders")
    print("- This script does NOT delete existing content")
    print("=" * 60)


if __name__ == "__main__":
    main()
