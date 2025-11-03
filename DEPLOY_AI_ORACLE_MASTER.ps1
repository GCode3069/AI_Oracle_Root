# DEPLOY_AI_ORACLE_MASTER.ps1

# Define the base directory for the AI Oracle Ecosystem
$baseDir = "scarify"

# Create the complete directory structure
dirs = @(
    "$baseDir/cli",
    "$baseDir/gui",
    "$baseDir/Output/YouTubeReady",
    "$baseDir/Output/ShortsReady",
    "$baseDir/lightning_strike",
    "$baseDir/logs",
    "$baseDir/config",
    "$baseDir/security",
    "$baseDir/analytics"
)

foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Output "Created directory: $dir"
    } else {
        Write-Output "Directory already exists: $dir"
    }
}

# Create a desktop shortcut (for Windows)
$shortcutPath = [System.IO.Path]::Combine([System.Environment]::GetFolderPath('Desktop'), 'AI_Oracle_Shortcut.lnk')
$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "C:\Path\To\Your\ScriptOrApplication.exe"  # Change to your executable path
$shortcut.Save()
Write-Output "Created desktop shortcut: $shortcutPath"

# Validate Python dependencies
try {
    $dependencies = @("numpy", "pandas", "requests")  # Add your required dependencies here

    foreach ($dep in $dependencies) {
        $installed = pip show $dep
        if (-not $installed) {
            Write-Output "Dependency $dep is not installed."
        } else {
            Write-Output "Dependency $dep is installed."
        }
    }
} catch {
    Write-Output "Error validating Python dependencies: $_"
}

# Validate FFmpeg installation
$ffmpegPath = "C:\Path\To\ffmpeg.exe"  # Change to your FFmpeg path
if (Test-Path $ffmpegPath) {
    Write-Output "FFmpeg is installed at: $ffmpegPath"
} else {
    Write-Output "FFmpeg is not installed. Please install it."
}