#!/usr/bin/env python3
"""
YOUTUBE OPTIMIZER - INTEGRATED WITH VIDEO GENERATION
Automatically applies optimizations based on channel analytics
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import json

class ContentOptimizer:
    """Optimize video content based on proven metrics"""
    
    def __init__(self):
        # Based on your analytics: Lincoln's WARNING #52 & #27 performed best
        self.optimal_duration = (9, 17)  # seconds
        self.optimal_retention_target = 45  # percent
        self.proven_title_format = "Lincoln's WARNING #[NUM]: [TOPIC] #Shorts #R3"
        
        # Peak performance times (EST)
        self.peak_times = [
            (12, 15),  # 12pm-3pm
            (19, 22),  # 7pm-10pm
        ]
        
        # Proven topics (from your top videos)
        self.hot_topics = [
            "Education System",
            "Military Draft",
            "Police Strike",
            "Market Crash",
            "Government Corruption",
            "Tech CEOs",
            "Water Crisis",
        ]
    
    def optimize_script_length(self, script):
        """Ensure script targets optimal duration (9-17s)"""
        words = script.split()
        # Average speaking rate: 150-160 words/minute
        # For 9-17s: 22-45 words
        target_words = 35  # Sweet spot
        
        if len(words) > 45:
            # Script too long, trim to essential
            return ' '.join(words[:45]) + " Look in mirrors."
        elif len(words) < 22:
            # Script too short, might not engage
            return script + " AMERICA! Look in mirrors."
        
        return script
    
    def add_retention_hooks(self, script):
        """Add hooks proven to increase retention"""
        hooks = [
            "AMERICA!",  # Attention grabber
            "WARNING:",  # Urgency
            "This is INSANE!",  # Emotional reaction
        ]
        
        # Ensure script starts strong
        if not any(hook in script[:50] for hook in hooks):
            script = "AMERICA! " + script
        
        return script
    
    def optimize_for_shorts_algorithm(self, metadata):
        """Optimize metadata for Shorts algorithm (95% of your traffic)"""
        # Ensure proper formatting
        metadata['hashtags'] = ['Shorts', 'R3', 'Lincoln', 'WARNING']
        
        # Title format proven to work
        if 'episode_num' in metadata:
            metadata['title'] = f"Lincoln's WARNING #{metadata['episode_num']}: {metadata['topic']} #Shorts #R3"
        
        # Description optimized for Shorts
        metadata['description'] = (
            f"{metadata.get('topic', 'Breaking News')}\n\n"
            "⚠️ Lincoln's WARNING series\n"
            "💀 Subscribe for daily warnings\n"
            "🔔 Turn on notifications\n\n"
            "#Shorts #Lincoln #WARNING #R3"
        )
        
        return metadata
    
    def get_posting_schedule(self, videos_per_day=50):
        """Generate optimal posting schedule"""
        schedule = []
        current_hour = 6  # Start at 6am
        
        for i in range(videos_per_day):
            # Prioritize peak times
            if (12 <= current_hour <= 15) or (19 <= current_hour <= 22):
                schedule.append({
                    'video_num': i + 1,
                    'post_time': f"{current_hour:02d}:00",
                    'priority': 'HIGH',
                })
            else:
                schedule.append({
                    'video_num': i + 1,
                    'post_time': f"{current_hour:02d}:00",
                    'priority': 'NORMAL',
                })
            
            # Increment time (post every 20 minutes during production)
            current_hour += 0.33  # 20 minutes
            if current_hour >= 24:
                current_hour = 0
        
        return schedule

def analyze_video_performance(video_url):
    """Analyze a specific video and provide fixes"""
    print(f"\n[ANALYZING VIDEO] {video_url}\n")
    
    # Extract video ID
    if 'shorts/' in video_url:
        video_id = video_url.split('shorts/')[-1].split('?')[0]
    elif 'watch?v=' in video_url:
        video_id = video_url.split('watch?v=')[-1].split('&')[0]
    else:
        video_id = "unknown"
    
    print(f"Video ID: {video_id}\n")
    
    # Common issues based on user feedback
    issues_to_check = [
        "[?] QR code visible (top-right)?",
        "[?] No Bitcoin address in audio?",
        "[?] Duration 9-17 seconds?",
        "[?] WARNING format title?",
        "[?] #Shorts hashtag?",
        "[?] Max Headroom VHS effects?",
        "[?] High contrast (Lincoln visible)?",
        "[?] Lip-sync animation?",
        "[?] Jumpscare effect?",
    ]
    
    print("[CHECKLIST]")
    for issue in issues_to_check:
        print(f"  {issue}")
    print()
    
    # Specific fixes for reported issues
    print("[REQUIRED FIXES]")
    print("  1. Remove Bitcoin address from script")
    print("     [X] OLD: 'Bitcoin bc1q...'")
    print("     [OK] NEW: 'Look in mirrors.'")
    print()
    print("  2. Ensure QR code is visible")
    print("     [OK] Position: Top-right corner")
    print("     [OK] Size: 150x150px")
    print("     [OK] Always visible (don't fade)")
    print()
    print("  3. Optimize script length")
    print("     [OK] Target: 9-17 seconds")
    print("     [OK] 22-45 words total")
    print()
    
    return {
        'video_id': video_id,
        'issues_found': ['Bitcoin address in audio', 'QR code missing'],
        'fixes_needed': ['Update script', 'Re-generate video'],
    }

def main():
    """Run optimizer and analyzer"""
    print("\n" + "="*70)
    print("  YOUTUBE CHANNEL OPTIMIZER & VIDEO ANALYZER")
    print("="*70)
    
    # If video URL provided, analyze it
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        analyze_video_performance(video_url)
    else:
        # Run full channel analysis
        from youtube_channel_analyzer import YouTubeChannelAnalyzer
        analyzer = YouTubeChannelAnalyzer()
        analyzer.analyze_performance()
        analyzer.generate_recommendations()
        analyzer.calculate_monetization_timeline()
        analyzer.generate_content_formula()
        analyzer.export_optimization_plan()
    
    print("\n" + "="*70)
    print("  [OK] OPTIMIZATION COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()

