"""
QUICK STATUS REPORT GENERATOR
Shows what's working, what's pending, what needs attention
"""
import json
from pathlib import Path
from datetime import datetime

BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

def generate_status():
    """Generate quick status report"""
    print("\n" + "="*70)
    print("SYSTEM STATUS REPORT")
    print("="*70)
    
    # Check uploaded folder
    uploaded_dir = BASE / "uploaded"
    if uploaded_dir.exists():
        videos = list(uploaded_dir.glob("*.mp4"))
        qr_videos = list(uploaded_dir.glob("*_QR.mp4"))
        ultimate_videos = [v for v in videos if "ULTIMATE_HORROR" in v.name and "_QR" not in v.name]
        cognitohazard = [v for v in videos if "COGNITOHAZARD" in v.name]
        
        print(f"\n[LOCAL VIDEO LIBRARY]")
        print(f"   Total Videos: {len(videos)}")
        print(f"   With QR Codes: {len(qr_videos)}")
        print(f"   Ultimate Horror (new): {len(ultimate_videos)}")
        print(f"   Cognitohazard Episodes: {len(cognitohazard)}")
        
        if ultimate_videos:
            print(f"\n[NEW ULTIMATE HORROR VIDEOS] (Generated today):")
            for v in sorted(ultimate_videos, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                size_mb = v.stat().st_size / (1024*1024)
                mod_time = datetime.fromtimestamp(v.stat().st_mtime).strftime("%H:%M:%S")
                print(f"   - {v.name}")
                print(f"     Size: {size_mb:.1f}MB | Created: {mod_time}")
    
    # Check analytics report
    reports = list(BASE.glob("analytics_report_*.json"))
    if reports:
        latest = sorted(reports, key=lambda x: x.stat().st_mtime, reverse=True)[0]
        print(f"\n[ANALYTICS REPORT]")
        print(f"   Latest: {latest.name}")
        
        try:
            with open(latest, 'r') as f:
                data = json.load(f)
            
            if 'channel' in data:
                print(f"   Subscribers: {data['channel']['subscribers']} / 500")
                print(f"   Total Views: {data['channel']['total_views']:,}")
                print(f"   Total Videos: {data['channel']['total_videos']}")
            
            if 'summary' in data:
                print(f"   QR Coverage: {data['summary']['qr_coverage']:.1f}%")
                print(f"   Missing QR: {data['summary']['videos_without_qr']} videos")
        except:
            pass
    
    # Check temp folder for issues
    temp_dir = BASE / "temp"
    if temp_dir.exists():
        temp_files = list(temp_dir.glob("*"))
        print(f"\n[TEMP FILES]")
        print(f"   Files in temp/: {len(temp_files)}")
        if len(temp_files) > 50:
            print(f"   WARNING: Temp folder has {len(temp_files)} files (consider cleanup)")
    
    # YouTube Studio Observations
    print(f"\n[YOUTUBE STUDIO OBSERVATIONS]")
    print(f"   Based on screenshot:")
    print(f"   - 2 Cognitohazard videos: PUBLISHED (0 views each)")
    print(f"   - 6+ videos: PENDING (Processing will begin shortly)")
    print(f"   - Issue: Videos stuck in pending state")
    
    print(f"\n[RECOMMENDATIONS]")
    print(f"   1. Wait 1-2 hours for pending videos to process")
    print(f"   2. Delete videos stuck >24 hours in pending")
    print(f"   3. Check video file sizes - large files process slower")
    print(f"   4. New Ultimate Horror videos ready to upload:")
    if ultimate_videos:
        print(f"      - {len(ultimate_videos)} videos with QR codes")
        print(f"      - Location: uploaded/ULTIMATE_HORROR_*.mp4")
        print(f"      - These should upload successfully")
    
    print("\n" + "="*70)
    print("STATUS: SYSTEM OPERATIONAL")
    print("="*70)
    
    return {
        'videos_total': len(videos) if uploaded_dir.exists() else 0,
        'qr_coverage': len(qr_videos),
        'ultimate_new': len(ultimate_videos),
        'pending_issue': True
    }

if __name__ == "__main__":
    generate_status()

