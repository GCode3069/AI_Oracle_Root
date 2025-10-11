# 🔍 Troubleshooting Guide

## Overview

This comprehensive troubleshooting guide covers common issues, diagnostic procedures, and solutions for the Oracle Horror Production System.

## Quick Diagnostic Commands

```powershell
# System health check
.\MasterControl.ps1 -Operation status -Verbose

# Comprehensive diagnostics
.\scripts\system_diagnostics.ps1 -Full

# Check specific component
.\scripts\diagnose_component.ps1 -Component "voiceover_vault"
```

## Common Issues and Solutions

### 🚨 MasterControl.ps1 Issues

#### Issue: Script Won't Start

**Symptoms:**
- PowerShell execution policy errors
- File not found errors
- Permission denied errors

**Diagnosis:**
```powershell
# Check execution policy
Get-ExecutionPolicy

# Check file existence and permissions
Test-Path ".\MasterControl.ps1"
Get-Acl ".\MasterControl.ps1"

# Check PowerShell version
$PSVersionTable.PSVersion
```

**Solutions:**
```powershell
# Set execution policy (run as administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Fix file permissions
icacls ".\MasterControl.ps1" /grant:r "$env:USERNAME:(R,X)"

# Run with explicit PowerShell version
powershell.exe -File ".\MasterControl.ps1" -Operation status
```

#### Issue: Invalid Operation Error

**Symptoms:**
```
❌ Invalid operation: [operation_name]
Valid operations: status, execute, test
```

**Solution:**
```powershell
# Use correct operation names
.\MasterControl.ps1 -Operation status     # ✅ Correct
.\MasterControl.ps1 -Operation execute    # ✅ Correct
.\MasterControl.ps1 -Operation test       # ✅ Correct

# Check available operations
Get-Help .\MasterControl.ps1 -Detailed
```

### 🚨 Google Sheets Integration Issues

#### Issue: Authentication Failed

**Symptoms:**
```
📊 Google Sheets: ❌ Token missing
Failed to authenticate with Google Sheets API
```

**Diagnosis:**
```powershell
# Check for token file
Test-Path "token_sheets_rw.pickle"

# Check credentials file
Test-Path "credentials/google_credentials.json"

# Test Google API connectivity
.\scripts\test_google_connectivity.ps1
```

**Solutions:**
```powershell
# Remove old token and re-authenticate
Remove-Item "token_sheets_rw.pickle" -Force -ErrorAction SilentlyContinue

# Verify credentials file format
Get-Content "credentials/google_credentials.json" | ConvertFrom-Json

# Re-run authentication setup
python scripts/setup_google_auth.py

# Test authentication
.\scripts\test_google_sheets.ps1
```

#### Issue: API Quota Exceeded

**Symptoms:**
```
Google Sheets API quota exceeded
Rate limit error: 429 Too Many Requests
```

**Solutions:**
```powershell
# Check current API usage
.\scripts\check_google_quota.ps1

# Implement rate limiting
$config = @{
    "googleSheets" = @{
        "requestsPerMinute" = 60
        "batchSize" = 25
    }
}

# Wait and retry
Start-Sleep -Seconds 60
.\MasterControl.ps1 -Operation execute -Force
```

### 🚨 Voice Generation Issues

#### Issue: TTS API Authentication Failed

**Symptoms:**
```
🔊 SSML Voice Forge: ❌ Authentication failed
Voice synthesis API key invalid
```

**Diagnosis:**
```powershell
# Check environment variables
$env:AZURE_SPEECH_KEY
$env:AZURE_SPEECH_REGION

# Test API connectivity
.\scripts\test_tts_api.ps1 -Provider "azure"
```

**Solutions:**
```powershell
# Set correct environment variables
$env:AZURE_SPEECH_KEY = "your_actual_api_key"
$env:AZURE_SPEECH_REGION = "eastus"

# Verify API key format
if ($env:AZURE_SPEECH_KEY.Length -ne 32) {
    Write-Host "⚠️ Azure Speech API key should be 32 characters"
}

# Test with new credentials
.\scripts\test_voice_generation.ps1 -TestMode
```

#### Issue: Voice Generation Timeout

**Symptoms:**
```
Voice generation timeout after 300 seconds
SSML processing failed for batch
```

**Solutions:**
```powershell
# Reduce batch size
.\MasterControl.ps1 -Operation execute -VoiceFiles 5

# Increase timeout in configuration
$config = @{
    "system" = @{
        "timeoutSeconds" = 600
    }
}

# Process files individually
.\scripts\process_voice_individual.ps1 -InputFolder "ssml_queue"
```

#### Issue: Poor Voice Quality

**Symptoms:**
- Robotic or unnatural sounding voice
- Audio artifacts or distortion
- Inconsistent voice characteristics

**Diagnosis:**
```powershell
# Analyze audio quality
.\scripts\analyze_audio_quality.ps1 -SampleFile "output.wav"

# Check voice profile settings
.\scripts\check_voice_profiles.ps1
```

**Solutions:**
```powershell
# Adjust voice parameters
$voiceConfig = @{
    "speed" = "0.9"      # Slower for clarity
    "pitch" = "+0st"     # Neutral pitch
    "volume" = "+0dB"    # Standard volume
}

# Use neural voices
$config = @{
    "voiceProfiles" = @{
        "primary" = "en-US-DavisNeural"  # Higher quality neural voice
    }
}

# Enable audio processing
$audioConfig = @{
    "noiseReduction" = $true
    "normalization" = $true
    "enhancement" = $true
}
```

### 🚨 Video Production Issues

#### Issue: Video Rendering Failed

**Symptoms:**
```
🎥 Video Composer: ❌ Templates missing
Rendering failed: Cannot find video templates
```

**Diagnosis:**
```powershell
# Check template directory
Test-Path "C:\Oracle_Scripts\Video_Templates"
Get-ChildItem "templates/" -Recurse

# Check system resources
Get-Process | Where-Object {$_.CPU -gt 50}
Get-WmiObject -Class Win32_OperatingSystem | Select-Object TotalPhysicalMemory,AvailablePhysicalMemory
```

**Solutions:**
```powershell
# Create missing template directory
New-Item -Path "C:\Oracle_Scripts\Video_Templates" -ItemType Directory -Force

# Copy templates from project
Copy-Item "templates/*" -Destination "C:\Oracle_Scripts\Video_Templates" -Recurse

# Free up system resources
Stop-Process -Name "chrome","firefox" -Force -ErrorAction SilentlyContinue

# Reduce rendering quality temporarily
.\MasterControl.ps1 -Operation execute -ConfigPath "config/low_quality.json"
```

#### Issue: Video Composition Memory Error

**Symptoms:**
```
Out of memory during video rendering
System.OutOfMemoryException
```

**Solutions:**
```powershell
# Reduce concurrent jobs
$config = @{
    "maxConcurrentJobs" = 2
    "videoProduction" = @{
        "renderQuality" = "720p"
        "maxDuration" = 300
    }
}

# Clear video cache
Remove-Item "cache/video/*" -Recurse -Force

# Process videos individually
.\scripts\render_individual_videos.ps1 -MaxMemory "4GB"
```

### 🚨 Upload System Issues

#### Issue: YouTube Upload Failed

**Symptoms:**
```
📤 Upload System: ❌ YouTube API authentication failed
Upload quota exceeded for today
```

**Diagnosis:**
```powershell
# Check YouTube API credentials
Test-Path "credentials/youtube_credentials.json"

# Check upload quota
.\scripts\check_youtube_quota.ps1

# Verify video file integrity
.\scripts\verify_video_files.ps1 -Path "output/final/"
```

**Solutions:**
```powershell
# Re-authenticate with YouTube
python scripts/youtube_auth_setup.py

# Wait for quota reset (daily at midnight PST)
$nextReset = Get-Date "2024-08-10 08:00:00"  # Adjust timezone
$waitTime = $nextReset - (Get-Date)
Write-Host "Quota resets in: $waitTime"

# Use test mode to skip uploads
.\MasterControl.ps1 -Operation test
```

### 🚨 System Performance Issues

#### Issue: Slow System Performance

**Symptoms:**
- Long processing times
- System unresponsiveness
- High CPU/memory usage

**Diagnosis:**
```powershell
# Check system resources
Get-Counter "\Processor(_Total)\% Processor Time"
Get-Counter "\Memory\Available MBytes"
Get-Counter "\LogicalDisk(_Total)\% Free Space"

# Identify resource-heavy processes
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
```

**Solutions:**
```powershell
# Optimize system configuration
$optimizedConfig = @{
    "maxConcurrentJobs" = 3
    "batchSize" = 10
    "outputQuality" = "medium"
    "cacheSize" = "2GB"
}

# Clean system cache
.\scripts\clean_system_cache.ps1

# Restart system services
Restart-Service -Name "Windows Search" -Force
```

#### Issue: Disk Space Full

**Symptoms:**
```
Insufficient disk space for video rendering
Cannot write to output directory
```

**Solutions:**
```powershell
# Check disk usage
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID,@{Name="Size(GB)";Expression={[math]::Round($_.Size/1GB,2)}},@{Name="FreeSpace(GB)";Expression={[math]::Round($_.FreeSpace/1GB,2)}}

# Clean up temporary files
.\scripts\cleanup_temp_files.ps1 -Aggressive

# Archive old output files
.\scripts\archive_old_outputs.ps1 -OlderThan "30days"

# Move cache to different drive
$config = @{
    "system" = @{
        "cacheLocation" = "D:\Oracle_Cache"
    }
}
```

## Advanced Troubleshooting

### Debugging Mode

Enable detailed debugging for complex issues:

```powershell
# Enable debug mode
.\MasterControl.ps1 -Operation execute -Verbose -ConfigPath "config/debug.json"

# Debug configuration
{
  "debugMode": true,
  "logLevel": "debug",
  "verboseLogging": true,
  "saveIntermediateFiles": true,
  "skipCleanup": true
}
```

### Log Analysis

```powershell
# Analyze system logs
.\scripts\analyze_logs.ps1 -LogPath "logs/" -TimeRange "24hours"

# Search for specific errors
Select-String -Path "logs/*.log" -Pattern "ERROR|FAILED" | Select-Object -Last 20

# Monitor real-time logs
Get-Content "logs/current.log" -Tail 50 -Wait
```

### System Health Monitoring

```powershell
# Continuous health monitoring
.\scripts\monitor_system_health.ps1 -Interval 30 -AlertThreshold 80

# Generate health report
.\scripts\generate_health_report.ps1 -OutputPath "reports/health_$(Get-Date -Format 'yyyyMMdd').html"
```

## Emergency Procedures

### Complete System Reset

```powershell
# Stop all processes
.\scripts\stop_all_processes.ps1

# Clear all caches
.\scripts\clear_all_caches.ps1

# Reset to default configuration
Copy-Item "config/templates/default.json" -Destination "config/current.json"

# Restart system
.\MasterControl.ps1 -Operation status -Force
```

### Recovery from Corruption

```powershell
# Verify system integrity
.\scripts\verify_system_integrity.ps1

# Restore from backup
.\scripts\restore_from_backup.ps1 -BackupDate "latest"

# Rebuild corrupted components
.\scripts\rebuild_component.ps1 -Component "all"
```

## Getting Additional Help

### System Information Collection

```powershell
# Collect comprehensive system information
.\scripts\collect_system_info.ps1 -OutputPath "support_info.zip"

# Generate support bundle
.\scripts\generate_support_bundle.ps1 -IncludeLogs -IncludeConfig
```

### Contact Information

- **GitHub Issues**: [Report a Bug](../../issues/new?template=bug_report.md)
- **Discussions**: [Ask Questions](../../discussions)
- **Documentation**: [Wiki Pages](../../wiki)
- **Emergency Contact**: [GCode3069](https://github.com/GCode3069)

### Support Checklist

Before contacting support, please:

- [ ] Run system diagnostics
- [ ] Check logs for error messages
- [ ] Verify configuration settings
- [ ] Test with minimal configuration
- [ ] Collect system information
- [ ] Document steps to reproduce

---

**Last Updated**: August 2024  
**Version**: 4.0  
**Maintainer**: [GCode3069](https://github.com/GCode3069)