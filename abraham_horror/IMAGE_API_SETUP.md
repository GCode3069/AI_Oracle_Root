# 🖼️ Image Generation API Setup

## Required Configuration

Edit `CHAPMAN_2025_YOUTUBE_AUTO.py` and update:

```python
# IMAGE GENERATION API - UPDATE WITH YOUR API ENDPOINT
IMAGE_API_URL = "https://api.yourapp.com/generate"  # Your API endpoint
IMAGE_API_KEY = "your_api_key_here"  # Your API key
```

## API Requirements

Your image generation API should accept:

### Request Format
```json
{
  "prompt": "Lincoln: The whistle's bribes, not arrivals...",
  "theme": "redacted_files_burning",
  "style": "horror_realistic",
  "resolution": "1080x1920",
  "api_key": "your_api_key"
}
```

### Expected Response
- Status: `200 OK`
- Body: Image file (JPEG/PNG) binary data
- Size: 1080x1920 pixels (vertical/portrait)

### Alternative: Authorization Header
If your API uses header auth instead of body:
```python
headers={"Authorization": f"Bearer {IMAGE_API_KEY}"}
```

## Fallback Behavior

If API fails or not configured:
- Script uses automatic fallback image generation
- Creates theme-based visuals (trains, rails, glitch effects)
- Videos still generate successfully

## Testing Your API

Test with curl:
```bash
curl -X POST "YOUR_API_URL" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "test",
    "theme": "test",
    "style": "horror_realistic",
    "resolution": "1080x1920"
  }' \
  --output test_image.jpg
```

## Next Steps

1. Add your API endpoint and key to script
2. Test with 1 video first
3. Check generated images in `temp/` folder
4. Scale up to batch generation


