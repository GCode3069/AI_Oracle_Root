#!/usr/bin/env python
"""Utility helpers for ElevenLabs TTS integration."""
import os
import requests
from pathlib import Path

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"

def _load_api_key():
    key = os.getenv("ELEVEN_LABS_API_KEY")
    if key:
        return key.strip()
    cred_path = Path(__file__).resolve().parent.parent / "credentials" / "ElevenLabs.key"
    if cred_path.exists():
        return cred_path.read_text(encoding="utf-8").strip()
    return None

def generate_elevenlabs_tts(text: str, output_path: str, voice: str = "jiminex") -> bool:
    """Generate TTS audio using ElevenLabs API."""
    api_key = _load_api_key()
    if not api_key:
        print("ElevenLabs API key not found.")
        return False
    headers = {"xi-api-key": api_key}
    payload = {"text": text}
    url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice}"
    resp = requests.post(url, json=payload, headers=headers, stream=True)
    if resp.status_code != 200:
        print(f"ERROR: ElevenLabs API returned {resp.status_code}: {resp.text}")
        return False
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f"Generated jiminex voice for {len(text)} characters...")
    return True

def list_voices():
    api_key = _load_api_key()
    if not api_key:
        print("ElevenLabs API key not found.")
        return
    headers = {"xi-api-key": api_key}
    resp = requests.get(f"{ELEVENLABS_API_URL}/voices", headers=headers)
    if resp.status_code != 200:
        print(f"ERROR: {resp.status_code} - {resp.text}")
        return
    data = resp.json()
    for voice in data.get("voices", []):
        print(f"{voice.get('voice_id')}: {voice.get('name')}")

if __name__ == "__main__":
    list_voices()
