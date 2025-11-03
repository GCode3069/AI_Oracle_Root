import os
from datetime import datetime

def generate_audio_elevenlabs(script_text, voice="Bella"):
    try:
        # Read ElevenLabs API key
        with open(r"F:\AI_Oracle_Root\scarify\config\credentials\elevenlabs_api.key", "rb") as f:
            raw_bytes = f.read()
        
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            clean_bytes = raw_bytes[3:]
        else:
            clean_bytes = raw_bytes
        
        api_key = clean_bytes.decode('utf-8').strip()
        print("✅ ElevenLabs API key loaded")
        
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
        print(f"✅ Audio generated: {audio_filename}")
        return audio_filename
        
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        return None

# Test content
script_content = "This is a real test of the SCARIFY deployment pipeline. No placeholders, no bullshit. We are building a working automated YouTube content system right now."

print("🚀 TESTING ELEVENLABS INTEGRATION")
audio_file = generate_audio_elevenlabs(script_content)

if audio_file:
    print("🎉 SUCCESS: Real audio file generated!")
    print(f"📍 Location: {audio_file}")
else:
    print("❌ FAILED: Check the error above")
