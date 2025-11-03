import os
import random
from real_tts_engine import RealTTSEngine
from real_video_forge import RealVideoForge

def main():
    print("🚀 STARTING SIMPLE NUKE...")
    
    pains = [
        "Chicago garage supply meltdown",
        "Mechanic deadweight employees", 
        "Barber no-show clients",
        "Plumber emergency call drought",
        "Welder material waste killing margins",
        "HVAC techs late to jobs",
        "Electrician bidding too low",
        "Landscaper seasonal cash crash",
        "Auto detailer slow client flow",
        "Concrete crew bidding wars",
        "Painter lead gen drought",
        "Tow truck slow nights"
    ]
    
    os.makedirs("output/audio", exist_ok=True)
    os.makedirs("output/videos", exist_ok=True)
    
    tts = RealTTSEngine()
    video_forge = RealVideoForge()
    
    success_count = 0
    
    for i, pain in enumerate(pains, 1):
        print(f"🎯 REBEL {i}/12: {pain}")
        
        bleed = [47,52,58,63,67,72,78,83,47,52,58,63][i-1]
        script = f"Bleeding ${bleed}k from {pain}? I was there. $97 Trench Kit stopped the bleed in {random.randint(3,7)} days. Get yours: https://gumroad.com/l/TRENCHKIT97"
        
        # Audio
        audio_file = f"output/audio/rebel_{i:02d}.mp3"
        audio_success = tts.generate_audio(script, audio_file)
        
        # Video
        video_file = f"output/videos/rebel_{i:02d}.mp4"
        try:
            video_forge.create_video(script, audio_file, video_file)
            if os.path.exists(video_file):
                success_count += 1
                print(f"✅ REBEL {i} FORGED: {video_file}")
            else:
                print(f"❌ REBEL {i} FAILED")
        except Exception as e:
            print(f"❌ REBEL {i} ERROR: {e}")
    
    print(f"🎉 SIMPLE NUKE COMPLETE: {success_count}/12 MP4s")
    return success_count

if __name__ == "__main__":
    main()
