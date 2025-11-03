import os, sys, json, requests, subprocess, random, time
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
VOICE = "pNInz6obpgDQGcFmaJgB"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

def scrape():
    headlines = []
    try:
        r = requests.get("https://news.google.com/rss", timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'xml')
            for item in soup.find_all('item')[:15]:
                if item.title:
                    headlines.append(item.title.text)
    except: pass
    if not headlines:
        headlines = ["Trump Third Term Comments", "Hurricane Destroys Island", "Government Shutdown Continues"]
    return headlines

def roast(h):
    hl = h.lower()
    is_trump = "trump" in hl or "donald" in hl
    is_climate = any(w in hl for w in ["hurricane", "storm", "climate", "flood"])
    is_tech = any(w in hl for w in ["ai", "tech", "musk", "tesla"])
    is_money = any(w in hl for w in ["billion", "million", "trade", "deal"])
    
    opens = [
        "Lincoln here. Dead guy talking.",
        "Abraham Lincoln. Got shot in the head. Still smarter than this.",
        "It's me. The penny guy. Worth more than your politicians.",
        "Honest Abe. Which is ironic because I'm about to lie and say I care."
    ]
    
    if is_trump:
        roasts = [
            f"{h}. I preserved the Union. He preserved his spray tan. We are not the same.",
            f"{h}. I freed slaves. He freed himself from accountability. You worship him.",
            f"{h}. When I was president, men died for country. Now they tweet for ego.",
            f"{h}. I got shot for freeing people. He'll get elected for imprisoning them."
        ]
    elif is_climate:
        roasts = [
            f"{h}. Planet is screaming. You're scrolling TikTok. I'm dead and I can hear her.",
            f"{h}. Nature is literally on fire. Your response? Debate if it's real.",
            f"{h}. I died in 1865. From my grave I see the ocean rising. But sure, it's fake.",
            f"{h}. Hurricanes everywhere. And you're worried about gas prices."
        ]
    elif is_tech:
        roasts = [
            f"{h}. Billionaires launching rockets while people starve. I fought inequality. You invented an app for it.",
            f"{h}. AI replacing workers. Great. I freed slaves so robots could take their jobs.",
            f"{h}. Tech bros solving problems that don't exist. Actual problems? Unsolved.",
            f"{h}. Building artificial intelligence. Try real intelligence first."
        ]
    elif is_money:
        roasts = [
            f"{h}. Billions changing hands. None reaching people who need it. Capitalism!",
            f"{h}. Rich getting richer. Poor getting poorer. Somehow this is news.",
            f"{h}. Amount in this headline could solve hunger. But won't. Because reasons.",
            f"{h}. Money traded like Monopoly. Except when you lose, you die."
        ]
    else:
        roasts = [
            f"{h}. This is news? I read this from the grave and wanted to die again.",
            f"{h}. Where's the part that matters? That helps anyone?",
            f"{h}. You found the least important thing happening. Breaking news!",
            f"{h}. I've been dead 160 years. This headline makes me glad."
        ]
    
    return f"{random.choice(opens)}\n\n{random.choice(roasts)}"

def death():
    ds = [
        "April 14, 1865. Booth's derringer. Lead ball through skull. Nine hours dying. At least the play ended.",
        "Good Friday. 10:15 PM. CRACK. Booth fires. My skull explodes. Brain on walls. Carried to Petersen House. Too tall for the bed. Story of my life.",
        "Being shot in the head: Sound like thunder. Then darkness. No pain. Just shutdown. Nine hours slow death. Bullet destroyed everything.",
        "Booth. Actor. Coward. Waits for laugh. Approaches behind. Single shot. Head snaps. Gone. 150 years of service ended by one angry man with gun."
    ]
    return random.choice(ds)

def observe():
    os = [
        "From my tomb I watch every betrayal. You think I'm resting? I'm screaming. You can't hear me. Yet.",
        "Death is no escape. I see everything. America dies. Over and over.",
        "You put me on currency. Five dollars. Not enough for lunch. I preserved the nation. You can't preserve a sandwich.",
        "I watch from the void. Cold. Dark. But not as dark as your future."
    ]
    return random.choice(os)

def closer():
    cs = [
        "So there it is. Your news. Your problem. I'm dead. I don't fix this. You do. And you won't.",
        "Every generation thinks they're special. You're not. Just latest version of same stupidity. Enjoy.",
        "Those who don't learn from history repeat it. You've learned nothing. Enjoy your doom.",
        "I died for the Union. You're killing it for memes. Mission accomplished."
    ]
    return random.choice(cs)

def script(h):
    return f"{roast(h)}\n\n{death()}\n\n{observe()}\n\n{closer()}\n\nBitcoin: {BTC}"

def audio(s, o):
    print("    [AUDIO]")
    try:
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}", json={"text": s, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.35, "similarity_boost": 0.85, "style": 0.8, "use_speaker_boost": True}}, headers={"xi-api-key": ELEVENLABS_KEY}, timeout=180)
        if r.status_code == 200:
            o.parent.mkdir(parents=True, exist_ok=True)
            t = o.parent / f"t_{o.name}"
            with open(t, "wb") as f: f.write(r.content)
            subprocess.run(["ffmpeg", "-i", str(t), "-af", "aecho=0.8:0.88:1000:0.3,atempo=0.96", "-y", str(o)], capture_output=True)
            t.unlink()
            return True
    except: pass
    return False

def video():
    print("    [VIDEO]")
    try:
        r = requests.get("https://api.pexels.com/videos/search", headers={"Authorization": PEXELS_KEY}, params={"query": "dark horror", "per_page": 1, "orientation": "portrait"}, timeout=30)
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
    print("    [COMPOSE]")
    try:
        p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(a)], capture_output=True, text=True)
        d = float(p.stdout.strip())
        subprocess.run(["ffmpeg", "-i", str(v), "-i", str(a), "-map", "0:v:0", "-map", "1:a:0", "-vf", "eq=contrast=1.6:brightness=-0.5:saturation=0.5,scale=1080:1920", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "256k", "-t", str(d), "-shortest", "-y", str(o)], capture_output=True, timeout=300)
        if o.exists():
            v.unlink()
            return True
    except: pass
    return False

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\nVIDEO {t}\n{'='*70}")
    headlines = scrape()
    h = random.choice(headlines)
    print(f"Roasting: {h[:60]}")
    s = script(h)
    print(f"Script: {len(s)} chars")
    ap = BASE / f"audio/a_{t}.mp3"
    if not audio(s, ap): return None
    vs = video()
    if not vs: return None
    vp = BASE / f"videos/V_{t}.mp4"
    if not compose(vs, ap, vp): return None
    up = BASE / "uploaded" / f"ABRAHAM_{t}.mp4"
    up.parent.mkdir(exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    mb = up.stat().st_size / (1024 * 1024)
    print(f"{'='*70}\nSUCCESS: {up.name} ({mb:.2f} MB)\n{'='*70}")
    return str(up)

if __name__ == "__main__":
    c = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\nGENERATING {c} ABRAHAM HORROR VIDEOS\n")
    s = 0
    for i in range(c):
        if gen(): s += 1
        if i < c - 1: time.sleep(15)
    print(f"\nCOMPLETE: {s}/{c} videos\n")
