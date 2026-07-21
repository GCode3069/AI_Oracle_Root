# Process existing YouTube content for TikTok
# PowerShell batch processing script

param(
    [string]$YouTubeVideosPath = "abraham_horror/generated_videos",
    [int]$BatchSize = 10,
    [switch]$SchedulePosts,
    [switch]$TestMode
)

Write-Host "🔄 PROCESSING YOUTUBE CONTENT FOR TIKTOK" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor Magenta

if (!(Test-Path $YouTubeVideosPath)) {
    Write-Host "❌ YouTube videos path not found: $YouTubeVideosPath" -ForegroundColor Red
    Write-Host "Trying alternative paths..." -ForegroundColor Yellow
    
    $alternativePaths = @(
        "abraham_horror/videos",
        "videos",
        "generated_videos"
    )
    
    $found = $false
    foreach ($altPath in $alternativePaths) {
        if (Test-Path $altPath) {
            $YouTubeVideosPath = $altPath
            $found = $true
            Write-Host "✅ Using: $YouTubeVideosPath" -ForegroundColor Green
            break
        }
    }
    
    if (!$found) {
        Write-Host "❌ No video directory found. Please specify correct path." -ForegroundColor Red
        exit 1
    }
}

# Get YouTube videos
$youtubeVideos = Get-ChildItem $YouTubeVideosPath -Filter "*.mp4" -ErrorAction SilentlyContinue | Select-Object -First $BatchSize

if (!$youtubeVideos -or $youtubeVideos.Count -eq 0) {
    Write-Host "❌ No YouTube videos found in: $YouTubeVideosPath" -ForegroundColor Red
    Write-Host "`nTo generate test videos:" -ForegroundColor Yellow
    Write-Host "  python ABE_MASTER_GENERATOR.py --topic 'Test Video'" -ForegroundColor White
    exit 1
}

Write-Host "✅ Found $($youtubeVideos.Count) YouTube videos to process" -ForegroundColor Green

# Process each video
$processingCode = @"
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tiktok.upload_automation import TikTokContentPipeline

pipeline = TikTokContentPipeline()
processed_videos = []

youtube_videos = json.loads('''$($youtubeVideos | ConvertTo-Json -Compress)''')

for video_info in youtube_videos:
    video_path = video_info['FullName']
    topic = "corporate horror"  # Would extract from filename or metadata
    horror_style = "psychological"
    
    job = pipeline.process_youtube_content_for_tiktok(video_path, topic, horror_style)
    processed_videos.append(job)
    
    print(f"Processed: {video_info['Name']}")

print(f"Successfully processed {len(processed_videos)} videos for TikTok")
print("Videos are ready in the processing queue")

# Process queue if not in test mode
if not $TestMode:
    process_count = min(3, len(processed_videos))
    print(f"Processing first {process_count} videos from queue...")
    for i in range(process_count):
        result = pipeline.process_next_in_queue()
        print(f"Upload result {i+1}: {result['upload_result']['status']}")
"@

$processingCode | Out-File -FilePath "temp_process_videos.py" -Encoding utf8
python temp_process_videos.py

Remove-Item "temp_process_videos.py" -ErrorAction SilentlyContinue

if ($SchedulePosts) {
    Write-Host "`n📅 Scheduling TikTok posts..." -ForegroundColor Yellow
    
    $schedulingCode = @"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tiktok.scheduling import TikTokScheduler

scheduler = TikTokScheduler()

# Get processed content (this would come from the pipeline)
sample_content = [
    {'topic': 'Corporate Horror', 'content_format': 'educational_horror'},
    {'topic': 'Business Truths', 'content_format': 'story_time'},
    {'topic': 'Profit Nightmares', 'content_format': 'pov_content'}
]

scheduled = scheduler.schedule_content_batch(sample_content)
print(f"Scheduled {len(scheduled)} posts for TikTok")

# Show today's schedule
today_posts = scheduler.get_todays_schedule()
print(f"Today's scheduled posts: {len(today_posts)}")
"@

    $schedulingCode | Out-File -FilePath "temp_schedule.py" -Encoding utf8
    python temp_schedule.py
    Remove-Item "temp_schedule.py" -ErrorAction SilentlyContinue
}

Write-Host "`n✅ YouTube to TikTok processing completed!" -ForegroundColor Green
Write-Host "Check 'tiktok/upload_queue' for processed content" -ForegroundColor Yellow
