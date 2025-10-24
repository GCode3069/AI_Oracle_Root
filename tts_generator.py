#!/usr/bin/env python3
"""
SCARIFY TTS Generator - Crash-Resistant Text-to-Speech
Handles audio generation with ElevenLabs API and fallback options
"""

import os
import sys
import time
import logging
import requests
from pathlib import Path
from typing import Optional, Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config/credentials/.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scarify/Output/tts_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TTSGenerator:
    """Crash-resistant TTS generator with multiple fallback options"""
    
    def __init__(self):
        self.elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
        self.max_retries = 3
        self.timeout = 30
        
    def generate_with_elevenlabs(self, text: str, voice: str = "Matthew", 
                                output_path: str = None) -> Optional[str]:
        """Generate audio using ElevenLabs API with retry logic"""
        
        if not self.elevenlabs_key or self.elevenlabs_key == 'test_key_for_demo':
            logger.warning("ElevenLabs API key not configured, using fallback")
            return self.generate_fallback(text, output_path)
        
        if not output_path:
            timestamp = int(time.time())
            output_path = f"scarify/Output/audio_{timestamp}.mp3"
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"ElevenLabs TTS attempt {attempt + 1}/{self.max_retries}")
                
                headers = {
                    'Authorization': f'Bearer {self.elevenlabs_key}',
                    'Content-Type': 'application/json'
                }
                
                data = {
                    "text": text,
                    "voice": voice,
                    "model_id": "eleven_monolingual_v1"
                }
                
                response = requests.post(
                    'https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM',
                    headers=headers,
                    json=data,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    
                    logger.info(f"✅ ElevenLabs TTS successful: {output_path}")
                    return output_path
                else:
                    logger.error(f"ElevenLabs API error: {response.status_code} - {response.text}")
                    if attempt < self.max_retries - 1:
                        time.sleep(5)
                    
            except requests.exceptions.Timeout:
                logger.error(f"ElevenLabs timeout on attempt {attempt + 1}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
            except Exception as e:
                logger.error(f"ElevenLabs error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
        
        logger.error("❌ ElevenLabs TTS failed after all retries")
        return self.generate_fallback(text, output_path)
    
    def generate_fallback(self, text: str, output_path: str = None) -> Optional[str]:
        """Fallback TTS using gTTS (Google Text-to-Speech)"""
        try:
            from gtts import gTTS
            import io
            
            logger.info("Using gTTS fallback")
            
            if not output_path:
                timestamp = int(time.time())
                output_path = f"scarify/Output/audio_fallback_{timestamp}.mp3"
            
            # Ensure output directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_path)
            
            logger.info(f"✅ Fallback TTS successful: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("gTTS not available, installing...")
            os.system("pip install gtts")
            return self.generate_fallback(text, output_path)
        except Exception as e:
            logger.error(f"Fallback TTS failed: {e}")
            return None
    
    def generate_audio(self, text: str, voice: str = "Matthew", 
                      output_path: str = None) -> Optional[str]:
        """Main method to generate audio with fallback"""
        
        logger.info(f"Generating TTS for text: {text[:50]}...")
        
        # Try ElevenLabs first
        result = self.generate_with_elevenlabs(text, voice, output_path)
        
        if result and os.path.exists(result):
            return result
        
        # Fallback to gTTS
        logger.warning("Falling back to gTTS")
        return self.generate_fallback(text, output_path)

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python tts_generator.py <text> [voice] [output_path]")
        sys.exit(1)
    
    text = sys.argv[1]
    voice = sys.argv[2] if len(sys.argv) > 2 else "Matthew"
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Create TTS generator
    tts = TTSGenerator()
    
    # Generate audio
    result = tts.generate_audio(text, voice, output_path)
    
    if result:
        print(f"✅ SUCCESS: {result}")
        sys.exit(0)
    else:
        print("❌ TTS generation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()