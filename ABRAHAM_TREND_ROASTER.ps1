# ═══════════════════════════════════════════════════════════════════════════
# ABRAHAM HORROR - TREND ROASTER EDITION
# Scrapes real headlines, roasts each one specifically with dark satire
# ═══════════════════════════════════════════════════════════════════════════

param([int]$Count = 50)

$ROOT = "F:\AI_Oracle_Root\scarify\abraham_horror"
$BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"

Write-Host ""
Write-Host "🔥 ABRAHAM - TREND ROASTER" -ForegroundColor Red
Write-Host ("=" * 70) -ForegroundColor Gray
Write-Host ""

$dirs = @("audio", "videos", "uploaded", "temp")
foreach ($dir in $dirs) {
    $path = Join-Path $ROOT $dir
    if (-not (Test-Path $path)) { New-Item -ItemType Directory -Path $path -Force | Out-Null }
}

pip install --quiet requests beautifulsoup4 lxml 2>&1 | Out-Null

$python = @'
import os, sys, json, requests, subprocess, random, time, re
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

ELEVENLABS_KEY = "3e27b6a9ea9e01667912a50c1912ab917271127c6ff0ea951669a7a257e0bdfa"
PEXELS_KEY = "RgE9Mdn3ToSQhn2RiLJ4mPMISjjp587QKRG9uhpOrLVtkKPCibUPUDGh"
VOICE = "pNInz6obpgDQGcFmaJgB"
BASE = Path("F:/AI_Oracle_Root/scarify/abraham_horror")
BTC = "bc1qaeylk80cz3cd9ckxlyuedyq9eupeqhaujk2plt"
PRODUCT = "https://trenchaikits.com/buy-rebel-$97"

def scrape():
    headlines = []
    sources = [
        "https://news.google.com/rss",
        "https://www.reddit.com/r/news/.rss",
        "https://www.reddit.com/r/worldnews/.rss"
    ]
    for url in sources:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'xml')
                items = soup.find_all('item')[:5]
                for item in items:
                    title = item.title.text if item.title else ""
                    if title and len(title) > 20:
                        headlines.append(title)
        except: pass
    return headlines if headlines else ["Trump Third Term", "Hurricane Destroys Island", "Government Shutdown Day 50"]

def roast_headline(h):
    h_lower = h.lower()
    
    # Extract key topics
    is_trump = any(x in h_lower for x in ["trump", "donald", "maga"])
    is_climate = any(x in h_lower for x in ["hurricane", "flood", "climate", "weather", "storm"])
    is_tech = any(x in h_lower for x in ["ai", "tech", "musk", "tesla", "twitter", "x.com"])
    is_money = any(x in h_lower for x in ["billion", "million", "stock", "market", "trade", "deal"])
    is_crime = any(x in h_lower for x in ["murder", "shoot", "kill", "dead", "crime", "police"])
    is_celeb = any(x in h_lower for x in ["kardashian", "celebrity", "star", "actor", "singer"])
    is_war = any(x in h_lower for x in ["war", "military", "strike", "bomb", "israel", "gaza", "ukraine"])
    
    openings = [
        f"Lincoln here. Dead since 1865. Still smarter than whoever wrote this headline.",
        f"Abraham Lincoln speaking. I took a bullet to the brain. Reading this feels worse.",
        f"It's me. The guy on the penny. Worth more than this news story.",
        f"Honest Abe. Except I'm lying when I say I care about your problems."
    ]
    
    # Specific roasts based on headline content
    if is_trump:
        roasts = [
            f"So. {h}. I preserved the Union during Civil War. He preserved his spray tan during federal investigation. We are not the same.",
            f"{h}. I freed slaves. He freed himself from accountability. Somehow you think HE'S the president to remember.",
            f"{h}. When I was president, men died for their country. Now men just tweet for their ego. Progress.",
            f"{h}. I got shot in a theatre for freeing people. He'll probably get elected for imprisoning them. America!"
        ]
    elif is_climate:
        roasts = [
            f"{h}. Mother Nature is screaming. You're scrolling TikTok. I'm dead and even I can hear her.",
            f"So. {h}. The planet is literally on fire. Your response? Debate if it's real. Bold strategy.",
            f"{h}. Hurricanes. Floods. Fires. And you're worried about gas prices. Priorities, people.",
            f"{h}. I died in 1865. Even from my grave I can see the ocean rising. But sure, climate change is fake."
        ]
    elif is_tech:
        roasts = [
            f"{h}. Billionaires launching rockets while people starve. I fought a war over inequality. You created an app for it.",
            f"So. {h}. AI will replace workers. Great. I freed slaves so robots could take their jobs. My legacy lives on.",
            f"{h}. Tech bros inventing solutions to problems that don't exist. Meanwhile actual problems: unsolved.",
            f"{h}. You're building artificial intelligence. Maybe focus on the real intelligence first. Just a thought."
        ]
    elif is_money:
        roasts = [
            f"{h}. Billions changing hands. None of it reaching the people who need it. Trickle-down economics, baby!",
            f"So. {h}. Rich people getting richer. Poor people getting poorer. And somehow this is news to you.",
            f"{h}. The dollar amount in this headline could solve world hunger. But won't. Because capitalism.",
            f"{h}. Money being traded like it's Monopoly. Except when you lose this game, you die."
        ]
    elif is_crime:
        roasts = [
            f"{h}. Another shooting. Another hashtag. Another moment of silence. Another day in America.",
            f"So. {h}. People dying in the streets. Your response? Thoughts and prayers. I got actual thoughts: you're useless.",
            f"{h}. Crime waves. You want more police. I suggest trying less poverty. But what do I know, I just ran a country.",
            f"{h}. Violence everywhere. But sure, the real problem is video games. Not guns. Never guns."
        ]
    elif is_celeb:
        roasts = [
            f"{h}. Celebrity news. While democracy collapses. Bread and circuses, baby. Rome fell this way too.",
            f"So. {h}. Famous person did thing. And you care. Why? I died for this? For celebrity gossip?",
            f"{h}. Rich celebrities pretending to be relatable. Poor people pretending to care. Everyone's pretending.",
            f"{h}. This is news? THIS? I held a nation together. You're obsessing over someone's Instagram."
        ]
    elif is_war:
        roasts = [
            f"{h}. More war. More death. More profit for weapons manufacturers. The system works as designed.",
            f"So. {h}. Bombs falling. Children dying. And you're debating who's right. Newsflash: nobody.",
            f"{h}. War never changes. Except now you can watch it live on Twitter. Progress.",
            f"{h}. People killing each other over invisible lines on maps. I died for the Union. You're dying for oil."
        ]
    else:
        roasts = [
            f"{h}. This is what passes for news. I read this from beyond the grave and wanted to die again.",
            f"So. {h}. And? Where's the part that matters? Where's the part that helps anyone?",
            f"{h}. Congratulations. You found the least important thing happening today. Reported it as breaking news.",
            f"{h}. I've been dead 160 years. This headline makes me glad."
        ]
    
    return f"{random.choice(openings)}\n\n{random.choice(roasts)}"

def assassination_detail():
    details = [
        "April 14, 1865. Ford's Theatre. Watching Our American Cousin. Bad play. Worse ending for me. Booth's derringer. Point blank. Lead ball enters behind left ear. Tunnels through brain. Fractures orbital bone. I collapse. Unconscious. Never wake. Nine hours later. Dead. At least the play was over.",
        
        "Good Friday. 10:15 PM. Presidential box. Mary beside me. Laughing at the play. Then the sound. CRACK. Booth's pistol. My skull explodes. Brain matter on the walls. Blood pooling. Major Rathbone tries to stop him. Fails. I'm carried to Petersen House. Dying. They lay me diagonal. I'm too tall for the bed. Story of my life. And death.",
        
        "Let me describe being shot in the head. The derringer fires. Sound like thunder. Then nothing. No pain. Just darkness. Brain ceasing function. Body shutting down. Nine hours of slow death. Doctors probing the wound. Finding nothing. Because there's nothing to find. The bullet destroyed everything that made me me. I'm a body. Not a person. Not anymore.",
        
        "Booth. Actor. Confederate. Coward. He waits for the laugh. Approaches from behind. Single shot. My head snaps forward. Grey matter sprays. Bone fragments scatter. Blood fountain. I slump. Gone. Just like that. 150 years of service to country. Ended by one angry man with a gun. American as apple pie."
    ]
    return random.choice(details)

def eerie_observation():
    observations = [
        "From my tomb I watch. Every betrayal. Every compromise. Every small death of democracy. You think I'm resting in peace? I'm screaming. You just can't hear me. Yet.",
        
        "They buried me. But death is no escape. I see everything. Past. Present. Future. All collapsed into one eternal now. And in that now? America dies. Over and over. And over.",
        
        "You put my face on currency. Five dollars. Not even enough for lunch. I preserved the nation. You can't preserve a sandwich. The disrespect is almost impressive.",
        
        "I watch from the void. The space between life and death. It's cold here. Dark. But not as dark as your future. Not as cold as your hearts."
    ]
    return random.choice(observations)

def dark_closer():
    closers = [
        "So there it is. Your news. Your world. Your problem. I'm dead. I don't have to fix this. You do. And you won't. I know you won't. Because I see the future. And it's not pretty. It's not hopeful. It's just... over.",
        
        "Every generation thinks they're different. Special. Chosen. You're not. You're just the latest version of the same stupidity. Same greed. Same violence. Same inevitable collapse. Enjoy.",
        
        "They say those who don't learn from history are doomed to repeat it. You've learned nothing. So enjoy your doom. I'll be watching. Laughing. From hell.",
        
        "I died for the Union. You're killing it for memes. Congratulations. You've achieved the impossible. You made death look appealing. Mission accomplished."
    ]
    return random.choice(closers)

def script(h):
    return f"""{roast_headline(h)}

{assassination_detail()}

{eerie_observation()}

{dark_closer()}

Bitcoin: {BTC}
Survival gear: {PRODUCT}"""

def audio(s, o):
    print("  [AUDIO]")
    try:
        r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}", json={"text": s, "model_id": "eleven_multilingual_v2", "voice_settings": {"stability": 0.35, "similarity_boost": 0.85, "style": 0.8, "use_speaker_boost": True}}, headers={"xi-api-key": ELEVENLABS_KEY}, timeout=180)
        if r.status_code == 200:
            o.parent.mkdir(parents=True, exist_ok=True)
            t = o.parent / f"t_{o.name}"
            with open(t, "wb") as f: f.write(r.content)
            subprocess.run(["ffmpeg", "-i", str(t), "-af", "aecho=0.8:0.88:1000:0.3,atempo=0.96,bass=g=2", "-y", str(o)], capture_output=True)
            t.unlink()
            return True
    except: pass
    return False

def video():
    print("  [VIDEO]")
    try:
        r = requests.get("https://api.pexels.com/videos/search", headers={"Authorization": PEXELS_KEY}, params={"query": "dark fog eerie", "per_page": 1, "orientation": "portrait"}, timeout=30)
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
        subprocess.run(["ffmpeg", "-i", str(v), "-i", str(a), "-map", "0:v:0", "-map", "1:a:0", "-vf", "eq=contrast=1.6:brightness=-0.5:saturation=0.5,scale=1080:1920", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-b:a", "256k", "-t", str(d), "-shortest", "-y", str(o)], capture_output=True, timeout=300)
        if o.exists():
            v.unlink()
            return True
    except: pass
    return False

def gen():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*70}\n{t}\n{'='*70}")
    headlines = scrape()
    if not headlines:
        print("No headlines scraped")
        return None
    h = random.choice(headlines)
    print(f"Roasting: {h}")
    s = script(h)
    print(f"Script: {len(s)} chars")
    ap = BASE / f"audio/a_{t}.mp3"
    if not audio(s, ap): return None
    vs = video()
    if not vs: return None
    vp = BASE / f"videos/V_{t}.mp4"
    if not compose(vs, ap, vp): return None
    up = BASE / "uploaded" / f"ABE_{t}.mp4"
    up.parent.mkdir(exist_ok=True)
    import shutil
    shutil.copy2(vp, up)
    mb = up.stat().st_size / (1024 * 1024)
    print(f"\n{'='*70}\nSUCCESS: {up.name} ({mb:.2f} MB)\n{'='*70}")
    return str(up)

if __name__ == "__main__":
    c = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\nROASTING {c} TRENDING HEADLINES\n")
    s = 0
    for i in range(c):
        if gen(): s += 1
        if i < c - 1: time.sleep(15)
    print(f"\nDONE: {s}/{c}\n")
'@

(Join-Path $ROOT "abraham_roaster.py") | Set-Content -Encoding UTF8 -Force
Write-Host "✅ Created abraham_roaster.py" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 SCRAPING & ROASTING $Count HEADLINES..." -ForegroundColor Yellow
Write-Host ""
cd $ROOT
python abraham_roaster.py $Count
Write-Host ""
Write-Host "✅ DONE!" -ForegroundColor Green
Start-Process explorer.exe -ArgumentList "$ROOT\uploaded"

