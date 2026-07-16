"""
KLING_CLIENT.py
Kling AI API client for lip-sync video generation.
"""

import os
import time
import requests
from typing import Optional, Dict
from pathlib import Path


class KlingClient:
    """Client for Kling AI lip-sync video generation API."""
    
    def __init__(self, api_key: str):
        """
        Initialize Kling client.
        
        Args:
            api_key: Kling AI API key
        """
        self.api_key = api_key
        self.base_url = "https://api.klingai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    def generate_talking_head(
        self,
        audio_path: str,
        image_path: str,
        output_dir: str = "./output",
        poll_interval: int = 10,
        max_wait_time: int = 300
    ) -> Optional[str]:
        """
        Generate talking head video with lip-sync.
        
        Args:
            audio_path: Path to audio file (MP3/WAV)
            image_path: Path to portrait image (JPG/PNG)
            output_dir: Directory to save output video
            poll_interval: Seconds between status checks (default: 10)
            max_wait_time: Maximum seconds to wait for completion (default: 300)
            
        Returns:
            Path to generated video file, or None if failed
        """
        # Validate inputs
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"[KLING] Submitting job...")
        print(f"  Audio: {audio_path}")
        print(f"  Image: {image_path}")
        
        # Submit generation job
        task_id = self._submit_job(audio_path, image_path)
        if not task_id:
            print("[KLING] ❌ Failed to submit job")
            return None
        
        print(f"[KLING] Task ID: {task_id}")
        print(f"[KLING] Polling every {poll_interval}s (max {max_wait_time}s)...")
        
        # Poll for completion
        start_time = time.time()
        while True:
            elapsed = time.time() - start_time
            
            if elapsed > max_wait_time:
                print(f"[KLING] ❌ Timeout after {max_wait_time}s")
                return None
            
            status_data = self._check_status(task_id)
            if not status_data:
                print("[KLING] ❌ Failed to check status")
                return None
            
            status = status_data.get("status")
            print(f"[KLING] Status: {status} (elapsed: {elapsed:.0f}s)")
            
            if status == "completed":
                video_url = status_data.get("result", {}).get("video_url")
                if video_url:
                    output_path = self._download_video(video_url, output_dir, task_id)
                    print(f"[KLING] ✅ Video saved: {output_path}")
                    return output_path
                else:
                    print("[KLING] ❌ No video URL in response")
                    return None
                    
            elif status == "failed":
                error = status_data.get("error", "Unknown error")
                print(f"[KLING] ❌ Generation failed: {error}")
                return None
            
            # Wait before next poll
            time.sleep(poll_interval)
    
    def _submit_job(self, audio_path: str, image_path: str) -> Optional[str]:
        """Submit video generation job to Kling API."""
        try:
            # Upload files first
            audio_url = self._upload_file(audio_path, "audio")
            image_url = self._upload_file(image_path, "image")
            
            if not audio_url or not image_url:
                return None
            
            # Submit generation request
            url = f"{self.base_url}/videos/generations"
            payload = {
                "model": "kling-v1",
                "type": "lip_sync",
                "audio_url": audio_url,
                "image_url": image_url,
                "duration": "auto"
            }
            
            response = requests.post(url, json=payload, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            return data.get("task_id")
            
        except Exception as e:
            print(f"[KLING] Submit error: {e}")
            return None
    
    def _upload_file(self, file_path: str, file_type: str) -> Optional[str]:
        """Upload file to Kling storage and return URL."""
        try:
            url = f"{self.base_url}/files/upload"
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'type': file_type}
                
                # Use separate headers for file upload
                upload_headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                response = requests.post(
                    url,
                    files=files,
                    data=data,
                    headers=upload_headers,
                    timeout=60
                )
                response.raise_for_status()
                
                result = response.json()
                return result.get("url")
                
        except Exception as e:
            print(f"[KLING] Upload error for {file_type}: {e}")
            return None
    
    def _check_status(self, task_id: str) -> Optional[Dict]:
        """Check generation status."""
        try:
            url = f"{self.base_url}/videos/generations/{task_id}"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"[KLING] Status check error: {e}")
            return None
    
    def _download_video(self, video_url: str, output_dir: str, task_id: str) -> str:
        """Download generated video."""
        try:
            response = requests.get(video_url, timeout=120)
            response.raise_for_status()
            
            # Save with task ID in filename
            output_path = os.path.join(output_dir, f"kling_{task_id}.mp4")
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            return output_path
            
        except Exception as e:
            print(f"[KLING] Download error: {e}")
            raise
    
    def get_account_info(self) -> Optional[Dict]:
        """Get account information including credit balance."""
        try:
            url = f"{self.base_url}/account"
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f"[KLING] Account info error: {e}")
            return None


# Mock client for testing without API calls
class MockKlingClient(KlingClient):
    """Mock Kling client for testing without making real API calls."""
    
    def __init__(self, api_key: str = "mock_key"):
        super().__init__(api_key)
        self.mock_delay = 2  # Simulate 2 second generation
    
    def generate_talking_head(
        self,
        audio_path: str,
        image_path: str,
        output_dir: str = "./output",
        poll_interval: int = 10,
        max_wait_time: int = 300
    ) -> Optional[str]:
        """Mock generation that returns a dummy video path."""
        print(f"[MOCK KLING] Simulating generation...")
        print(f"  Audio: {audio_path}")
        print(f"  Image: {image_path}")
        
        # Simulate processing time
        time.sleep(self.mock_delay)
        
        # Create mock output
        os.makedirs(output_dir, exist_ok=True)
        mock_path = os.path.join(output_dir, "mock_kling_output.mp4")
        
        # Create empty file
        Path(mock_path).touch()
        
        print(f"[MOCK KLING] ✅ Mock video created: {mock_path}")
        return mock_path


if __name__ == "__main__":
    # Test with mock client
    print("=== KLING Client Test (Mock Mode) ===\n")
    
    client = MockKlingClient()
    
    # Create test files
    os.makedirs("test_input", exist_ok=True)
    Path("test_input/test_audio.mp3").touch()
    Path("test_input/test_image.jpg").touch()
    
    # Test generation
    result = client.generate_talking_head(
        audio_path="test_input/test_audio.mp3",
        image_path="test_input/test_image.jpg",
        output_dir="test_output"
    )
    
    if result:
        print(f"\n✅ Success! Video at: {result}")
    else:
        print("\n❌ Generation failed")
    
    # Cleanup
    import shutil
    shutil.rmtree("test_input", ignore_errors=True)
    shutil.rmtree("test_output", ignore_errors=True)
