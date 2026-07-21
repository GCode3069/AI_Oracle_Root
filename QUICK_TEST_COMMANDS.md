# 🧪 Quick Test Commands

## Test TikTok System

```bash
# Test optimization, captions, and branding
python TEST_TIKTOK_SYSTEM.py
```

## Test YouTube Uploader

```bash
# Test authentication
python upload/youtube_upload_enhanced.py --test-auth

# Test upload (requires video file)
python upload/youtube_upload_enhanced.py video.mp4 --title "Test Video" --description "Test" --tags shorts test
```

## Generate Test Video

```bash
# Generate a test video
python ABE_MASTER_GENERATOR.py --topic "Corporate Horror Test"

# Generate and optimize for TikTok
python ABE_MASTER_GENERATOR.py --topic "Test" && \
python TIKTOK_AUTOMATION_SYSTEM.py --optimize abraham_horror/generated_videos/ABRAHAM_*.mp4
```

## Test TikTok Optimization on Existing Videos

```bash
# If videos exist in abraham_horror/videos/
python TIKTOK_AUTOMATION_SYSTEM.py --optimize abraham_horror/videos/MAX_HEADROOM_*.mp4

# Batch optimize 3 videos
python TIKTOK_AUTOMATION_SYSTEM.py --batch abraham_horror/videos --limit 3
```

## Verify Branding

```bash
# Check brand config
python -c "from TIKTOK_AUTOMATION_SYSTEM import BRAND_CONFIG; print(BRAND_CONFIG)"

# Test caption generation
python -c "from TIKTOK_AUTOMATION_SYSTEM import TikTokCaptionGenerator; gen = TikTokCaptionGenerator(); print(gen.generate_caption('Corporate Horror'))"
```

## Full Pipeline Test

```bash
# Generate → Optimize → Upload to TikTok
python ABE_MASTER_GENERATOR.py --topic "Business Nightmare" && \
python TIKTOK_AUTOMATION_SYSTEM.py --full abraham_horror/generated_videos/ABRAHAM_*.mp4 --topic "Business Nightmare"
```
