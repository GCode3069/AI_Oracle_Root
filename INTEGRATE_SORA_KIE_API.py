#!/usr/bin/env python3
"""
INTEGRATE_SORA_KIE_API.py - Use Sora/KIE.ai for video generation

KIE.ai provides access to Sora and other video generation models
API Key: d3e70f88c536f7c2da06f8f57d5193e6

This can generate:
- Lip-sync videos (better than FFmpeg zoom)
- Smooth motion (better than static image)
- Professional quality
"""

import requests
import time
from pathlib import Path

KIE_API_KEY = "d3e70f88c536f7c2da06f8f57d5193e6"
KIE_API_BASE = "https://kie.ai/api"

def generate_lipsync_sora(lincoln_image: Path, audio_path: Path, output_path: Path, prompt: str = None):
    """
    Generate lip-sync video using Sora/KIE.ai
    
    Args:
        lincoln_image: Path to Lincoln image
        audio_path: Path to audio file
        output_path: Path to save output video
        prompt: Optional text prompt for video generation
    
    Returns:
        Path to generated video or None
    """
    
    print("[Sora/KIE] Generating lip-sync video...")
    
    if not lincoln_image.exists():
        print(f"[Sora/KIE] Image not found: {lincoln_image}")
        return None
    
    if not audio_path.exists():
        print(f"[Sora/KIE] Audio not found: {audio_path}")
        return None
    
    # Default prompt
    if not prompt:
        prompt = "Abraham Lincoln speaking, Max Headroom glitchy TV broadcast aesthetic, 1980s CRT television, realistic lip sync, VHS distortion, cyan tint"
    
    try:
        # Step 1: Upload image
        print("[Sora/KIE] Uploading image...")
        with open(lincoln_image, 'rb') as f:
            files = {'image': f}
            headers = {'Authorization': f'Bearer {KIE_API_KEY}'}
            
            upload_response = requests.post(
                f"{KIE_API_BASE}/upload",
                files=files,
                headers=headers,
                timeout=120
            )
        
        if upload_response.status_code != 200:
            print(f"[Sora/KIE] Upload failed: {upload_response.status_code}")
            print(f"[Sora/KIE] Response: {upload_response.text}")
            return None
        
        image_url = upload_response.json().get('url')
        print(f"[Sora/KIE] Image uploaded")
        
        # Step 2: Upload audio
        print("[Sora/KIE] Uploading audio...")
        with open(audio_path, 'rb') as f:
            files = {'audio': f}
            
            audio_response = requests.post(
                f"{KIE_API_BASE}/upload",
                files=files,
                headers=headers,
                timeout=120
            )
        
        if audio_response.status_code != 200:
            print(f"[Sora/KIE] Audio upload failed")
            return None
        
        audio_url = audio_response.json().get('url')
        print(f"[Sora/KIE] Audio uploaded")
        
        # Step 3: Generate video with lip-sync
        print("[Sora/KIE] Generating video (this may take 1-2 minutes)...")
        
        generation_data = {
            'image_url': image_url,
            'audio_url': audio_url,
            'prompt': prompt,
            'model': 'sora-lipsync',  # Or appropriate model name
            'resolution': '1080x1920',
            'fps': 25
        }
        
        gen_response = requests.post(
            f"{KIE_API_BASE}/generate/lipsync",
            json=generation_data,
            headers=headers,
            timeout=300
        )
        
        if gen_response.status_code != 200:
            print(f"[Sora/KIE] Generation failed: {gen_response.status_code}")
            print(f"[Sora/KIE] Response: {gen_response.text}")
            return None
        
        result = gen_response.json()
        task_id = result.get('task_id')
        
        # Step 4: Poll for completion
        print("[Sora/KIE] Waiting for video generation...")
        max_attempts = 60  # 5 minutes
        
        for attempt in range(max_attempts):
            status_response = requests.get(
                f"{KIE_API_BASE}/task/{task_id}",
                headers=headers
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data.get('status')
                
                if status == 'completed':
                    video_url = status_data.get('video_url')
                    
                    # Download video
                    print(f"[Sora/KIE] Downloading video...")
                    video_response = requests.get(video_url, timeout=300)
                    
                    if video_response.status_code == 200:
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, 'wb') as f:
                            f.write(video_response.content)
                        
                        size_mb = output_path.stat().st_size / (1024*1024)
                        print(f"[Sora/KIE] Success: {output_path.name} ({size_mb:.1f} MB)")
                        return output_path
                    
                elif status == 'failed':
                    print(f"[Sora/KIE] Generation failed: {status_data.get('error')}")
                    return None
                
                else:
                    # Still processing
                    print(f"[Sora/KIE] Status: {status}... ({attempt+1}/{max_attempts})")
                    time.sleep(5)
            
            time.sleep(5)
        
        print("[Sora/KIE] Timeout waiting for video")
        return None
        
    except Exception as e:
        print(f"[Sora/KIE] Error: {e}")
        return None

def test_kie_api():
    """Test if KIE API is working"""
    print("\n" + "="*60)
    print("TESTING KIE.AI API CONNECTION")
    print("="*60 + "\n")
    
    headers = {'Authorization': f'Bearer {KIE_API_KEY}'}
    
    try:
        # Test endpoint (check models available)
        response = requests.get(
            f"{KIE_API_BASE}/models",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            print("[OK] API connected successfully")
            models = response.json()
            print(f"[OK] Available models: {len(models)}")
            
            # List relevant models
            for model in models:
                if 'video' in model.get('name', '').lower() or 'lipsync' in model.get('name', '').lower():
                    print(f"  - {model.get('name')}: {model.get('description', 'N/A')}")
            
            return True
        else:
            print(f"[FAIL] API returned: {response.status_code}")
            print(f"[FAIL] Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Connection error: {e}")
        return False

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════╗
║              SORA/KIE.AI INTEGRATION                          ║
╚═══════════════════════════════════════════════════════════════╝

API Provider: kie.ai
API Key: d3e70f88c536f7c2da06f8f57d5193e6

Capabilities:
- Lip-sync video generation
- Smooth motion (better than static)
- Professional quality
- Fast generation (1-2 minutes)

This can replace:
- FFmpeg zoom fallback (static/corrupted)
- D-ID API (expensive)
- Wav2Lip local (complex setup)

""")
    
    # Test the API
    test_kie_api()


