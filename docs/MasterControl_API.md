# 🔧 MasterControl.ps1 API Documentation

## Overview

MasterControl.ps1 is the central orchestration script for the Oracle Horror Production System, providing a unified interface for managing all pipeline stages and system operations.

## Command Line Interface

### Basic Syntax

```powershell
.\MasterControl.ps1 -Operation <operation> [additional parameters]
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `Operation` | String | "status" | Primary operation to execute |
| `ConfigPath` | String | "" | Path to custom configuration file |
| `Verbose` | Switch | False | Enable detailed logging output |
| `Force` | Switch | False | Override safety checks and warnings |
| `VoiceFiles` | Integer | 15 | Number of voice files to process |
| `TemplateProfile` | String | "tech_alerts" | Content template profile to use |

## Operations

### Status Operation

Check system health and component status.

```powershell
# Basic status check
.\MasterControl.ps1 -Operation status

# Verbose status with detailed information
.\MasterControl.ps1 -Operation status -Verbose
```

**Expected Output:**
```
🔍 CHIMERA LEGION SYSTEM STATUS CHECK
🎮 MasterControl.ps1: ✅ Online (Phase 1 Complete)
🧠 PsyOps Engine: ✅ Operational (15 voice files)
📊 Google Sheets: ✅ Synced
🗂️ Queues: ✅ Loaded (All queues primed)
🎥 Video Composer: ✅ Tested (20/20 rendered)
🔊 SSML Voice Forge: ✅ Active (15 voices queued)
📤 Upload System: ✅ Online (YouTube deploy confirmed)
🧪 Test Cycle: ✅ Passed (Zero failures)
```

### Execute Operation

Run the full production pipeline.

```powershell
# Standard execution
.\MasterControl.ps1 -Operation execute

# Custom voice file count
.\MasterControl.ps1 -Operation execute -VoiceFiles 25

# Force execution despite warnings
.\MasterControl.ps1 -Operation execute -Force

# Custom configuration file
.\MasterControl.ps1 -Operation execute -ConfigPath "config/production.json"

# Specific template profile
.\MasterControl.ps1 -Operation execute -TemplateProfile "cosmic_horror"
```

### Test Operation

Run pipeline in test mode (no actual uploads).

```powershell
# Basic test run
.\MasterControl.ps1 -Operation test

# Verbose test with detailed logging
.\MasterControl.ps1 -Operation test -Verbose
```

## Configuration System

### Default Configuration

The system uses the following default configuration when no custom config is provided:

```json
{
  "voiceGen": true,
  "renderEnabled": true,
  "uploadEnabled": true,
  "templateProfile": "tech_alerts",
  "maxConcurrentJobs": 5,
  "retryAttempts": 3,
  "outputQuality": "high",
  "debugMode": false
}
```

### Custom Configuration

Create custom configuration files to override defaults:

```json
{
  "voiceGen": true,
  "renderEnabled": true,
  "uploadEnabled": false,
  "templateProfile": "horror_whisper",
  "maxConcurrentJobs": 8,
  "retryAttempts": 5,
  "outputQuality": "ultra",
  "debugMode": true,
  "customSettings": {
    "voiceSpeed": 0.85,
    "videoQuality": "4K",
    "effectsLevel": "maximum"
  }
}
```

## Template Profiles

### Available Profiles

| Profile | Description | Content Type | Voice Style |
|---------|-------------|--------------|-------------|
| `tech_alerts` | Technical emergency broadcasts | Educational | Authoritative |
| `horror_alerts` | Horror-themed emergency alerts | Suspense | Ominous |
| `cosmic_horror` | Lovecraftian space themes | Atmospheric | Ethereal |
| `urban_legends` | Modern myth adaptations | Narrative | Mysterious |
| `arg_narrative` | ARG storyline development | Interactive | Variable |

### Profile Usage

```powershell
# Use specific profile
.\MasterControl.ps1 -Operation execute -TemplateProfile "cosmic_horror"

# Override profile in config
{
  "templateProfile": "urban_legends",
  "profileOverrides": {
    "voiceStyle": "whisper",
    "pacing": "slow",
    "effects": "atmospheric"
  }
}
```

## Return Values

MasterControl.ps1 returns a PowerShell object with execution details:

```powershell
$result = .\MasterControl.ps1 -Operation execute
# Returns:
# {
#   "Operation": "execute",
#   "Status": "COMPLETED",
#   "Timestamp": "2024-08-09T10:30:00Z",
#   "ConfigProfile": "tech_alerts",
#   "Commander": "GCode3069"
# }
```

## Error Handling

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| 1 | Invalid operation | Check operation parameter spelling |
| 2 | Configuration file not found | Verify ConfigPath parameter |
| 3 | Google Sheets authentication failed | Regenerate authentication token |
| 4 | Voice generation failed | Check TTS API credentials |
| 5 | Video rendering failed | Verify video processing dependencies |

### Error Examples

```powershell
# Error: Invalid operation
.\MasterControl.ps1 -Operation invalid_op
# Output: ❌ Invalid operation: invalid_op

# Error: Missing configuration
.\MasterControl.ps1 -ConfigPath "nonexistent.json"
# Output: Failed to load config, using defaults: Cannot find path...
```

## Logging System

### Log Levels

- **INFO**: General information messages
- **SUCCESS**: Successful operation completions
- **WARNING**: Non-critical issues or advisories
- **ERROR**: Error conditions requiring attention
- **LEGION**: System-wide status messages

### Log Format

```
[2024-08-09 10:30:15] [SUCCESS] ✅ SSML voice queue processed (15 files)
[2024-08-09 10:30:16] [INFO] 🖼️ Rendering video files...
[2024-08-09 10:30:45] [SUCCESS] ✅ Video files rendered (20/20 success)
```

## Progress Tracking

The system provides real-time progress tracking for long-running operations:

```powershell
# Progress tracking example
🔊 Processing SSML voice queue...
Processing voice file 5 of 15 [████████░░] 33%

🖼️ Rendering video files...
Rendering video 12 of 20 [████████████░░░░] 60%

📤 Uploading to YouTube...
Uploading video 18 of 20 [█████████████████░] 90%
```

## Integration Examples

### PowerShell Script Integration

```powershell
# Example: Automated daily execution
$result = .\MasterControl.ps1 -Operation execute -TemplateProfile "daily_content"

if ($result.Status -eq "COMPLETED") {
    Write-Host "Daily content generation completed successfully"
    # Send notification or update database
} else {
    Write-Host "Content generation failed, initiating recovery"
    # Error handling and retry logic
}
```

### Batch Processing

```powershell
# Process multiple configurations
$configs = @("morning.json", "afternoon.json", "evening.json")
foreach ($config in $configs) {
    $result = .\MasterControl.ps1 -Operation execute -ConfigPath $config
    Start-Sleep -Seconds 300  # Wait 5 minutes between batches
}
```

### Scheduled Execution

```powershell
# Windows Task Scheduler integration
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-File 'C:\Oracle\MasterControl.ps1' -Operation execute"

$trigger = New-ScheduledTaskTrigger -Daily -At "02:00AM"

Register-ScheduledTask -Action $action -Trigger $trigger `
    -TaskName "Oracle_Daily_Production" -Description "Daily content generation"
```

## Performance Optimization

### Resource Management

```json
{
  "performance": {
    "maxConcurrentJobs": 8,
    "memoryLimit": "8GB",
    "cpuThreads": 6,
    "diskCache": "10GB",
    "networkTimeout": 300
  }
}
```

### Optimization Tips

1. **Concurrent Jobs**: Adjust `maxConcurrentJobs` based on system capabilities
2. **Memory Usage**: Monitor memory consumption with large voice file batches
3. **Disk Space**: Ensure adequate space for video rendering cache
4. **Network Bandwidth**: Consider API rate limits for external services

## Security Considerations

### Credential Management

```powershell
# Store credentials securely
$SecureCredentials = @{
    "GoogleAPIKey" = ConvertTo-SecureString $env:GOOGLE_API_KEY -AsPlainText -Force
    "YouTubeToken" = ConvertTo-SecureString $env:YOUTUBE_TOKEN -AsPlainText -Force
}

# Use in configuration
$config = @{
    "credentials" = $SecureCredentials
    "encryptionLevel" = "AES256"
}
```

### Access Control

- Run with minimal required privileges
- Store sensitive configuration files in secure locations
- Use environment variables for API keys
- Implement audit logging for sensitive operations

## Troubleshooting Guide

### Common Issues and Solutions

**🔧 System Status Check Failed**
```powershell
# Solution: Validate all dependencies
.\MasterControl.ps1 -Operation status -Verbose
# Check specific component status
```

**🔧 Google Sheets Authentication Error**
```powershell
# Solution: Regenerate authentication
Remove-Item "token_sheets_rw.pickle" -Force
# Re-run authentication setup
```

**🔧 Voice Generation Timeout**
```powershell
# Solution: Reduce batch size and retry
.\MasterControl.ps1 -Operation execute -VoiceFiles 5 -Force
```

**🔧 Video Rendering Memory Error**
```powershell
# Solution: Reduce concurrent jobs
$config = @{ "maxConcurrentJobs" = 2 }
$config | ConvertTo-Json | Out-File "temp_config.json"
.\MasterControl.ps1 -ConfigPath "temp_config.json"
```

## API Reference Summary

| Function | Purpose | Parameters | Returns |
|----------|---------|------------|---------|
| `Write-ChimeraLog` | Logging with progress | Message, Level, ProgressId, Activity | None |
| `Load-ChimeraConfig` | Configuration loading | ConfigPath | Hashtable |
| `Get-ChimeraSystemStatus` | System health check | None | Status object |
| `Invoke-ChimeraExecution` | Pipeline execution | Config hashtable | None |

---

**Last Updated**: August 2024  
**Version**: 4.0  
**Maintainer**: [GCode3069](https://github.com/GCode3069)