# ⚙️ Configuration Guide

## Overview

The Oracle Horror Production System uses a flexible JSON-based configuration system that allows fine-tuning of all pipeline stages and system behavior.

## Configuration Hierarchy

The system loads configuration in the following priority order:

1. **Command-line parameters** (highest priority)
2. **Custom configuration file** (specified with `-ConfigPath`)
3. **Environment variables**
4. **Default configuration** (lowest priority)

## Base Configuration

### Default Settings

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

### Complete Configuration Schema

```json
{
  "system": {
    "version": "4.0",
    "environment": "production",
    "logLevel": "info",
    "maxConcurrentJobs": 5,
    "retryAttempts": 3,
    "timeoutSeconds": 300,
    "debugMode": false
  },
  "pipeline": {
    "voiceGen": true,
    "renderEnabled": true,
    "uploadEnabled": true,
    "templateProfile": "tech_alerts",
    "outputQuality": "high",
    "batchSize": 15
  },
  "stages": {
    "scriptEngine": {
      "enabled": true,
      "googleSheetsSync": true,
      "contentGeneration": true,
      "ssmlProcessing": true
    },
    "voiceoverVault": {
      "enabled": true,
      "ttsProvider": "azure",
      "audioQuality": "high",
      "voiceProfiles": ["neural-dark", "neural-whisper"]
    },
    "visualAssets": {
      "enabled": true,
      "aiGeneration": true,
      "imageProcessing": true,
      "styleConsistency": true
    },
    "argElements": {
      "enabled": false,
      "interactiveContent": false,
      "socialIntegration": false
    },
    "videoProduction": {
      "enabled": true,
      "renderQuality": "1080p",
      "effects": true,
      "optimization": "youtube"
    },
    "monetization": {
      "enabled": false,
      "adOptimization": false,
      "sponsorships": false
    },
    "analytics": {
      "enabled": false,
      "dataCollection": false,
      "reporting": false
    },
    "admin": {
      "enabled": true,
      "monitoring": true,
      "maintenance": true,
      "alerting": true
    }
  }
}
```

## Stage-Specific Configuration

### Script Engine Configuration

```json
{
  "scriptEngine": {
    "contentGeneration": {
      "aiProvider": "openai",
      "model": "gpt-4",
      "temperature": 0.7,
      "maxTokens": 2000,
      "promptTemplates": {
        "horror": "Create a horror-themed narrative about {topic}",
        "tech": "Generate technical documentation for {topic}",
        "arg": "Develop an ARG storyline involving {topic}"
      }
    },
    "ssmlProcessing": {
      "voiceMapping": {
        "narrator": "neural-dark",
        "character": "neural-whisper",
        "emergency": "neural-robotic"
      },
      "effects": {
        "emphasis": true,
        "pauses": true,
        "prosody": true
      }
    },
    "googleSheets": {
      "spreadsheetId": "your_spreadsheet_id",
      "worksheetName": "Content_Queue",
      "syncInterval": 300,
      "batchSize": 50
    }
  }
}
```

### Voiceover Vault Configuration

```json
{
  "voiceoverVault": {
    "ttsProviders": {
      "azure": {
        "enabled": true,
        "apiKey": "${AZURE_SPEECH_KEY}",
        "region": "eastus",
        "voiceProfiles": {
          "neural-dark": {
            "voice": "en-US-DavisNeural",
            "style": "angry",
            "speed": "0.9",
            "pitch": "-2st"
          },
          "neural-whisper": {
            "voice": "en-US-JennyNeural", 
            "style": "whispering",
            "speed": "0.7",
            "pitch": "-5st"
          }
        }
      },
      "google": {
        "enabled": false,
        "apiKey": "${GOOGLE_TTS_KEY}",
        "voiceProfiles": {}
      }
    },
    "audioProcessing": {
      "sampleRate": 44100,
      "bitDepth": 16,
      "channels": 1,
      "format": "wav",
      "effects": {
        "noiseReduction": true,
        "normalization": true,
        "compression": {
          "enabled": true,
          "ratio": 3.5,
          "threshold": -12
        },
        "eq": {
          "lowCut": 80,
          "highCut": 15000,
          "midBoost": 2.5
        }
      }
    }
  }
}
```

### Visual Assets Configuration

```json
{
  "visualAssets": {
    "aiGeneration": {
      "provider": "dalle3",
      "apiKey": "${OPENAI_API_KEY}",
      "settings": {
        "quality": "hd",
        "size": "1792x1024",
        "style": "vivid"
      },
      "promptEngineering": {
        "styleModifiers": ["horror", "dark", "atmospheric"],
        "qualityEnhancers": ["highly detailed", "professional photography"],
        "negativePrompts": ["cheerful", "bright", "cartoon"]
      }
    },
    "imageProcessing": {
      "resolution": {
        "width": 1920,
        "height": 1080,
        "dpi": 300
      },
      "effects": {
        "vignette": 0.3,
        "colorGrading": "horror_lut",
        "contrast": 1.2,
        "saturation": 0.8,
        "textureOverlay": "film_grain"
      },
      "optimization": {
        "format": "png",
        "quality": 95,
        "compression": "lossless"
      }
    }
  }
}
```

### Video Production Configuration

```json
{
  "videoProduction": {
    "rendering": {
      "profiles": {
        "youtube_standard": {
          "resolution": "1920x1080",
          "framerate": 30,
          "bitrate": "8000k",
          "codec": "h264",
          "audio": {
            "codec": "aac",
            "bitrate": "192k",
            "sampleRate": 44100
          }
        },
        "youtube_high": {
          "resolution": "2560x1440",
          "framerate": 60,
          "bitrate": "16000k",
          "codec": "h265",
          "audio": {
            "codec": "aac",
            "bitrate": "320k",
            "sampleRate": 48000
          }
        }
      },
      "effects": {
        "transitions": true,
        "overlays": true,
        "colorGrading": true,
        "audioSync": true
      }
    },
    "templates": {
      "tech_alerts": {
        "duration": "3-5min",
        "style": "documentary",
        "elements": ["title_card", "content", "outro"]
      },
      "cosmic_horror": {
        "duration": "5-8min",
        "style": "cinematic",
        "elements": ["intro", "buildup", "climax", "resolution"]
      }
    }
  }
}
```

## Environment-Specific Configurations

### Development Configuration

```json
{
  "system": {
    "environment": "development",
    "debugMode": true,
    "logLevel": "debug"
  },
  "pipeline": {
    "uploadEnabled": false,
    "batchSize": 3
  },
  "stages": {
    "voiceoverVault": {
      "audioQuality": "medium"
    },
    "videoProduction": {
      "renderQuality": "720p"
    }
  }
}
```

### Production Configuration

```json
{
  "system": {
    "environment": "production",
    "debugMode": false,
    "logLevel": "info",
    "maxConcurrentJobs": 8
  },
  "pipeline": {
    "uploadEnabled": true,
    "outputQuality": "ultra",
    "batchSize": 25
  },
  "monitoring": {
    "alerting": true,
    "metrics": true,
    "reporting": true
  }
}
```

### Test Configuration

```json
{
  "system": {
    "environment": "test",
    "debugMode": true,
    "logLevel": "debug"
  },
  "pipeline": {
    "uploadEnabled": false,
    "voiceGen": false,
    "renderEnabled": false
  },
  "testing": {
    "mockMode": true,
    "simulationOnly": true
  }
}
```

## Configuration Validation

### Schema Validation

The system validates configuration against a JSON schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "system": {
      "type": "object",
      "properties": {
        "maxConcurrentJobs": {
          "type": "integer",
          "minimum": 1,
          "maximum": 20
        },
        "retryAttempts": {
          "type": "integer",
          "minimum": 0,
          "maximum": 10
        }
      }
    }
  }
}
```

### Validation Commands

```powershell
# Validate configuration file
.\scripts\validate_config.ps1 -ConfigPath "config/production.json"

# Test configuration loading
.\MasterControl.ps1 -Operation status -ConfigPath "config/test.json" -Verbose
```

## Configuration Management

### Version Control

```bash
# Store configurations in version control
git add config/*.json
git commit -m "Update production configuration"

# Use branches for different environments
git checkout -b config/staging
# Edit staging configurations
git commit -m "Staging configuration updates"
```

### Configuration Templates

```bash
# Create configuration from template
cp config/templates/production.template.json config/production.json
# Edit with environment-specific values
```

### Environment Variables

```powershell
# Set environment variables for sensitive data
$env:AZURE_SPEECH_KEY = "your_azure_key"
$env:OPENAI_API_KEY = "your_openai_key"
$env:YOUTUBE_API_KEY = "your_youtube_key"

# Reference in configuration
{
  "apiKey": "${AZURE_SPEECH_KEY}"
}
```

## Configuration Best Practices

### Security

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Implement configuration encryption** for production
4. **Regular credential rotation**

### Performance

1. **Tune concurrent jobs** based on system capabilities
2. **Adjust batch sizes** for optimal throughput
3. **Configure appropriate timeouts**
4. **Monitor resource utilization**

### Maintainability

1. **Use descriptive configuration names**
2. **Document configuration changes**
3. **Implement configuration validation**
4. **Maintain environment parity**

### Example Maintenance Commands

```powershell
# Update configuration with new API keys
.\scripts\update_config.ps1 -ConfigPath "config/production.json" -UpdateKeys

# Backup current configuration
.\scripts\backup_config.ps1 -All

# Restore configuration from backup
.\scripts\restore_config.ps1 -BackupId "20240809_120000"
```

## Troubleshooting Configuration Issues

### Common Problems

**🔧 Configuration File Not Found**
```powershell
# Check file path and permissions
Test-Path "config/production.json"
Get-Acl "config/production.json"
```

**🔧 Invalid JSON Syntax**
```powershell
# Validate JSON syntax
Get-Content "config/production.json" | ConvertFrom-Json
```

**🔧 Missing Required Settings**
```powershell
# Use configuration validation
.\scripts\validate_config.ps1 -ConfigPath "config/production.json" -Strict
```

**🔧 Environment Variable Not Set**
```powershell
# Check environment variables
Get-ChildItem Env: | Where-Object Name -Like "*API*"
```

---

**Last Updated**: August 2024  
**Version**: 4.0  
**Maintainer**: [GCode3069](https://github.com/GCode3069)