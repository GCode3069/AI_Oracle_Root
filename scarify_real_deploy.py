import os
import random
from datetime import datetime

print("🚀 SCARIFY DEPLOYMENT - NO BULLSHIT VERSION")
print("===========================================")

def generate_audio_elevenlabs(script_text, voice="Bella"):
    try:
        with open(r"F:\AI_Oracle_Root\scarify\config\credentials\elevenlabs_api.key", "rb") as f:
            raw_bytes = f.read()
        
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            clean_bytes = raw_bytes[3:]
        else:
            clean_bytes = raw_bytes
        
        api_key = clean_bytes.decode('utf-8').strip()
        
        from elevenlabs.client import ElevenLabs
        from elevenlabs import save
        
        client = ElevenLabs(api_key=api_key)
        
        audio = client.generate(
            text=script_text,
            voice=voice,
            model="eleven_monolingual_v1"
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = f"F:\\AI_Oracle_Root\\scarify\\output\\audio\\{voice}_{timestamp}.mp3"
        os.makedirs(os.path.dirname(audio_filename), exist_ok=True)
        
        save(audio, audio_filename)
        print(f"✅ Real audio file: {audio_filename}")
        return audio_filename
        
    except Exception as e:
        print(f"❌ Audio failed: {e}")
        return None

def get_real_content(archetype):
    content = {
        "Rebel": "They told you to follow the rules. They said stay in line. But what if everything you've been taught is designed to keep you small? This is about breaking patterns and thinking differently. Real revolutionary content for real change.",
        "Mystic": "There are realms beyond what your senses perceive. Ancient wisdom meets modern truth in this exploration of consciousness. We're diving deep into reality, perception, and what it means to be awake in this world.",
        "Sage": "In an ocean of information, wisdom is the rarest treasure. We're cutting through the noise to find signal. This is about practical wisdom, critical thinking, and making better decisions in complex times."
    }
    return content.get(archetype, content["Mystic"])

# MAIN EXECUTION
archetype = "Mystic"
print(f"🎯 Generating real {archetype} content...")

script_content = get_real_content(archetype)
print(f"📝 Script: {len(script_content)} characters")

audio_file = generate_audio_elevenlabs(script_content)

if audio_file:
    print("")
    print("🎉 DEPLOYMENT SUCCESS!")
    print(f"   ✅ Real audio generated")
    print(f"   ✅ File: {os.path.basename(audio_file)}") 
    print(f"   ✅ Path: {audio_file}")
    print("")
    print("🔧 Next: Video generation with actual AI tools")
else:
    print("❌ Deployment failed at audio stage")
