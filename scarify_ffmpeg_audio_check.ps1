param (
    [string]$audio_dir = "F:\AI_Oracle_Root\scarify\output\audio\new",
    [string]$output_dir = "F:\AI_Oracle_Root\scarify\output\videos\fixed"
)

# Ensure output directory exists
if (-not (Test-Path $output_dir)) {
    New-Item -ItemType Directory -Path $output_dir | Out-Null
}

$audio_file = Join-Path $audio_dir "Rebel_narration_20251020_230050.mp3"
$video_file = Join-Path $output_dir "video_6.mp4"

if (Test-Path $audio_file) {
    $ffmpeg_cmd = @(
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", "color=color=#FF6B6B:size=1080x1920:duration=15",
        "-i", "`"$audio_file`"",
        "-vf", "drawtext=text='Revolution begins':fontcolor=white:fontsize=48:box=1:boxcolor=black@0.5:boxborderw=5:x=(w-text_w)/2:y=(h-text_h)/2",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "`"$video_file`""
    ) -join " "

    Write-Host "🎬 Running FFmpeg to generate video..." -ForegroundColor Cyan
    $result = & cmd /c $ffmpeg_cmd

    if (Test-Path $video_file) {
        Write-Host "✅ Generated video: $video_file"
    } else {
        Write-Host "❌ FFmpeg failed to create video."
    }
} else {
    Write-Host "❌ Audio file missing: $audio_file" -ForegroundColor Red
}

Write-Host "`n🎉 AUTOMATION COMPLETE!"
Write-Host "✅ Check: $output_dir"
Pause