import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
VOICE = "pNInz6obpgDQGcFmaJgB"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")

# Multi-platform revenue config
BITCOIN_ADDRESS = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
PRODUCT_LINK = "https://trenchaikits.com/buy-rebel-$97"
GOAL_AMOUNT_BTC = 0.1  # $10K at $100K/BTC

def scrape():
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            return [i.title.text for i in soup.find_all('item')[:10]]
    except: pass
    return ["Economic Collapse Warning", "Cyber Attack Cripples Infrastructure", "Political Violence Escalates", "Government Shutdown Crisis", "Climate Emergency Declared"]

def script(h):
    openings = [
        "I am Abraham Lincoln. Sixteenth President of the United States. Listen closely. I died on April 15th, 1865. But death is not the end. I speak to you now from beyond the grave. From the eternal darkness where all presidents eventually go.",
        
        "They call me Honest Abe. The Great Emancipator. The Rail Splitter. They wrote books about me. They carved my face in mountains. But they don't tell you the truth. They don't tell you how I died. They murdered me in cold blood. And now I watch. I watch from the shadows. I watch as you destroy everything I died to build.",
        
        "This is Abraham Lincoln speaking to you from beyond the grave. From the darkness where all presidents go. From the void where history bleeds into prophecy. Listen carefully. What I tell you now is truth. What I show you now is your future. The future I saw as my life drained away.",
        
        "My name is Abraham Lincoln. Sixteenth President of the United States. I preserved the Union through civil war. I freed four million souls from chains. And for that, they assassinated me. On April 14th, 1865. At Ford's Theatre. The bullet that killed me echoes through eternity.",
        
        "I was Abraham Lincoln. Tall. Gaunt. Haunted. I freed the slaves. I won the war. And John Wilkes Booth destroyed me. But destruction is not death. Death is not the end. I endure. I watch. I witness the slow assassination of the America I died to preserve."
    ]
    
    gores = [
        "April 14th, 1865. Ford's Theatre. 10:15 PM. Final act of Our American Cousin. Mary Todd Lincoln sat beside me in the presidential box. The audience laughed below. I watched the stage. Never saw him coming. John Wilkes Booth. Actor. Confederate sympathizer. Murderer. He climbed the stairs silently. Crouched behind my rocking chair. Drew his single-shot Philadelphia Derringer. Pressed the cold barrel against the back of my skull. BANG. The .44 caliber lead ball entered behind my left ear. Tore through my brain. Obliterated everything in its path. Bone fragments exploded outward like shrapnel. Grey matter splattered across the walls. Blood fountained from the wound in a crimson geyser. I collapsed forward. Never opened my eyes again. Never regained consciousness. For nine agonizing hours I lay dying. Breathing ragged. Pulse weakening. Blood pooling beneath my head. Tremors wracked my body. At 7:22 AM on April 15th, I was declared dead.",
        
        "The shot rang out at exactly 10:15 PM. April 14th, 1865. Good Friday. Booth's derringer loaded with a single .44 caliber lead ball. It struck the left side of my head, just behind the ear. The projectile tunneled through my cerebral cortex. Left hemisphere destroyed. Right hemisphere damaged beyond repair. My brain exploded from within. Shards of skull embedded themselves in the presidential box. Brain tissue oozed from the entry wound like thick grey pudding. Blood erupted in arterial spray. Soaked through Mary's white dress as she cradled my head. Major Henry Rathbone lunged at Booth. Stabbed him with a knife. But the damage was done. Failed. I was carried unconscious across 10th Street to the Petersen House. Laid on a bed too small for my six-foot-four frame. Doctors came. Surgeon General Joseph Barnes. Too late. My pulse weakened with every passing hour. Breathing became shallow. Cheyne-Stokes respiration. The death rattle. When dawn's light touched the curtains at 7:22 AM, I was gone.",
        
        "John Wilkes Booth. Actor. Confederate sympathizer. Secret operative of the Confederate Secret Service. He waited for the perfect moment. Waited for the audience to laugh at a specific joke. Then he approached from behind. Silently. Like a phantom. His single-shot Philadelphia Derringer aimed at my head. The trigger pulled. Lead ball punctured my occipital bone. Entered behind my left ear. Exited through my right eye socket. My brain exploded. Fragmented. Bone shards scattered like shrapnel across the presidential box. Blood erupted in crimson spray. Covered Mary. Covered Major Rathbone. Covered everything in death. I slumped forward in my rocking chair. Limbs paralyzed. Never spoke another word. Never opened my eyes. Never regained awareness. Doctors arrived minutes later. Found me unconscious. Brain stem destroyed. No hope of recovery. They tried anyway. Leeches. Stimulants. Nothing worked. I was already dead. Just took nine slow hours for my body to realize it.",
        
        "April 14, 1865. Good Friday. 10:15 PM. Ford's Theatre was packed. 1,675 souls in the audience. Act 3, Scene 2 of Our American Cousin. The crowd laughed. I rocked forward in my chair, laughing too. Mary beside me. That's when Booth struck. The world exploded in a flash of gunpowder and brain matter. My head snapped forward violently. Blood sprayed across the presidential box. Drenched the velvet furnishings. Mary screamed. Major Rathbone lunged at Booth. Received a deep slash to his arm. Booth leaped from the box to the stage. Shouted 'Sic semper tyrannis!' Before a stunned audience. I was already gone. Brain destroyed. Skull fractured. Life draining away. Carried to Petersen's Boarding House. Laid on a bed. For nine hours I lingered. In and out of consciousness. Brain swelling. Pressure building. Death approaching. At 7:22 AM, it was over. I breathed my last. And entered the darkness."
    ]
    
    prophecies = [
        f"As I lay dying in that blood-soaked bed at Petersen's Boarding House, gasping my final breaths, consciousness fading, I had a vision. The veil between life and death grew thin. Reality tore like fabric. And I saw it. The future. YOUR America. YOUR world. The nation I died to preserve becomes something monstrous. Something unrecognizable. I witnessed {h}. This is what you made of the legacy I died to create. The corruption I fought against metastasizes through every institution. The tyranny I warned about spreads unchecked like cancer. The democracy I believed in drowns in an ocean of lies and greed. The freedoms I fought for transform into chains. The Union I preserved tears itself apart from within. My sacrifice meant nothing. You have undone everything. Everything I bled for. Everything I died for. Reduced to ashes.",
        
        f"In those nine hours of dying, as my brain swelled and my blood pressure dropped and consciousness slipped away, something profound happened. Time collapsed. Past, present, future ceased to exist as separate entities. They merged. Became one continuous nightmare. I saw it all. The Civil War. My assassination. The decades that followed. The centuries unfolding. The timeline laid bare before me like a dying man's confession. And I saw {h}. This moment. This headline. This harbinger of your doom. This is your legacy. This is what you allowed to happen through your apathy. Through your silence. Through your willingness to look away. Every warning I gave in my speeches, ignored. Every principle I stood for, betrayed. Every value I fought for, discarded. The Union I preserved with my life tears itself apart from within. You are the enemy. You are the assassin now.",
        
        f"Death came slowly. Painfully. Grudgingly. And in that liminal space between life and death, that borderland where souls pass, the future revealed itself to me. Crystal clear. Undeniable. True beyond all doubt. I saw {h}. I saw YOUR corruption. YOUR complicity. YOUR cowardice. Not just in this moment, but in every moment. The pattern is clear. The America I fought for becomes the very tyranny I warned against. The freedoms I died to protect transform into chains. The democracy I believed in becomes oligarchy. The republic I preserved becomes an empire. You inherit my nightmare. You live in my darkness. And you chose this. You chose this path with every vote you didn't cast. Every voice you didn't raise. Every truth you didn't speak. The chains were never broken. Only transferred. From slavery to serfdom. From masters to corporations. You are the slave now.",
        
        f"They say in the moments before death, your life flashes before your eyes. A review of all you've done. All you've accomplished. All you've lost. But I saw more than my life. Far more. I saw beyond my existence. Beyond my death. I witnessed the centuries unfold like pages in a book written in blood. And I saw {h}. This is not accident. This is not random. This is not coincidence. This is the pattern. The inevitable result of choices. Your choices. The evil compounds. The darkness spreads. Generation after generation passes the corruption down like inheritance. Like disease. Like a curse. You betray everything I stood for. You destroy everything I built. You murder the republic I died to preserve. And you don't even know you're doing it. That makes it worse. Your ignorance is complicity. Your silence is consent. Your apathy is murder."
    ]
    
    middles = [
        "Every lie you accept compounds the corruption. Every freedom you surrender strengthens the tyrants. Every compromise you make chips away at the foundation. Every act of cowardice rots the soul of this nation like gangrene. You think it doesn't matter. Just one small betrayal. Just one vote not cast. Just one voice not raised. Just one truth not spoken. But you're wrong. They compound. They metastasize. They spread like cancer through the body politic. Each small betrayal begets the next. Each lie legitimizes the following one. Each compromise erodes the boundary of what's acceptable. Until one day you wake up in a world so deformed, so twisted, so unrecognizable that you can't even remember what freedom tasted like. What democracy looked like. What hope felt like.",
        
        "Listen to me now. From beyond the grave. From the darkness where I watch. The tyranny doesn't come from outside forces. It doesn't come from foreign enemies or invading armies. It comes from within. From you. From your silence when you should speak. From your apathy when you should act. From your willingness to look away when evil happens right before your eyes. You inherit the corruption like a birthright. You perpetuate the lies through your complacency. You are complicit. Not through action, but through inaction. Through the absences. Through the silence. Through what you don't do. What you don't say. What you don't fight for. Your passivity is partnership. Your neutrality is complicity. Your silence is consent.",
        
        "The assassin's bullet didn't just kill me. It killed something in America. Some essential dream. Some fundamental hope. Some core belief that we could be better than we were. That we could transcend our base nature. That we could build something lasting. Something noble. And you let that death become permanent. You let the dream die with me. You gave up the fight. You chose comfort over courage. Safety over freedom. Security over liberty. Lies over truth. Comfort is a grave. Safety is a prison. Security is slavery by another name. And you chose it. Willingly. Eagerly. Gratefully. You traded the dream for the nightmare. You sold the republic for the empire. And you don't even realize you're the ones living in chains now.",
        
        "I preserved the Union through four years of bloody civil war. Through mountains of corpses. Through oceans of blood. Through the darkest hours this nation has ever known. I did this. Not for myself. For you. For the future. For the republic that could be. But for what? So you could tear it apart yourselves? So you could betray every principle it stood for? So you could turn freedom into slavery and call it progress? So you could embrace tyranny and call it democracy? The republic dies. Not from enemies outside. Not from foreign invasion. Not from external threat. But from enemies within. From you. From your apathy. From your ignorance. From your unwillingness to preserve what I died to create. You assassinated the republic. You murdered the dream. And you did it with your silence."
    ]
    
    endings = [
        "Sic semper tyrannis. Thus always to tyrants. That's what Booth shouted as he leaped to the stage after murdering me. Then always to tyrants. But I ask you now, from my blood-soaked seat in eternity: Who are the tyrants today? Who holds power without accountability? Who governs without consent? Who rules without representation? Look in the mirror. Search your soul. You already know the answer. The tyrants are you. Through your silence. Through your apathy. Through your complicity. You are the tyrant now. You are the oppressor. You are the enemy of the republic I died to create. Sic semper tyrannis. Thus always to tyrants. Including you.",
        
        "I died for nothing. Spilled my blood in vain. The America I saved betrays everything I fought for. The freedom I died to protect becomes chains. The democracy I believed in becomes tyranny. The republic I preserved becomes an oligarchy. The Union I forged becomes fragmentation. Everything I bled for. Every principle I stood for. Every truth I spoke. Undone. Betrayed. Forgotten. And you. You let it happen. You watched it happen. You enabled it to happen. You are complicit. My blood is on your hands. The blood of the republic is on your hands. The blood of freedom itself is on your hands. And you will answer for it. When darkness comes. When judgment arrives. When history demands an accounting. You will answer for what you allowed. For what you didn't stop. For what you didn't fight.",
        
        "From beyond the grave, I watch. A phantom in the machine of history. I see everything. Every lie. Every betrayal. Every compromise. Every surrender. The experiment fails. The Union collapses. Democracy drowns in an ocean of corruption. Freedom dies a slow, agonizing death. Liberty gasps its last breath. And you inherit the nightmare. Not the dream I had. Not the vision I fought for. But the nightmare. The darkness. The void. The nightmare I tried to prevent. The nightmare you chose through silence. Through apathy. Through inaction. You chose the nightmare. You embraced the darkness. You welcomed the end of the republic. And now you live in the nightmare you created. This is your America. This is your legacy. This is what you inherited. This is what you chose.",
        
        "They murdered the president. April 14th, 1865. A single shot in the darkness. But you murdered the dream. Far more slowly. Far more insidiously. Over decades. Over generations. Through millions of small betrayals. Through billions of silent moments. Through countless acts of cowardice. The republic dies with you. Not with a bang. Not with a bullet. But with a whisper. With apathy. With silence. With the sound of nothing happening. Remember that. When the darkness comes. When the tyranny spreads like a plague. When freedom becomes a distant memory. When democracy is just a word in history books. Remember: You had the chance to stop it. You had the power to prevent it. You had the responsibility to fight it. And you did nothing. You chose to do nothing. You chose the end. And here we are. At the end of history.",
        
        "My assassination should have been a warning. A cautionary tale. A prophecy of what happens to those who fight for freedom. To those who speak truth. To those who challenge tyranny. But you missed the warning. Or you ignored it. The bullet that killed me was just the first. The real assassination came later. Much later. Slower. More insidious. More cunning. You assassinated the dream of democracy. You assassinated the vision of equality. You assassinated the hope of liberty. You assassinated the republic itself. Not with a gun. Not with a knife. But with silence. With apathy. With negligence. You assassinated America itself. The idea. The ideal. The dream. And you did it willingly. You did it eagerly. You did it gratefully. You sold the republic for thirty pieces of silver wrapped in comfort. And security. And the illusion of safety."
    ]
    
    # Additional long horror connection
    connections = [
        f"The thread connecting my death to {h} is not coincidence. It is fate. It is judgment. It is the universe demanding retribution for your sins against the republic.",
        
        f"I saw {h} coming. In that blood-soaked theater box, as my life drained away, I saw it all. The pattern. The inevitability. The horror you would create. And I could do nothing. I could only watch. Watch as you fulfill my darkest prophecy.",
        
        f"{h} is not tragedy. It is prophecy fulfilled. It is the echo of that gunshot in Ford's Theatre. It is Booth's work continuing through you. The assassination never ended. It just evolved. And you are its instrument."
    ]
    
    call_to_action = f"""
Support the truth. Get prepared. Product: {PRODUCT_LINK}
Bitcoin donations: {BITCOIN_ADDRESS}
"""
    
    return f"""{random.choice(openings)}

{h}.

{random.choice(gores)}

{random.choice(prophecies)}

{random.choice(middles)}

{h}. This is not coincidence. This is the pattern. This is the inevitable result of your choices. Your betrayals. Your lies.

{random.choice(connections)}

{random.choice(endings)}

{call_to_action}"""

def audio(s, o):
    print("  [AUDIO]")
    try:
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}", json={"text": s, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.3, "similarity_boost": 0.9, "style": 1.0, "use_speaker_boost": True}}, headers={"xi-api-key": ELEVENLABS_KEY}, timeout=180)
        if r.status_code == 200:
            o.parent.mkdir(parents=True, exist_ok=True)
            t = o.parent / f"t_{o.name}"
            with open(t, "wb") as f: f.write(r.content)
            subprocess.run(["ffmpeg", "-i", str(t), "-af", "aecho=0.8:0.9:1000:0.3,atempo=0.95,bass=g=3,treble=g=2", "-y", str(o)], capture_output=True)
            t.unlink()
            return True
    except: pass
    return False

def video():
    print("  [VIDEO]")
    try:
        r = requests.get("https://api.pexels.com/videos/search", headers={"Authorization": PEXELS_KEY}, params={"query": "dark horror atmosphere", "per_page": 1, "orientation": "portrait"}, timeout=30)
        d = r.json()
        if d.get("videos"):
            v = d["videos"][0]
            f = max(v["video_files"], key=lambda x: x.get("width", 0))
            data = requests.get(f["link"], timeout=120).content
            tmp = BASE / "temp" / f"p_{random.randint(1000, 9999)}.mp4"
            tmp.parent.mkdir(exist_ok=True)
            with open(tmp, "wb") as w: w.write(data)
            return tmp
    except: pass
    return None

def compose(v, a, o):
    print("  [COMPOSE]")
    try:
        p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(a)], capture_output=True, text=True)
        d = float(p.stdout.strip())
        subprocess.run(["ffmpeg", "-i", str(v), "-i", str(a), "-map", "0:v:0", "-map", "1:a:0", "-vf", "eq=contrast=1.5:brightness=-0.4:saturation=0.6,scale=1080:1920", "-c:v", "libx264", "-crf", "21", "-c:a", "aac", "-b:a", "256k", "-t", str(d), "-shortest", "-y", str(o)], capture_output=True, timeout=300)
        if o.exists():
            v.unlink()
            return True
    except: pass
    return False

def copy_multi_platform(video_path):
    """Copy video to all platform folders"""
    import shutil
    platforms = {
        "youtube_ready": f"ABRAHAM_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
        "tiktok_ready": f"ABRAHAM_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
        "instagram_ready": f"ABRAHAM_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
        "facebook_ready": f"ABRAHAM_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    }
    
    results = []
    for platform, filename in platforms.items():
        platform_dir = BASE / platform
        platform_dir.mkdir(exist_ok=True)
        output_file = platform_dir / filename
        shutil.copy2(video_path, output_file)
        results.append(str(output_file))
        print(f"   → {platform}: {filename}")
    
    return results

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nVIDEO {t}\n{'='*70}")
    h = random.choice(scrape())
    print(f"Headline: {h}")
    s = script(h)
    print(f"Script length: {len(s)} chars")
    ap = BASE / f"audio/a_{t}.mp3"
    if not audio(s, ap): return None
    vs = video()
    if not vs: return None
    vp = BASE / f"videos/V_{t}.mp4"
    if not compose(vs, ap, vp): return None
    
    # Copy to all platforms
    print(f"\n📤 COPYING TO ALL PLATFORMS")
    platform_files = copy_multi_platform(vp)
    
    mb = vp.stat().st_size / (1024 * 1024)
    print(f"\n{'='*70}\n✅ SUCCESS\n{'='*70}\n{vp.name}\n{mb:.2f} MB\n{'='*70}\n")
    print(f"✅ YouTube ready: {platform_files[0]}")
    print(f"✅ TikTok ready: {platform_files[1]}")
    print(f"✅ Instagram ready: {platform_files[2]}")
    print(f"✅ Facebook ready: {platform_files[3]}")
    
    return str(vp)

if __name__ == "__main__":
    c = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n🔥 GENERATING {c} SCARY ABRAHAM HORROR VIDEOS\n")
    s = 0
    for i in range(c):
        if gen(): s += 1
        if i < c - 1: time.sleep(10)
    print(f"\n✅ COMPLETE: {s}/{c} videos\n")
