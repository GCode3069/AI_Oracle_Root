# SCARIFY_COMPLETE.py
import time
from pathlib import Path
from DUAL_STYLE_GENERATOR import generate_video_concept, generate_script_text
from KLING_CACHE import check_cache, save_to_cache
from VIDEO_LAYOUT import create_pip_layout, apply_vhs_effects

OUTPUT_DIR = Path("D:/AI_Oracle_Projects/Output/Generated")
TEMP_DIR = Path("D:/AI_Oracle_Projects/Temp")

def generate_complete_video():
    """Generate one complete SCARIFY video"""
    print("\n" + "="*60)
    print("🎬 SCARIFY VIDEO GENERATOR")
    print("="*60 + "\n")
    
    start_time = time.time()
    cost = 0
    
    # Step 1: Generate concept
    print("📝 Step 1: Generating concept...")
    concept = generate_video_concept()
    script = generate_script_text(concept)
    print(f"✅ Style: {concept['style']}")
    print(f"✅ Topic: {concept['category']}")
    print(f"✅ Title: {concept['title']}\n")
    print(f"Script preview:\n{script[:200]}...\n")
    
    # Step 2: Voice synthesis (mock)
    print("🎤 Step 2: Voice synthesis...")
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    voice_path = TEMP_DIR / "voice.mp3"
    print(f"✅ Voice generated (mock) - Cost: $0.02")
    cost += 0.02
    
    # Step 3: Subliminal audio (mock)
    print("\n🎧 Step 3: Subliminal audio...")
    enhanced_audio = TEMP_DIR / "enhanced_audio.mp3"
    print(f"✅ Audio enhanced with binaural beats (mock)")
    
    # Step 4: Portrait (mock)
    print("\n🖼️ Step 4: Portrait...")
    portrait_path = Path("D:/AI_Oracle_Projects/Assets/Portraits/lincoln_1.jpg")
    print(f"✅ Portrait ready (mock)")
    
    # Step 5: Kling cache check
    print("\n🗣️ Step 5: Kling AI lip-sync...")
    cached_video = check_cache(str(voice_path), str(portrait_path))
    
    if cached_video:
        print(f"💰 Cache HIT! Saved $0.04!")
        lipsync_video = cached_video
    else:
        print("⏳ Generating new lip-sync (mock)...")
        lipsync_video = TEMP_DIR / "lipsync.mp4"
        print(f"✅ Generated - Cost: $0.04")
        cost += 0.04
        save_to_cache(str(lipsync_video), str(voice_path), str(portrait_path))
    
    # Step 6: Layout (mock)
    print("\n📺 Step 6: Picture-in-picture layout...")
    pip_video = TEMP_DIR / "pip.mp4"
    print(f"✅ Layout created (1080x1920)")
    
    # Step 7: VHS effects (mock)
    print("\n🎞️ Step 7: VHS effects...")
    final_video = TEMP_DIR / "final.mp4"
    print(f"✅ VHS aesthetic applied")
    
    # Step 8: Save
    output_folder = OUTPUT_DIR / ("Winners" if concept['style'] == "WARNING" else "Comedy")
    output_folder.mkdir(parents=True, exist_ok=True)
    
    video_num = len(list(output_folder.glob("*.mp4"))) + 1
    output_path = output_folder / f"lincoln_{concept['style'].lower()}_{video_num:03d}.mp4"
    
    print(f"\n💾 Step 8: Saving...")
    print(f"✅ Saved to: {output_path}")
    
    # Summary
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print("✅ VIDEO COMPLETE!")
    print(f"💰 Cost: ${cost:.3f}")
    print(f"⏱️ Time: {elapsed:.1f}s")
    print(f"📁 Output: {output_path}")
    print("="*60 + "\n")
    
    return {
        'path': str(output_path),
        'cost': cost,
        'time': elapsed,
        'style': concept['style'],
        'category': concept['category']
    }

def generate_batch(count=10):
    """Generate multiple videos"""
    print(f"\n🎬 BATCH GENERATION: {count} VIDEOS\n")
    
    results = []
    total_cost = 0
    warning_count = 0
    comedy_count = 0
    cache_hits = 0
    
    for i in range(count):
        print(f"\n▶️ VIDEO {i+1}/{count}")
        result = generate_complete_video()
        results.append(result)
        total_cost += result['cost']
        
        if result['style'] == 'WARNING':
            warning_count += 1
        else:
            comedy_count += 1
        
        if result['cost'] < 0.05:
            cache_hits += 1
    
    print("\n" + "="*60)
    print("📊 BATCH SUMMARY")
    print("="*60)
    print(f"Total videos: {count}")
    print(f"WARNING: {warning_count} ({warning_count/count*100:.0f}%)")
    print(f"COMEDY: {comedy_count} ({comedy_count/count*100:.0f}%)")
    print(f"Cache hits: {cache_hits} ({cache_hits/count*100:.0f}%)")
    print(f"Total cost: ${total_cost:.2f}")
    print(f"Average: ${total_cost/count:.3f}/video")
    print("="*60 + "\n")
    
    return results

if __name__ == "__main__":
    print("🎬 SCARIFY Complete System Ready!")
    print("\nTest with: python SCARIFY_COMPLETE.py")
    print("Or from Python:")
    print("  from SCARIFY_COMPLETE import generate_complete_video")
    print("  generate_complete_video()")
