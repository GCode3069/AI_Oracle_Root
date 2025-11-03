"""
SCARIFY LINCOLN HORROR GENERATOR
Rips trending fear headlines, generates Lincoln-narrated gore videos
Integration module for SCARIFY Bootstrap System

Usage:
    python scarify_lincoln_horror.py --count 5
    python scarify_lincoln_horror.py --headline "Government shutdown chaos"
    
Requirements:
    pip install requests beautifulsoup4 elevenlabs runwayml anthropic
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
import random
import time

# Configuration
ROOT_DIR = Path(__file__).parent
OUTPUT_DIR = ROOT_DIR / "output"
VIDEOS_DIR = OUTPUT_DIR / "lincoln_horror"
AUDIO_DIR = OUTPUT_DIR / "lincoln_audio"
SCRIPTS_DIR = OUTPUT_DIR / "lincoln_scripts"

# Create directories
for directory in [VIDEOS_DIR, AUDIO_DIR, SCRIPTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# API Keys from environment
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
RUNWAY_API_KEY = os.getenv('RUNWAYML_API_SECRET')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# ============================================================================
# HEADLINE SCRAPING - Trending Fear Content
# ============================================================================

FEAR_SOURCES = {
    'chapman_survey': [
        "Corrupt government officials (69% fear)",
        "Cyber-terrorism threatens infrastructure (55.9% fear)",
        "Economic collapse imminent (58.2% fear)",
        "Authoritarian takeover of democracy",
        "Mass surveillance state expansion"
    ],
    'current_events_oct_2025': [
        "ICE raids spreading terror in communities",
        "Trump's Antifa fearmongering escalates",
        "Government shutdown enters 10th day",
        "Bitcoin crash: crypto's dead headlines flood media",
        "Foreclosure explosion: housing market collapse",
        "Nuclear tensions rise as diplomacy fails",
        "Climate disasters multiply as systems fail",
        "AI surveillance expands without oversight",
        "Debt ceiling crisis threatens economic meltdown",
        "Social security bankruptcy looms for millions"
    ],
    'evergreen_horror': [
        "Politicians feast while people starve",
        "Banks foreclose on families during holidays",
        "Corporate bailouts while workers lose pensions",
        "War profiteers grow rich on soldier blood",
        "Pharmaceutical companies price life-saving drugs beyond reach",
        "Prison industrial complex enslaves millions",
        "Wealth inequality reaches feudal levels",
        "Environmental destruction for corporate profit",
        "Healthcare denied while CEOs earn millions",
        "Democracy sold to highest bidder"
    ]
}

def get_trending_headlines(count=5):
    """
    Get trending fear-based headlines
    Combines scraped + curated content
    """
    print(f"🔪 Ripping {count} fear headlines...")
    
    # Combine all headline sources
    all_headlines = []
    for category, headlines in FEAR_SOURCES.items():
        all_headlines.extend(headlines)
    
    # Random sample
    selected = random.sample(all_headlines, min(count, len(all_headlines)))
    
    print(f"✅ Headlines acquired:")
    for i, headline in enumerate(selected, 1):
        print(f"   {i}. {headline}")
    
    return selected

def scrape_live_headlines():
    """
    Optional: Scrape live news headlines
    Returns list of fear-based headlines
    """
    # This is a placeholder for live scraping
    # In production, you'd scrape from news APIs or RSS feeds
    print("⚠️  Live scraping not implemented - using curated headlines")
    return []

# ============================================================================
# LINCOLN HORROR SCRIPT GENERATION
# ============================================================================

LINCOLN_GORE_PROMPTS = {
    'opening': [
        "The derringer's muzzle burns cold against my temple...",
        "Four score and seven nightmares ago...",
        "In the blood-soaked box at Ford's Theatre...",
        "My assassin's bullet enters, but never exits...",
        "The cursed relics pulse: Sic semper tyrannis..."
    ],
    'body_horror': [
        "jaw unhinged, ichor weeping from the wound",
        "fingers probe the skull cavity, dislodging clots",
        "bone fragments grind beneath searching hands",
        "grey matter spills like wax from a candle",
        "the entrance wound weeps blood that never dries",
        "vertebrae crack as the head lolls backward",
        "sinew tears as the neck refuses to support",
        "teeth chatter in the shattered jaw"
    ],
    'political_rage': [
        "They feast while you starve, just as my generals did",
        "Your democracy bleeds out in dark theatres of power",
        "The Union I died for rots from within",
        "Tyrants wear suits now, not crowns",
        "They murder freedom with legislation, not derringers",
        "The blood of the people oils the gears of their machines",
        "Every dollar they steal is a bullet to liberty's head",
        "They preserve not the Union, but their own purses"
    ],
    'closing': [
        "The stage is set. The box awaits. Sic semper tyrannis.",
        "History repeats, but the blood never dries.",
        "I died for this Union. You'll die for their greed.",
        "The derringer clicks empty. Your turn.",
        "From my grave, I watch. From theirs, they'll scream."
    ]
}

def generate_lincoln_script(headline):
    """
    Generate Lincoln horror narration for headline
    Uses Claude API for sophisticated generation
    """
    print(f"🩸 Generating Lincoln script for: {headline}")
    
    # If Claude API available, use it for sophisticated generation
    if ANTHROPIC_API_KEY:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            
            prompt = f"""Generate a 50-word horror narration in Abraham Lincoln's voice about this headline: "{headline}"

Style requirements:
- Lincoln speaks from death, jaw shattered from Booth's bullet
- Graphic body horror (weeping wounds, probing fingers, bone fragments)
- Righteous rage at corruption/injustice
- End with "Sic semper tyrannis" or similar
- 15-second read time (50 words max)

Make it visceral, angry, and horrifying."""

            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            script = message.content[0].text.strip()
            print(f"✅ Claude generated script")
            return script
            
        except Exception as e:
            print(f"⚠️  Claude failed: {e}, using template")
    
    # Fallback: Template-based generation
    opening = random.choice(LINCOLN_GORE_PROMPTS['opening'])
    body = random.choice(LINCOLN_GORE_PROMPTS['body_horror'])
    rage = random.choice(LINCOLN_GORE_PROMPTS['political_rage'])
    closing = random.choice(LINCOLN_GORE_PROMPTS['closing'])
    
    script = f"{opening} {headline}. {body}. {rage}. {closing}"
    
    # Truncate to ~50 words for 15s timing
    words = script.split()
    if len(words) > 55:
        script = ' '.join(words[:55]) + "..."
    
    print(f"✅ Template script generated ({len(words)} words)")
    return script

# ============================================================================
# ELEVENLABS LINCOLN VOICE CLONING
# ============================================================================

LINCOLN_VOICE_CONFIG = {
    'voice_id': '7aavy6c5cYIloDVj2JvH',  # Custom Lincoln clone or historical model
    'model': 'eleven_monolingual_v1',
    'stability': 0.6,  # Lower = more emotion/variance
    'similarity_boost': 0.8,  # Higher = closer to training voice
    'style': 0.7,  # Gravel/rasp intensity
}

def generate_lincoln_audio(script, voice_config=None):
    """
    Generate Lincoln's voice using ElevenLabs
    Falls back to SOVA TTS if ElevenLabs unavailable
    """
    print(f"🎙️  Generating Lincoln voice...")
    
    if not ELEVENLABS_API_KEY:
        print("⚠️  No ElevenLabs API key, falling back to gTTS")
        return generate_audio_fallback(script)
    
    try:
        from elevenlabs import generate, set_api_key, Voice, VoiceSettings
        
        set_api_key(ELEVENLABS_API_KEY)
        
        # Use custom config or default
        config = voice_config or LINCOLN_VOICE_CONFIG
        
        # Generate with emotional delivery
        audio = generate(
            text=script,
            voice=Voice(
                voice_id=config['voice_id'],
                settings=VoiceSettings(
                    stability=config['stability'],
                    similarity_boost=config['similarity_boost'],
                    style=config.get('style', 0.5)
                )
            ),
            model=config['model']
        )
        
        # Save audio
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_file = AUDIO_DIR / f"lincoln_{timestamp}.mp3"
        
        with open(audio_file, 'wb') as f:
            f.write(audio)
        
        print(f"✅ Lincoln voice generated: {audio_file.name}")
        return str(audio_file)
        
    except Exception as e:
        print(f"❌ ElevenLabs failed: {e}")
        return generate_audio_fallback(script)

def generate_audio_fallback(script):
    """Fallback to gTTS if ElevenLabs fails"""
    try:
        from gtts import gTTS
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_file = AUDIO_DIR / f"lincoln_fallback_{timestamp}.mp3"
        
        # Slow rate for gravitas
        tts = gTTS(text=script, lang='en', slow=True)
        tts.save(str(audio_file))
        
        print(f"✅ Fallback audio generated: {audio_file.name}")
        return str(audio_file)
        
    except Exception as e:
        print(f"❌ Audio generation failed completely: {e}")
        return None

# ============================================================================
# RUNWAYML HORROR VISUAL GENERATION
# ============================================================================

LINCOLN_VISUAL_PROMPTS = {
    'base': "Abraham Lincoln's ghost, Victorian horror, 1860s theatre box",
    'gore': [
        "shattered jaw hanging loose, bullet hole weeping black ichor",
        "skeletal fingers clutching bleeding head wound",
        "bone fragments visible through torn flesh",
        "blood-soaked formal attire, theatre curtains dripping",
        "eyes hollowed but glowing with rage",
        "fractured skull with brain matter exposed",
        "decomposed flesh revealing bone beneath",
        "viscera spilling from neck wound"
    ],
    'atmosphere': [
        "crimson fog, gothic shadows, gaslight flickering",
        "blood rain falling on theatre ruins",
        "haunted stage with hanging corpses",
        "demonic shadows dancing on walls",
        "cursed relics pulsing with dark energy",
        "ethereal screams visualized as smoke",
        "temporal distortion showing assassination loop",
        "hellfire consuming ornate theatre"
    ],
    'style': "cinematic horror, high contrast, practical effects aesthetic, 1080p, 24fps"
}

def generate_runway_video(script, headline):
    """
    Generate horror video with RunwayML Gen-3
    15 seconds, 1080p, optimized for vertical
    """
    print(f"🎬 Generating RunwayML horror visual...")
    
    if not RUNWAY_API_KEY:
        print("⚠️  No RunwayML API key, using fallback video")
        return generate_video_fallback(script, headline)
    
    try:
        # Construct horror prompt
        gore = random.choice(LINCOLN_VISUAL_PROMPTS['gore'])
        atmosphere = random.choice(LINCOLN_VISUAL_PROMPTS['atmosphere'])
        
        full_prompt = f"{LINCOLN_VISUAL_PROMPTS['base']}, {gore}, {atmosphere}. {LINCOLN_VISUAL_PROMPTS['style']}"
        
        print(f"   Prompt: {full_prompt[:100]}...")
        
        # RunwayML API call
        response = requests.post(
            'https://api.runwayml.com/v1/generate',
            headers={
                'Authorization': f'Bearer {RUNWAY_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'prompt': full_prompt,
                'duration': 15,
                'resolution': '1080p',
                'model': 'gen3-alpha',
                'aspect_ratio': '9:16'  # Vertical for Shorts
            },
            timeout=120
        )
        
        if response.status_code == 200:
            video_data = response.json()
            video_url = video_data.get('video_url')
            
            # Download video
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_file = VIDEOS_DIR / f"lincoln_runway_{timestamp}.mp4"
            
            video_response = requests.get(video_url)
            with open(video_file, 'wb') as f:
                f.write(video_response.content)
            
            print(f"✅ RunwayML video generated: {video_file.name}")
            return str(video_file)
        else:
            print(f"❌ RunwayML API error: {response.status_code}")
            print(f"   Response: {response.text}")
            return generate_video_fallback(script, headline)
            
    except Exception as e:
        print(f"❌ RunwayML failed: {e}")
        return generate_video_fallback(script, headline)

def generate_video_fallback(script, headline):
    """
    Fallback video generation using MoviePy
    Creates text-based horror aesthetic
    """
    try:
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
        
        print("🎬 Generating fallback video with MoviePy...")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_file = VIDEOS_DIR / f"lincoln_fallback_{timestamp}.mp4"
        
        # Dark blood-red background
        bg = ColorClip(size=(1080, 1920), color=(60, 0, 0), duration=15)
        
        # Title: Headline
        title = TextClip(
            headline.upper(),
            fontsize=70,
            color='white',
            font='Arial-Bold',
            size=(980, None),
            method='caption',
            align='center'
        )
        title = title.set_position(('center', 200)).set_duration(15)
        
        # Lincoln quote overlay
        quote = TextClip(
            script[:150] + "...",
            fontsize=50,
            color='#8B0000',
            font='Georgia',
            size=(980, None),
            method='caption',
            align='center'
        )
        quote = quote.set_position(('center', 800)).set_duration(15)
        
        # Attribution
        attribution = TextClip(
            "- ABRAHAM LINCOLN, FROM THE GRAVE",
            fontsize=40,
            color='darkgray',
            font='Arial'
        )
        attribution = attribution.set_position(('center', 1600)).set_duration(15)
        
        # Composite
        video = CompositeVideoClip([bg, title, quote, attribution])
        video.write_videofile(
            str(video_file),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        print(f"✅ Fallback video created: {video_file.name}")
        return str(video_file)
        
    except Exception as e:
        print(f"❌ Fallback video failed: {e}")
        return None

# ============================================================================
# VIDEO ASSEMBLY - Audio + Visual + Captions
# ============================================================================

def assemble_final_video(video_file, audio_file, script, headline):
    """
    Assemble final video with:
    - RunwayML/fallback visuals
    - ElevenLabs Lincoln audio
    - Timed captions
    - Glitch effects on key words
    """
    print(f"🎞️  Assembling final video...")
    
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
        
        # Load video and audio
        video = VideoFileClip(video_file)
        audio = AudioFileClip(audio_file)
        
        # Set audio
        video = video.set_audio(audio)
        
        # Add caption overlays (timed)
        # Extract key phrases for emphasis
        key_phrases = extract_key_phrases(script)
        
        clips = [video]
        
        for i, phrase in enumerate(key_phrases[:3]):  # Max 3 captions
            start_time = i * (audio.duration / 3)
            caption = TextClip(
                phrase.upper(),
                fontsize=80,
                color='red',
                font='Impact',
                stroke_color='black',
                stroke_width=3
            )
            caption = caption.set_position(('center', 1400))
            caption = caption.set_start(start_time).set_duration(3)
            clips.append(caption)
        
        # Composite final video
        final = CompositeVideoClip(clips)
        
        # Export
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = VIDEOS_DIR / f"lincoln_final_{timestamp}.mp4"
        
        final.write_videofile(
            str(output_file),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='5000k',
            verbose=False,
            logger=None
        )
        
        print(f"✅ Final video assembled: {output_file.name}")
        return str(output_file)
        
    except Exception as e:
        print(f"❌ Assembly failed: {e}")
        # Return original video if assembly fails
        return video_file

def extract_key_phrases(script):
    """Extract 2-3 word impactful phrases for captions"""
    # Target words that carry emotional weight
    keywords = ['blood', 'death', 'tyrant', 'corrupt', 'feast', 'starve', 
                'murder', 'bullet', 'skull', 'bone', 'grave', 'scream']
    
    words = script.split()
    phrases = []
    
    for i, word in enumerate(words):
        clean_word = word.lower().strip('.,!?')
        if clean_word in keywords and i < len(words) - 1:
            # Take 2-3 words around keyword
            start = max(0, i-1)
            end = min(len(words), i+2)
            phrase = ' '.join(words[start:end])
            phrases.append(phrase)
    
    return phrases[:3] if phrases else [script.split('.')[0]]

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def generate_lincoln_horror_video(headline=None):
    """
    Complete pipeline: Headline → Script → Audio → Video → Assembly
    """
    print(f"\n{'='*70}")
    print(f"🩸 ABRAHAM LINCOLN HORROR GENERATOR")
    print(f"{'='*70}\n")
    
    # Step 1: Get headline
    if not headline:
        headlines = get_trending_headlines(1)
        headline = headlines[0]
    
    print(f"\n📰 Headline: {headline}\n")
    
    # Step 2: Generate script
    script = generate_lincoln_script(headline)
    
    # Save script
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    script_file = SCRIPTS_DIR / f"lincoln_{timestamp}.txt"
    script_file.write_text(f"HEADLINE: {headline}\n\nSCRIPT:\n{script}")
    print(f"📝 Script saved: {script_file.name}\n")
    
    # Step 3: Generate audio
    audio_file = generate_lincoln_audio(script)
    if not audio_file:
        print("❌ Audio generation failed, aborting")
        return None
    print()
    
    # Step 4: Generate video
    video_file = generate_runway_video(script, headline)
    if not video_file:
        print("❌ Video generation failed, aborting")
        return None
    print()
    
    # Step 5: Assemble final
    final_video = assemble_final_video(video_file, audio_file, script, headline)
    
    print(f"\n{'='*70}")
    print(f"✅ LINCOLN HORROR VIDEO COMPLETE")
    print(f"{'='*70}")
    print(f"📹 Video: {Path(final_video).name}")
    print(f"🎵 Audio: {Path(audio_file).name}")
    print(f"📝 Script: {script_file.name}")
    print(f"📊 Size: {Path(final_video).stat().st_size / 1_000_000:.2f}MB")
    print()
    
    return {
        'video': final_video,
        'audio': audio_file,
        'script': str(script_file),
        'headline': headline,
        'script_text': script
    }

def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Lincoln Horror Videos')
    parser.add_argument('--count', type=int, default=1, help='Number of videos to generate')
    parser.add_argument('--headline', type=str, help='Specific headline to use')
    
    args = parser.parse_args()
    
    if args.headline:
        # Single video with custom headline
        result = generate_lincoln_horror_video(args.headline)
        if result:
            print(f"✅ Generated: {result['video']}")
    else:
        # Generate multiple videos
        headlines = get_trending_headlines(args.count)
        results = []
        
        for i, headline in enumerate(headlines, 1):
            print(f"\n\n{'#'*70}")
            print(f"VIDEO {i}/{args.count}")
            print(f"{'#'*70}")
            
            result = generate_lincoln_horror_video(headline)
            if result:
                results.append(result)
            
            if i < len(headlines):
                print(f"\n⏳ Waiting 5 seconds before next video...")
                time.sleep(5)
        
        # Summary
        print(f"\n\n{'='*70}")
        print(f"🎬 BATCH COMPLETE: {len(results)}/{args.count} videos generated")
        print(f"{'='*70}")
        for i, r in enumerate(results, 1):
            print(f"{i}. {Path(r['video']).name}")
        print()

if __name__ == "__main__":
    main()

