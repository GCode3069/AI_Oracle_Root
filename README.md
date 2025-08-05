# Chimera Orchestrator v3.2 - Enhanced Edition

## Overview

The Chimera Orchestrator is an advanced PowerShell automation system for processing voice files and generating video content with multiple template styles. Version 3.2 includes significant enhancements based on the emergency fixes in v3.1, adding progress bars, configuration support, additional video templates, and comprehensive testing.

## 🆕 New Features in v3.2

### ✨ **Progress Bars for Long-Running Operations**
- **Voice File Processing**: Real-time progress indicators during file discovery and metadata analysis
- **Video Composition**: Detailed progress tracking with percentage completion and estimated time remaining
- **Template Generation**: Progress bars for each template creation phase
- **Batch Processing**: Progress tracking across file batches with current operation status

### 🧪 **Comprehensive Unit Tests**
- **Array Handling Tests**: 15 comprehensive test cases covering edge scenarios
- **Empty Directory Scenarios**: Safe handling of directories with no voice files
- **Type Safety Validation**: Tests for @() array wrapping and Math.Min bounds checking
- **Cross-Platform Testing**: Compatible with PowerShell Core and Windows PowerShell

### 🎨 **Enhanced Video Templates** (9 Templates Total)
Original 5 templates (from v3.1):
- `emergency` - Urgent Alert style
- `news` - News Bulletin style  
- `weather` - Weather Report style
- `traffic` - Traffic Update style
- `psa` - Public Service Announcement style

**NEW** 4 additional templates:
- `sports` - Sports Update style
- `entertainment` - Entertainment News style
- `tech` - Technology Alert style
- `health` - Health Advisory style

### ⚙️ **Configuration File Support**
- **JSON Configuration**: Full support for JSON configuration files
- **YAML Configuration**: Basic YAML support for key-value configurations
- **Runtime Overrides**: Command-line parameters override configuration settings
- **Environment-Specific**: Support for different configurations per environment
- **Fallback Defaults**: Works without configuration files using sensible defaults

### 🎯 **Enhanced User Experience**
- **Interactive Mode**: Guided template selection with confirmation prompts
- **Better Error Messages**: Detailed error descriptions with suggested solutions
- **Cross-Platform Compatibility**: Works on Windows, Linux, and macOS
- **Summary Reports**: Comprehensive operation summaries with actionable insights
- **Resource Validation**: System readiness checks with detailed scoring

## 📋 Requirements

- **PowerShell**: Version 5.1 or higher (including PowerShell Core 6+)
- **Disk Space**: Minimum 5GB free space (configurable)
- **Memory**: Recommended 4GB+ RAM for batch processing
- **Operating System**: Windows, Linux, or macOS

## 🚀 Usage Examples

### Basic Usage
```powershell
# Run with default settings
.\Chimera_Orchestrator.ps1
```

### With Configuration File
```powershell
# Use JSON configuration
.\Chimera_Orchestrator.ps1 -ConfigPath "chimera_config.json"

# Use YAML configuration
.\Chimera_Orchestrator.ps1 -ConfigPath "chimera_config.yaml"
```

### Interactive Mode
```powershell
# Enable interactive template selection
.\Chimera_Orchestrator.ps1 -InteractiveMode -ConfigPath "config.json"
```

### Custom Batch Processing
```powershell
# Process files in batches of 10
.\Chimera_Orchestrator.ps1 -BatchSize 10
```

## 📁 Directory Structure

```
AI_Oracle_Root/
├── Chimera_Orchestrator.ps1          # Main orchestrator script
├── chimera_config.json               # JSON configuration example
├── chimera_config.yaml               # YAML configuration example
├── Test-ChimeraArrayHandling.ps1     # Comprehensive unit tests
├── Test-ArrayHandling-Simple.ps1     # Quick validation tests
├── Oracle_VoiceOuts/                 # Voice input directory
│   ├── emergency_alert.wav
│   ├── weather_update.wav
│   └── traffic_report.mp3
└── Oracle_VideoOuts/                 # Video output directory
    ├── emergency_alert_emergency.mp4
    ├── emergency_alert_emergency_metadata.json
    └── ...
```

## 🔧 Configuration Options

### JSON Configuration Example
```json
{
  "VoiceInputDirectory": "Oracle_VoiceOuts",
  "VideoOutputDirectory": "Oracle_VideoOuts",
  "SupportedAudioFormats": ["*.wav", "*.mp3", "*.m4a", "*.flac"],
  "MinDiskSpaceGB": 10,
  "MaxConcurrentJobs": 6,
  "LogLevel": "Debug",
  "BatchSize": 25
}
```

### YAML Configuration Example
```yaml
VoiceInputDirectory: "Oracle_VoiceOuts"
VideoOutputDirectory: "Oracle_VideoOuts"
MinDiskSpaceGB: 8
MaxConcurrentJobs: 4
LogLevel: "Info"
BatchSize: 15
```

## 🎨 Video Template Styles

| Template | Style | Background | Text Color | Use Case |
|----------|-------|------------|------------|----------|
| emergency | Emergency Alert | Red (#FF4444) | White | Urgent alerts, breaking news |
| news | Breaking News | Blue (#0066CC) | White | News bulletins, updates |
| weather | Weather Report | Green (#4CAF50) | White | Weather alerts, forecasts |
| traffic | Traffic Report | Orange (#FF9800) | Black | Traffic updates, road conditions |
| psa | Public Service | Purple (#9C27B0) | White | Public announcements |
| sports | Sports Update | Pink (#E91E63) | White | Sports news, scores |
| entertainment | Entertainment News | Red-Orange (#FF5722) | White | Celebrity news, entertainment |
| tech | Technology Alert | Blue-Gray (#607D8B) | White | Tech alerts, updates |
| health | Health Advisory | Green (#4CAF50) | White | Health information, advisories |

## 🧪 Testing

### Run Unit Tests
```powershell
# Comprehensive test suite (requires Pester)
Invoke-Pester -Script .\Test-ChimeraArrayHandling.ps1

# Quick validation tests
.\Test-ArrayHandling-Simple.ps1
```

### Test Results
All 15 array handling tests pass, validating:
- ✅ Type-safe @() array wrapping
- ✅ Math.Min for safe indexing  
- ✅ Bounds checking for empty arrays
- ✅ Safe array slicing operations
- ✅ Pipeline and iteration safety

## 📊 System Validation

The orchestrator performs comprehensive system validation:

- **Disk Space**: Checks available storage vs. requirements
- **Directory Structure**: Validates input/output directories
- **System Resources**: Monitors CPU and memory usage
- **Dependencies**: Verifies PowerShell version compatibility
- **Configuration**: Validates template and parameter settings

**Scoring**: Each validation area contributes 20% to the overall readiness score.

## 🎯 Performance Features

### Progress Tracking
- **Phase 1**: Voice file discovery with metadata analysis
- **Phase 2**: Template generation with creation status
- **Phase 3**: Video composition with batch processing progress
- **Phase 4**: System validation with resource checking

### Batch Processing
- Configurable batch sizes (default: 20 files)
- Memory-efficient processing for large file sets
- Progress tracking across batches
- Pause between batches to prevent system overload

### Resource Management
- Cross-platform system resource monitoring
- Automatic fallback for unavailable system metrics
- Configurable minimum disk space requirements
- Memory usage optimization

## 🔄 Backward Compatibility

Version 3.2 maintains full backward compatibility with v3.1:
- All original functions preserved
- Same command-line interface
- Existing configurations work unchanged
- Original template names and styles maintained

## 🐛 Error Handling

Enhanced error handling includes:
- **Detailed Error Messages**: Clear descriptions with suggested solutions
- **Graceful Degradation**: System continues operation when possible
- **Fallback Mechanisms**: Default values when system queries fail
- **Comprehensive Logging**: Color-coded log levels with timestamps
- **Cross-Platform Support**: Handles platform-specific differences

## 📈 Monitoring and Reporting

### Operation Summary
- Total processing duration
- Files processed count
- Templates generated count
- Videos composed count
- System readiness percentage
- Success rate calculations

### Actionable Insights
- Suggestions for performance improvement
- Configuration recommendations
- Resource optimization tips
- Next steps guidance

## 🤝 Contributing

When contributing to the Chimera Orchestrator:
1. Maintain type-safe array operations using @() wrapping
2. Use Math.Min for safe array indexing
3. Include comprehensive error handling
4. Add appropriate progress tracking
5. Update tests for new functionality
6. Maintain backward compatibility

## 📝 Version History

- **v3.2** (Current): Enhanced edition with progress bars, configuration support, additional templates
- **v3.1**: Emergency fixes for PowerShell array type conversion errors
- **v3.0**: Initial Chimera Orchestrator release

## 🏷️ License

This project is part of the AI Oracle Root system and follows the repository's licensing terms.

---

*For technical support or feature requests, please create an issue in the GitHub repository.*