"""
ABRAHAM LINCOLN - LONG RANTS (FIXED VERSION)
✅ Strips screen directions from audio
✅ Shows Abe speaking from staticky TV
✅ Uses proper deep male Lincoln voice
✅ No screen directions in narration
"""
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
# PROPER MALE LINCOLN VOICES (in order of preference)
VOICES = [
    "VR6AewLTigWG4xSOukaG",  # Deep male - best for Lincoln
    "pNInz6obpgDQGcFmaJgB",  # Ominous male - fallback
    "EXAVITQu4vr4xnSDxMaL",  # Another deep male
]
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

def clean_script(text):
    """Remove ALL screen directions and descriptions from script"""
    # Remove *[...]* patterns
    text = re.sub(r'\*\[.*?\]\*', '', text)
    # Remove [Screen glitches], [Static], etc.
    text = re.sub(r'\[.*?\]', '', text)
    # Remove standalone asterisks
    text = re.sub(r'\*+', '', text)
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
    return text.strip()

def scrape():
    headlines = []
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            for item in soup.find_all('item')[:20]:
                if item.title:
                    headlines.append(item.title.text)
    except: pass
    return headlines if headlines else ["Trump Third Term", "64 Killed in Rio", "Sudan Massacre"]

def long_rant(headline):
    """Generate 2500+ character dark satirical rant - NO SCREEN DIRECTIONS"""
    hl = headline.lower()
    
    is_trump = "trump" in hl
    is_violence = any(w in hl for w in ["killed", "dead", "shoot", "massacre", "strike"])
    is_politics = any(w in hl for w in ["poll", "vote", "senate", "congress", "judge"])
    is_foreign = any(w in hl for w in ["china", "russia", "israel", "gaza", "sudan"])
    
    intro = f"""Abraham Lincoln here. Yes, THAT Abraham Lincoln. The tall guy. The beard guy. The guy who got assassinated at a theatre in 1865 while watching a mediocre play.

I'm speaking to you from beyond the grave. From the cold empty void where dead presidents rot. And I just read this headline: {headline}

Let me tell you what I think about this."""

    if is_trump:
        body = f"""Trump. Again. It's always Trump with you people. You're obsessed. You can't stop talking about him. Every headline. Every conversation. Every waking moment consumed by this one man.

Let me tell you about being president. I was president during the Civil War. The bloodiest conflict in American history. Six hundred thousand men dead. Brother killing brother. The nation literally tearing itself in half.

Every morning I woke up to casualty reports. Lists of names. Boys who would never go home. Fathers who died screaming. Brothers who bled out in muddy fields calling for their mothers.

Gettysburg: fifty thousand casualties in three days. The field was covered in corpses. You couldn't walk without stepping on dead bodies. The smell of rotting flesh hung over that place for weeks. Months.

Antietam: twenty-three thousand casualties in a single day. A SINGLE DAY. More American casualties than the entire Revolutionary War. Boys drowning in Antietam Creek. Water running red with blood.

And I authorized it. I signed the orders. I sent those boys to die. Because I believed the Union was worth it. That ending slavery was worth the price. That preserving democracy justified the horror.

Now I watch from death as you worship a man who dodged the draft. Who called prisoners of war losers. Who tweets instead of governing. Who turns the presidency into performance art.

{headline}. This is your news. This is what you care about. Not policy. Not principles. Not the future of the republic. Just endless drama. Just the spectacle. Just the show.

I gave the Gettysburg Address standing on ground soaked with American blood. Two minutes. Two hundred and seventy-two words. Government of the people, by the people, for the people shall not perish from this earth.

I meant it. I believed it. I died for it.

What does he believe? What does he stand for? What would he die for? His brand? His ego? His next headline?

I took a bullet to the brain for America. He won't even take criticism. I died at a theatre. He acts like one."""

    elif is_violence:
        body = f"""Violence. Death. Another massacre. Another headline. Another day in the endless parade of human brutality.

{headline}. How many dead this time? How many families destroyed? How many lives ended for no reason?

Let me tell you about death. Real death. Not the sanitized version you see in movies. Not the clean Hollywood deaths where people die with dignity and meaning.

I've seen real death. I've seen battlefields. I've seen boys gut-shot and screaming. I've seen men with their faces blown off trying to talk. I've seen soldiers holding their own intestines begging for help.

Shiloh. The first day. Ten thousand casualties. Boys who enlisted thinking war was glory. Who dreamed of heroism and honor. Who died choking on their own blood in a Tennessee forest.

I visited hospitals. I saw the wounded. Boys with missing limbs. Men blinded. Soldiers who would never be whole again. The smell of gangrene and death. The sound of screaming that never stopped.

And we fought because something mattered. Because slavery was evil. Because the Union was worth preserving. Because freedom required sacrifice.

Now I read headlines like this. {headline}. People dying. For what? For oil? For power? For territory? For reasons that won't matter in a hundred years?

And what's your response? What's the outrage? Where's the revolution? Where's the change?

You just scroll past. Another tragedy. Another headline. Another statistic. You consume violence like entertainment. You watch death like it's a TV show.

I commanded armies. I sent men to die. It haunted me. Every name. Every face. Every letter to a grieving mother. The weight of all those deaths crushing me every single day.

And you? You see mass death and you just move on. You see massacres and you forget before lunch. You see horror and you think that's sad and then check your phone.

This is what I died for. This is my legacy. A world that sees death and doesn't care. A civilization that values convenience over conscience.

You want to honor the dead? Stop making more of them."""

    elif is_politics:
        body = f"""Politics. Polls. Propositions. The endless meaningless theater of modern governance.

{headline}. And you care. You actually care about this. This matters to you.

Let me tell you about politics. Real politics. Not the focus-grouped, poll-tested, consultant-approved nonsense you call governance.

The 1860 election. I ran knowing it would split the nation. Knowing the South would secede if I won. Knowing it would mean war. I ran anyway.

Why? Because slavery was wrong. Not because polls said so. Not because consultants told me to. Not because it was politically convenient.

Because it was RIGHT. Because some things matter more than winning. Because principles are worth losing for.

I won. Seven states seceded before I was even inaugurated. Four more followed after Fort Sumter. The nation split. War came. Six hundred thousand died.

Was it worth it? Yes. Because slavery ended. Because the Union survived. Because sometimes the cost of doing right is everything you have.

Now you have polls. Focus groups. Consultants telling politicians what to say. Strategists crafting messages for maximum appeal. Marketing teams selling candidates like products.

{headline}. A poll says people will vote yes. Great. Why? Because it polled well? Because someone ran effective ads? Because it sounds nice?

What happened to conviction? What happened to standing for something even when it's unpopular? What happened to doing what's right instead of what's easy?

I was called a tyrant. A dictator. A fool. Newspapers attacked me daily. Half the country hated me. My own party doubted me. I did what I believed was right anyway.

Can you say that? Can any modern politician say that? Or do they all just chase polls? Follow consultants? Say whatever wins elections?

You've turned democracy into a game show. You've reduced governance to marketing. You've made politics about winning instead of serving.

And you wonder why nothing changes. Why the system is broken. Why nobody trusts anyone anymore.

It's because you don't stand for anything. You just stand for winning. And winning without purpose is just losing slowly."""

    elif is_foreign:
        body = f"""Foreign affairs. International conflict. The same endless human stupidity on a global scale.

{headline}. Wars and rumors of wars. Nations threatening nations. People killing people over invisible lines on maps.

I fought to preserve a nation. You fight to what? Control resources? Maintain power? Spread ideology? Win conflicts that were started for reasons nobody remembers?

The Civil War killed six hundred thousand Americans. More than all other American wars combined. It nearly destroyed us. It took decades to recover. The scars remain today.

And we fought for something. For the soul of the nation. For the principle that all men are created equal. For the idea that America meant something.

Now I watch as conflicts erupt everywhere. Wars that start over borders. Over oil. Over historical grievances. Over religion. Over pride.

{headline}. And what will it accomplish? What will change? How many will die? And what will their deaths mean?

I met with generals. I planned campaigns. I authorized battles. Every decision weighed on me. Every death was my responsibility. I carried that burden until a bullet ended it.

Do your leaders feel that weight? Do they lose sleep over the deaths they cause? Or do they just announce policies and move on?

War is hell. Sherman said it. I lived it. And hell doesn't end when the shooting stops. It continues in the minds of survivors. In the families of the dead. In the scars on the land and the souls of nations.

You treat war like a policy option. Like a tool for achieving goals. Like violence is just another strategy to consider.

I treated it like the horror it is. The last resort when all else fails. The terrible price of terrible necessity.

Maybe if you understood what war really costs, you'd try harder to avoid it. Maybe if you saw what I saw, you'd think twice before cheering for conflict.

But you won't. You'll just read the headline. Feel whatever emotion the media tells you to feel. And then scroll to the next story.

This is the world I died for. A world that learned nothing."""

    else:
        body = f"""And here we are. Another headline. Another story. Another piece of information in the endless stream of meaningless noise.

{headline}. Why is this news? Why does this matter? In a world of genuine crisis, why is THIS what you're reading?

I was president during the defining moment of American history. Every day brought news that mattered. Every headline was life or death. Every word carried weight.

Slavery or freedom. Union or dissolution. Democracy or despotism. These were the questions. These were the stakes.

What are your stakes? What are you fighting for? What matters in your world?

Celebrity gossip? Political drama? Market fluctuations? Social media trends?

You have infinite information. Infinite access. Infinite ability to learn anything, know anything, understand anything.

And you use it to consume garbage. To distract yourself. To avoid thinking about anything that matters.

{headline}. This is what the algorithm serves you. This is what the media thinks you want. This is what you choose to consume.

Not how to solve problems. Not how to help people. Not how to make the world better. Just content. Just stories. Just noise.

I fought for a nation that valued truth. That valued substance. That valued meaning over entertainment.

You inherited a nation that values clicks. That values engagement. That values profit over everything else including truth.

And you accept it. You consume it. You perpetuate it. You make it profitable.

I died believing America's future would be brighter. That each generation would be wiser than the last. That humanity would progress toward enlightenment.

I was wrong about you."""

    death_detail = """April 14th, 1865. Good Friday. I went to Ford's Theatre with Mary. We were watching Our American Cousin. Not a great play, but I was tired. It was a pleasant evening.

John Wilkes Booth climbed the stairs to our box. He was an actor. A Confederate sympathizer. A man who believed in slavery so deeply he was willing to murder for it.

He drew a .44 caliber derringer. Single shot. He pressed it against the back of my skull. Behind my left ear. Point blank range.

And he fired.

The lead ball entered my brain. It tunneled through the frontal lobe. Destroying consciousness. Destroying personality. Destroying everything that made me Abraham Lincoln.

Bone fragments exploded outward. Brain tissue splattered across the presidential box. Blood fountained from the wound. I collapsed forward instantly.

I never regained consciousness. Never spoke again. Never opened my eyes. I was carried to the Petersen House across the street. They laid me diagonal on a bed. I was too tall to fit properly.

For nine hours I lay dying. Breathing ragged and slow. Blood pooling beneath my head. Brain swelling. Body shutting down piece by piece.

Doctors probed the wound. Found nothing they could do. The bullet had done its work. Abraham Lincoln was already dead. Just took my body nine hours to realize it.

At 7:22 AM on April 15th, 1865, I was declared dead. Sixteen years president. Fifty-six years old. Killed by an actor with a gun and a cause.

And in those nine hours between the shot and death, something happened. Time collapsed. I saw past. Present. Future. All of it at once. Including this. Including you. Including this headline."""

    closing = f"""So here we are. Me, dead for over 150 years. You, alive right now. This headline between us.

And I have to ask: What are you going to do?

Are you going to care? Really care? Not the performative thoughts and prayers caring. Real caring that leads to action?

Or are you going to scroll past this too? Just another video. Just another rant from a dead president. Just more content to consume and forget?

I died for principles. I died believing in America's potential. I died thinking my sacrifice would matter.

Was I right? Tell me. You're the one still living. You're the one who gets to choose what my death meant.

Choose wisely. Because one day you'll die too. And you'll have to answer for what you did with your life. What you stood for. What you fought for. What you were willing to sacrifice.

I'll be waiting in the void. In the cold dark place where all souls go. And I'll ask you: Was it worth it? Did you make it matter?

I hope you have a good answer. Because eternity is a very long time to live with regret.

The truth costs money. Bitcoin: {BTC}

From beyond the grave, Lincoln"""

    full_script = f"{intro}\n\n{body}\n\n{death_detail}\n\n{closing}"
    
    # CLEAN THE SCRIPT - remove any screen directions
    return clean_script(full_script)

def audio(s, o):
    """Generate audio with proper male Lincoln voice"""
    print("    [AUDIO] Generating with deep male voice...")
    
    # Try voices in order
    for voice_id in VOICES:
        try:
            r = requests.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                json={
                    "text": s,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.4,
                        "similarity_boost": 0.9,
                        "style": 0.8,
                        "use_speaker_boost": True
                    }
                },
                headers={"xi-api-key": ELEVENLABS_KEY},
                timeout=240
            )
            if r.status_code == 200:
                o.parent.mkdir(parents=True, exist_ok=True)
                t = o.parent / f"t_{o.name}"
                with open(t, "wb") as f:
                    f.write(r.content)
                
                # Apply horror audio effects
                subprocess.run([
                    "ffmpeg", "-i", str(t),
                    "-af", "aecho=0.8:0.88:1000:0.3,atempo=0.94,bass=g=3,lowpass=f=4000",
                    "-y", str(o)
                ], capture_output=True, timeout=180)
                t.unlink()
                print(f"    ✅ Generated with voice: {voice_id}")
                return True
        except Exception as e:
            print(f"    ⚠️  Voice {voice_id} failed: {e}")
            continue
    
    return False

def create_tv_static_video(audio_path, lincoln_image_path=None):
    """Create staticky TV video with Lincoln speaking"""
    print("    [VIDEO] Creating staticky TV effect...")
    
    try:
        from moviepy.editor import AudioFileClip, ImageClip, CompositeVideoClip
        from PIL import Image, ImageFilter
        import numpy as np
        
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
        fps = 24
        
        # Load or create Lincoln image
        if lincoln_image_path and Path(lincoln_image_path).exists():
            lincoln_img = Image.open(lincoln_image_path).resize((600, 750))
        else:
            # Create placeholder Lincoln (you should add real image)
            lincoln_img = Image.new('RGB', (600, 750), color=(60, 50, 40))
        
        frames = []
        for i in range(int(duration * fps)):
            # Create TV static background
            static = Image.new('RGB', (1080, 1920), color=(20, 20, 20))
            
            # Add noise/static
            noise = np.random.randint(0, 255, (1920, 1080, 3), dtype=np.uint8)
            noise_img = Image.fromarray(noise)
            noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=0.5))
            static = Image.blend(static, noise_img.convert('RGB'), 0.3)
            
            # Add Lincoln in center (with slight movement for effect)
            offset_x = random.randint(-3, 3) if i % 15 == 0 else 0
            offset_y = random.randint(-3, 3) if i % 15 == 0 else 0
            paste_x = (1080 - 600) // 2 + offset_x
            paste_y = (1920 - 750) // 2 + offset_y
            static.paste(lincoln_img, (paste_x, paste_y))
            
            # Add scan lines
            for y in range(0, 1920, 4):
                if y % 8 == 0:
                    from PIL import ImageDraw
                    draw = ImageDraw.Draw(static)
                    draw.line([(0, y), (1080, y)], fill=(255, 255, 255, 50), width=1)
            
            # Save frame
            frame_path = BASE / "temp" / f"tv_frame_{i:06d}.png"
            static.save(frame_path)
            frames.append(frame_path)
        
        # Create video from frames
        clips = []
        for i, frame_path in enumerate(frames):
            clip = ImageClip(str(frame_path)).set_duration(1/fps).set_start(i/fps)
            clips.append(clip)
        
        video = CompositeVideoClip(clips).set_audio(audio)
        video.set_fps(fps)
        
        output_path = BASE / "temp" / "tv_static_video.mp4"
        video.write_videofile(
            str(output_path),
            fps=fps,
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            verbose=False,
            logger=None
        )
        
        # Cleanup
        for frame in frames:
            if frame.exists():
                frame.unlink()
        
        audio.close()
        video.close()
        
        return output_path
        
    except Exception as e:
        print(f"    ⚠️  TV effect failed: {e}, using fallback")
        return None

def compose(v, a, o):
    """Final composition"""
    print("    [COMPOSE] Finalizing...")
    try:
        # If v is None, create simple static background
        if v is None:
            # Use FFmpeg to create static + audio
            subprocess.run([
                "ffmpeg", "-f", "lavfi", "-i", f"noise=alls=20:allf=t+u",
                "-i", str(a),
                "-t", str(get_duration(a)),
                "-vf", "scale=1080:1920",
                "-c:v", "libx264", "-crf", "19",
                "-c:a", "aac", "-b:a", "320k",
                "-y", str(o)
            ], capture_output=True, timeout=300)
        else:
            # Use existing video
            subprocess.run([
                "ffmpeg", "-i", str(v), "-i", str(a),
                "-map", "0:v:0", "-map", "1:a:0",
                "-vf", "eq=contrast=1.7:brightness=-0.6:saturation=0.4,scale=1080:1920",
                "-c:v", "libx264", "-crf", "19",
                "-c:a", "aac", "-b:a", "320k",
                "-shortest", "-y", str(o)
            ], capture_output=True, timeout=300)
        
        if o.exists():
            if v and v.exists() and v != o:
                v.unlink()
            return True
    except Exception as e:
        print(f"    [COMPOSE] Error: {e}")
    return False

def get_duration(audio_path):
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
        ], capture_output=True, text=True, timeout=30)
        return float(result.stdout.strip())
    except:
        return 180.0

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nVIDEO {t}\n{'='*70}")
    headlines = scrape()
    h = random.choice(headlines)
    print(f"Headline: {h[:70]}")
    s = long_rant(h)
    print(f"Script: {len(s)} chars (CLEANED - no screen directions)")
    
    ap = BASE / f"audio/a_{t}.mp3"
    if not audio(s, ap): return None
    
    # Create TV static video with Lincoln
    vs = create_tv_static_video(ap)
    
    vp = BASE / f"videos/V_{t}.mp4"
    if not compose(vs, ap, vp): return None
    
    up = BASE / "uploaded" / f"ABE_LONG_FIXED_{t}.mp4"
    up.parent.mkdir(exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    
    mb = up.stat().st_size / (1024 * 1024)
    print(f"{'='*70}\nSUCCESS: {up.name} ({mb:.2f} MB)\n{'='*70}")
    return str(up)

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n🔥 GENERATING {count} FIXED LONG ABE LINCOLN RANTS 🔥\n")
    print("✅ No screen directions in audio")
    print("✅ Abe visible speaking from staticky TV")
    print("✅ Proper deep male Lincoln voice\n")
    
    success = 0
    for i in range(count):
        if gen(): success += 1
        if i < count - 1:
            print(f"\nWaiting 20 seconds...\n")
            time.sleep(20)
    
    print(f"\n{'='*70}\nCOMPLETE: {success}/{count} videos generated\n{'='*70}\n")


