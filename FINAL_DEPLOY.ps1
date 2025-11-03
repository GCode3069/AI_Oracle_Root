param([int]$NumRebels = 12)

Write-Host "🔥 FINAL DEPLOYMENT: $NumRebels REBELS" -ForegroundColor Red

# Create directories
mkdir output, output\scripts, output\audio, output\videos, assets\b-roll -Force

$pains = @(
    "Chicago garage supply meltdown", "Mechanic deadweight employees", "Barber no-show clients",
    "Plumber emergency call drought", "Welder material waste killing margins", "HVAC techs late to jobs", 
    "Electrician bidding too low", "Landscaper seasonal cash crash", "Auto detailer slow client flow",
    "Concrete crew bidding wars", "Painter lead gen drought", "Tow truck slow nights"
)

$successCount = 0

foreach ($i in 1..$NumRebels) {
    $pain = $pains[$i-1]
    Write-Host "`n--- REBEL $i: $pain ---" -ForegroundColor Magenta
    
    # Generate video using Python
    python -c "
import os
import random
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip

# Create video with text overlays
bg_color = ($(Get-Random -Maximum 100), $(Get-Random -Maximum 100), $(Get-Random -Maximum 100))
video_clip = ColorClip(size=(1080, 1920), color=bg_color, duration=15)

# Add title
title = TextClip('REBEL $i: $pain'.ToUpper(), fontsize=48, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2)
title = title.set_position(('center', 300)).set_duration(15)

# Add solution  
bleed = @(47,52,58,63,67,72,78,83,47,52,58,63)[$i-1]
solution = TextClip('`$$bleed K BLEED STOPPED', fontsize=36, color='yellow', font='Arial-Bold')
solution = solution.set_position(('center', 800)).set_duration(15)

# Add CTA
cta = TextClip('`$97 TRENCH KIT FIX', fontsize=32, color='white', font='Arial-Bold')
cta = cta.set_position(('center', 1600)).set_duration(15)

# Combine and export
final_clip = CompositeVideoClip([video_clip, title, solution, cta])
final_clip.write_videofile('output/videos/rebel_$i.mp4', fps=24, verbose=False, logger=None)

print('Video created: output/videos/rebel_$i.mp4')
"
    
    if (Test-Path "output/videos/rebel_$i.mp4") {
        $successCount++
        Write-Host "✅ REBEL $i CREATED" -ForegroundColor Green
    }
}

# Create X content
$xThread = @"
🚨 $successCount REBEL MP4s FORGED - DAWN `$6K LOCKED

$($pains[0..($successCount-1)] | ForEach { "• $_.ToUpper()" } | Out-String)

`$97 TRENCH KIT: https://gumroad.com/l/TRENCHKIT97
DM 'VIP' FOR CUSTOM FIX
"@

$xThread | Out-File "output/x_thread.txt" -Encoding UTF8

Write-Host "`n🎯 DEPLOYMENT COMPLETE" -ForegroundColor Green
Write-Host "📹 VIDEOS: $successCount/$NumRebels in output/videos/" -ForegroundColor White
Write-Host "🐦 X THREAD: output/x_thread.txt" -ForegroundColor White
Write-Host "💰 TARGET: `$$($successCount * 97 * 84) by 0600" -ForegroundColor Green
