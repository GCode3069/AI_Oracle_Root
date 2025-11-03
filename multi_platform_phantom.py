# multi_platform_phantom.py - 2025 Compact Shadow Uploader
import os, random, time, json
from faker import Faker
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

fake = Faker()
SOURCE_ROOT = "F:\\Extreme SSD\\SCARIFY_CONSOLIDATED"
CLIENT_SECRETS = {"youtube": "client_secrets_youtube.json"}
PROXIES_FILE = "proxies.json"
MAX_UPLOADS = 10
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
ARCHETYPES = {"Mystic": {"tags": ["mystic", "brainwave"], "p": 10}, "Rebel": {"tags": ["rebel", "freedom"], "p": 8}}

def meta(archetype): return {"title": f"{random.choice(ARCHETYPES[archetype]['tags'])}#{random.randint(1,100)}", "desc": f"{archetype} void.", "tags": ARCHETYPES[archetype]["tags"]}
def proxy(): return json.load(open(PROXIES_FILE))['http']
def service(): return build('youtube', 'v3', credentials=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS["youtube"], SCOPES).run_local_server(port=0))

def upload(video, meta):
    body = {"snippet": {"title": meta["title"], "description": meta["desc"], "tags": meta["tags"], "categoryId": "22"}, "status": {"privacyStatus": "public"}}
    media = MediaFileUpload(video, resumable=True)
    service().videos().insert(part="snippet,status", body=body, media_body=media).execute_with_session(session=requests.Session(proxies={"http": proxy()}))

files = {f.split("\\")[-2]: f for f in os.listdir(SOURCE_ROOT) if any(a in f for a in ARCHETYPES)}
for _ in range(min(MAX_UPLOADS, len(files))):
    archetype = max(files, key=lambda k: ARCHETYPES[k]["p"])
    upload(os.path.join(SOURCE_ROOT, files.pop(archetype)), meta(archetype))
    time.sleep(random.randint(7200, 43200))

print("Upload cycle done.")