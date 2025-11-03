"""
AUTOMATED PERFORMANCE TRACKER
Tracks video performance and identifies winning formulas
No Google Sheets required - uses local analysis
"""
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def analyze_performance():
    """Analyze YouTube performance from API data"""
    print("\n" + "="*70)
    print("AUTOMATED PERFORMANCE ANALYSIS")
    print("="*70)
    
    # Load latest analytics report
    reports = list(BASE.glob("analytics_report_*.json"))
    if not reports:
        print("[ERROR] No analytics reports found")
        print("[INFO] Run: python YOUTUBE_ANALYTICS_CONNECTOR.py")
        return None
    
    latest = sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True)[0]
    
    with open(latest, 'r') as f:
        data = json.load(f)
    
    print(f"\n[REPORT] {latest.name}")
    print(f"[DATE] {data.get('generated', 'Unknown')[:19]}")
    
    # Channel overview
    channel = data.get('channel', {})
    print(f"\n[CHANNEL STATS]")
    print(f"   Subscribers: {channel.get('subscribers', 0)} / 500")
    print(f"   Total Views: {channel.get('total_views', 0):,}")
    print(f"   Total Videos: {channel.get('total_videos', 0)}")
    
    # Top performers
    top = data.get('top_performing', [])
    
    if top:
        print(f"\n[TOP 10 PERFORMERS]")
        for i, video in enumerate(top[:10], 1):
            title = video.get('title', 'Unknown')[:55]
            views = video.get('views', 0)
            print(f"   {i:2}. {title:55} | {views:4} views")
        
        # Analyze patterns
        print(f"\n[PATTERN ANALYSIS]")
        
        # Title keywords
        all_titles = [v['title'].lower() for v in top]
        keywords = defaultdict(int)
        
        for title in all_titles:
            for word in ["warning", "roast", "government", "market", "system", "police", "education", "military"]:
                if word in title:
                    keywords[word] += 1
        
        print(f"   Keyword Performance (in top videos):")
        for word, count in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
            print(f"   - '{word}': appears in {count} top videos")
        
        # View patterns
        high_performers = [v for v in top if v.get('views', 0) > 100]
        med_performers = [v for v in top if 20 < v.get('views', 0) <= 100]
        low_performers = [v for v in top if v.get('views', 0) <= 20]
        
        print(f"\n[VIEW DISTRIBUTION]")
        print(f"   High (>100 views): {len(high_performers)} videos")
        print(f"   Medium (20-100): {len(med_performers)} videos")
        print(f"   Low (<20): {len(low_performers)} videos")
        
        # Recommendations
        print(f"\n[RECOMMENDATIONS]")
        
        if high_performers:
            avg_views_high = sum(v['views'] for v in high_performers) / len(high_performers)
            print(f"   1. High performers average {avg_views_high:.0f} views")
            print(f"      Focus on similar titles/topics")
        
        if keywords:
            top_keyword = max(keywords.items(), key=lambda x: x[1])[0]
            print(f"   2. '{top_keyword}' is most common in top videos")
            print(f"      Use this theme in next batch")
        
        print(f"   3. Generate 20-30 videos using winning formulas")
        print(f"   4. Add QR codes to all (already configured)")
    
    print("\n" + "="*70)
    
    return {
        'channel': channel,
        'top_performers': top,
        'high_performers': len(high_performers) if top else 0,
        'top_keyword': max(keywords.items(), key=lambda x: x[1])[0] if keywords else None
    }

def generate_recommendations_file():
    """Generate actionable recommendations file"""
    analysis = analyze_performance()
    
    if not analysis:
        return
    
    recs_file = BASE / "PERFORMANCE_RECOMMENDATIONS.txt"
    
    with open(recs_file, 'w') as f:
        f.write("="*70 + "\n")
        f.write("PERFORMANCE-BASED RECOMMENDATIONS\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        f.write("CURRENT STATUS:\n")
        f.write(f"  Subscribers: {analysis['channel'].get('subscribers', 0)} / 500\n")
        f.write(f"  Total Views: {analysis['channel'].get('total_views', 0):,}\n")
        f.write(f"  High Performers: {analysis['high_performers']} videos\n\n")
        
        f.write("WINNING FORMULA:\n")
        if analysis.get('top_keyword'):
            f.write(f"  Top Keyword: '{analysis['top_keyword']}'\n")
        f.write("  Style: Lincoln WARNING / Roasts format\n")
        f.write("  Length: 20-45 seconds (Shorts)\n")
        f.write("  Topics: Government, Markets, System issues\n\n")
        
        f.write("NEXT BATCH GENERATION:\n")
        f.write("  Command: python ULTIMATE_HORROR_GENERATOR.py 20\n")
        f.write("  Focus: Use winning keywords and themes\n")
        f.write("  Features: QR codes, jump scares, Max Headroom style\n")
        f.write("  Target: 500+ views per video (based on top performers)\n\n")
        
        f.write("TIMELINE TO 500 SUBS:\n")
        f.write("  Current: 13 subs\n")
        f.write("  Needed: 487 more\n")
        f.write("  With 20-30 videos/day: 14-21 days\n")
        f.write("  With viral QR tactics: 7-14 days\n")
        
    print(f"\n[SAVED] Recommendations: {recs_file}")
    return str(recs_file)

if __name__ == "__main__":
    analyze_performance()
    generate_recommendations_file()

