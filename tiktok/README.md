# 🎬 TikTok Automation System for @nunyabeznes2

Complete automation system for posting Abraham Lincoln horror content to TikTok with @nunyabeznes2 branding.

## 🎯 Features

- **Brand Integration**: Dark satirical business horror voice
- **Content Adaptation**: YouTube → TikTok format conversion
- **Upload Automation**: Multiple methods (Playwright, Selenium, Manual)
- **Smart Scheduling**: Optimal posting times (9AM, 12PM, 3PM, 6PM, 9PM)
- **Analytics Tracking**: Performance insights and recommendations

## 📁 Structure

```
tiktok/
├── brand_integration.py      # Brand voice and content strategy
├── upload_automation.py      # Upload methods and pipeline
├── scheduling.py             # Scheduling and analytics
├── __init__.py               # Package exports
├── generated_videos/         # TikTok-optimized videos
├── upload_queue/            # Videos ready for upload
├── analytics/                # Performance tracking
└── brand_assets/            # Brand logos and assets
```

## 🚀 Quick Start

### 1. Setup

```powershell
# Run setup script
.\Setup-TikTokAutomation.ps1
```

### 2. Test System

```powershell
# Test brand integration
.\Test-TikTokAutomation.ps1 -TestTopic "corporate greed" -HorrorStyle "psychological"

# Full integration test
.\Test-TikTokAutomation.ps1 -FullIntegrationTest
```

### 3. Process YouTube Content

```powershell
# Process existing YouTube videos for TikTok
.\Process-YouTubeForTikTok.ps1 -YouTubeVideosPath "abraham_horror/generated_videos" -BatchSize 5

# Process and schedule posts
.\Process-YouTubeForTikTok.ps1 -BatchSize 5 -SchedulePosts
```

## 📝 Usage Examples

### Brand Integration

```python
from tiktok.brand_integration import NunyaBeznes2Brand, TikTokAutomation

# Generate branded caption
brand = NunyaBeznes2Brand()
caption = brand.generate_tiktok_caption("corporate greed", "psychological")
print(caption)

# Adapt YouTube content for TikTok
automation = TikTokAutomation()
tiktok_content = automation.adapt_youtube_content_for_tiktok(
    "YouTube script here",
    "corporate horror",
    "psychological"
)
```

### Upload Video

```python
from tiktok.upload_automation import TikTokUploader

uploader = TikTokUploader()
result = uploader.upload_video(
    video_path="video.mp4",
    caption="🚨 Corporate horror 🚨\n\n#nunyabeznes #businesshorror\n@nunyabeznes2",
    hashtags="#nunyabeznes #businesshorror"
)

if result['status'] == 'SUCCESS':
    print(f"Uploaded: {result['url']}")
elif result['status'] == 'MANUAL_INSTRUCTIONS_GENERATED':
    print(f"Instructions: {result['instruction_file']}")
```

### Scheduling

```python
from tiktok.scheduling import TikTokScheduler

scheduler = TikTokScheduler()

# Schedule batch of content
content_batch = [
    {'topic': 'Corporate Horror', 'content_format': 'educational_horror'},
    {'topic': 'Business Truths', 'content_format': 'story_time'}
]

scheduled = scheduler.schedule_content_batch(content_batch)
print(f"Scheduled {len(scheduled)} posts")

# Get today's schedule
today_posts = scheduler.get_todays_schedule()
```

### Analytics

```python
from tiktok.scheduling import TikTokAnalytics

analytics = TikTokAnalytics()

# Track video performance
analytics.track_video_performance(
    video_data={'topic': 'Corporate Horror'},
    tiktok_url='https://tiktok.com/@nunyabeznes2/video/123',
    metrics={'views': 1000, 'likes': 50}
)

# Get insights
insights = analytics.get_performance_insights()
print(insights)
```

## 🎨 Brand Configuration

**Username**: @nunyabeznes2  
**Brand Voice**: Dark satirical business horror  
**Color Palette**: Red (#FF0000), Black (#000000), White (#FFFFFF)  
**Hashtags**: #nunyabeznes #businesshorror #corporatenightmare #profitsoverpeople

## 📅 Content Calendar

- **Monday**: Business Horrors, Corporate Truths
- **Tuesday**: Profit Nightmares, CEO Confessions
- **Wednesday**: Workplace Horror, Salary Secrets
- **Thursday**: Corporate Conspiracies, Business Lies
- **Friday**: Weekend Warning, Corporate Exposed
- **Saturday**: Dark Business Facts, Capitalism Horrors
- **Sunday**: Monday Preparation, Corporate Dread

## ⚙️ Upload Methods

1. **Playwright Automation** (Recommended)
   - Browser automation with Playwright
   - Requires manual login first time
   - Then fully automated

2. **Selenium Automation** (Alternative)
   - Similar to Playwright
   - Requires Selenium setup

3. **Manual Instructions** (Fallback)
   - Generates detailed upload instructions
   - Ensures content gets posted even if automation fails

## 🔧 Requirements

```bash
pip install playwright selenium
playwright install
```

## 📊 Analytics

Track performance metrics:
- Views
- Likes
- Engagement rate
- Best performing content
- Content recommendations

## 🎯 Content Formats

- **Educational Horror**: "3 signs your company is..."
- **Trend Jacking**: "POV: You discover..."
- **Story Time**: "Story time: How..."
- **POV Content**: "POV: You're a CEO..."
- **Green Screen**: "Reacting to... statistics"

## ✅ Status

**Production Ready** - All systems operational

For support or issues, check the main project documentation.
