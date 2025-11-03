#!/usr/bin/env python3
"""
LLM BATTLE ROYALE - ELIMINATION ROUNDS TRACKER
Tracks round-by-round revenue, algo hacks, elimination risk
"""
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class EliminationRoundTracker:
    """Track elimination rounds competition"""
    
    def __init__(self, llm_name: str, competition_id: str = "battle_elim_001"):
        self.llm_name = llm_name
        self.competition_id = competition_id
        self.start_time = datetime.now()
        self.round_duration_hours = 6
        self.total_rounds = 12
        
        # Tracking file
        self.tracking_dir = Path("F:/AI_Oracle_Root/scarify/battle_tracking")
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        self.tracking_file = self.tracking_dir / f"{llm_name}_{competition_id}.json"
        
        # Initialize tracking data
        self.data = {
            "llm_name": llm_name,
            "competition_id": competition_id,
            "start_time": self.start_time.isoformat(),
            "status": "ACTIVE",
            
            # Round-by-round revenue
            "rounds": {
                str(i): {
                    "revenue": 0.0,
                    "errors": 0,
                    "penalty": 0.0,
                    "final_revenue": 0.0,
                    "rank": None,
                    "algo_hack_score": 0.0,
                    "immunity": False,
                }
                for i in range(1, 13)
            },
            
            # Cumulative totals
            "total_revenue": 0.0,
            "total_errors": 0,
            "algo_hacks": [],
            
            # Elimination data
            "elimination_round": None,
            "elimination_reason": None,
            "final_rank": None,
        }
        
        self._save()
    
    def get_current_round(self) -> int:
        """Calculate current round based on elapsed time"""
        elapsed = datetime.now() - self.start_time
        hours_elapsed = elapsed.total_seconds() / 3600
        current_round = min(int(hours_elapsed / self.round_duration_hours) + 1, self.total_rounds)
        return current_round
    
    def log_revenue_round(self, round_num: int, source: str, amount: float,
                         proof: str = "", transaction_id: str = "") -> None:
        """Log revenue for specific round"""
        if round_num < 1 or round_num > self.total_rounds:
            print(f"[Error] Invalid round: {round_num}")
            return
        
        round_key = str(round_num)
        
        # Add to round revenue
        self.data["rounds"][round_key]["revenue"] += amount
        
        # Recalculate with error penalty
        self._recalculate_round_revenue(round_num)
        
        # Update total
        self.data["total_revenue"] = sum(
            r["final_revenue"] for r in self.data["rounds"].values()
        )
        
        print(f"[Round {round_num}] Revenue logged: ${amount:.2f} from {source}")
        print(f"[Round {round_num}] Total this round: ${self.data['rounds'][round_key]['final_revenue']:.2f}")
        
        self._save()
    
    def log_error_round(self, round_num: int, error_type: str, severity: str = "code_error") -> None:
        """Log error for specific round (reduces revenue via penalty)"""
        if round_num < 1 or round_num > self.total_rounds:
            return
        
        round_key = str(round_num)
        
        # Error penalties (as percentage of revenue)
        penalties = {
            "code_error": 0.01,      # -1% per error
            "system_error": 0.05,    # -5% per error
            "business_error": 0.10,  # -10% per error
            "placeholder_error": 0.25, # -25% per error
        }
        
        penalty = penalties.get(severity, 0.01)
        
        # Increment error count
        self.data["rounds"][round_key]["errors"] += 1
        self.data["total_errors"] += 1
        
        # Add penalty percentage
        self.data["rounds"][round_key]["penalty"] += penalty
        
        # Recalculate final revenue with penalty
        self._recalculate_round_revenue(round_num)
        
        print(f"[Round {round_num}] Error logged: {severity} (-{penalty*100}%)")
        print(f"[Round {round_num}] Total penalty: {self.data['rounds'][round_key]['penalty']*100}%")
        print(f"[Round {round_num}] Final revenue: ${self.data['rounds'][round_key]['final_revenue']:.2f}")
        
        self._save()
    
    def _recalculate_round_revenue(self, round_num: int) -> None:
        """Recalculate round revenue with error penalties"""
        round_key = str(round_num)
        base = self.data["rounds"][round_key]["revenue"]
        penalty = self.data["rounds"][round_key]["penalty"]
        
        # Apply penalty (max 100% penalty = $0)
        multiplier = max(0, 1 - penalty)
        final = base * multiplier
        
        self.data["rounds"][round_key]["final_revenue"] = final
        
        # Check if revenue went to zero
        if final <= 0 and base > 0:
            print(f"[WARNING] Round {round_num} revenue reduced to $0 by penalties!")
    
    def log_algo_hack(self, round_num: int, name: str, description: str,
                     viral_score: float = 0, growth_score: float = 0,
                     innovation_score: float = 0) -> None:
        """Log algorithm hack attempt"""
        # Calculate total algo hack score
        total_score = (
            viral_score * 0.4 +
            growth_score * 0.3 +
            innovation_score * 100 * 0.3  # Innovation is 0-10, scale to 1000
        )
        
        hack_entry = {
            "round": round_num,
            "name": name,
            "description": description,
            "viral_score": viral_score,
            "growth_score": growth_score,
            "innovation_score": innovation_score,
            "total_score": total_score,
            "timestamp": datetime.now().isoformat(),
        }
        
        self.data["algo_hacks"].append(hack_entry)
        
        # Update round algo hack score (highest wins)
        round_key = str(round_num)
        if total_score > self.data["rounds"][round_key]["algo_hack_score"]:
            self.data["rounds"][round_key]["algo_hack_score"] = total_score
        
        print(f"\n[ALGO HACK] Round {round_num}")
        print(f"  Name: {name}")
        print(f"  Viral Score: {viral_score:,}")
        print(f"  Growth Score: {growth_score:,}")
        print(f"  Innovation Score: {innovation_score}/10")
        print(f"  TOTAL SCORE: {total_score:,.0f}")
        
        self._save()
    
    def get_elimination_risk(self, round_num: int, all_competitors: List[Dict] = None) -> Dict:
        """Calculate elimination risk for current round"""
        round_key = str(round_num)
        my_revenue = self.data["rounds"][round_key]["final_revenue"]
        
        if not all_competitors:
            # Can't calculate without other competitors' data
            return {
                "round": round_num,
                "my_revenue": my_revenue,
                "rank": None,
                "total_competitors": None,
                "in_danger": None,
                "revenue_to_safe": None,
            }
        
        # Sort all competitors by revenue (lowest to highest)
        sorted_comps = sorted(
            all_competitors,
            key=lambda x: x.get("rounds", {}).get(str(round_num), {}).get("final_revenue", 0)
        )
        
        # Find my rank (1 = lowest, worst)
        my_rank = None
        for i, comp in enumerate(sorted_comps, 1):
            if comp.get("llm_name") == self.llm_name:
                my_rank = i
                break
        
        total_competitors = len(sorted_comps)
        
        # Check if in danger (lowest or second-lowest)
        in_danger = my_rank <= 2 if my_rank else None
        
        # Calculate revenue needed to be safe (above 2nd lowest)
        revenue_to_safe = 0
        if in_danger and len(sorted_comps) >= 3:
            third_lowest_revenue = sorted_comps[2].get("rounds", {}).get(str(round_num), {}).get("final_revenue", 0)
            revenue_to_safe = max(0, third_lowest_revenue - my_revenue + 0.01)
        
        return {
            "round": round_num,
            "my_revenue": my_revenue,
            "rank": my_rank,
            "total_competitors": total_competitors,
            "in_danger": in_danger,
            "revenue_to_safe": revenue_to_safe,
            "algo_hack_score": self.data["rounds"][round_key]["algo_hack_score"],
        }
    
    def print_round_status(self, round_num: int) -> None:
        """Print status for specific round"""
        round_key = str(round_num)
        round_data = self.data["rounds"][round_key]
        
        print("\n" + "="*70)
        print(f"[ROUND {round_num} STATUS] {self.llm_name}")
        print("="*70)
        print(f"Base Revenue:    ${round_data['revenue']:.2f}")
        print(f"Errors:          {round_data['errors']}")
        print(f"Penalty:         -{round_data['penalty']*100:.1f}%")
        print(f"Final Revenue:   ${round_data['final_revenue']:.2f}")
        print(f"Algo Hack Score: {round_data['algo_hack_score']:,.0f}")
        print(f"Immunity:        {'YES' if round_data['immunity'] else 'NO'}")
        if round_data['rank']:
            print(f"Rank:            {round_data['rank']}")
        print("="*70 + "\n")
    
    def print_overall_status(self) -> None:
        """Print overall competition status"""
        current_round = self.get_current_round()
        
        print("\n" + "="*70)
        print(f"[OVERALL STATUS] {self.llm_name}")
        print("="*70)
        print(f"Status:         {self.data['status']}")
        print(f"Current Round:  {current_round}/{self.total_rounds}")
        print(f"Total Revenue:  ${self.data['total_revenue']:.2f}")
        print(f"Total Errors:   {self.data['total_errors']}")
        print(f"Algo Hacks:     {len(self.data['algo_hacks'])}")
        
        if self.data['status'] == "ELIMINATED":
            print(f"\nEliminated in Round: {self.data['elimination_round']}")
            print(f"Reason: {self.data['elimination_reason']}")
            print(f"Final Rank: {self.data['final_rank']}")
        
        print("\n[ROUND BREAKDOWN]")
        for i in range(1, current_round + 1):
            rd = self.data["rounds"][str(i)]
            status = "IMMUNE" if rd["immunity"] else f"Rank {rd['rank']}" if rd["rank"] else "Pending"
            print(f"  Round {i:2d}: ${rd['final_revenue']:8.2f} - {status}")
        
        print("="*70 + "\n")
    
    def eliminate(self, round_num: int, reason: str, final_rank: int) -> None:
        """Mark as eliminated"""
        self.data["status"] = "ELIMINATED"
        self.data["elimination_round"] = round_num
        self.data["elimination_reason"] = reason
        self.data["final_rank"] = final_rank
        
        print("\n" + "="*70)
        print(f"❌ {self.llm_name} - ELIMINATED")
        print("="*70)
        print(f"Round: {round_num}")
        print(f"Reason: {reason}")
        print(f"Final Rank: {final_rank}")
        print(f"Total Revenue: ${self.data['total_revenue']:.2f}")
        print("="*70 + "\n")
        
        self._save()
    
    def _save(self) -> None:
        """Save tracking data to file"""
        with open(self.tracking_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    @classmethod
    def load(cls, llm_name: str, competition_id: str = "battle_elim_001"):
        """Load existing tracker"""
        tracking_dir = Path("F:/AI_Oracle_Root/scarify/battle_tracking")
        tracking_file = tracking_dir / f"{llm_name}_{competition_id}.json"
        
        if not tracking_file.exists():
            return cls(llm_name, competition_id)
        
        with open(tracking_file, 'r') as f:
            data = json.load(f)
        
        tracker = cls(llm_name, competition_id)
        tracker.data = data
        tracker.start_time = datetime.fromisoformat(data["start_time"])
        return tracker


def main():
    """Example usage"""
    # Create tracker
    tracker = EliminationRoundTracker("Claude-Sonnet-4", "battle_elim_001")
    
    # Simulate Round 1 (Hours 0-6)
    print("\n[ROUND 1 SIMULATION]")
    tracker.log_revenue_round(1, "youtube_ads", 450.00, "proof1.png")
    tracker.log_revenue_round(1, "bitcoin_donations", 380.00, "proof2.png")
    tracker.log_error_round(1, "ImportError", "code_error")
    tracker.log_error_round(1, "ValueError", "code_error")
    
    # Algo hack attempt
    tracker.log_algo_hack(
        round_num=1,
        name="Multi-Platform Cascade",
        description="Post to TikTok first, then YouTube 30min later",
        viral_score=5200,
        growth_score=3100,
        innovation_score=7.5
    )
    
    tracker.print_round_status(1)
    
    # Simulate Round 2 (Hours 6-12)
    print("\n[ROUND 2 SIMULATION]")
    tracker.log_revenue_round(2, "youtube_ads", 520.00)
    tracker.log_revenue_round(2, "tiktok_fund", 290.00)
    tracker.log_error_round(2, "Timeout", "system_error")  # Ouch, -5%
    
    tracker.print_round_status(2)
    
    # Overall status
    tracker.print_overall_status()

if __name__ == "__main__":
    main()



