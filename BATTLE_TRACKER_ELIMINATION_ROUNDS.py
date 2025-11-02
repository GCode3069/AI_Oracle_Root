#!/usr/bin/env python3
"""
BATTLE_TRACKER_ELIMINATION_ROUNDS.py
LLM Battle Royale elimination logic and tracking system.

This script reads battle_data.json, computes performance metrics per LLM,
applies elimination logic based on configured rules, and writes elimination.json.

Usage:
    python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase 1
    python BATTLE_TRACKER_ELIMINATION_ROUNDS.py --phase 2 --eliminate

Phases:
    - Phase 1: Initial battle, all LLMs participate
    - Phase 2: Quarterfinals
    - Phase 3: Semifinals
    - Phase 4: Finals

Elimination Logic:
    - Lowest performing LLMs based on engagement metrics are eliminated
    - Metrics include: video count, view count (if available), engagement rate
    - Operator can override with manual elimination list
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

BATTLE_DATA_PATH = 'battle_data.json'
ELIMINATION_DATA_PATH = 'elimination.json'


def load_battle_data():
    """Load current battle data from JSON file."""
    path = Path(BATTLE_DATA_PATH)
    if not path.exists():
        print(f"ERROR: {BATTLE_DATA_PATH} not found")
        print("Run BATTLE_CTR_INTEGRATION.py first to generate battle data")
        return None
    
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"ERROR: Failed to load {BATTLE_DATA_PATH}: {e}")
        return None


def load_elimination_data():
    """Load current elimination data or create new structure."""
    path = Path(ELIMINATION_DATA_PATH)
    if not path.exists():
        return {
            'phases': [],
            'eliminated': [],
            'remaining': [],
            'generated_at': None
        }
    
    try:
        return json.loads(path.read_text())
    except Exception as e:
        print(f"WARNING: Failed to load {ELIMINATION_DATA_PATH}: {e}")
        return {
            'phases': [],
            'eliminated': [],
            'remaining': [],
            'generated_at': None
        }


def save_elimination_data(data):
    """Save elimination data to JSON file."""
    data['generated_at'] = datetime.now(timezone.utc).isoformat()
    path = Path(ELIMINATION_DATA_PATH)
    path.write_text(json.dumps(data, indent=2))
    print(f"✓ Updated {ELIMINATION_DATA_PATH}")


def compute_llm_totals(battle_data):
    """Compute total metrics per LLM from battle data."""
    llm_summary = battle_data.get('llm_summary', {})
    
    totals = {}
    for llm, data in llm_summary.items():
        totals[llm] = {
            'llm': llm,
            'total_videos': data.get('total_videos', 0),
            'rounds': len(data.get('rounds', [])),
            'last_timestamp': data.get('rounds', [{}])[-1].get('timestamp', 'unknown') if data.get('rounds') else 'unknown',
            # Placeholder for future metrics
            'total_views': 0,
            'engagement_rate': 0.0,
            'score': data.get('total_videos', 0)  # Simple scoring by video count for now
        }
    
    return totals


def rank_llms(totals):
    """Rank LLMs by performance score."""
    llms = list(totals.values())
    # Sort by score descending
    llms.sort(key=lambda x: x['score'], reverse=True)
    
    for i, llm_data in enumerate(llms, 1):
        llm_data['rank'] = i
    
    return llms


def apply_elimination_logic(ranked_llms, phase, eliminate_count=None):
    """Apply elimination logic based on phase."""
    if not eliminate_count:
        # Default elimination rules per phase
        elimination_rules = {
            1: 2,  # Eliminate 2 LLMs in phase 1
            2: 1,  # Eliminate 1 LLM in phase 2
            3: 1,  # Eliminate 1 LLM in phase 3
            4: 0,  # Finals - no elimination, declare winner
        }
        eliminate_count = elimination_rules.get(phase, 0)
    
    if eliminate_count >= len(ranked_llms):
        print(f"WARNING: Cannot eliminate {eliminate_count} LLMs, only {len(ranked_llms)} remain")
        eliminate_count = max(0, len(ranked_llms) - 1)
    
    # Eliminate from the bottom of the rankings
    eliminated = ranked_llms[-eliminate_count:] if eliminate_count > 0 else []
    remaining = ranked_llms[:-eliminate_count] if eliminate_count > 0 else ranked_llms
    
    return eliminated, remaining


def record_phase(elimination_data, phase, totals, eliminated, remaining, apply_elimination):
    """Record the phase results in elimination data."""
    timestamp = datetime.now(timezone.utc).isoformat()
    
    phase_record = {
        'phase': phase,
        'timestamp': timestamp,
        'totals': totals,
        'eliminated_this_phase': [llm['llm'] for llm in eliminated] if apply_elimination else [],
        'remaining_after_phase': [llm['llm'] for llm in remaining] if apply_elimination else [llm['llm'] for llm in totals.values()],
        'elimination_applied': apply_elimination
    }
    
    elimination_data['phases'].append(phase_record)
    
    if apply_elimination:
        # Add to global eliminated list
        for llm in eliminated:
            if llm['llm'] not in elimination_data['eliminated']:
                elimination_data['eliminated'].append(llm['llm'])
        
        # Update remaining list
        elimination_data['remaining'] = [llm['llm'] for llm in remaining]
    
    print(f"\n✓ Phase {phase} recorded")
    print(f"  Timestamp: {timestamp}")
    if apply_elimination:
        print(f"  Eliminated: {', '.join([llm['llm'] for llm in eliminated]) if eliminated else 'None'}")
        print(f"  Remaining: {', '.join([llm['llm'] for llm in remaining])}")


def display_rankings(ranked_llms, phase):
    """Display current rankings in a formatted table."""
    print(f"\n{'=' * 70}")
    print(f"PHASE {phase} RANKINGS")
    print(f"{'=' * 70}")
    print(f"{'Rank':<6} {'LLM':<15} {'Videos':<10} {'Rounds':<10} {'Score':<10}")
    print(f"{'-' * 70}")
    
    for llm in ranked_llms:
        print(f"{llm['rank']:<6} {llm['llm']:<15} {llm['total_videos']:<10} {llm['rounds']:<10} {llm['score']:<10}")
    
    print(f"{'=' * 70}")


def main():
    parser = argparse.ArgumentParser(
        description='LLM Battle Royale Elimination Tracker'
    )
    parser.add_argument('--phase', type=int, required=True,
                        help='Battle phase number (1-4)')
    parser.add_argument('--eliminate', action='store_true',
                        help='Apply elimination logic (default: compute rankings only)')
    parser.add_argument('--eliminate-count', type=int,
                        help='Override number of LLMs to eliminate')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("LLM BATTLE ROYALE - ELIMINATION TRACKER")
    print("=" * 70)
    
    # Load battle data
    battle_data = load_battle_data()
    if not battle_data:
        return 1
    
    # Load elimination data
    elimination_data = load_elimination_data()
    
    # Compute totals per LLM
    totals = compute_llm_totals(battle_data)
    
    if not totals:
        print("ERROR: No LLM data found in battle_data.json")
        return 1
    
    print(f"\nAnalyzing {len(totals)} LLM(s)...")
    
    # Rank LLMs
    ranked_llms = rank_llms(totals)
    
    # Display rankings
    display_rankings(ranked_llms, args.phase)
    
    # Apply elimination logic if requested
    if args.eliminate:
        print(f"\n⚠️  APPLYING ELIMINATION LOGIC FOR PHASE {args.phase}")
        eliminated, remaining = apply_elimination_logic(
            ranked_llms,
            args.phase,
            args.eliminate_count
        )
        
        if eliminated:
            print(f"\n❌ ELIMINATED:")
            for llm in eliminated:
                print(f"   - {llm['llm']} (Rank {llm['rank']}, Score {llm['score']})")
        
        print(f"\n✓ REMAINING:")
        for llm in remaining:
            print(f"   - {llm['llm']} (Rank {llm['rank']}, Score {llm['score']})")
    else:
        print(f"\n[INFO] Dry-run mode - no elimination applied")
        print(f"       Use --eliminate to apply elimination logic")
        eliminated = []
        remaining = ranked_llms
    
    # Record phase
    record_phase(
        elimination_data,
        args.phase,
        totals,
        eliminated,
        remaining,
        args.eliminate
    )
    
    # Save elimination data
    save_elimination_data(elimination_data)
    
    print("\n" + "=" * 70)
    print("✓ TRACKING COMPLETE")
    print("=" * 70)
    
    if args.phase == 4 and args.eliminate and len(remaining) == 1:
        print(f"\n🏆 WINNER: {remaining[0]['llm']} 🏆")
    
    return 0


if __name__ == '__main__':
    exit(main())
