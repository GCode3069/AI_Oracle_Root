import os
import random
import time
import json
import logging
from pathlib import Path
from faker import Faker
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from instagrapi import Client  # For Instagram Reels
import requests

# Setup logging
logging.basicConfig(filename='phantom_upload.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
SOURCE_ROOT = "F:\\Extreme SSD\\SCARIFY_CONSOLIDATED"
CLIENT_SECRETS = {
    "youtube": "client_secrets_youtube.json",
    "instagram": {"username": "your_instagram_user", "password": "your_instagram_pass"}
}
PROXIES_FILE = "proxies.json"
MAX_UPLOADS = 10
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
ARCHETYPES = {"Mystic": {"tags": ["mystic", "brainwave"], "p": 10}, "Rebel": {"tags": ["rebel", "freedom"], "p": 8}}

# Helper functions
def meta(archetype, platform):
    tags = ARCHETYPES[archetype]["tags"]
    if platform == "youtube":
        return {"title": f"{random.choice(tags)}#{random.randint(1,100)}", "desc": f"{archetype} void.", "tags": tags + ["shorts"]}
    elif platform == "instagram":
        return {"caption": f"{archetype} void #{random.choice(tags)} #reels", "tags": tags}

def proxy():
    return json.load(open(PROXIES_FILE)).get('http')

def service(platform):
    if platform == "youtube":
        return build('youtube', 'v3', credentials=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS["youtube"], SCOPES).run_local_server(port=0))
    elif platform == "instagram":
        return Client()

def upload(video, meta, platform):
    try:
        if platform == "youtube":
            body = {"snippet": {"title": meta["title"], "description": meta["desc"], "tags": meta["tags"], "categoryId": "22"}, "status": {"privacyStatus": "public"}}
            media = MediaFileUpload(video, resumable=True)
            session = requests.Session()
            if proxy(): session.proxies = {"http": proxy()}
            request = service("youtube").videos().insert(part="snippet,status", body=body, media_body=media)
            response = request.execute_with_session(session)
            logging.info(f"✅ YouTube: {meta['title']} (ID: {response['id']})")
        elif platform == "instagram":
            cl = service("instagram")
            cl.login(CLIENT_SECRETS["instagram"]["username"], CLIENT_SECRETS["instagram"]["password"])
            media = cl.video_upload(video, caption=meta["caption"])
            logging.info(f"✅ Instagram: {meta['caption']} (ID: {media.id})")
    except Exception as e:
        logging.error(f"❌ {platform} failed: {e}")

# Main execution logic
platforms = ["youtube", "instagram"]
files = {archetype: list(Path(SOURCE_ROOT).glob(f"**/{archetype}/*.mp4")) for archetype in ARCHETYPES}
for platform in platforms:
    for _ in range(min(MAX_UPLOADS//len(platforms), sum(len(v) for v in files.values()))):
        archetype = max(files, key=lambda k: ARCHETYPES[k]["p"])
        if files[archetype]:
            upload(files[archetype].pop(0), meta(archetype, platform), platform)
            delay = random.randint(7200, 43200)
            time.sleep(delay)
            logging.info(f"⏰ {platform} next in {delay}s")
logging.info("🎉 Upload cycle done")