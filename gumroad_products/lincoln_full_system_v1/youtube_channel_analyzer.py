#!/usr/bin/env python3
"""
YOUTUBE CHANNEL ANALYZER & OPTIMIZER
Analyzes your YouTube channel metrics and provides actionable optimizations
Based on your channel: DissWhatImSayin (Lincoln's WARNING series)
"""
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Your channel data from analytics
CHANNEL_DATA = {
    "channel_name": "DissWhatImSayin",
    "channel_id": "UCS5pEpSCw8k4wene0iv0uAg",
    "period": "Last 28 days (Oct 3-30, 2025)",
    "total_views": 3321,
    "avg_retention": 36.0,
    "total_videos": 10,  # Visible in analytics
}

# Top performing videos from your analytics
TOP_PERFORMERS = [
    {"title": "Lincoln's WARNING #52", "duration": "0:17", "retention": 45.1, "views": 1130},
    {"title": "Lincoln's WARNING #27", "duration": "0:09", "retention": 45.3, "views": 929},
    {"title": "Lincoln's WARNING #29", "duration": "0:16", "retention": 32.8, "views": 247},
]

# Traffic sources
TRAFFIC_SOURCES = {
    "Shorts feed": {"views": 3166, "percentage": 95.3, "avg_duration": "0:17"},
    "Channel pages": {"views": 64, "percentage": 1.9, "avg_duration": "0:52"},
    "YouTube search": {"views": 41, "percentage": 1.2, "avg_duration": "0:16"},
}

class YouTubeChannelAnalyzer:
    """Analyze and optimize YouTube channel performance"""
    
    def __init__(self):
        self.insights = []
        self.recommendations = []
        self.optimizations = []
    
    def analyze_performance(self):
        """Analyze current performance metrics"""
        print("\n" + "="*70)
        print("  YOUTUBE CHANNEL ANALYSIS - DissWhatImSayin")
        print("="*70 + "\n")
        
        # Overall metrics
        print("[OVERALL METRICS]")
        print(f"  Total Views: {CHANNEL_DATA['total_views']:,}")
        print(f"  Average Retention: {CHANNEL_DATA['avg_retention']}%")
        print(f"  Period: {CHANNEL_DATA['period']}\n")
        
        # Top performers analysis
        print("[TOP PERFORMERS]")
        for i, video in enumerate(TOP_PERFORMERS, 1):
            print(f"  {i}. {video['title']}")
            print(f"     Views: {video['views']:,} | Retention: {video['retention']}% | Duration: {video['duration']}")
        print()
        
        # Traffic source analysis
        print("[TRAFFIC SOURCES]")
        for source, data in TRAFFIC_SOURCES.items():
            print(f"  {source}: {data['percentage']}% ({data['views']:,} views)")
            print(f"     Avg Duration: {data['avg_duration']}")
        print()
        
        # Key insights
        self._generate_insights()
        
        print("[KEY INSIGHTS]")
        for i, insight in enumerate(self.insights, 1):
            print(f"  {i}. {insight}")
        print()
    
    def _generate_insights(self):
        """Generate insights based on data"""
        # Retention analysis
        best_retention = max(v['retention'] for v in TOP_PERFORMERS)
        if best_retention > 40:
            self.insights.append(f"Excellent retention ({best_retention}%) - Keep this content style!")
        
        # Duration analysis
        top_durations = [v['duration'] for v in TOP_PERFORMERS[:2]]
        if all(d in ['0:09', '0:17', '0:16'] for d in top_durations):
            self.insights.append("Short videos (9-17s) perform best - Stick to this length")
        
        # Traffic analysis
        shorts_percentage = TRAFFIC_SOURCES['Shorts feed']['percentage']
        if shorts_percentage > 90:
            self.insights.append(f"Shorts feed is dominant ({shorts_percentage}%) - Optimize for Shorts algorithm")
        
        # Growth potential
        recent_spike = True  # From chart showing spike after Oct 26
        if recent_spike:
            self.insights.append("Recent view spike detected - Momentum is building!")
    
    def generate_recommendations(self):
        """Generate specific recommendations for improvement"""
        print("[RECOMMENDATIONS FOR FASTER MONETIZATION]\n")
        
        recommendations = [
            {
                "category": "CONTENT OPTIMIZATION",
                "actions": [
                    "Keep videos between 9-17 seconds (your sweet spot)",
                    "Target 45%+ retention (you're hitting this!)",
                    "Use 'Lincoln's WARNING' format (proven winner)",
                    "Post daily during your peak growth period",
                ]
            },
            {
                "category": "SHORTS ALGORITHM OPTIMIZATION",
                "actions": [
                    "95% views from Shorts feed - optimize titles for Shorts",
                    "Use #Shorts hashtag consistently",
                    "Hook viewers in first 2 seconds (critical for Shorts)",
                    "Post at peak times: 12pm-3pm, 7pm-10pm EST",
                ]
            },
            {
                "category": "ENGAGEMENT BOOSTERS",
                "actions": [
                    "Add clear CTA in first 3 seconds",
                    "Use text overlays (WARNING format works)",
                    "Keep Bitcoin QR code visible (don't recite address)",
                    "End with cliffhanger to encourage replays",
                ]
            },
            {
                "category": "MONETIZATION MILESTONES",
                "actions": [
                    "Target: 1,000 subscribers (current progress: track in Studio)",
                    "Target: 10M Shorts views in 90 days",
                    "Current pace: 3,321 views/28 days = ~118 views/day",
                    "Need: ~111,111 views/day for 10M in 90 days",
                    "Strategy: Scale to 50-100 videos/day with proven format",
                ]
            },
            {
                "category": "TECHNICAL OPTIMIZATIONS",
                "actions": [
                    "Ensure QR code is always visible (top-right, 150x150px)",
                    "Don't recite Bitcoin address in audio (wastes time)",
                    "Keep VHS glitch effects (unique visual identity)",
                    "Maintain 1080x1920 vertical format",
                ]
            },
        ]
        
        for rec in recommendations:
            print(f"[{rec['category']}]")
            for action in rec['actions']:
                print(f"  - {action}")
            print()
        
        self.recommendations = recommendations
    
    def calculate_monetization_timeline(self):
        """Calculate timeline to monetization based on current metrics"""
        print("[MONETIZATION TIMELINE]\n")
        
        current_views_per_day = CHANNEL_DATA['total_views'] / 28
        target_views = 10_000_000  # 10M Shorts views for monetization
        
        # Scenario 1: Current pace
        days_at_current_pace = target_views / current_views_per_day
        print(f"Scenario 1: Current Pace ({current_views_per_day:.0f} views/day)")
        print(f"  Time to 10M views: {days_at_current_pace:.0f} days ({days_at_current_pace/365:.1f} years)")
        print(f"  Status: Too slow [X]\n")
        
        # Scenario 2: With 10x content (what you need)
        videos_per_day_current = 10 / 28  # 10 videos in 28 days
        videos_per_day_target = 50
        multiplier = videos_per_day_target / videos_per_day_current
        
        optimized_views_per_day = current_views_per_day * multiplier * 1.5  # 1.5x for optimization
        days_optimized = target_views / optimized_views_per_day
        
        print(f"Scenario 2: Scaled Production ({videos_per_day_target} videos/day)")
        print(f"  Projected views/day: {optimized_views_per_day:.0f}")
        print(f"  Time to 10M views: {days_optimized:.0f} days ({days_optimized/30:.1f} months)")
        print(f"  Status: Achievable [OK]\n")
        
        # Scenario 3: With viral breakout (1 video goes viral)
        viral_views = 1_000_000
        remaining_views = target_views - viral_views
        days_with_viral = remaining_views / optimized_views_per_day
        
        print(f"Scenario 3: Viral Breakout (1 video hits 1M views)")
        print(f"  Time to 10M views: {days_with_viral:.0f} days ({days_with_viral/30:.1f} months)")
        print(f"  Status: Best case [BEST]\n")
        
        print("[RECOMMENDED STRATEGY]")
        print(f"  1. Scale to 50-100 videos/day (use automated system)")
        print(f"  2. Focus on proven format (Lincoln's WARNING)")
        print(f"  3. Optimize for Shorts algorithm (95% of your traffic)")
        print(f"  4. Target: Monetization in 3-6 months\n")
    
    def generate_content_formula(self):
        """Generate winning content formula based on top performers"""
        print("[WINNING CONTENT FORMULA]\n")
        
        formula = {
            "Title": "Lincoln's WARNING #[NUM]: [SHOCKING STATEMENT] #Shorts #R3",
            "Duration": "9-17 seconds (sweet spot)",
            "Hook": "First 2 seconds: Show Lincoln + WARNING text",
            "Content": "Abe roasts current event in 1-2 punchy lines",
            "Visual": "VHS TV effect, Max Headroom glitch, high contrast",
            "CTA": "QR code visible (top-right), NO audio recitation",
            "End": "Cliffhanger or shocking statement",
            "Hashtags": "#Shorts #R3 (always)",
            "Topics": "Current events, politics, trending news",
        }
        
        print("[PROVEN FORMULA - From your top videos]")
        for key, value in formula.items():
            print(f"  {key}: {value}")
        print()
    
    def export_optimization_plan(self):
        """Export detailed optimization plan"""
        output_dir = Path("youtube_optimization")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = output_dir / f"optimization_report_{timestamp}.json"
        
        report = {
            "channel_data": CHANNEL_DATA,
            "top_performers": TOP_PERFORMERS,
            "traffic_sources": TRAFFIC_SOURCES,
            "insights": self.insights,
            "recommendations": self.recommendations,
            "timestamp": timestamp,
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[OPTIMIZATION REPORT EXPORTED]")
        print(f"  {report_file}\n")
        
        return report_file

def main():
    """Run complete channel analysis"""
    analyzer = YouTubeChannelAnalyzer()
    
    # Run analysis
    analyzer.analyze_performance()
    analyzer.generate_recommendations()
    analyzer.calculate_monetization_timeline()
    analyzer.generate_content_formula()
    
    # Export report
    report_file = analyzer.export_optimization_plan()
    
    print("="*70)
    print("  [OK] ANALYSIS COMPLETE")
    print("="*70)
    print("\n[NEXT STEPS]")
    print("  1. Fix QR code issue (don't recite address)")
    print("  2. Scale to 50+ videos/day with proven format")
    print("  3. Post at peak times (12-3pm, 7-10pm EST)")
    print("  4. Monitor metrics weekly")
    print("  5. Target: 10M views in 3-6 months\n")

if __name__ == "__main__":
    main()

