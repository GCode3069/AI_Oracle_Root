# Test TikTok Automation System
# PowerShell test script

param(
    [string]$TestTopic = "student loan debt crisis",
    [string]$HorrorStyle = "psychological",
    [switch]$FullIntegrationTest
)

Write-Host "🧪 TESTING TIKTOK AUTOMATION SYSTEM" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

# Test Brand Integration
Write-Host "`n🏷️ Testing Brand Integration..." -ForegroundColor Yellow

$brandTest = @"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tiktok.brand_integration import NunyaBeznes2Brand

brand = NunyaBeznes2Brand()
branded_script = brand.inject_brand_voice("$TestTopic is destroying lives", "$HorrorStyle")
caption = brand.generate_tiktok_caption("$TestTopic", "$HorrorStyle")

print("BRAND INTEGRATION TEST:")
print(f"Original: $TestTopic is destroying lives")
print(f"Branded: {branded_script}")
print(f"Caption: {caption}")
"@

$brandTest | Out-File -FilePath "temp_brand_test.py" -Encoding utf8
python temp_brand_test.py

# Test Content Strategy
Write-Host "`n🎭 Testing Content Strategy..." -ForegroundColor Yellow

$strategyTest = @"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tiktok.brand_integration import TikTokContentStrategy

strategy = TikTokContentStrategy()
formats = []

for format_name, format_func in strategy.tiktok_formats.items():
    result = format_func("$TestTopic")
    formats.append(f"{format_name}: {result}")

print("CONTENT FORMATS:")
for fmt in formats:
    print(f"  - {fmt}")

sound = strategy.select_trending_sound("$HorrorStyle")
print(f"Recommended Sound: {sound}")
"@

$strategyTest | Out-File -FilePath "temp_strategy_test.py" -Encoding utf8
python temp_strategy_test.py

if ($FullIntegrationTest) {
    Write-Host "`n🚀 Testing Full Integration..." -ForegroundColor Yellow
    
    $integrationTest = @"
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tiktok.brand_integration import TikTokAutomation
from tiktok.upload_automation import TikTokUploader

# Test content adaptation
automation = TikTokAutomation()
tiktok_content = automation.adapt_youtube_content_for_tiktok(
    "Sample YouTube script about $TestTopic",
    "$TestTopic", 
    "$HorrorStyle"
)

print("TIKTOK CONTENT ADAPTATION:")
print(f"Script: {tiktok_content['script']}")
print(f"Caption: {tiktok_content['caption']}")
print(f"Format: {tiktok_content['content_format']}")
print(f"Sound: {tiktok_content['sound']}")

# Test uploader
uploader = TikTokUploader()
test_video = "sample_video.mp4"  # Would be real video in production
upload_result = uploader.generate_manual_instructions(test_video, tiktok_content['caption'], "#test")

print(f"Upload Result: {upload_result['status']}")
print(f"Method: {upload_result['method']}")
"@

    $integrationTest | Out-File -FilePath "temp_integration_test.py" -Encoding utf8
    python temp_integration_test.py
}

# Cleanup
Remove-Item "temp_*.py" -ErrorAction SilentlyContinue

Write-Host "`n✅ TikTok automation tests completed!" -ForegroundColor Green
