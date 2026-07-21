# SCARIFY Desktop Launcher - Complete GUI for Video Production

## Overview

The SCARIFY Desktop Launcher provides a unified Windows Forms GUI interface for the complete SCARIFY video production ecosystem. This launcher integrates all major components including video production, YouTube upload management, audio enhancement, and system monitoring into a single, easy-to-use desktop application.

## Features

### 🎬 Main Control Panel
- **⚡ Lightning Strike Protocol**: Rapid video production and deployment
- **🎵 Audio Enhancement**: Advanced audio processing and optimization
- **🔄 Full Pipeline**: Complete end-to-end video production workflow
- **📺 YouTube Studio**: Direct access to YouTube Studio interface
- **🌐 Multilingual Batch**: Batch processing for multiple languages
- **💰 Monetization Optimizer**: Revenue optimization tools
- **📊 System Status**: Real-time system health monitoring
- **🔧 Advanced Tools**: Extended functionality and maintenance tools

### 📁 Quick Access Panel
- **📂 Output Folder**: Access to all generated content
- **🎬 Shorts Folder**: Quick access to short-form videos
- **📋 Logs Folder**: System logs and debugging information
- **🗂️ Temp Folder**: Temporary files and cache
- **🎥 Videos Folder**: Final video outputs

### 📊 System Log & Status
- Real-time log display with color-coded messages
- System status monitoring
- Progress tracking for operations
- Error reporting and diagnostics

## Installation

### Automated Installation (Recommended)

1. Run the SCARIFY Complete Installer:
   ```powershell
   .\scarify\SCARIFY-Complete-Installer.ps1
   ```

2. The installer will:
   - Create the complete directory structure
   - Generate desktop shortcuts
   - Set up all required components
   - Configure the launcher

### Manual Installation

1. Copy all PowerShell scripts to your SCARIFY directory
2. Run the launcher setup:
   ```powershell
   .\SCARIFY-Desktop-Launcher.ps1 -Setup
   ```

## Usage

### Windows (GUI Mode)

1. **Launch the GUI**:
   - Double-click the "SCARIFY Desktop Launcher" desktop shortcut
   - Or run: `.\SCARIFY-Desktop-Launcher.ps1`

2. **Using the Interface**:
   - Click any main control button to execute that function
   - Use quick access buttons to open folders
   - Monitor progress in the log display section
   - Check system status for component health

### Linux/Mac (Console Mode)

The launcher automatically detects non-Windows platforms and runs in console mode:

```powershell
.\SCARIFY-Desktop-Launcher.ps1
```

Navigate using the numbered menu system.

## System Requirements

### Windows
- Windows 10 or later
- PowerShell 5.1 or PowerShell 7+
- .NET Framework 4.7.2 or later (for Windows Forms)

### Linux/Mac
- PowerShell 7+
- Console mode operation

## Directory Structure

The launcher automatically creates and manages this structure:

```
AI_Oracle_Root/
├── Output/
│   ├── Videos/          # Final video outputs
│   ├── Shorts/          # Short-form content
│   └── Runs/            # Processing run logs
├── logs/                # System logs
├── temp/                # Temporary files
├── cli/                 # Command-line tools
├── 1_Audio_Processing/  # Audio workflow
├── 2_Image_Generation/  # Visual content
├── 3_Script_Generation/ # Content scripts
├── 4_Voice_Synthesis/   # TTS processing
├── 5_Video_Production/  # Video assembly
├── 6_Monetization/      # Revenue optimization
└── 7_Analytics_Strategy/ # Performance analysis
```

## Available Scripts

### Core System
- **SCARIFY-Desktop-Launcher.ps1**: Main GUI launcher
- **MasterLaunch.ps1**: End-to-end orchestrator
- **MasterControl.ps1**: System control and monitoring

### Production Pipeline
- **scarify_complete_video_production.ps1**: Complete video creation
- **SCARIFY-Master.ps1**: Master control system
- **Advanced-SCARIFY-Features.ps1**: Extended functionality

### Optimization
- **YouTube-Algorithm-Optimizer.ps1**: Content optimization for YouTube

## Configuration

### Default Paths
- Windows: `D:\AI_Oracle_Root\scarify`
- Linux/Mac: `~/AI_Oracle_Root/scarify`

### Customization
Modify the `$InstallPath` parameter when running the launcher:
```powershell
.\SCARIFY-Desktop-Launcher.ps1 -InstallPath "C:\Custom\Path"
```

## Troubleshooting

### Common Issues

1. **GUI Not Loading on Windows**:
   - Ensure .NET Framework is installed
   - Check PowerShell execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned`

2. **Scripts Not Found**:
   - Verify all scripts are in the same directory as the launcher
   - Run with `-Setup` flag to initialize directories

3. **Permission Errors**:
   - Run PowerShell as Administrator
   - Check file permissions on the installation directory

### Debug Mode
Enable verbose logging:
```powershell
.\SCARIFY-Desktop-Launcher.ps1 -DebugMode
```

## Integration with Existing Scripts

The launcher integrates seamlessly with existing SCARIFY components:

- **MasterLaunch.ps1**: Called for Lightning Strike and Full Pipeline operations
- **MasterControl.ps1**: Used for system status and audio enhancement
- **Video Production Scripts**: Automated through the GUI interface

## Advanced Features

### Custom Workflows
Access through Advanced Tools menu:
- Batch processing configuration
- Custom script execution
- System maintenance tasks
- Performance optimization

### API Integration
The launcher supports:
- YouTube Studio integration
- Analytics data collection
- Custom plugin architecture

## Contributing

To extend the launcher:

1. Add new functions to the appropriate sections
2. Update the GUI button definitions
3. Implement corresponding action handlers
4. Test cross-platform compatibility

## Support

For issues and feature requests:
- Check the system logs for error details
- Use the System Status feature to diagnose problems
- Refer to individual script documentation for specific functionality

## Version History

### v1.0
- Initial release with complete GUI
- Cross-platform support
- Integration with all major SCARIFY components
- Real-time logging and status monitoring
- Desktop shortcut creation
- Advanced tools and maintenance features