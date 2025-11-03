import os
import random
from datetime import datetime

print("🚀 SCARIFY LOCAL DEPLOYMENT PIPELINE")
print("=====================================")

def generate_audio_elevenlabs(script_text, voice="Bella"):
    """Generate audio using ElevenLabs - our working API"""
    try:
        # Read ElevenLabs API key using binary method
        with open(r"F:\AI_Oracle_Root\scarify\config\credentials\elevenlabs_api.key", "rb") as f:
            raw_bytes = f.read()
        
        if raw_bytes.startswith(b'\xef\xbb\xbf'):
            clean_bytes = raw_bytes[3:]
        else:
            clean_bytes = raw_bytes
        
        api_key = clean_bytes.decode('utf-8').strip()
        print(f"✅ ElevenLabs API key loaded (length: {len(api_key)})")
        
        from elevenlabs import generate, save
        from elevenlabs import set_api_key
        
        set_api_key(api_key)
        
        # Use the script text
        audio_text = script_text
        
        audio = generate(
            text=audio_text,
            voice=voice,
            model="eleven_monolingual_v1"
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = f"F:\\AI_Oracle_Root\\scarify\\output\\audio\\{voice}_{timestamp}.mp3"
        
        save(audio, audio_filename)
        print(f"✅ Audio generated: {audio_filename}")
        return audio_filename
        
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        return None

def create_content(archetype="Mystic"):
    """Create content without API calls"""
    content_templates = {
        "Rebel": """
        BREAKING THE CHAINS: Why Everything You Know Is Wrong
        
        [HOOK]
        What if I told you that every rule you follow is designed to keep you small?
        
        [INTRODUCTION]
        We live in a world of systems and structures that want compliance, not creativity.
        But true innovation comes from breaking patterns, not following them.
        
        [MAIN CONTENT]
        1. The Conformity Trap: How society programs obedience
        2. Revolutionary Thinking: Seeing beyond the matrix
        3. Practical Rebellion: Small acts of defiance that change everything
        
        [CONCLUSION]
        The most dangerous thought is the one you haven't thought yet.
        """,
        
        "Mystic": """
        THE AWAKENING: Consciousness Beyond Reality
        
        [HOOK]
        There are more dimensions to existence than your physical senses can perceive.
        
        [INTRODUCTION]  
        Ancient mystics and modern physicists agree: reality is not what it seems.
        
        [MAIN CONTENT]
        1. The Veil of Perception: How we filter reality
        2. Spiritual Technologies: Meditation, intuition, and beyond
        3. The Collective Awakening: Humanity's next evolutionary step
        
        [CONCLUSION]
        The universe is consciousness experiencing itself.
        """,
        
        "Sage": """
        WISDOM IN THE AGE OF INFORMATION OVERLOAD
        
        [HOOK]
        In a world drowning in data, true wisdom is the rarest currency.
        
        [INTRODUCTION]
        Knowledge is accumulating at unprecedented rates, but wisdom seems scarcer than ever.
        
        [MAIN CONTENT]
        1. The Signal vs Noise Problem: Filtering what matters
        2. Timeless Principles: What the ancients knew that we've forgotten  
        3. Applied Wisdom: Making better decisions in complex times
        
        [CONCLUSION]
        The wise don't know all the answers, but they ask the right questions.
        """
    }
    
    return content_templates.get(archetype, content_templates["Mystic"])

# MAIN EXECUTION
archetype = "Mystic"  # Default archetype

print(f"🎯 Generating content for: {archetype}")
print("📝 Creating script...")

script_content = create_content(archetype)
print(f"✅ Script created ({len(script_content)} characters)")

print("🎵 Generating audio with ElevenLabs...")
audio_file = generate_audio_elevenlabs(script_content)

if audio_file:
    print("🎉 DEPLOYMENT SUCCESSFUL!")
    print(f"   Audio file: {audio_file}")
    print("   Next: Video generation with Pika/RunwayML")
else:
    print("❌ Audio generation failed")
