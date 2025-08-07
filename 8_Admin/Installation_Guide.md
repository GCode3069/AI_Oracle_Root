# Operation Viral Dominance - Tool Installer

## Overview
Automated installer script for essential tools required by the Operation Viral Dominance workflow, compatible with the Chimera Legion Deployment System v4.0.

## Tools Installed
- **DaVinci Resolve**: Professional video editing and color grading
- **CapCut**: Modern video editing for content creation
- **Python 3.10+**: Programming environment for automation
- **ElevenLabs SDK**: AI voice synthesis capabilities
- **Canva**: Browser-based design platform (no installation required)

## Usage

### Prerequisites
- Windows 10/11
- PowerShell 5.0 or later
- Administrator privileges
- Internet connection

### Basic Installation
```powershell
# Run as Administrator
.\Operation_Viral_Dominance_Installer.ps1
```

### Advanced Options
```powershell
# Force reinstallation of existing tools
.\Operation_Viral_Dominance_Installer.ps1 -Force

# Skip specific tools
.\Operation_Viral_Dominance_Installer.ps1 -SkipDaVinci -SkipCapCut
.\Operation_Viral_Dominance_Installer.ps1 -SkipPython

# Verbose output
.\Operation_Viral_Dominance_Installer.ps1 -Verbose
```

### Parameters
- `-Force`: Forces installation even if tools are already detected
- `-SkipPython`: Skips Python and ElevenLabs SDK installation
- `-SkipDaVinci`: Skips DaVinci Resolve installation
- `-SkipCapCut`: Skips CapCut installation
- `-Verbose`: Enables detailed logging output

## Manual Steps Required
- **DaVinci Resolve**: Requires registration at blackmagicdesign.com before download
- **Canva**: Access via browser at https://canva.com (no installation needed)

## Integration
This installer is designed to work alongside:
- MasterControl.ps1 (Chimera Legion main automation)
- Oracle_VoiceOuts voice generation system
- YouTube deployment pipeline

## Security
- All downloads from official vendor URLs
- Administrator privileges required for system-wide installations
- Temporary files automatically cleaned up

## Support
Commander: GCode3069  
Encryption Level: REDLINE // OPERATIONAL READY  
Compatible with Chimera Legion Deployment System v4.0