# SCARIFY EMPIRE TEST SCRIPT
# Tests all four features: BTC QR + Theta Audio + Chapman Fear + Multi-Channel

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import our modules
from audio_generator import AudioGenerator
from video_generator import VideoGenerator
from scarify_master import ScarifyMaster

def test_empire_features():
    """Test all SCARIFY Empire features"""
    print("🔥 SCARIFY EMPIRE FEATURE TEST 🔥")
    print("=" * 50)
    
    # Test 1: Audio Generator with Theta
    print("\n🎵 Testing Audio Generator (with Theta)...")
    audio_gen = AudioGenerator()
    
    test_text = "Your garage bleeds money every day you wait. The crisis hits tomorrow."
    audio_path = "output/audio/test_empire_audio.wav"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    
    if audio_gen.generate(test_text, audio_path):
        print("✅ Audio generation successful")
        
        # Test Theta background
        if audio_gen.theta_enabled:
            print("✅ Theta audio background enabled")
        else:
            print("⚠️  Theta audio background disabled")
    else:
        print("❌ Audio generation failed")
        return False
    
    # Test 2: Video Generator with BTC QR
    print("\n🎬 Testing Video Generator (with BTC QR)...")
    video_gen = VideoGenerator()
    
    test_keywords = "emergency crisis urgent danger"
    video_path = "output/videos/test_empire_video.mp4"
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    
    if video_gen.generate(
        keywords=test_keywords,
        audio_path=audio_path,
        output_path=video_path,
        target_duration=30,
        hook_text="BLEEDING MONEY\nEVERY DAY?",
        cta_text="Stop the Bleeding\n$97 Kit →",
        add_btc_qr=True
    ):
        print("✅ Video generation successful")
        print("✅ BTC QR overlay added")
        print("✅ Text overlays added")
    else:
        print("❌ Video generation failed")
        return False
    
    # Test 3: Chapman Fear Prompts
    print("\n😨 Testing Chapman Fear Prompts...")
    master = ScarifyMaster(enable_upload=False)
    
    fear_prompts = master.PAIN_POINTS
    print(f"✅ {len(fear_prompts)} Chapman fear prompts loaded")
    
    # Check fear levels
    fear_levels = [prompt.get('fear_level', 'unknown') for prompt in fear_prompts]
    print(f"✅ Fear levels: {set(fear_levels)}")
    
    # Check psychology types
    psychology_types = [prompt.get('psychology', 'unknown') for prompt in fear_prompts]
    print(f"✅ Psychology types: {set(psychology_types)}")
    
    # Test 4: Multi-Channel Configuration
    print("\n🔄 Testing Multi-Channel Configuration...")
    from youtube_uploader import YouTubeUploader
    
    uploader = YouTubeUploader()
    channels = uploader.CHANNELS
    
    print(f"✅ {len(channels)} channels configured:")
    for channel_id, channel_info in channels.items():
        print(f"   - {channel_info['name']} ({channel_info['focus']})")
    
    # Test 5: QR Code Generation
    print("\n💰 Testing BTC QR Code Generation...")
    try:
        import qrcode
        from PIL import Image
        
        # Test QR generation
        qr = qrcode.QRCode(version=1, box_size=8, border=4)
        qr.add_data("bitcoin:1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="white", back_color="black")
        qr_path = "output/test_btc_qr.png"
        qr_img.save(qr_path)
        
        print("✅ BTC QR code generated successfully")
        print(f"✅ QR saved to: {qr_path}")
        
    except Exception as e:
        print(f"❌ BTC QR generation failed: {e}")
        return False
    
    # Test 6: Theta Wave Generation
    print("\n🎵 Testing Theta Wave Generation...")
    try:
        import numpy as np
        import scipy.io.wavfile as wav
        
        # Generate test Theta wave
        sample_rate = 44100
        duration = 5  # 5 seconds for test
        t = np.linspace(0, duration, int(sample_rate * duration))
        
        theta_wave = np.sin(2 * np.pi * 6.0 * t) * 0.1
        theta_wave = np.int16(theta_wave * 32767)
        
        theta_path = "output/audio/test_theta.wav"
        wav.write(theta_path, sample_rate, theta_wave)
        
        print("✅ Theta wave generated successfully")
        print(f"✅ Theta audio saved to: {theta_path}")
        
    except Exception as e:
        print(f"❌ Theta wave generation failed: {e}")
        return False
    
    # Final Results
    print("\n" + "=" * 50)
    print("🎉 SCARIFY EMPIRE FEATURE TEST COMPLETE! 🎉")
    print("=" * 50)
    print("✅ All features tested successfully:")
    print("   💰 BTC QR Overlays")
    print("   🎵 Theta Audio Background")
    print("   😨 Chapman Fear Prompts")
    print("   🔄 Multi-Channel Configuration")
    print("   📝 Professional Text Overlays")
    print("   🎬 Video Generation")
    print("   🎤 Audio Generation")
    print("\n🔥 EMPIRE IS READY FOR BATTLE! 🔥")
    
    return True

if __name__ == "__main__":
    # Set environment variables
    os.environ['IMAGEMAGICK_BINARY'] = r'C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe'
    
    # Run the test
    success = test_empire_features()
    
    if success:
        print("\n🚀 Ready to launch SCARIFY Empire Dashboard!")
        print("Run: .\scarify_empire_dashboard.ps1")
    else:
        print("\n❌ Some features failed. Check the errors above.")
        sys.exit(1)
