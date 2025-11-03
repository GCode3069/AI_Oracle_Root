# GENERATE_CHATGPT_VIDEOS.ps1
# Generate ChatGPT_4o Battle Royale submission videos with OPTIMIZED TAGS

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  CHATGPT BATTLE ROYALE ENTRY - GENERATING 5 VIDEOS" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "COMPETITOR: ChatGPT_4o" -ForegroundColor Yellow
Write-Host "ROUND: 1" -ForegroundColor White
Write-Host "EPISODES: #30000-30004" -ForegroundColor White
Write-Host "FEATURE: OPTIMIZED TAGS (20-25 per video)`n" -ForegroundColor Green

# ChatGPT's 5 episodes with REAL optimized tags
$episodes = @(
    @{
        num = 30000
        title = "Lincoln's WARNING #30000: Digital Dollar TRAP Revealed #Shorts"
        script = "Stop scrolling. The digital dollar isn't convenience - it's control. Every transaction tracked, every purchase monitored. They're building your digital prison. Now you know. Bitcoin below."
        tags = @('abraham lincoln', 'lincoln horror', 'max headroom', 'digital dollar', 'CBDC', 'central bank digital currency', 'financial control', 'privacy', 'surveillance', 'cryptocurrency', 'bitcoin', 'scary', 'exposed', 'truth', 'warning', 'shorts', 'youtube shorts', 'viral', 'trending', 'conspiracy', 'political satire', 'dark comedy', 'government control', 'financial freedom', 'wake up')
    },
    @{
        num = 30001
        title = "Lincoln's WARNING #30001: AI Job Replacement DECEPTION #Shorts"
        script = "AI taking jobs? Look closer. They're not replacing workers - they're replacing middle managers. The elites stay in power, you get automated. Now you see the pattern. Bitcoin below."
        tags = @('abraham lincoln', 'lincoln horror', 'max headroom', 'AI jobs', 'automation', 'job replacement', 'artificial intelligence', 'unemployment', 'tech layoffs', 'future of work', 'elites', 'scary', 'exposed', 'truth', 'warning', 'shorts', 'youtube shorts', 'viral', 'political satire', 'dark comedy', 'ai takeover', 'robots replacing humans', 'unemployment crisis', 'wake up call')
    },
    @{
        num = 30002
        title = "Lincoln's WARNING #30002: Student Loan FORGIVENESS Scam #Shorts"
        script = "Student loan 'forgiveness'? It's not forgiveness - it's taxpayer transfer. They trapped you with debt, now they play hero with your own money. Now you know the game. Bitcoin below."
        tags = @('abraham lincoln', 'lincoln horror', 'max headroom', 'student loans', 'loan forgiveness', 'debt', 'college debt', 'education', 'student debt crisis', 'scam', 'taxpayer', 'exposed', 'truth', 'warning', 'shorts', 'youtube shorts', 'viral', 'political satire', 'dark comedy', 'financial trap', 'college scam', 'debt slavery', 'biden student loans')
    },
    @{
        num = 30003
        title = "Lincoln's WARNING #30003: Healthcare System DECEPTION #Shorts"
        script = "Healthcare debate? Look at the money. Insurance companies, pharma giants - they profit from your sickness. The system is designed to keep you sick. Now you see. Bitcoin below."
        tags = @('abraham lincoln', 'lincoln horror', 'max headroom', 'healthcare', 'health insurance', 'big pharma', 'medical system', 'insurance scam', 'pharmaceutical companies', 'healthcare crisis', 'exposed', 'truth', 'warning', 'shorts', 'youtube shorts', 'viral', 'political satire', 'dark comedy', 'medical industry', 'health conspiracy', 'system deception', 'profit over people')
    },
    @{
        num = 30004
        title = "Lincoln's WARNING #30004: Social Media ADDICTION Truth #Shorts"
        script = "Social media 'connecting people'? It's dividing you. Algorithms feed rage, destroy attention, isolate everyone. They profit from your loneliness. Now you know. Bitcoin below."
        tags = @('abraham lincoln', 'lincoln horror', 'max headroom', 'social media addiction', 'algorithm manipulation', 'facebook', 'instagram', 'tiktok', 'mental health', 'loneliness', 'isolation', 'exposed', 'truth', 'warning', 'shorts', 'youtube shorts', 'viral', 'political satire', 'dark comedy', 'tech manipulation', 'attention economy', 'social media toxic', 'digital addiction')
    }
)

Write-Host "Generating 5 ChatGPT videos with OPTIMIZED TAGS...`n" -ForegroundColor Cyan

foreach ($ep in $episodes) {
    Write-Host "[$($episodes.IndexOf($ep)+1)/5] Episode #$($ep.num)" -ForegroundColor Yellow
    Write-Host "  Title: $($ep.title)" -ForegroundColor White
    Write-Host "  Tags: $($ep.tags.Count) optimized tags" -ForegroundColor Green
    Write-Host "  Generating...`n" -ForegroundColor Cyan
    
    # Format tags for Python (JSON array)
    $tagsJson = ($ep.tags | ForEach-Object { "'$_'" }) -join ', '
    
    python -c "
import sys, json
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path.cwd()))

from abraham_MAX_HEADROOM import generate_voice, generate_lincoln_face_pollo, BASE_DIR
from CLEAN_UP_MESSY_VISUALS import create_clean_max_headroom
from YOUTUBE_TAG_OPTIMIZATION import format_tags_for_youtube

# Episode data
episode = $($ep.num)
title = '''$($ep.title)'''
script = '''$($ep.script)'''
tags = [$tagsJson]

print(f'Episode: #{episode}')
print(f'Script: {len(script.split())} words')
print(f'Tags: {len(tags)} (OPTIMIZED!)\n')

# Generate voice
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
audio_path = BASE_DIR / 'audio' / f'CHATGPT_{episode}_{timestamp}.mp3'
audio_path.parent.mkdir(parents=True, exist_ok=True)

if generate_voice(script, audio_path):
    lincoln = generate_lincoln_face_pollo()
    qr = BASE_DIR / 'qr_codes' / 'cashapp_qr.png'
    
    output = BASE_DIR / 'uploaded' / f'CHATGPT_{episode}_{timestamp}.mp4'
    output.parent.mkdir(parents=True, exist_ok=True)
    
    video = create_clean_max_headroom(lincoln, audio_path, output, qr)
    
    if video and Path(video).exists():
        size = Path(video).stat().st_size / (1024*1024)
        print(f'[OK] Video: {size:.1f} MB')
        
        # Upload with OPTIMIZED TAGS
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials
        import pickle
        
        # YouTube API upload with TAGS
        creds_pickle = Path('config/youtube_credentials.pickle')
        creds_json = Path('config/youtube_credentials.json')
        
        creds = None
        if creds_pickle.exists():
            with open(creds_pickle, 'rb') as f:
                creds = pickle.load(f)
        
        if creds and creds.valid:
            youtube = build('youtube', 'v3', credentials=creds)
            
            request_body = {
                'snippet': {
                    'title': title,
                    'description': f'''Abraham Lincoln roasts the headlines in Max Headroom glitchy style.

{script}

Support: https://cash.app/\$healthiwealthi/bitcoin

{', '.join('#' + t.replace(' ', '') for t in tags[:15])}''',
                    'tags': tags,  # OPTIMIZED TAGS HERE!
                    'categoryId': '24',  # Entertainment
                    'defaultLanguage': 'en',
                    'defaultAudioLanguage': 'en'
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False
                }
            }
            
            media = MediaFileUpload(str(video), chunksize=-1, resumable=True)
            
            request = youtube.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f'[Upload] {progress}%', end='\r')
            
            video_id = response['id']
            url = f'https://youtube.com/watch?v={video_id}'
            
            print(f'\n[UPLOADED] {url}')
            print(f'[TAGS] {len(tags)} tags applied!')
        else:
            print('[No YouTube credentials - video created but not uploaded]')
"
    
    Write-Host "  Waiting 30 seconds before next video...`n" -ForegroundColor Gray
    Start-Sleep -Seconds 30
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  CHATGPT ENTRY COMPLETE - ALL 5 VIDEOS" -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "All 5 ChatGPT videos generated with 20-25 OPTIMIZED TAGS each!" -ForegroundColor Green
Write-Host "Check YouTube Studio to verify uploads`n" -ForegroundColor Cyan

Write-Host "================================================================`n" -ForegroundColor Cyan


