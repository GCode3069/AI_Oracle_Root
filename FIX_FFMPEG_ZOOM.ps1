# FIX_FFMPEG_ZOOM.ps1
# Debug and fix the FFmpeg zoom filter issue

Write-Host "`n================================================================" -ForegroundColor Magenta
Write-Host "  DEBUGGING FFMPEG ZOOM FILTER" -ForegroundColor Magenta
Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "ISSUE:" -ForegroundColor Yellow
Write-Host "  FFmpeg zoom creates corrupted MP4 (moov atom not found)" -ForegroundColor White
Write-Host "  File: lipsync_XXXX.mp4 cannot be read`n" -ForegroundColor White

Write-Host "DIAGNOSIS:" -ForegroundColor Yellow
Write-Host "  Testing different zoom filter syntaxes...`n" -ForegroundColor White

# Test 1: Simple static zoom
Write-Host "[TEST 1] Simple static zoom..." -ForegroundColor Cyan
ffmpeg -loop 1 -i "assets/master_images/lincoln_optimized.jpg" `
    -f lavfi -i "anullsrc=r=44100:cl=stereo" `
    -filter_complex "[0:v]scale=1080:1080,zoompan=z=1.2:d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1080x1080[v]" `
    -map "[v]" -map "1:a" `
    -c:v libx264 -preset ultrafast -crf 23 `
    -c:a aac -b:a 128k `
    -t 5 -y `
    "test_zoom_simple.mp4" 2>&1 | Out-Null

if (Test-Path "test_zoom_simple.mp4") {
    $size = (Get-Item "test_zoom_simple.mp4").Length
    if ($size -gt 1000) {
        Write-Host "  [OK] Simple zoom works ($([math]::Round($size/1KB, 1)) KB)" -ForegroundColor Green
        $test1 = $true
    } else {
        Write-Host "  [FAIL] File too small" -ForegroundColor Red
        $test1 = $false
    }
} else {
    Write-Host "  [FAIL] File not created" -ForegroundColor Red
    $test1 = $false
}

# Test 2: Animated zoom (sin function)
Write-Host "`n[TEST 2] Animated zoom with sin function..." -ForegroundColor Cyan
ffmpeg -loop 1 -i "assets/master_images/lincoln_optimized.jpg" `
    -f lavfi -i "anullsrc=r=44100:cl=stereo" `
    -filter_complex "[0:v]scale=1080:1080,zoompan=z='1.0+0.2*sin(2*2*PI*t)':d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1080x1080[v]" `
    -map "[v]" -map "1:a" `
    -c:v libx264 -preset ultrafast -crf 23 `
    -c:a aac -b:a 128k `
    -t 5 -y `
    "test_zoom_animated.mp4" 2>&1 | Out-Null

if (Test-Path "test_zoom_animated.mp4") {
    $size = (Get-Item "test_zoom_animated.mp4").Length
    if ($size -gt 1000) {
        Write-Host "  [OK] Animated zoom works ($([math]::Round($size/1KB, 1)) KB)" -ForegroundColor Green
        $test2 = $true
    } else {
        Write-Host "  [FAIL] File too small" -ForegroundColor Red
        $test2 = $false
    }
} else {
    Write-Host "  [FAIL] File not created" -ForegroundColor Red
    $test2 = $false
}

# Test 3: With actual audio file (real scenario)
Write-Host "`n[TEST 3] With real audio file..." -ForegroundColor Cyan

# Find a real audio file
$audioFile = Get-ChildItem "audio" -Filter "*.mp3" | Select-Object -First 1

if ($audioFile) {
    Write-Host "  Using: $($audioFile.Name)" -ForegroundColor Gray
    
    ffmpeg -loop 1 -i "assets/master_images/lincoln_optimized.jpg" `
        -i $audioFile.FullName `
        -filter_complex "[0:v]scale=1080:1080,zoompan=z='1.0+0.2*sin(2*2*PI*t)':d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1080x1080[v]" `
        -map "[v]" -map "1:a" `
        -c:v libx264 -preset ultrafast -crf 23 `
        -c:a aac -b:a 128k `
        -shortest -y `
        "test_zoom_real.mp4" 2>&1 | Out-Null
    
    if (Test-Path "test_zoom_real.mp4") {
        $size = (Get-Item "test_zoom_real.mp4").Length
        if ($size -gt 1000) {
            Write-Host "  [OK] Real audio works ($([math]::Round($size/1MB, 1)) MB)" -ForegroundColor Green
            $test3 = $true
        } else {
            Write-Host "  [FAIL] File too small" -ForegroundColor Red
            $test3 = $false
        }
    } else {
        Write-Host "  [FAIL] File not created" -ForegroundColor Red
        $test3 = $false
    }
} else {
    Write-Host "  [SKIP] No audio files found" -ForegroundColor Yellow
    $test3 = $false
}

# Test 4: Verify with FFprobe
Write-Host "`n[TEST 4] Verifying file integrity..." -ForegroundColor Cyan

if (Test-Path "test_zoom_real.mp4") {
    $probe = ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "test_zoom_real.mp4" 2>&1
    
    if ($probe -match "^\d+\.?\d*$") {
        Write-Host "  [OK] File is valid (duration: $probe s)" -ForegroundColor Green
        $test4 = $true
    } else {
        Write-Host "  [FAIL] File corrupted: $probe" -ForegroundColor Red
        $test4 = $false
    }
} else {
    Write-Host "  [SKIP] No file to verify" -ForegroundColor Yellow
    $test4 = $false
}

# Summary
Write-Host "`n================================================================" -ForegroundColor Magenta
Write-Host "  TEST RESULTS" -ForegroundColor Magenta
Write-Host "================================================================`n" -ForegroundColor Magenta

Write-Host "Test 1 (Simple zoom):    $(if ($test1) {'PASS'} else {'FAIL'})" -ForegroundColor $(if ($test1) {'Green'} else {'Red'})
Write-Host "Test 2 (Animated zoom):  $(if ($test2) {'PASS'} else {'FAIL'})" -ForegroundColor $(if ($test2) {'Green'} else {'Red'})
Write-Host "Test 3 (Real audio):     $(if ($test3) {'PASS'} else {'FAIL'})" -ForegroundColor $(if ($test3) {'Green'} else {'Red'})
Write-Host "Test 4 (Integrity):      $(if ($test4) {'PASS'} else {'FAIL'})`n" -ForegroundColor $(if ($test4) {'Green'} else {'Red'})

if ($test1 -and $test2 -and $test3 -and $test4) {
    Write-Host "CONCLUSION:" -ForegroundColor Green
    Write-Host "  FFmpeg zoom filter works correctly!" -ForegroundColor White
    Write-Host "  Issue must be elsewhere in the code.`n" -ForegroundColor White
    
    Write-Host "LIKELY CAUSE:" -ForegroundColor Yellow
    Write-Host "  - Timeout during generation" -ForegroundColor White
    Write-Host "  - File path issue" -ForegroundColor White
    Write-Host "  - Incomplete FFmpeg process`n" -ForegroundColor White
    
    Write-Host "RECOMMENDED FIX:" -ForegroundColor Yellow
    Write-Host "  1. Increase timeout in abraham_MAX_HEADROOM.py" -ForegroundColor Cyan
    Write-Host "  2. Add better error checking" -ForegroundColor Cyan
    Write-Host "  3. Verify output file exists before using`n" -ForegroundColor Cyan
} else {
    Write-Host "CONCLUSION:" -ForegroundColor Red
    Write-Host "  FFmpeg zoom has issues on this system.`n" -ForegroundColor White
    
    Write-Host "RECOMMENDED SOLUTION:" -ForegroundColor Yellow
    Write-Host "  Use Wav2Lip instead (run: .\SETUP_WAV2LIP_LOCAL.ps1)`n" -ForegroundColor Cyan
}

Write-Host "TEST FILES CREATED:" -ForegroundColor Yellow
if (Test-Path "test_zoom_simple.mp4") { Write-Host "  - test_zoom_simple.mp4" -ForegroundColor White }
if (Test-Path "test_zoom_animated.mp4") { Write-Host "  - test_zoom_animated.mp4" -ForegroundColor White }
if (Test-Path "test_zoom_real.mp4") { Write-Host "  - test_zoom_real.mp4" -ForegroundColor White }

Write-Host "`nWatch these files to see zoom effects in action.`n" -ForegroundColor Gray

Write-Host "================================================================`n" -ForegroundColor Magenta


