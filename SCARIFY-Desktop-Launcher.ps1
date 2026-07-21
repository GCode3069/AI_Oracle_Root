<#
.SYNOPSIS
SCARIFY Desktop Launcher - Unified GUI for Complete Video Production Workflow

.DESCRIPTION
Provides a comprehensive Windows Forms GUI for the SCARIFY system including:
- Video Production workflows
- YouTube Upload management  
- Audio Enhancement tools
- System status monitoring
- Quick folder access
- Desktop shortcuts creation

.AUTHOR
GCode3069

.VERSION
1.0

.USAGE
.\SCARIFY-Desktop-Launcher.ps1
#>

param(
    [string]$InstallPath = "",
    [switch]$Setup,
    [switch]$DebugMode
)

# ================================================
# INITIALIZATION AND SETUP
# ================================================

$ErrorActionPreference = "Continue"
$Host.UI.RawUI.WindowTitle = "SCARIFY Desktop Launcher v1.0"

# Determine default install path based on platform
if ([string]::IsNullOrEmpty($InstallPath)) {
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        $InstallPath = "D:\AI_Oracle_Root\scarify"
    } else {
        $InstallPath = Join-Path $HOME "AI_Oracle_Root/scarify"
    }
}

# Check if we can load Windows Forms (Windows only)
$SupportsGUI = $false
if ($IsWindows -or $env:OS -eq "Windows_NT") {
    try {
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        $SupportsGUI = $true
    } catch {
        Write-Warning "Windows Forms not available. Running in console mode."
        $SupportsGUI = $false
    }
} else {
    Write-Warning "GUI mode not supported on this platform. Running in console mode."
}

# Global variables
$Global:LogBuffer = @()
$Global:StatusText = "System Ready"
$Global:CurrentWorkingDir = (Get-Location).Path

# ================================================
# DIRECTORY STRUCTURE SETUP
# ================================================

function Initialize-ScarifyDirectories {
    param([string]$BasePath = $InstallPath)
    
    Write-ScarifyLog "🏗️ Setting up SCARIFY directory structure..." "INFO"
    
    $directories = @(
        "Output",
        "Output\Videos", 
        "Output\Shorts",
        "Output\Runs",
        "logs",
        "temp", 
        "cli",
        "1_Audio_Processing",
        "2_Image_Generation",
        "3_Script_Generation", 
        "4_Voice_Synthesis",
        "5_Video_Production",
        "6_Monetization",
        "7_Analytics_Strategy"
    )
    
    foreach ($dir in $directories) {
        $fullPath = Join-Path $BasePath $dir
        if (-not (Test-Path $fullPath)) {
            try {
                New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
                Write-ScarifyLog "📁 Created: $dir" "SUCCESS"
            } catch {
                Write-ScarifyLog "❌ Failed to create: $dir - $($_.Exception.Message)" "ERROR"
            }
        } else {
            Write-ScarifyLog "✅ Exists: $dir" "INFO"
        }
    }
    
    Write-ScarifyLog "🎯 Directory structure setup complete!" "SUCCESS"
    return $true
}

# ================================================
# LOGGING SYSTEM
# ================================================

function Write-ScarifyLog {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    # Add to global buffer
    $Global:LogBuffer += $logEntry
    
    # Keep only last 100 entries
    if ($Global:LogBuffer.Count -gt 100) {
        $Global:LogBuffer = $Global:LogBuffer[-100..-1]
    }
    
    # Update GUI if form exists
    if ($Global:Form -and $Global:LogTextBox) {
        try {
            $Global:Form.Invoke([Action]{
                $Global:LogTextBox.Text = ($Global:LogBuffer -join "`r`n")
                $Global:LogTextBox.SelectionStart = $Global:LogTextBox.Text.Length
                $Global:LogTextBox.ScrollToCaret()
                
                # Update status
                $Global:StatusLabel.Text = "$Global:StatusText | Last: $Message"
            })
        } catch {
            # GUI not ready, just continue
        }
    }
    
    # Console output with colors
    $color = switch ($Level) {
        "SUCCESS" { "Green" }
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        "INFO" { "Cyan" }
        default { "White" }
    }
    
    Write-Host $logEntry -ForegroundColor $color
}

# ================================================
# DESKTOP SHORTCUTS CREATION
# ================================================

function New-DesktopShortcut {
    param(
        [string]$Name,
        [string]$TargetPath,
        [string]$Arguments = "",
        [string]$WorkingDirectory = "",
        [string]$IconLocation = "shell32.dll,137"
    )
    
    try {
        $desktop = [Environment]::GetFolderPath("Desktop")
        $shortcutPath = Join-Path $desktop "$Name.lnk"
        
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($shortcutPath)
        $Shortcut.TargetPath = $TargetPath
        $Shortcut.Arguments = $Arguments
        $Shortcut.WorkingDirectory = $WorkingDirectory
        $Shortcut.IconLocation = $IconLocation
        $Shortcut.Save()
        
        Write-ScarifyLog "🔗 Created shortcut: $Name" "SUCCESS"
        return $true
    } catch {
        Write-ScarifyLog "❌ Failed to create shortcut: $Name - $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Initialize-DesktopShortcuts {
    Write-ScarifyLog "🖥️ Creating desktop shortcuts..." "INFO"
    
    $shortcuts = @(
        @{
            Name = "SCARIFY Master Studio"
            Target = "powershell.exe"
            Args = "-ExecutionPolicy Bypass -File `"$($Global:CurrentWorkingDir)\MasterControl.ps1`""
            WorkDir = $Global:CurrentWorkingDir
            Icon = "shell32.dll,137"
        },
        @{
            Name = "Lightning Strike Protocol"
            Target = "powershell.exe" 
            Args = "-ExecutionPolicy Bypass -File `"$($Global:CurrentWorkingDir)\MasterLaunch.ps1`" -Mode full -Campaign awakening"
            WorkDir = $Global:CurrentWorkingDir
            Icon = "shell32.dll,25"
        },
        @{
            Name = "SCARIFY Desktop Launcher"
            Target = "powershell.exe"
            Args = "-ExecutionPolicy Bypass -File `"$($Global:CurrentWorkingDir)\SCARIFY-Desktop-Launcher.ps1`""
            WorkDir = $Global:CurrentWorkingDir
            Icon = "shell32.dll,44"
        }
    )
    
    foreach ($shortcut in $shortcuts) {
        New-DesktopShortcut -Name $shortcut.Name -TargetPath $shortcut.Target -Arguments $shortcut.Args -WorkingDirectory $shortcut.WorkDir -IconLocation $shortcut.Icon
    }
    
    Write-ScarifyLog "✅ Desktop shortcuts created successfully!" "SUCCESS"
}

# ================================================
# SCRIPT EXECUTION FUNCTIONS
# ================================================

function Invoke-ScarifyScript {
    param(
        [string]$ScriptName,
        [string]$Arguments = "",
        [switch]$ShowWindow = $false
    )
    
    $scriptPath = Join-Path $Global:CurrentWorkingDir $ScriptName
    
    if (-not (Test-Path $scriptPath)) {
        Write-ScarifyLog "❌ Script not found: $ScriptName" "ERROR"
        [System.Windows.Forms.MessageBox]::Show("Script not found: $ScriptName`nPath: $scriptPath", "Error", "OK", "Error")
        return $false
    }
    
    try {
        Write-ScarifyLog "🚀 Launching: $ScriptName $Arguments" "INFO"
        
        $processArgs = @{
            FilePath = "powershell.exe"
            ArgumentList = @("-ExecutionPolicy", "Bypass", "-File", $scriptPath) + ($Arguments -split " " | Where-Object { $_ -ne "" })
            NoNewWindow = -not $ShowWindow
            PassThru = $true
        }
        
        $process = Start-Process @processArgs
        
        if ($process) {
            Write-ScarifyLog "✅ Successfully launched: $ScriptName (PID: $($process.Id))" "SUCCESS"
            return $true
        } else {
            Write-ScarifyLog "❌ Failed to launch: $ScriptName" "ERROR"
            return $false
        }
    } catch {
        Write-ScarifyLog "❌ Error launching $ScriptName`: $($_.Exception.Message)" "ERROR"
        [System.Windows.Forms.MessageBox]::Show("Error launching script: $($_.Exception.Message)", "Error", "OK", "Error")
        return $false
    }
}

function Open-ScarifyFolder {
    param([string]$FolderName)
    
    $folderPath = switch ($FolderName) {
        "Output" { Join-Path $Global:CurrentWorkingDir "Output" }
        "Shorts" { Join-Path $Global:CurrentWorkingDir "Output/Shorts" }
        "Logs" { Join-Path $Global:CurrentWorkingDir "logs" }
        "Temp" { Join-Path $Global:CurrentWorkingDir "temp" }
        "Videos" { Join-Path $Global:CurrentWorkingDir "Output/Videos" }
        "Root" { $Global:CurrentWorkingDir }
        default { Join-Path $Global:CurrentWorkingDir $FolderName }
    }
    
    if (Test-Path $folderPath) {
        try {
            if ($IsWindows -or $env:OS -eq "Windows_NT") {
                Start-Process "explorer.exe" -ArgumentList $folderPath
            } else {
                # Linux/Mac - try common file managers
                if (Get-Command nautilus -ErrorAction SilentlyContinue) {
                    Start-Process "nautilus" -ArgumentList $folderPath
                } elseif (Get-Command open -ErrorAction SilentlyContinue) {
                    Start-Process "open" -ArgumentList $folderPath
                } else {
                    Write-ScarifyLog "📂 Folder path: $folderPath" "INFO"
                    Get-ChildItem $folderPath | Format-Table Name, LastWriteTime, Length
                }
            }
            Write-ScarifyLog "📂 Opened folder: $FolderName" "SUCCESS"
        } catch {
            Write-ScarifyLog "❌ Failed to open folder: $FolderName - $($_.Exception.Message)" "ERROR"
        }
    } else {
        Write-ScarifyLog "❌ Folder not found: $folderPath" "ERROR"
        
        # Try to create it
        try {
            New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
            Write-ScarifyLog "📁 Created folder: $FolderName" "SUCCESS"
            Open-ScarifyFolder -FolderName $FolderName
        } catch {
            Write-ScarifyLog "❌ Could not create folder: $folderPath" "ERROR"
        }
    }
}

# ================================================
# SYSTEM STATUS FUNCTIONS
# ================================================

function Get-ScarifySystemStatus {
    Write-ScarifyLog "🔍 Checking system status..." "INFO"
    
    $status = @{
        MasterLaunch = Test-Path (Join-Path $Global:CurrentWorkingDir "MasterLaunch.ps1")
        MasterControl = Test-Path (Join-Path $Global:CurrentWorkingDir "MasterControl.ps1")
        OutputDir = Test-Path (Join-Path $Global:CurrentWorkingDir "Output")
        LogsDir = Test-Path (Join-Path $Global:CurrentWorkingDir "logs")
        TempDir = Test-Path (Join-Path $Global:CurrentWorkingDir "temp")
        PowerShell = $true
    }
    
    $statusText = "System Status:`n"
    foreach ($component in $status.Keys) {
        $icon = if ($status[$component]) { "✅" } else { "❌" }
        $statusText += "$icon $component`n"
    }
    
    $allGreen = ($status.Values | Where-Object { $_ -eq $false }).Count -eq 0
    
    if ($allGreen) {
        $Global:StatusText = "All Systems Operational"
        Write-ScarifyLog "✅ All systems operational!" "SUCCESS"
    } else {
        $Global:StatusText = "System Issues Detected"
        Write-ScarifyLog "⚠️ Some system components need attention" "WARNING"
    }
    
    [System.Windows.Forms.MessageBox]::Show($statusText, "SCARIFY System Status", "OK", "Information")
    return $status
}

# ================================================
# GUI CREATION
# ================================================

function New-ScarifyMainForm {
    if (-not $SupportsGUI) {
        Write-ScarifyLog "❌ GUI not supported on this platform" "ERROR"
        return $null
    }
    
    Write-ScarifyLog "🖼️ Initializing SCARIFY GUI..." "INFO"
    
    # Main Form
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "SCARIFY Desktop Launcher v1.0 - Video Production Suite"
    $form.Size = New-Object System.Drawing.Size(900, 700)
    $form.StartPosition = "CenterScreen"
    $form.FormBorderStyle = "FixedSingle"
    $form.MaximizeBox = $false
    $form.BackColor = [System.Drawing.Color]::FromArgb(40, 40, 40)
    $form.ForeColor = [System.Drawing.Color]::White
    
    # Title Panel
    $titlePanel = New-Object System.Windows.Forms.Panel
    $titlePanel.Size = New-Object System.Drawing.Size(880, 60)
    $titlePanel.Location = New-Object System.Drawing.Point(10, 10)
    $titlePanel.BackColor = [System.Drawing.Color]::FromArgb(25, 25, 25)
    $titlePanel.BorderStyle = "FixedSingle"
    
    $titleLabel = New-Object System.Windows.Forms.Label
    $titleLabel.Text = "🎬 SCARIFY DESKTOP LAUNCHER"
    $titleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
    $titleLabel.ForeColor = [System.Drawing.Color]::FromArgb(0, 180, 255)
    $titleLabel.Location = New-Object System.Drawing.Point(20, 15)
    $titleLabel.Size = New-Object System.Drawing.Size(400, 30)
    $titlePanel.Controls.Add($titleLabel)
    
    $subtitleLabel = New-Object System.Windows.Forms.Label
    $subtitleLabel.Text = "Complete Video Production & YouTube Upload Suite"
    $subtitleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 9)
    $subtitleLabel.ForeColor = [System.Drawing.Color]::LightGray
    $subtitleLabel.Location = New-Object System.Drawing.Point(450, 20)
    $subtitleLabel.Size = New-Object System.Drawing.Size(400, 20)
    $titlePanel.Controls.Add($subtitleLabel)
    
    $form.Controls.Add($titlePanel)
    
    # Main Control Buttons Panel
    $controlPanel = New-Object System.Windows.Forms.Panel
    $controlPanel.Size = New-Object System.Drawing.Size(430, 350)
    $controlPanel.Location = New-Object System.Drawing.Point(10, 80)
    $controlPanel.BackColor = [System.Drawing.Color]::FromArgb(50, 50, 50)
    $controlPanel.BorderStyle = "FixedSingle"
    
    $controlTitle = New-Object System.Windows.Forms.Label
    $controlTitle.Text = "📺 MAIN CONTROL PANEL"
    $controlTitle.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
    $controlTitle.ForeColor = [System.Drawing.Color]::Yellow
    $controlTitle.Location = New-Object System.Drawing.Point(10, 10)
    $controlTitle.Size = New-Object System.Drawing.Size(400, 25)
    $controlPanel.Controls.Add($controlTitle)
    
    # Control buttons
    $buttons = @(
        @{ Text = "⚡ Lightning Strike"; Y = 45; Action = "LightningStrike"; Color = "Orange" },
        @{ Text = "🎵 Audio Enhancement"; Y = 85; Action = "AudioEnhancement"; Color = "Purple" },
        @{ Text = "🔄 Full Pipeline"; Y = 125; Action = "FullPipeline"; Color = "Green" },
        @{ Text = "📺 YouTube Studio"; Y = 165; Action = "YouTubeStudio"; Color = "Red" },
        @{ Text = "🌐 Multilingual Batch"; Y = 205; Action = "MultilingualBatch"; Color = "Blue" },
        @{ Text = "💰 Monetization Optimizer"; Y = 245; Action = "MonetizationOptimizer"; Color = "Gold" },
        @{ Text = "📊 System Status"; Y = 285; Action = "SystemStatus"; Color = "Cyan" },
        @{ Text = "🔧 Advanced Tools"; Y = 315; Action = "AdvancedTools"; Color = "Magenta" }
    )
    
    foreach ($buttonInfo in $buttons) {
        $button = New-Object System.Windows.Forms.Button
        $button.Text = $buttonInfo.Text
        $button.Size = New-Object System.Drawing.Size(200, 30)
        $button.Location = New-Object System.Drawing.Point(10, $buttonInfo.Y)
        $button.BackColor = [System.Drawing.Color]::FromArgb(70, 70, 70)
        $button.ForeColor = [System.Drawing.Color]::White
        $button.FlatStyle = "Flat"
        $button.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
        
        # Add click event
        $action = $buttonInfo.Action
        $button.Add_Click({
            param($sender, $e)
            $actionName = $sender.Tag
            Invoke-ScarifyAction -Action $actionName
        }.GetNewClosure())
        $button.Tag = $action
        
        $controlPanel.Controls.Add($button)
    }
    
    $form.Controls.Add($controlPanel)
    
    # Quick Access Panel
    $quickPanel = New-Object System.Windows.Forms.Panel
    $quickPanel.Size = New-Object System.Drawing.Size(430, 200)
    $quickPanel.Location = New-Object System.Drawing.Point(450, 80)
    $quickPanel.BackColor = [System.Drawing.Color]::FromArgb(50, 50, 50)
    $quickPanel.BorderStyle = "FixedSingle"
    
    $quickTitle = New-Object System.Windows.Forms.Label
    $quickTitle.Text = "📁 QUICK ACCESS"
    $quickTitle.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
    $quickTitle.ForeColor = [System.Drawing.Color]::Yellow
    $quickTitle.Location = New-Object System.Drawing.Point(10, 10)
    $quickTitle.Size = New-Object System.Drawing.Size(400, 25)
    $quickPanel.Controls.Add($quickTitle)
    
    # Quick access buttons
    $quickButtons = @(
        @{ Text = "📂 Output Folder"; Y = 45; Folder = "Output" },
        @{ Text = "🎬 Shorts Folder"; Y = 75; Folder = "Shorts" },
        @{ Text = "📋 Logs Folder"; Y = 105; Folder = "Logs" },
        @{ Text = "🗂️ Temp Folder"; Y = 135; Folder = "Temp" },
        @{ Text = "🎥 Videos Folder"; Y = 165; Folder = "Videos" }
    )
    
    foreach ($quickButton in $quickButtons) {
        $button = New-Object System.Windows.Forms.Button
        $button.Text = $quickButton.Text
        $button.Size = New-Object System.Drawing.Size(180, 25)
        $button.Location = New-Object System.Drawing.Point(10, $quickButton.Y)
        $button.BackColor = [System.Drawing.Color]::FromArgb(60, 90, 60)
        $button.ForeColor = [System.Drawing.Color]::White
        $button.FlatStyle = "Flat"
        $button.Font = New-Object System.Drawing.Font("Segoe UI", 8)
        
        $folder = $quickButton.Folder
        $button.Add_Click({
            param($sender, $e)
            $folderName = $sender.Tag
            Open-ScarifyFolder -FolderName $folderName
        }.GetNewClosure())
        $button.Tag = $folder
        
        $quickPanel.Controls.Add($button)
    }
    
    $form.Controls.Add($quickPanel)
    
    # Log Display Panel
    $logPanel = New-Object System.Windows.Forms.Panel
    $logPanel.Size = New-Object System.Drawing.Size(870, 220)
    $logPanel.Location = New-Object System.Drawing.Point(10, 440)
    $logPanel.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
    $logPanel.BorderStyle = "FixedSingle"
    
    $logTitle = New-Object System.Windows.Forms.Label
    $logTitle.Text = "📊 SYSTEM LOG & STATUS"
    $logTitle.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
    $logTitle.ForeColor = [System.Drawing.Color]::Yellow
    $logTitle.Location = New-Object System.Drawing.Point(10, 10)
    $logTitle.Size = New-Object System.Drawing.Size(400, 25)
    $logPanel.Controls.Add($logTitle)
    
    # Log TextBox
    $logTextBox = New-Object System.Windows.Forms.TextBox
    $logTextBox.Multiline = $true
    $logTextBox.ScrollBars = "Vertical"
    $logTextBox.Size = New-Object System.Drawing.Size(850, 150)
    $logTextBox.Location = New-Object System.Drawing.Point(10, 40)
    $logTextBox.BackColor = [System.Drawing.Color]::Black
    $logTextBox.ForeColor = [System.Drawing.Color]::Lime
    $logTextBox.Font = New-Object System.Drawing.Font("Consolas", 9)
    $logTextBox.ReadOnly = $true
    $logTextBox.Text = "SCARIFY Desktop Launcher initialized...`nReady for operations."
    $logPanel.Controls.Add($logTextBox)
    
    # Status Label
    $statusLabel = New-Object System.Windows.Forms.Label
    $statusLabel.Text = "Status: System Ready"
    $statusLabel.Font = New-Object System.Drawing.Font("Segoe UI", 9)
    $statusLabel.ForeColor = [System.Drawing.Color]::LightGreen
    $statusLabel.Location = New-Object System.Drawing.Point(10, 195)
    $statusLabel.Size = New-Object System.Drawing.Size(850, 20)
    $logPanel.Controls.Add($statusLabel)
    
    $form.Controls.Add($logPanel)
    
    # Store references globally
    $Global:Form = $form
    $Global:LogTextBox = $logTextBox
    $Global:StatusLabel = $statusLabel
    
    # Setup Form Events
    $form.Add_FormClosing({
        Write-ScarifyLog "👋 SCARIFY Desktop Launcher closing..." "INFO"
    })
    
    Write-ScarifyLog "✅ GUI initialized successfully!" "SUCCESS"
    return $form
}

# ================================================
# ACTION HANDLERS
# ================================================

function Invoke-ScarifyAction {
    param([string]$Action)
    
    Write-ScarifyLog "🎯 Executing action: $Action" "INFO"
    
    switch ($Action) {
        "LightningStrike" {
            $result = Invoke-ScarifyScript -ScriptName "MasterLaunch.ps1" -Arguments "-Mode full -Campaign awakening -Deploy" -ShowWindow
            if ($result) {
                Write-ScarifyLog "⚡ Lightning Strike Protocol initiated!" "SUCCESS"
            }
        }
        
        "AudioEnhancement" {
            Write-ScarifyLog "🎵 Launching Audio Enhancement module..." "INFO"
            $result = Invoke-ScarifyScript -ScriptName "MasterControl.ps1" -Arguments "-Operation execute -TemplateProfile audio_enhanced" -ShowWindow
            if ($result) {
                Write-ScarifyLog "🎵 Audio Enhancement started!" "SUCCESS"
            }
        }
        
        "FullPipeline" {
            Write-ScarifyLog "🔄 Initiating Full Pipeline workflow..." "INFO"
            $result = Invoke-ScarifyScript -ScriptName "MasterLaunch.ps1" -Arguments "-Mode full -Campaign memory_merchants -Deploy -Count 3" -ShowWindow
            if ($result) {
                Write-ScarifyLog "🔄 Full Pipeline initiated!" "SUCCESS"
            }
        }
        
        "YouTubeStudio" {
            Write-ScarifyLog "📺 Opening YouTube Studio interface..." "INFO"
            try {
                Start-Process "https://studio.youtube.com"
                Write-ScarifyLog "📺 YouTube Studio opened in browser!" "SUCCESS"
            } catch {
                Write-ScarifyLog "❌ Failed to open YouTube Studio: $($_.Exception.Message)" "ERROR"
            }
        }
        
        "MultilingualBatch" {
            Write-ScarifyLog "🌐 Starting Multilingual Batch processing..." "INFO"
            $result = Invoke-ScarifyScript -ScriptName "MasterControl.ps1" -Arguments "-Operation execute -TemplateProfile multilingual -VoiceFiles 30" -ShowWindow
            if ($result) {
                Write-ScarifyLog "🌐 Multilingual Batch started!" "SUCCESS"
            }
        }
        
        "MonetizationOptimizer" {
            Write-ScarifyLog "💰 Launching Monetization Optimizer..." "INFO"
            # Could launch a specific monetization script or open a web interface
            try {
                Start-Process "notepad.exe" -ArgumentList (Join-Path $Global:CurrentWorkingDir "6_Monetization\monetization_notes.txt")
                Write-ScarifyLog "💰 Monetization Optimizer interface opened!" "SUCCESS"
            } catch {
                Write-ScarifyLog "💰 Creating monetization workspace..." "INFO"
                Open-ScarifyFolder -FolderName "6_Monetization"
            }
        }
        
        "SystemStatus" {
            Get-ScarifySystemStatus
        }
        
        "AdvancedTools" {
            Write-ScarifyLog "🔧 Opening Advanced Tools..." "INFO"
            $tools = @(
                "System Status Check",
                "Create Desktop Shortcuts", 
                "Reinitialize Directories",
                "Open Root Folder",
                "Clear Logs",
                "Exit Application"
            )
            
            $selection = Show-ScarifyMenu -Title "Advanced Tools" -Options $tools
            
            switch ($selection) {
                "System Status Check" { Get-ScarifySystemStatus }
                "Create Desktop Shortcuts" { Initialize-DesktopShortcuts }
                "Reinitialize Directories" { Initialize-ScarifyDirectories }
                "Open Root Folder" { Open-ScarifyFolder -FolderName "Root" }
                "Clear Logs" { 
                    $Global:LogBuffer = @()
                    $Global:LogTextBox.Text = "Logs cleared."
                    Write-ScarifyLog "🗑️ Log buffer cleared!" "INFO"
                }
                "Exit Application" { $Global:Form.Close() }
            }
        }
        
        default {
            Write-ScarifyLog "❓ Unknown action: $Action" "WARNING"
        }
    }
}

function Show-ScarifyMenu {
    param(
        [string]$Title,
        [string[]]$Options
    )
    
    $menuForm = New-Object System.Windows.Forms.Form
    $menuForm.Text = $Title
    $menuForm.Size = New-Object System.Drawing.Size(400, 300)
    $menuForm.StartPosition = "CenterParent"
    $menuForm.BackColor = [System.Drawing.Color]::FromArgb(40, 40, 40)
    $menuForm.ForeColor = [System.Drawing.Color]::White
    
    $listBox = New-Object System.Windows.Forms.ListBox
    $listBox.Size = New-Object System.Drawing.Size(360, 200)
    $listBox.Location = New-Object System.Drawing.Point(10, 10)
    $listBox.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
    $listBox.ForeColor = [System.Drawing.Color]::White
    
    foreach ($option in $Options) {
        $listBox.Items.Add($option) | Out-Null
    }
    
    $okButton = New-Object System.Windows.Forms.Button
    $okButton.Text = "OK"
    $okButton.Size = New-Object System.Drawing.Size(75, 25)
    $okButton.Location = New-Object System.Drawing.Point(150, 220)
    $okButton.BackColor = [System.Drawing.Color]::FromArgb(70, 70, 70)
    $okButton.ForeColor = [System.Drawing.Color]::White
    
    $selectedOption = $null
    $okButton.Add_Click({
        if ($listBox.SelectedItem) {
            $selectedOption = $listBox.SelectedItem
            $menuForm.Close()
        }
    })
    
    $menuForm.Controls.Add($listBox)
    $menuForm.Controls.Add($okButton)
    
    $menuForm.ShowDialog() | Out-Null
    return $selectedOption
}

# ================================================
# MAIN EXECUTION
# ================================================

function Start-ScarifyLauncher {
    Write-Host "🚀 Starting SCARIFY Desktop Launcher..." -ForegroundColor Magenta
    Write-Host "📍 Install Path: $InstallPath" -ForegroundColor Cyan
    Write-Host "🖥️ GUI Support: $SupportsGUI" -ForegroundColor Cyan
    
    # Setup if requested
    if ($Setup) {
        Write-ScarifyLog "🏗️ Running setup procedures..." "INFO"
        Initialize-ScarifyDirectories
        if ($SupportsGUI -and ($IsWindows -or $env:OS -eq "Windows_NT")) {
            Initialize-DesktopShortcuts
        }
    }
    
    # Initialize directories
    Initialize-ScarifyDirectories
    Write-ScarifyLog "🎬 SCARIFY Desktop Launcher ready!" "SUCCESS"
    Write-ScarifyLog "📺 All video production tools available" "INFO"
    Write-ScarifyLog "⚡ Lightning Strike Protocol armed and ready" "INFO"
    
    if ($SupportsGUI) {
        # Create and show the main form
        $form = New-ScarifyMainForm
        
        # Show the form
        [System.Windows.Forms.Application]::EnableVisualStyles()
        $form.ShowDialog() | Out-Null
    } else {
        # Console mode
        Write-ScarifyLog "💻 Running in console mode" "INFO"
        Show-ConsoleMenu
    }
    
    Write-ScarifyLog "👋 Session ended. Goodbye!" "INFO"
}

function Show-ConsoleMenu {
    do {
        Clear-Host
        Write-Host "🎬 SCARIFY DESKTOP LAUNCHER - CONSOLE MODE" -ForegroundColor Magenta
        Write-Host "=" * 50 -ForegroundColor Cyan
        Write-Host "1. ⚡ Lightning Strike Protocol"
        Write-Host "2. 🎵 Audio Enhancement"  
        Write-Host "3. 🔄 Full Pipeline"
        Write-Host "4. 📺 YouTube Studio" 
        Write-Host "5. 🌐 Multilingual Batch"
        Write-Host "6. 💰 Monetization Optimizer"
        Write-Host "7. 📊 System Status"
        Write-Host "8. 🔧 Advanced Tools"
        Write-Host "9. 📂 Open Folders Menu"
        Write-Host "0. Exit"
        Write-Host "=" * 50 -ForegroundColor Cyan
        
        $choice = Read-Host "Select option (0-9)"
        
        switch ($choice) {
            "1" { Invoke-ScarifyAction -Action "LightningStrike" }
            "2" { Invoke-ScarifyAction -Action "AudioEnhancement" }
            "3" { Invoke-ScarifyAction -Action "FullPipeline" }
            "4" { Invoke-ScarifyAction -Action "YouTubeStudio" }
            "5" { Invoke-ScarifyAction -Action "MultilingualBatch" }
            "6" { Invoke-ScarifyAction -Action "MonetizationOptimizer" }
            "7" { Invoke-ScarifyAction -Action "SystemStatus" }
            "8" { Invoke-ScarifyAction -Action "AdvancedTools" }
            "9" { Show-FolderMenu }
            "0" { break }
            default { Write-Host "Invalid option. Please try again." -ForegroundColor Red }
        }
        
        if ($choice -ne "0") {
            Read-Host "Press Enter to continue"
        }
    } while ($choice -ne "0")
}

function Show-FolderMenu {
    do {
        Clear-Host
        Write-Host "📂 FOLDER ACCESS MENU" -ForegroundColor Yellow
        Write-Host "=" * 30 -ForegroundColor Cyan
        Write-Host "1. Output Folder"
        Write-Host "2. Shorts Folder"
        Write-Host "3. Logs Folder"
        Write-Host "4. Temp Folder"
        Write-Host "5. Videos Folder"
        Write-Host "6. Root Folder"
        Write-Host "0. Back to Main Menu"
        Write-Host "=" * 30 -ForegroundColor Cyan
        
        $choice = Read-Host "Select folder (0-6)"
        
        switch ($choice) {
            "1" { Open-ScarifyFolder -FolderName "Output" }
            "2" { Open-ScarifyFolder -FolderName "Shorts" }
            "3" { Open-ScarifyFolder -FolderName "Logs" }
            "4" { Open-ScarifyFolder -FolderName "Temp" }
            "5" { Open-ScarifyFolder -FolderName "Videos" }
            "6" { Open-ScarifyFolder -FolderName "Root" }
            "0" { break }
            default { Write-Host "Invalid option. Please try again." -ForegroundColor Red }
        }
        
        if ($choice -ne "0") {
            Read-Host "Press Enter to continue"
        }
    } while ($choice -ne "0")
}

# ================================================
# SCRIPT ENTRY POINT
# ================================================

if ($MyInvocation.InvocationName -ne '.') {
    Start-ScarifyLauncher
}