# KLING_CLIENT.py
import os
import time
import requests
from pathlib import Path

class KlingClient:
    """Client for Kling AI video generation API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("KLING_API_KEY")
        self.base_url = "https://api.kling.ai/v1"
        
    def generate_lipsync(self, audio_path, image_path, output_path=None):
        """
        Generate lip-sync video from audio and portrait image
        
        Args:
            audio_path: Path to audio file
            image_path: Path to portrait image
            output_path: Optional output path for video
            
        Returns:
            Path to generated video
        """
        if not self.api_key:
            raise ValueError("KLING_API_KEY not set")
        
        print(f"🎬 Generating lip-sync video...")
        print(f"   Audio: {audio_path}")
        print(f"   Portrait: {image_path}")
        
        # Prepare files
        audio_path = Path(audio_path)
        image_path = Path(image_path)
        
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Submit job
        task_id = self._submit_job(audio_path, image_path)
        print(f"   Task ID: {task_id}")
        
        # Poll for completion
        video_url = self._wait_for_completion(task_id)
        print(f"   Video URL: {video_url}")
        
        # Download video
        if output_path is None:
            output_path = Path(f"kling_output_{task_id}.mp4")
        
        self._download_video(video_url, output_path)
        print(f"✅ Video generated: {output_path}")
        
        return str(output_path)
    
    def _submit_job(self, audio_path, image_path):
        """Submit lip-sync generation job"""
        url = f"{self.base_url}/videos/lipsync"
        
        with open(audio_path, 'rb') as audio, open(image_path, 'rb') as image:
            files = {
                'audio': audio,
                'image': image
            }
            headers = {
                'Authorization': f'Bearer {self.api_key}'
            }
            
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            return data['task_id']
    
    def _wait_for_completion(self, task_id, timeout=300):
        """Wait for video generation to complete"""
        url = f"{self.base_url}/videos/{task_id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Video generation timed out after {timeout}s")
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            status = data['status']
            
            if status == 'completed':
                return data['video_url']
            elif status == 'failed':
                raise RuntimeError(f"Video generation failed: {data.get('error')}")
            
            print(f"   Status: {status}... waiting...")
            time.sleep(5)
    
    def _download_video(self, video_url, output_path):
        """Download generated video"""
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

def generate_lipsync_video(audio_path, image_path, output_path=None, api_key=None):
    """
    Convenience function to generate lip-sync video
    
    Args:
        audio_path: Path to audio file
        image_path: Path to portrait image
        output_path: Optional output path for video
        api_key: Optional API key (uses env var if not provided)
        
    Returns:
        Path to generated video
    """
    client = KlingClient(api_key=api_key)
    return client.generate_lipsync(audio_path, image_path, output_path)

if __name__ == "__main__":
    print("🎬 KLING AI CLIENT\n")
    print("Usage:")
    print("  from KLING_CLIENT import generate_lipsync_video")
    print("  video = generate_lipsync_video('audio.mp3', 'portrait.jpg')")
    print("\nEnvironment:")
    print(f"  KLING_API_KEY: {'✅ Set' if os.getenv('KLING_API_KEY') else '❌ Not set'}")
