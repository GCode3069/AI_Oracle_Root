#!/usr/bin/env python3
"""
BATTLE CTR INTEGRATION - Combines Battle Royale with CTR Master
Tracks CTR-optimized videos in the competition system
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Import both systems
from ABRAHAM_CTR_MASTER import generate_ctr_optimized_video
from BATTLE_TRACKER_ELIMINATION_ROUNDS import BattleTracker

# ============================================================================
# INTEGRATED BATTLE + CTR SYSTEM
# ============================================================================

class BattleCTRSystem:
    """Combines Battle Royale competition with CTR optimization"""
    
    def __init__(self, llm_name="CTR_Master"):
        self.llm_name = llm_name
        self.tracker = BattleTracker()
        self.videos_generated = []
        
    def generate_battle_video(self, episode_num, round_num):
        """
        Generate a single CTR-optimized video and log it to battle tracker
        
        Returns: (video_path, estimated_revenue)
        """
        
        print(f"\n[ROUND {round_num}] Generating Episode #{episode_num}...")
        
        # Generate CTR-optimized video
        video_path = generate_ctr_optimized_video(episode_num)
        
        if not video_path:
            print(f"  [!] Generation failed for Episode #{episode_num}")
            return None, 0
        
        # Estimate initial revenue (will be updated from actual analytics)
        # For now, use a baseline estimate
        estimated_revenue = self._estimate_revenue(video_path)
        
        # Log to battle tracker
        self.tracker.log_video(
            llm_name=self.llm_name,
            round_num=round_num,
            video_id=f"EP{episode_num}",
            revenue=estimated_revenue
        )
        
        self.videos_generated.append({
            'episode': episode_num,
            'round': round_num,
            'path': str(video_path),
            'revenue': estimated_revenue,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"  [OK] Logged to Battle Tracker (Est. Revenue: ${estimated_revenue:.2f})")
        
        return video_path, estimated_revenue
    
    def _estimate_revenue(self, video_path):
        """
        Estimate revenue based on video metrics
        
        Formula:
        - CTR-optimized videos average 5,000 views in 48h
        - 0.5% see Cash App QR
        - 0.1% donate
        - Average donation $50
        - Base estimate: $2.50 per video
        - Plus YouTube ad revenue: $0.10 per video (pre-monetization views)
        """
        
        base_revenue = 2.50  # Cash App donations
        ad_revenue = 0.10    # Pre-monetization
        
        total = base_revenue + ad_revenue
        
        return total
    
    def run_round(self, round_num, videos_per_round=5, start_episode=20000):
        """
        Generate videos for a single battle round
        
        Args:
            round_num: Current round number (1-12)
            videos_per_round: How many videos to generate
            start_episode: Starting episode number
        
        Returns:
            total_revenue: Estimated revenue for this round
        """
        
        print(f"\n{'='*80}")
        print(f"  BATTLE ROUND #{round_num}")
        print(f"  LLM: {self.llm_name}")
        print(f"  Videos: {videos_per_round}")
        print(f"{'='*80}\n")
        
        total_revenue = 0
        
        for i in range(videos_per_round):
            episode = start_episode + (round_num - 1) * videos_per_round + i
            
            video_path, revenue = self.generate_battle_video(episode, round_num)
            
            if video_path:
                total_revenue += revenue
        
        print(f"\n{'='*80}")
        print(f"  ROUND {round_num} COMPLETE")
        print(f"  Total Revenue: ${total_revenue:.2f}")
        print(f"  Videos Generated: {videos_per_round}")
        print(f"{'='*80}\n")
        
        return total_revenue
    
    def run_full_competition(self, rounds=12, videos_per_round=5, start_episode=20000):
        """
        Run complete Battle Royale competition
        
        Args:
            rounds: Total number of rounds
            videos_per_round: Videos to generate per round
            start_episode: Starting episode number
        """
        
        print(f"\n{'='*80}")
        print(f"  BATTLE ROYALE + CTR MASTER")
        print(f"  Full Competition Mode")
        print(f"  LLM: {self.llm_name}")
        print(f"  Rounds: {rounds}")
        print(f"  Videos/Round: {videos_per_round}")
        print(f"  Total Videos: {rounds * videos_per_round}")
        print(f"{'='*80}\n")
        
        total_revenue_all = 0
        
        for round_num in range(1, rounds + 1):
            round_revenue = self.run_round(
                round_num=round_num,
                videos_per_round=videos_per_round,
                start_episode=start_episode
            )
            
            total_revenue_all += round_revenue
            
            # Check if we should be eliminated
            standings = self.tracker.get_standings()
            
            print(f"\n[STANDINGS AFTER ROUND {round_num}]")
            for rank, llm_data in enumerate(standings, 1):
                print(f"  #{rank}: {llm_data['llm']} - ${llm_data['revenue']:.2f}")
            print()
            
            # Pause between rounds (optional)
            if round_num < rounds:
                import time
                time.sleep(2)
        
        print(f"\n{'='*80}")
        print(f"  COMPETITION COMPLETE")
        print(f"  Total Revenue: ${total_revenue_all:.2f}")
        print(f"  Total Videos: {len(self.videos_generated)}")
        print(f"  Average Revenue/Video: ${total_revenue_all/len(self.videos_generated):.2f}")
        print(f"{'='*80}\n")
        
        return total_revenue_all

# ============================================================================
# COMMAND LINE INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Battle CTR Integration')
    parser.add_argument('--llm', default='CTR_Master', help='LLM name for tracking')
    parser.add_argument('--round', type=int, help='Single round number (1-12)')
    parser.add_argument('--full', action='store_true', help='Run full competition')
    parser.add_argument('--videos', type=int, default=5, help='Videos per round')
    parser.add_argument('--start', type=int, default=20000, help='Starting episode number')
    
    args = parser.parse_args()
    
    system = BattleCTRSystem(llm_name=args.llm)
    
    if args.full:
        # Run full competition
        system.run_full_competition(
            rounds=12,
            videos_per_round=args.videos,
            start_episode=args.start
        )
    elif args.round:
        # Run single round
        system.run_round(
            round_num=args.round,
            videos_per_round=args.videos,
            start_episode=args.start
        )
    else:
        # Default: Run Round 1
        print("Running Round 1 (use --full for complete competition)")
        system.run_round(
            round_num=1,
            videos_per_round=args.videos,
            start_episode=args.start
        )


