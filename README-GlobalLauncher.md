# Global Content Generation System

This system provides a comprehensive GUI-based content generation platform with monetization and cancellation support for the AI Oracle project.

## Files

### `GlobalLauncher.ps1`
The main GUI application (Windows only) that provides:
- Windows Forms-based interface for content generation
- Multi-language and multi-platform selection
- Batch processing with progress tracking
- Graceful cancellation support
- Automated monetization content generation

### `GlobalLauncher-Test.ps1`
Cross-platform test version that demonstrates core functionality without GUI dependencies.

## Features

### 🌍 Multi-Language Support
- English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese
- Each language includes proper flag emoji and voice configuration
- Automatic localization of content

### 📱 Platform Support
- YouTube (primary platform)
- TikTok
- Instagram

### 🎭 Content Generation
- Horror, Thriller, Mystery, Sci-Fi, Suspense genres
- AI models: GPT-4, Claude-3, Gemini-Pro
- Configurable batch sizes (1-50 items)

### 💰 Monetization Integration
- Automatic description generation with UTM tracking
- Pinned comment creation for engagement
- Upload manifest generation (JSON format)
- Plain text exports for manual uploading

### ⏹️ Cancellation Support
- Graceful cancellation mid-process
- Preserves completed work
- Clean UI state restoration

## Usage

### Windows (GUI)
```powershell
.\GlobalLauncher.ps1
```

### Cross-platform (Testing)
```powershell
.\GlobalLauncher-Test.ps1
```

## Output Structure

The system creates the following directory structure:

```
Output/
└── Global/
    └── [language]/
        └── [platform]/
            └── manifests/
                ├── upload_[lang]_[platform]_[timestamp].json
                ├── description_[lang]_[platform]_[timestamp].txt
                └── pinned_[lang]_[platform]_[timestamp].txt
```

## Generated Files

### Upload Manifest (`upload_*.json`)
Contains complete metadata for video uploads:
- Title and description
- Pinned comment text
- Tags and privacy settings
- Story snippet
- Timestamp

### Description File (`description_*.txt`)
Plain text description ready for copy-paste into upload forms.

### Pinned Comment File (`pinned_*.txt`)
Engagement-optimized comment text for pinning after upload.

## Integration with Existing Scripts

The system is designed to work alongside:
- `MasterControl.ps1` - Core content generation
- `MasterLaunch.ps1` - Orchestration and deployment

## Monetization Macros

The system attempts to load external monetization macros from:
1. `$env:SCARIFY_MACROS_PATH` environment variable
2. `../cli/SCARIFY-Monetize-Macros.ps1` (relative to script location)

If external macros are not found, it falls back to built-in templates.

## Configuration

Global configuration is stored in `$Global:Config` and includes:
- Supported languages with voice mappings
- Platform configurations
- Genre options
- AI model selections

## Helper Functions

### Core Helpers
- `New-Point($x, $y)` - Creates System.Drawing.Point objects
- `New-Size($w, $h)` - Creates System.Drawing.Size objects  
- `Ensure-Dir($path)` - Creates directories if they don't exist

### Monetization
- `Ensure-MonetizationMacros()` - Loads external macro scripts
- `Invoke-MonetizationForItem()` - Generates monetization content

### Content Generation
- `GlobalContentGenerator` class - Handles multi-language content
- `Start-GlobalContentGeneration()` - Main processing function with cancellation

## Requirements

### Windows Version
- Windows PowerShell 5.1+ or PowerShell Core 6+
- .NET Framework (for Windows Forms)

### Cross-platform Version
- PowerShell Core 6+
- No additional dependencies

## Error Handling

The system includes comprehensive error handling:
- Graceful degradation when monetization macros are unavailable
- Validation of user selections
- Progress preservation during cancellation
- Detailed logging of operations

## Testing

Run the test version to verify functionality:
```powershell
.\GlobalLauncher-Test.ps1
```

This will create sample output files demonstrating the complete workflow.