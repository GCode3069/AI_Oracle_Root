#!/usr/bin/env python3
"""
SCARIFY Video Quality Analyzer & Voice Fixer v2.0
With YouTube Upload Integration
Custom Voice ID: 7aavy6c5cYIloDVj2JvH
"""

import os
import sys
import json
import subprocess
import wave
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import requests

class ScarifyQualityConfig:
    """Configuration for quality analysis and voice fixing"""
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')
    YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID', '')
    YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET', '')
    
    # YOUR CUSTOM VOICE ID
    CUSTOM_VOICE_ID = '7aavy6c5cYIloDVj2JvH'
    
    VOICE_PROFILES = {
        'scarify_custom': '7aavy6c5cYIloDVj2JvH',
        'horror_narrator': '21m00Tcm4TlvDq8ikWAM',
        'deep_male': 'VR6AewLTigWG4xSOukaG',
        'creepy_female': 'EXAVITQu4vr4xnSDxMaL',
        'ominous_male': 'pNInz6obpgDQGcFmaJgB',
        'whisper_female': 'ThT5KcBeYPX3keUQqHPh',
    }
    
    MIN_VIDEO_BITRATE = 2500
    MIN_AUDIO_BITRATE = 128
    MIN_RESOLUTION = (1280, 720)
    ROBOTIC_FREQUENCY_THRESHOLD = 0.3
    LOW_DYNAMIC_RANGE_THRESHOLD = 15
    
    ANALYSIS_OUTPUT = "F:/AI_Oracle_Root/scarify/analytics/quality_reports"
    TEMP_AUDIO = "F:/AI_Oracle_Root/scarify/temp/audio_analysis"
    FIXED_VIDEOS = "F:/AI_Oracle_Root/scarify/videos/elevenlabs_fixed"
    YOUTUBE_READY = "F:/AI_Oracle_Root/scarify/videos/youtube_ready"

class VideoQualityAnalyzer:
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        self.ffprobe_path = self._find_ffprobe()
        
    def _find_ffmpeg(self):
        try:
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True, check=True)
            return result.stdout.strip().split('\n')[0]
        except:
            return 'ffmpeg'
    
    def _find_ffprobe(self):
        try:
            result = subprocess.run(['where', 'ffprobe'], capture_output=True, text=True, check=True)
            return result.stdout.strip().split('\n')[0]
        except:
            return 'ffprobe'
    
    def analyze_video(self, video_path: str) -> Dict:
        print(f"\n🔍 Analyzing: {Path(video_path).name}")
        
        if not os.path.exists(video_path):
            return {'error': 'Video file not found'}
        
        analysis = {
            'file': video_path,
            'timestamp': datetime.now().isoformat(),
            'video_metrics': {},
            'audio_metrics': {},
            'quality_score': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            cmd = [
                self.ffprobe_path, '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
            if video_stream:
                width = int(video_stream.get('width', 0))
                height = int(video_stream.get('height', 0))
                bitrate = int(video_stream.get('bit_rate', 0)) / 1000
                
                analysis['video_metrics'] = {
                    'resolution': f"{width}x{height}",
                    'width': width,
                    'height': height,
                    'codec': video_stream.get('codec_name'),
                    'bitrate_kbps': bitrate,
                    'fps': eval(video_stream.get('r_frame_rate', '0/1'))
                }
                
                if width < ScarifyQualityConfig.MIN_RESOLUTION[0]:
                    analysis['issues'].append(f"Low resolution: {width}x{height}")
                    analysis['recommendations'].append("Upscale to at least 1280x720")
                
                if bitrate < ScarifyQualityConfig.MIN_VIDEO_BITRATE:
                    analysis['issues'].append(f"Low video bitrate: {bitrate:.0f} kbps")
            
            audio_stream = next((s for s in data['streams'] if s['codec_type'] == 'audio'), None)
            if audio_stream:
                audio_bitrate = int(audio_stream.get('bit_rate', 0)) / 1000
                
                analysis['audio_metrics'] = {
                    'codec': audio_stream.get('codec_name'),
                    'bitrate_kbps': audio_bitrate,
                    'sample_rate': int(audio_stream.get('sample_rate', 0)),
                    'channels': int(audio_stream.get('channels', 0))
                }
            
            analysis['duration'] = float(data['format'].get('duration', 0))
            analysis['size_mb'] = int(data['format'].get('size', 0)) / (1024 * 1024)
            
        except Exception as e:
            analysis['error'] = f"Analysis failed: {str(e)}"
            return analysis
        
        analysis['quality_score'] = self._calculate_quality_score(analysis)
        return analysis
    
    def _calculate_quality_score(self, analysis: Dict) -> int:
        score = 100
        vm = analysis.get('video_metrics', {})
        if vm.get('width', 0) < 1280:
            score -= 30
        elif vm.get('width', 0) < 1920:
            score -= 10
        if vm.get('bitrate_kbps', 0) < ScarifyQualityConfig.MIN_VIDEO_BITRATE:
            score -= 20
        am = analysis.get('audio_metrics', {})
        if am.get('bitrate_kbps', 0) < ScarifyQualityConfig.MIN_AUDIO_BITRATE:
            score -= 15
        return max(0, score)

class AudioQualityAnalyzer:
    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
    
    def _find_ffmpeg(self):
        try:
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True, check=True)
            return result.stdout.strip().split('\n')[0]
        except:
            return 'ffmpeg'
    
    def extract_audio(self, video_path: str, output_path: str) -> bool:
        try:
            cmd = [
                self.ffmpeg_path, '-i', video_path, '-vn',
                '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', '-y', output_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            return os.path.exists(output_path)
        except:
            return False
    
    def analyze_audio_quality(self, audio_path: str) -> Dict:
        print(f"🎵 Analyzing audio quality...")
        
        analysis = {
            'is_robotic': False,
            'quality_score': 100,
            'confidence': 0,
            'issues': [],
            'recommendations': []
        }
        
        try:
            with wave.open(audio_path, 'rb') as wav:
                frames = wav.readframes(wav.getnframes())
                sample_rate = wav.getframerate()
                audio_data = np.frombuffer(frames, dtype=np.int16)
                
                dynamic_range = self._calculate_dynamic_range(audio_data)
                analysis['dynamic_range_db'] = dynamic_range
                
                if dynamic_range < ScarifyQualityConfig.LOW_DYNAMIC_RANGE_THRESHOLD:
                    analysis['issues'].append(f"Low dynamic range: {dynamic_range:.1f} dB")
                    analysis['is_robotic'] = True
                    analysis['confidence'] += 0.3
                
                freq_score = self._analyze_frequency_patterns(audio_data, sample_rate)
                analysis['frequency_naturalness'] = freq_score
                
                if freq_score < 0.5:
                    analysis['issues'].append("Unnatural frequency patterns")
                    analysis['is_robotic'] = True
                    analysis['confidence'] += 0.4
                
                monotone_score = self._detect_monotone(audio_data)
                analysis['monotone_score'] = monotone_score
                
                if monotone_score > 0.7:
                    analysis['issues'].append("Monotone delivery detected")
                    analysis['is_robotic'] = True
                    analysis['confidence'] += 0.3
                
                if analysis['is_robotic']:
                    analysis['quality_score'] = 30
                    analysis['recommendations'].append("REPLACE WITH ELEVENLABS VOICE")
                
        except Exception as e:
            analysis['error'] = f"Audio analysis failed: {str(e)}"
        
        return analysis
    
    def _calculate_dynamic_range(self, audio_data: np.ndarray) -> float:
        if len(audio_data) == 0:
            return 0.0
        rms = np.sqrt(np.mean(audio_data.astype(float) ** 2))
        peak = np.abs(audio_data).max()
        if rms == 0:
            return 0.0
        return 20 * np.log10(peak / rms)
    
    def _analyze_frequency_patterns(self, audio_data: np.ndarray, sample_rate: int) -> float:
        fft = np.fft.fft(audio_data[:sample_rate * 5])
        frequencies = np.fft.fftfreq(len(fft), 1/sample_rate)
        magnitude = np.abs(fft)
        positive_mag = magnitude[:len(magnitude)//2]
        variance = np.var(positive_mag)
        max_val = np.max(positive_mag)
        if max_val == 0:
            return 0.5
        normalized_variance = variance / (max_val ** 2)
        return min(1.0, normalized_variance * 100)
    
    def _detect_monotone(self, audio_data: np.ndarray) -> float:
        window_size = 4410
        num_windows = len(audio_data) // window_size
        if num_windows < 2:
            return 0.5
        amplitudes = []
        for i in range(num_windows):
            window = audio_data[i*window_size:(i+1)*window_size]
            amp = np.sqrt(np.mean(window.astype(float) ** 2))
            amplitudes.append(amp)
        if len(amplitudes) == 0 or np.mean(amplitudes) == 0:
            return 0.5
        variation = np.std(amplitudes) / np.mean(amplitudes)
        return 1.0 - min(1.0, variation * 2)

class ElevenLabsVoiceFixer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def generate_voice(self, text: str, voice_id: str, output_path: str) -> bool:
        print(f"🎙️ Generating ElevenLabs voice...")
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.75,
                "style": 0.5,
                "use_speaker_boost": True
            }
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Voice generated successfully")
                return True
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Voice generation failed: {e}")
            return False
    
    def replace_video_audio(self, video_path: str, new_audio_path: str, output_path: str) -> bool:
        print(f"🎬 Replacing video audio...")
        try:
            ffmpeg_path = self._find_ffmpeg()
            cmd = [
                ffmpeg_path, '-i', video_path, '-i', new_audio_path,
                '-c:v', 'copy', '-map', '0:v:0', '-map', '1:a:0',
                '-c:a', 'aac', '-b:a', '192k', '-shortest', '-y', output_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            print(f"✅ Video audio replaced successfully")
            return True
        except Exception as e:
            print(f"❌ Audio replacement failed: {e}")
            return False
    
    def _find_ffmpeg(self):
        try:
            result = subprocess.run(['where', 'ffmpeg'], capture_output=True, text=True, check=True)
            return result.stdout.strip().split('\n')[0]
        except:
            return 'ffmpeg'

class YouTubeUploader:
    def prepare_for_upload(self, video_path: str, title: str = None, description: str = None) -> str:
        print(f"\n📤 Preparing video for YouTube upload...")
        os.makedirs(ScarifyQualityConfig.YOUTUBE_READY, exist_ok=True)
        youtube_filename = f"YT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{Path(video_path).name}"
        youtube_path = os.path.join(ScarifyQualityConfig.YOUTUBE_READY, youtube_filename)
        
        import shutil
        shutil.copy2(video_path, youtube_path)
        
        metadata = {
            'title': title or f"SCARIFY - {datetime.now().strftime('%Y-%m-%d')}",
            'description': description or "High-quality horror content created with SCARIFY system.",
            'tags': ['horror', 'scary', 'creepy', 'dark', 'atmospheric', 'scarify'],
            'category': '24',
            'privacy': 'unlisted',
            'original_file': video_path,
            'prepared_at': datetime.now().isoformat()
        }
        
        metadata_path = youtube_path.replace('.mp4', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Video ready for upload")
        print(f"📁 Location: {youtube_path}")
        return youtube_path
    
    def open_youtube_studio(self):
        import webbrowser
        print(f"\n🌐 Opening YouTube Studio...")
        webbrowser.open("https://studio.youtube.com")
        print(f"✅ YouTube Studio opened")
        print(f"\n📋 UPLOAD INSTRUCTIONS:")
        print(f"   1. Click 'CREATE' then 'Upload videos'")
        print(f"   2. Drag video from: {ScarifyQualityConfig.YOUTUBE_READY}")
        print(f"   3. Set as 'Unlisted' for quality check")
        print(f"   4. After checking, change to 'Public'")

class BatchVideoProcessor:
    def __init__(self, api_key: str):
        self.video_analyzer = VideoQualityAnalyzer()
        self.audio_analyzer = AudioQualityAnalyzer()
        self.voice_fixer = ElevenLabsVoiceFixer(api_key)
        self.youtube_uploader = YouTubeUploader()
        
        os.makedirs(ScarifyQualityConfig.ANALYSIS_OUTPUT, exist_ok=True)
        os.makedirs(ScarifyQualityConfig.TEMP_AUDIO, exist_ok=True)
        os.makedirs(ScarifyQualityConfig.FIXED_VIDEOS, exist_ok=True)
        os.makedirs(ScarifyQualityConfig.YOUTUBE_READY, exist_ok=True)
    
    def scan_video_directory(self, directory: str) -> List[str]:
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
        videos = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    videos.append(os.path.join(root, file))
        return videos
    
    def analyze_all_videos(self, directory: str) -> Dict:
        videos = self.scan_video_directory(directory)
        print(f"\n📊 SCARIFY Video Quality Analysis")
        print(f"{'='*60}")
        print(f"Found {len(videos)} videos\n")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_videos': len(videos),
            'analyzed': [],
            'robotic_voices_detected': [],
            'low_quality_videos': [],
            'summary': {}
        }
        
        for i, video_path in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}] {Path(video_path).name}")
            print("-" * 60)
            
            video_analysis = self.video_analyzer.analyze_video(video_path)
            temp_audio = os.path.join(ScarifyQualityConfig.TEMP_AUDIO, f"temp_{i}.wav")
            audio_analysis = {}
            
            if self.audio_analyzer.extract_audio(video_path, temp_audio):
                audio_analysis = self.audio_analyzer.analyze_audio_quality(temp_audio)
                try:
                    os.remove(temp_audio)
                except:
                    pass
            
            combined = {
                'video_path': video_path,
                'video_analysis': video_analysis,
                'audio_analysis': audio_analysis,
                'needs_voice_fix': audio_analysis.get('is_robotic', False),
                'quality_score': video_analysis.get('quality_score', 0)
            }
            
            results['analyzed'].append(combined)
            
            if audio_analysis.get('is_robotic'):
                results['robotic_voices_detected'].append(video_path)
                conf = audio_analysis.get('confidence', 0)
                print(f"⚠️ ROBOTIC VOICE - Confidence: {conf:.0%}")
            
            if video_analysis.get('quality_score', 100) < 70:
                results['low_quality_videos'].append(video_path)
        
        results['summary'] = {
            'total_analyzed': len(results['analyzed']),
            'robotic_voices': len(results['robotic_voices_detected']),
            'low_quality': len(results['low_quality_videos'])
        }
        
        report_path = os.path.join(
            ScarifyQualityConfig.ANALYSIS_OUTPUT,
            f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n{'='*60}")
        print(f"📊 ANALYSIS COMPLETE")
        print(f"✅ Videos: {results['summary']['total_analyzed']}")
        print(f"🤖 Robotic: {results['summary']['robotic_voices']}")
        print(f"📄 Report: {report_path}")
        
        return results
    
    def fix_video_voice(self, video_path: str, voice_profile: str = 'scarify_custom', 
                       script: Optional[str] = None, upload_to_youtube: bool = True) -> bool:
        print(f"\n🔧 FIXING VIDEO VOICE")
        print(f"{'='*60}")
        
        if script is None:
            json_path = Path(video_path).with_suffix('.json')
            if json_path.exists():
                try:
                    with open(json_path, 'r') as f:
                        metadata = json.load(f)
                        script = metadata.get('script') or metadata.get('description')
                except:
                    pass
        
        if not script:
            print("⚠️ No script provided")
            return False
        
        voice_id = ScarifyQualityConfig.VOICE_PROFILES.get(voice_profile, ScarifyQualityConfig.CUSTOM_VOICE_ID)
        
        temp_voice = os.path.join(
            ScarifyQualityConfig.TEMP_AUDIO,
            f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        )
        
        if not self.voice_fixer.generate_voice(script, voice_id, temp_voice):
            return False
        
        output_path = os.path.join(
            ScarifyQualityConfig.FIXED_VIDEOS,
            f"FIXED_{Path(video_path).name}"
        )
        
        success = self.voice_fixer.replace_video_audio(video_path, temp_voice, output_path)
        
        try:
            os.remove(temp_voice)
        except:
            pass
        
        if success:
            print(f"\n✅ VIDEO FIXED!")
            print(f"📁 {output_path}")
            
            if upload_to_youtube:
                youtube_path = self.youtube_uploader.prepare_for_upload(output_path)
                open_yt = input("\nOpen YouTube Studio? (y/n): ").strip().lower()
                if open_yt == 'y':
                    self.youtube_uploader.open_youtube_studio()
        
        return success

def main():
    print("\n🎬 SCARIFY QUALITY ANALYZER v2.0")
    print("=" * 60)
    print(f"🎙️ Voice: 7aavy6c5cYIloDVj2JvH")
    print("=" * 60)
    
    api_key = ScarifyQualityConfig.ELEVENLABS_API_KEY
    if not api_key:
        print("\n❌ ERROR: ELEVENLABS_API_KEY not found!")
        return
    
    print(f"✅ API key configured")
    processor = BatchVideoProcessor(api_key)
    
    while True:
        print("\n" + "=" * 60)
        print("MAIN MENU")
        print("=" * 60)
        print("1. Analyze videos")
        print("2. Fix video + Upload to YouTube")
        print("3. Fix all robotic voices")
        print("4. Test custom voice")
        print("5. Prepare video for YouTube")
        print("6. Exit")
        
        choice = input("\nSelect (1-6): ").strip()
        
        if choice == '1':
            directory = input("\nVideo directory: ").strip()
            if os.path.exists(directory):
                processor.analyze_all_videos(directory)
            else:
                print("❌ Directory not found!")
        
        elif choice == '2':
            video_path = input("\nVideo path: ").strip()
            if os.path.exists(video_path):
                script = input("\nScript (or Enter for metadata): ").strip() or None
                processor.fix_video_voice(video_path, 'scarify_custom', script, True)
            else:
                print("❌ Video not found!")
        
        elif choice == '3':
            reports = [f for f in os.listdir(ScarifyQualityConfig.ANALYSIS_OUTPUT) if f.endswith('.json')]
            if reports:
                latest = os.path.join(ScarifyQualityConfig.ANALYSIS_OUTPUT, sorted(reports)[-1])
                with open(latest, 'r') as f:
                    results = json.load(f)
                robotic = results['robotic_voices_detected']
                print(f"\nFound {len(robotic)} videos")
                if robotic:
                    fix = input("Fix all? (y/n): ").strip().lower()
                    if fix == 'y':
                        for v in robotic:
                            processor.fix_video_voice(v, 'scarify_custom', None, False)
            else:
                print("❌ No reports. Run analysis first!")
        
        elif choice == '4':
            test_text = input("\nTest text (or Enter for default): ").strip()
            if not test_text:
                test_text = "This is SCARIFY custom voice quality test."
            output = os.path.join(ScarifyQualityConfig.TEMP_AUDIO, f"test_{datetime.now().strftime('%H%M%S')}.mp3")
            fixer = ElevenLabsVoiceFixer(api_key)
            if fixer.generate_voice(test_text, ScarifyQualityConfig.CUSTOM_VOICE_ID, output):
                print(f"\n✅ Test voice: {output}")
                try:
                    os.startfile(output)
                except:
                    pass
        
        elif choice == '5':
            video_path = input("\nVideo path: ").strip()
            if os.path.exists(video_path):
                processor.youtube_uploader.prepare_for_upload(video_path)
                processor.youtube_uploader.open_youtube_studio()
            else:
                print("❌ Video not found!")
        
        elif choice == '6':
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
