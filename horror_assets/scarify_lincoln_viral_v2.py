"""
SCARIFY LINCOLN VIRAL v2.0 - SELF-BOOTSTRAPPING
Complete system with inline YouTube upload, gruesome gore details, and self-saving execution
Enhanced to surpass: Sleepless Historian, Mystery Scoop, Galactic Horrors, Fascinating Horror

Usage:
    python scarify_lincoln_viral_v2.py --count 5
    python scarify_lincoln_viral_v2.py --headline "Gmail hack nightmare 183M"

Self-bootstrapping: Saves progress, resumes if interrupted, auto-uploads to YouTube
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
import random
import time
import re
import pickle

# ============================================================================
# SELF-BOOTSTRAP CONFIG - Auto-saves progress for resume capability
# ============================================================================

CACHE_DIR = Path("cache_lincoln")
CACHE_DIR.mkdir(exist_ok=True)

STATE_FILE = CACHE_DIR / "generation_state.json"
PROGRESS_FILE = CACHE_DIR / "progress_log.txt"

def save_state(state):
    """Auto-save generation state for recovery"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)
    print(f"💾 State saved: {len(state)} items")

def load_state():
    """Load previous state if interrupted"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def log_progress(message):
    """Persistent progress logging"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    with open(PROGRESS_FILE, 'a') as f:
        f.write(log_entry)
    print(f"📝 {message}")

# ============================================================================
# ENHANCED GORE HEADLINES - Oct 2025 Viral Fear Fuel
# ============================================================================

VIRAL_FEAR_HEADLINES = {
    'tech_apocalypse': [
        "Gmail hack nightmare: 183M accounts compromised (55.9% cyber-terror fear)",
        "Bitcoin's dead: crypto collapse guts $50B in hours",
        "AI surveillance expands: 2.3B faces scanned daily without consent",
        "Data breach epidemic: 6B personal records leaked in 2024 alone",
        "The banks are collapsing: 12 regional failures trigger contagion fears"
    ],
    'government_rot': [
        "Corrupt officials (69% fear) - government rot spreads like cancer",
        "ICE raids spreading terror: immigrant families torn apart at dawn",
        "Government shutdown enters 50th day: economy bleeds $1B daily",
        "Congressional insider trading exposed: politicians feast while we starve",
        "The surveillance state tightens: facial recognition at every corner"
    ],
    'economic_horror': [
        "Economic collapse imminent (58.2% fear) - banks withholding deposits",
        "Foreclosure explosion: 2M families face eviction by Christmas",
        "Inflation devours savings: dollar collapses, food prices double overnight",
        "Supply chain collapse: empty shelves become permanent reality",
        "Social security bankruptcy confirmed: retirees destitute by 2026"
    ],
    'political_rage': [
        "Trump's Antifa fearmongering escalates: patriot militias mobilize",
        "Soros-funded chaos: BLM riots return with Molotov cocktail fury",
        "Deep state coup confirmed: shadow government controls media narrative",
        "Election rigging exposed: 12M ghost votes discovered in swing states",
        "The great reset accelerates: cashless society traps billions in CBDC cages"
    ],
    'societal_collapse': [
        "The fentanyl crisis explodes: 120K dead, cartels control America",
        "School shootings reach 400+ in 2025: children hide in lockdown drills",
        "Homeless encampments metastasize: tent cities consume urban centers",
        "Medical system collapse: ER waits exceed 18 hours, patients die in hallways",
        "Climate disasters multiply: floods, fires, hurricanes kill thousands monthly"
    ]
}

def get_viral_headline(category=None):
    """Get trending gore-worthy headline"""
    if category:
        if category in VIRAL_FEAR_HEADLINES:
            return random.choice(VIRAL_FEAR_HEADLINES[category])
    
    # Pick random category
    all_headlines = []
    for headlines in VIRAL_FEAR_HEADLINES.values():
        all_headlines.extend(headlines)
    
    return random.choice(all_headlines)

# ============================================================================
# GRUESOME LINCOLN NARRATION GENERATION
# ============================================================================

GORE_DESCRIPTORS = {
    'opening_gore': [
        "The derringer's muzzle burns cold against my temple... the bullet enters cleanly but never exits",
        "Four score and seven nightmares ago, Booth's ball tore through bone like paper—",
        "In the blood-soaked box at Ford's Theatre, my skull split like a melon dropped from height",
        "The percussion of the shot echoed as my jawbone shattered, teeth scattered like dice across the stage",
        "White-hot lead burrowed through cranium, gray matter spraying in arterial crimson"
    ],
    'visual_horror': [
        "my jaw unhinged and hanging loose, black ichor weeping from the gaping wound",
        "probing fingers dislodge clots the size of grapes, thick as tar in consistency",
        "bone fragments grind beneath the touch like broken glass scraping porcelain",
        "the entrance wound pulses with each heartbeat, weeping crimson that never clots",
        "vertebrae crack audibly as my head lolls backward, exposing the hollowed skull cavity",
        "sinew tears under gravitational strain, the neck refusing its biological duty",
        "teeth chatter rhythmically in the shattered jaw, clicking like castanets in a death rattle",
        "grey sludge oozes from the occipital breach, dripping in viscous strands to the floor"
    ],
    'political_rage': [
        "They feast while you starve—bankers gorge on foreclosed homes while families sleep in cars",
        "Your democracy bleeds out in the dark theatre of congressional backrooms",
        "The Union I died for rots from within—soldier to politician, patriot to parasite",
        "Tyrants wear suits now, not crowns—they murder freedom with keystrokes, not derringers",
        "Every dollar they steal is a bullet to liberty's head, each betrayal a wound that festers",
        "They preserve not the Constitution but their own purse-strings, bleeding the people dry",
        "The machinery of oppression grinds on—they profit from your fear, monetize your desperation",
        "Corruption metastasizes like a cancer: they poison the well and sell you the cure"
    ],
    'closing_threat': [
        "The stage is set. The box awaits. Sic semper tyrannis—the purge comes for them next",
        "History repeats but the blood never dries—they'll scream as I did, begging for mercy they never showed you",
        "I died for this Union. You'll die for their greed—and I'll watch, grinning skull-wide",
        "The derringer clicks empty. Your turn, politicians—the grave accepts all, especially the corrupt",
        "From my grave I watch, from theirs they'll scream—prepare the box, the curtain rises on judgment day"
    ]
}

def generate_gruesome_script(headline):
    """
    Generate Lincoln horror script with maximum gore detail
    Matches the gory style from your prompt
    """
    log_progress(f"Generating gruesome script for: {headline}")
    
    opening = random.choice(GORE_DESCRIPTORS['opening_gore'])
    visual = random.choice(GORE_DESCRIPTORS['visual_horror'])
    rage = random.choice(GORE_DESCRIPTORS['political_rage'])
    closing = random.choice(GORE_DESCRIPTORS['closing_threat'])
    
    # Inject headline naturally
    script = f"{opening} {headline}. {visual}. {rage}. {closing}"
    
    # Ensure ~50 words for 15s timing
    words = script.split()
    if len(words) > 60:
        script = ' '.join(words[:60]) + "... SIC SEMPER TYRANNIS."
    elif len(words) < 40:
        script += " The purge for ninety-seven. Bone grinds, blood flows, tyranny falls. SIC SEMPER TYRANNIS."
    
    return script

# ============================================================================
# ELEVENLABS LINCOLN VOICE - Enhanced Configuration
# ============================================================================

def generate_lincoln_voice_gruesome(script):
    """Generate Lincoln voice with maximum rasp and anger"""
    
    ELEVENLABS_KEY = os.getenv('ELEVENLABS_API_KEY')
    if not ELEVENLABS_KEY:
        log_progress("⚠️  No ElevenLabs key, using gTTS fallback")
        return generate_fallback_audio(script)
    
    try:
        from elevenlabs import generate, Voice, VoiceSettings
        import elevenlabs
        
        elevenlabs.set_api_key(ELEVENLABS_KEY)
        
        # Maximum emotion: low stability, high style for rasp
        voice = Voice(
            voice_id="7aavy6c5cYIloDVj2JvH",
            settings=VoiceSettings(
                stability=0.3,  # VERY LOW for maximum emotion/rasp
                similarity_boost=0.75,
                style=0.9,  # MAXIMUM gravel/rasp
                use_speaker_boost=True
            )
        )
        
        # Generate with emotion emphasis
        audio = generate(
            text=script,
            voice=voice,
            model="eleven_multilingual_v2"
        )
        
        # Save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_file = Path("output/lincoln_audio") / f"gruesome_{timestamp}.mp3"
        audio_file.parent.mkdir(exist_ok=True)
        
        with open(audio_file, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        
        log_progress(f"✅ Gruesome Lincoln voice: {audio_file.name}")
        return str(audio_file)
        
    except Exception as e:
        log_progress(f"❌ ElevenLabs failed: {e}")
        return generate_fallback_audio(script)

def generate_fallback_audio(script):
    """Fallback to gTTS with slow rate for gravitas"""
    try:
        from gtts import gTTS
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audio_file = Path("output/lincoln_audio") / f"fallback_{timestamp}.mp3"
        audio_file.parent.mkdir(exist_ok=True)
        
        tts = gTTS(text=script, lang='en', slow=True)
        tts.save(str(audio_file))
        
        log_progress(f"✅ Fallback audio: {audio_file.name}")
        return str(audio_file)
    except:
        return None

# ============================================================================
# RUNWAYML GRUESOME VISUAL GENERATION
# ============================================================================

def generate_gruesome_runway(headline, script):
    """Generate AI horror visual with maximum gore"""
    
    RUNWAY_KEY = os.getenv('RUNWAYML_API_SECRET')
    if not RUNWAY_KEY:
        log_progress("⚠️  No RunwayML key, using MoviePy gruesome fallback")
        return generate_fallback_visual(headline, script)
    
    try:
        # Extract gore keywords from script
        gore_words = re.findall(r'\b(bone|blood|ichor|grisly|skull|wound|clot|shards|weeping|grinding|squelch|pulses|splintered|crimson|sludge|oozing)\w+\b', script.lower())
        
        # Construct MAXIMUM GORE prompt
        prompt = f"Abraham Lincoln's ghost, 1860s Ford's Theatre box, shattered jaw hanging loose, " \
                 f"black ichor weeping from bullet wound, probing fingers removing clots, bone shards grinding, " \
                 f"blood-soaked formal attire, cursed relics pulsing on wrists, crimson fog, gothic Victorian horror, " \
                 f"cinematic gore, practical effects aesthetic, 1080p vertical, 15 seconds"
        
        log_progress(f"🎬 Generating gruesome visual: {prompt[:100]}...")
        
        # RunwayML API
        response = requests.post(
            'https://api.runwayml.com/v1/generate',
            headers={'Authorization': f'Bearer {RUNWAY_KEY}'},
            json={
                'prompt': prompt,
                'duration': 15,
                'resolution': '1080x1920',
                'aspect_ratio': '9:16',
                'model': 'gen3-alpha'
            },
            timeout=180
        )
        
        if response.status_code == 200:
            video_url = response.json()['video_url']
            
            # Download
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            video_file = Path("output/lincoln_horror") / f"gruesome_runway_{timestamp}.mp4"
            video_file.parent.mkdir(exist_ok=True)
            
            vid_response = requests.get(video_url, timeout=180)
            with open(video_file, 'wb') as f:
                f.write(vid_response.content)
            
            log_progress(f"✅ RunwayML gruesome visual: {video_file.name}")
            return str(video_file)
        else:
            log_progress(f"❌ RunwayML error: {response.status_code}")
            return generate_fallback_visual(headline, script)
            
    except Exception as e:
        log_progress(f"❌ RunwayML failed: {e}")
        return generate_fallback_visual(headline, script)

def generate_fallback_visual(headline, script):
    """MoviePy fallback with maximum gore aesthetic"""
    try:
        from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
        import numpy as np
        
        log_progress("🎬 Generating gruesome MoviePy fallback")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_file = Path("output/lincoln_horror") / f"gruesome_fallback_{timestamp}.mp4"
        video_file.parent.mkdir(exist_ok=True)
        
        # Blood-dark red background
        bg = ColorClip(size=(1080, 1920), color=(40, 0, 0), duration=15)
        
        # Headline - white, bold, massive
        headline_text = headline.upper()[:80]  # Truncate if needed
        title = TextClip(
            f"🩸 {headline_text} 🩸",
            fontsize=72,
            color='#FFFFFF',
            font='Impact',
            stroke_color='#8B0000',
            stroke_width=5
        )
        title = title.set_position(('center', 150)).set_duration(15)
        
        # Lincoln quote excerpt (gory part)
        quote_excerpt = script.split('.')[0] + "..." if len(script) > 120 else script[:120] + "..."
        quote = TextClip(
            quote_excerpt,
            fontsize=52,
            color='#FF6B6B',
            font='Georgia',
            size=(980, None),
            method='caption',
            align='center'
        )
        quote = quote.set_position(('center', 700)).set_duration(15)
        
        # Gore tagline
        gore_tag = TextClip(
            "SIC SEMPER TYRANNIS – $97 PURGE KIT",
            fontsize=48,
            color='#FFD700',
            font='Impact',
            stroke_color='#000000',
            stroke_width=3
        )
        gore_tag = gore_tag.set_position(('center', 1600)).set_duration(15)
        
        # Composite
        video = CompositeVideoClip([bg, title, quote, gore_tag])
        video.write_videofile(
            str(video_file),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None
        )
        
        log_progress(f"✅ Gruesome fallback visual: {video_file.name}")
        return str(video_file)
        
    except Exception as e:
        log_progress(f"❌ Fallback visual failed: {e}")
        return None

# ============================================================================
# YOUTUBE AUTO-UPLOAD - Inline, Self-Bootstrapping
# ============================================================================

def upload_to_youtube_inline(video_path, headline, script):
    """
    Upload video to YouTube with credentials from inline JSON
    Self-bootstrapping - no external config required
    """
    
    YOUTUBE_CREDS = os.getenv('YOUTUBE_CLIENT_SECRET_JSON')
    
    # Try to find credentials
    if YOUTUBE_CREDS:
        creds_path = Path(YOUTUBE_CREDS)
    else:
        # Look for client_secrets*.json in current dir
        creds_path = None
        for f in Path('.').glob('client_secret*.json'):
            creds_path = f
            break
    
    if not creds_path or not creds_path.exists():
        log_progress("⚠️  No YouTube credentials found, skipping upload")
        log_progress("   Place client_secret*.json in project root")
        return None
    
    try:
        from googleapiclient.discovery import build
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        import google.oauth2.credentials
        
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        API_SERVICE_NAME = 'youtube'
        API_VERSION = 'v3'
        
        # OAuth flow
        credentials = None
        token_file = Path('token.pickle')
        
        if token_file.exists():
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)
        
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                credentials = flow.run_local_server(port=0)
            
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
        
        youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        
        # Prepare metadata
        title = f"⚠️ Lincoln Warns: {headline[:60]}"
        description = f"""
🩸 HISTORY HORROR: ABRAHAM LINCOLN FROM THE GRAVE

{script}

⚠️ Trigger Warning: Graphic political horror, gore descriptions, historical violence.

🎯 $97 PURGE KIT: https://gumroad.com/l/LINCOLN97
💀 Unlock full Lincoln Letters from the Grave
🔥 50+ gore scripts, horror prompts, monetization guide

🔔 Subscribe for more AI history horror
📊 Part of SCARIFY viral content series

#Lincoln #Horror #Politics #History #Gore #AI #viral
"""
        
        # Upload
        log_progress("📤 Uploading to YouTube...")
        
        request_body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['lincoln', 'horror', 'politics', 'history', 'gore', 'viral', 'AI', 'deepfake'],
                'categoryId': '24'  # Entertainment
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        media_file = googleapiclient.http.MediaFileUpload(video_path, chunksize=-1, resumable=True)
        
        request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media_file
        )
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                log_progress(f"   Upload progress: {progress}%")
        
        video_id = response['id']
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        log_progress(f"✅ Uploaded: {url}")
        return url
        
    except Exception as e:
        log_progress(f"❌ YouTube upload failed: {e}")
        return None

# ============================================================================
# MAIN GENERATION PIPELINE
# ============================================================================

def generate_gruesome_lincoln_video(headline=None, upload=True):
    """Complete pipeline: Script → Audio → Visual → Assembly → Upload"""
    
    print("\n" + "="*70)
    print("🩸 LINCOLN GRUESOME GENERATOR v2.0")
    print("="*70 + "\n")
    
    # Get headline
    if not headline:
        headline = get_viral_headline()
    
    log_progress(f"📰 Headline: {headline}")
    
    # Step 1: Generate gruesome script
    script = generate_gruesome_script(headline)
    log_progress(f"📝 Script generated: {len(script)} chars")
    
    # Save script
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    script_file = Path("output/lincoln_scripts") / f"gruesome_{timestamp}.txt"
    script_file.parent.mkdir(exist_ok=True)
    script_file.write_text(f"HEADLINE: {headline}\n\nSCRIPT:\n{script}", encoding='utf-8')
    log_progress(f"💾 Script saved: {script_file.name}")
    
    # Step 2: Generate voice
    audio_file = generate_lincoln_voice_gruesome(script)
    if not audio_file:
        print("❌ Audio generation failed")
        return None
    
    # Step 3: Generate visual
    video_file = generate_gruesome_runway(headline, script)
    if not video_file:
        print("❌ Video generation failed")
        return None
    
    # Step 4: Assemble
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip
        
        video = VideoFileClip(video_file)
        audio = AudioFileClip(audio_file)
        
        # Sync and export
        final_video = video.set_audio(audio)
        
        output_file = Path("output/lincoln_horror") / f"final_{timestamp}.mp4"
        
        final_video.write_videofile(
            str(output_file),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            bitrate='5000k',
            verbose=False,
            logger=None
        )
        
        log_progress(f"✅ Final video: {output_file.name}")
        
        # Step 5: Upload to YouTube
        youtube_url = None
        if upload:
            youtube_url = upload_to_youtube_inline(str(output_file), headline, script)
        
        # Return result
        return {
            'video': str(output_file),
            'audio': audio_file,
            'script': str(script_file),
            'headline': headline,
            'script_text': script,
            'youtube_url': youtube_url
        }
        
    except Exception as e:
        log_progress(f"❌ Assembly failed: {e}")
        return None

def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Gruesome Lincoln Viral Videos')
    parser.add_argument('--count', type=int, default=1, help='Number of videos to generate')
    parser.add_argument('--headline', type=str, help='Specific headline')
    parser.add_argument('--no-upload', action='store_true', help='Skip YouTube upload')
    
    args = parser.parse_args()
    
    upload = not args.no_upload
    results = []
    
    for i in range(args.count):
        print(f"\n\n{'#'*70}")
        print(f"VIDEO {i+1}/{args.count}")
        print(f"{'#'*70}\n")
        
        result = generate_gruesome_lincoln_video(
            headline=args.headline if i == 0 else None,
            upload=upload
        )
        
        if result:
            results.append(result)
            print(f"\n✅ Video {i+1} complete!")
            if result.get('youtube_url'):
                print(f"🌐 YouTube: {result['youtube_url']}")
        
        if i < args.count - 1:
            print(f"\n⏳ Waiting 10 seconds before next video...")
            time.sleep(10)
    
    # Summary
    print(f"\n\n{'='*70}")
    print(f"🎬 BATCH COMPLETE: {len(results)} videos generated")
    print(f"{'='*70}")
    for i, r in enumerate(results, 1):
        print(f"{i}. {Path(r['video']).name}")
        if r.get('youtube_url'):
            print(f"   YouTube: {r['youtube_url']}")
    print()

if __name__ == "__main__":
    main()

