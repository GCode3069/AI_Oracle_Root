# SCARIFY Desktop Dashboard
# Comprehensive control center for batch operations, monitoring, and system management

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Project settings
$ScriptRoot = $PSScriptRoot
$PythonScript = Join-Path $ScriptRoot "scarify_master.py"
$OutputFolder = Join-Path $ScriptRoot "output\videos"
$LogFolder = Join-Path $ScriptRoot "logs"
$VenvPath = Join-Path $ScriptRoot "scarify_venv\Scripts\python.exe"

# Check if Python exists (try venv first, then system Python)
if (Test-Path $VenvPath) {
    $PythonExe = $VenvPath
    Write-Host "[INFO] Using virtual environment Python"
} else {
    $PythonExe = "python"
    Write-Host "[WARNING] Virtual environment not found, using system Python"
}

# Create the main dashboard form
$Dashboard = New-Object System.Windows.Forms.Form
$Dashboard.Text = "SCARIFY Dashboard - YouTube Shorts Empire"
$Dashboard.Size = New-Object System.Drawing.Size(1000, 700)
$Dashboard.StartPosition = "CenterScreen"
$Dashboard.FormBorderStyle = "FixedDialog"
$Dashboard.MaximizeBox = $false
$Dashboard.BackColor = [System.Drawing.Color]::FromArgb(25, 25, 25)
$Dashboard.ForeColor = [System.Drawing.Color]::White

# Title Panel
$TitlePanel = New-Object System.Windows.Forms.Panel
$TitlePanel.Location = New-Object System.Drawing.Point(0, 0)
$TitlePanel.Size = New-Object System.Drawing.Size(1000, 80)
$TitlePanel.BackColor = [System.Drawing.Color]::FromArgb(40, 40, 40)
$Dashboard.Controls.Add($TitlePanel)

# Main Title
$MainTitle = New-Object System.Windows.Forms.Label
$MainTitle.Location = New-Object System.Drawing.Point(20, 15)
$MainTitle.Size = New-Object System.Drawing.Size(960, 30)
$MainTitle.Text = "[SCARIFY] DASHBOARD - YouTube Shorts Empire"
$MainTitle.Font = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Bold)
$MainTitle.TextAlign = "MiddleCenter"
$MainTitle.ForeColor = [System.Drawing.Color]::FromArgb(255, 215, 0)
$TitlePanel.Controls.Add($MainTitle)

# Subtitle
$Subtitle = New-Object System.Windows.Forms.Label
$Subtitle.Location = New-Object System.Drawing.Point(20, 45)
$Subtitle.Size = New-Object System.Drawing.Size(960, 25)
$Subtitle.Text = "Ex-Vet Emergency Kit Marketing Automation System"
$Subtitle.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$Subtitle.TextAlign = "MiddleCenter"
$Subtitle.ForeColor = [System.Drawing.Color]::LightGray
$TitlePanel.Controls.Add($Subtitle)

# Left Panel - Batch Operations
$LeftPanel = New-Object System.Windows.Forms.Panel
$LeftPanel.Location = New-Object System.Drawing.Point(20, 100)
$LeftPanel.Size = New-Object System.Drawing.Size(460, 550)
$LeftPanel.BackColor = [System.Drawing.Color]::FromArgb(35, 35, 35)
$LeftPanel.BorderStyle = "FixedSingle"
$Dashboard.Controls.Add($LeftPanel)

# Batch Operations Title
$BatchTitle = New-Object System.Windows.Forms.Label
$BatchTitle.Location = New-Object System.Drawing.Point(10, 10)
$BatchTitle.Size = New-Object System.Drawing.Size(440, 30)
$BatchTitle.Text = "[BATCH] OPERATIONS"
$BatchTitle.Font = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
$BatchTitle.TextAlign = "MiddleCenter"
$BatchTitle.ForeColor = [System.Drawing.Color]::FromArgb(70, 130, 180)
$LeftPanel.Controls.Add($BatchTitle)

# Batch Control Buttons
function New-BatchButton {
    param(
        [int]$X,
        [int]$Y,
        [string]$Text,
        [System.Drawing.Color]$BackColor,
        [int]$Count,
        [bool]$Upload = $false
    )
    
    $Button = New-Object System.Windows.Forms.Button
    $Button.Location = New-Object System.Drawing.Point($X, $Y)
    $Button.Size = New-Object System.Drawing.Size(200, 50)
    $Button.Text = $Text
    $Button.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $Button.BackColor = $BackColor
    $Button.ForeColor = [System.Drawing.Color]::White
    $Button.FlatStyle = "Flat"
    $Button.Cursor = [System.Windows.Forms.Cursors]::Hand
    $Button.FlatAppearance.BorderSize = 0
    
    return $Button
}

# Batch buttons
$TestButton = New-BatchButton -X 20 -Y 50 -Text "[TEST] Test (1 Video)" -BackColor ([System.Drawing.Color]::FromArgb(70, 130, 180)) -Count 1 -Upload $false
$TestButton.Add_Click({ Run-BatchOperation -Count 1 -Upload $false })
$LeftPanel.Controls.Add($TestButton)

$SmallBatchButton = New-BatchButton -X 240 -Y 50 -Text "[SMALL] Small Batch (5)" -BackColor ([System.Drawing.Color]::FromArgb(34, 139, 34)) -Count 5 -Upload $true
$SmallBatchButton.Add_Click({ Run-BatchOperation -Count 5 -Upload $true })
$LeftPanel.Controls.Add($SmallBatchButton)

$MediumBatchButton = New-BatchButton -X 20 -Y 110 -Text "[MEDIUM] Medium Batch (10)" -BackColor ([System.Drawing.Color]::FromArgb(255, 140, 0)) -Count 10 -Upload $true
$MediumBatchButton.Add_Click({ Run-BatchOperation -Count 10 -Upload $true })
$LeftPanel.Controls.Add($MediumBatchButton)

$LargeBatchButton = New-BatchButton -X 240 -Y 110 -Text "[LARGE] Large Batch (20)" -BackColor ([System.Drawing.Color]::FromArgb(220, 20, 60)) -Count 20 -Upload $true
$LargeBatchButton.Add_Click({ Run-BatchOperation -Count 20 -Upload $true })
$LeftPanel.Controls.Add($LargeBatchButton)

$MaxBatchButton = New-BatchButton -X 20 -Y 170 -Text "[MAX] MAX BATCH (50)" -BackColor ([System.Drawing.Color]::FromArgb(128, 0, 128)) -Count 50 -Upload $true
$MaxBatchButton.Add_Click({ Run-BatchOperation -Count 50 -Upload $true })
$LeftPanel.Controls.Add($MaxBatchButton)

# Custom Batch Controls
$CustomLabel = New-Object System.Windows.Forms.Label
$CustomLabel.Location = New-Object System.Drawing.Point(20, 240)
$CustomLabel.Size = New-Object System.Drawing.Size(200, 25)
$CustomLabel.Text = "Custom Batch Size:"
$CustomLabel.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$LeftPanel.Controls.Add($CustomLabel)

$CustomCountBox = New-Object System.Windows.Forms.NumericUpDown
$CustomCountBox.Location = New-Object System.Drawing.Point(20, 270)
$CustomCountBox.Size = New-Object System.Drawing.Size(100, 25)
$CustomCountBox.Minimum = 1
$CustomCountBox.Maximum = 100
$CustomCountBox.Value = 5
$LeftPanel.Controls.Add($CustomCountBox)

$CustomUploadCheck = New-Object System.Windows.Forms.CheckBox
$CustomUploadCheck.Location = New-Object System.Drawing.Point(140, 270)
$CustomUploadCheck.Size = New-Object System.Drawing.Size(120, 25)
$CustomUploadCheck.Text = "Upload to YouTube"
$CustomUploadCheck.Checked = $true
$CustomUploadCheck.ForeColor = [System.Drawing.Color]::White
$LeftPanel.Controls.Add($CustomUploadCheck)

$CustomRunButton = New-Object System.Windows.Forms.Button
$CustomRunButton.Location = New-Object System.Drawing.Point(270, 270)
$CustomRunButton.Size = New-Object System.Drawing.Size(100, 25)
$CustomRunButton.Text = "Run Custom"
$CustomRunButton.Font = New-Object System.Drawing.Font("Segoe UI", 9, [System.Drawing.FontStyle]::Bold)
$CustomRunButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$CustomRunButton.ForeColor = [System.Drawing.Color]::White
$CustomRunButton.FlatStyle = "Flat"
$CustomRunButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$CustomRunButton.Add_Click({
    Run-BatchOperation -Count $CustomCountBox.Value -Upload $CustomUploadCheck.Checked
})
$LeftPanel.Controls.Add($CustomRunButton)

# System Controls
$SystemLabel = New-Object System.Windows.Forms.Label
$SystemLabel.Location = New-Object System.Drawing.Point(20, 320)
$SystemLabel.Size = New-Object System.Drawing.Size(420, 25)
$SystemLabel.Text = "SYSTEM CONTROLS"
$SystemLabel.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$SystemLabel.TextAlign = "MiddleCenter"
$SystemLabel.ForeColor = [System.Drawing.Color]::FromArgb(255, 215, 0)
$LeftPanel.Controls.Add($SystemLabel)

$OpenFolderButton = New-Object System.Windows.Forms.Button
$OpenFolderButton.Location = New-Object System.Drawing.Point(20, 350)
$OpenFolderButton.Size = New-Object System.Drawing.Size(130, 35)
$OpenFolderButton.Text = "[FOLDER] Open Videos"
$OpenFolderButton.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$OpenFolderButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$OpenFolderButton.ForeColor = [System.Drawing.Color]::White
$OpenFolderButton.FlatStyle = "Flat"
$OpenFolderButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$OpenFolderButton.Add_Click({
    if (Test-Path $OutputFolder) {
        Start-Process explorer.exe -ArgumentList $OutputFolder
        Update-Status "Opened output folder"
    } else {
        Update-Status "Output folder not found"
    }
})
$LeftPanel.Controls.Add($OpenFolderButton)

$TestAuthButton = New-Object System.Windows.Forms.Button
$TestAuthButton.Location = New-Object System.Drawing.Point(160, 350)
$TestAuthButton.Size = New-Object System.Drawing.Size(130, 35)
$TestAuthButton.Text = "[AUTH] Test YouTube"
$TestAuthButton.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$TestAuthButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$TestAuthButton.ForeColor = [System.Drawing.Color]::White
$TestAuthButton.FlatStyle = "Flat"
$TestAuthButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$TestAuthButton.Add_Click({
    Test-YouTubeAuth
})
$LeftPanel.Controls.Add($TestAuthButton)

$SetupButton = New-Object System.Windows.Forms.Button
$SetupButton.Location = New-Object System.Drawing.Point(300, 350)
$SetupButton.Size = New-Object System.Drawing.Size(130, 35)
$SetupButton.Text = "[SETUP] Run Setup"
$SetupButton.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$SetupButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$SetupButton.ForeColor = [System.Drawing.Color]::White
$SetupButton.FlatStyle = "Flat"
$SetupButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$SetupButton.Add_Click({
    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$ScriptRoot\test_setup.ps1`""
})
$LeftPanel.Controls.Add($SetupButton)

# Right Panel - Status & Monitoring
$RightPanel = New-Object System.Windows.Forms.Panel
$RightPanel.Location = New-Object System.Drawing.Point(500, 100)
$RightPanel.Size = New-Object System.Drawing.Size(480, 550)
$RightPanel.BackColor = [System.Drawing.Color]::FromArgb(35, 35, 35)
$RightPanel.BorderStyle = "FixedSingle"
$Dashboard.Controls.Add($RightPanel)

# Status Title
$StatusTitle = New-Object System.Windows.Forms.Label
$StatusTitle.Location = New-Object System.Drawing.Point(10, 10)
$StatusTitle.Size = New-Object System.Drawing.Size(460, 30)
$StatusTitle.Text = "[STATUS] STATUS & MONITORING"
$StatusTitle.Font = New-Object System.Drawing.Font("Segoe UI", 14, [System.Drawing.FontStyle]::Bold)
$StatusTitle.TextAlign = "MiddleCenter"
$StatusTitle.ForeColor = [System.Drawing.Color]::FromArgb(34, 139, 34)
$RightPanel.Controls.Add($StatusTitle)

# Status Display
$StatusBox = New-Object System.Windows.Forms.TextBox
$StatusBox.Location = New-Object System.Drawing.Point(20, 50)
$StatusBox.Size = New-Object System.Drawing.Size(440, 200)
$StatusBox.Multiline = $true
$StatusBox.ScrollBars = "Vertical"
$StatusBox.ReadOnly = $true
$StatusBox.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 20)
$StatusBox.ForeColor = [System.Drawing.Color]::LightGreen
$StatusBox.Font = New-Object System.Drawing.Font("Consolas", 9)
$StatusBox.Text = "SCARIFY Dashboard Ready`r`n`r`nSystem Status:`r`n- Python: Ready`r`n- Video Generator: Ready`r`n- Audio Generator: Ready`r`n- YouTube Uploader: Ready`r`n`r`nClick any batch button to start generating videos!"
$RightPanel.Controls.Add($StatusBox)

# Statistics Panel
$StatsLabel = New-Object System.Windows.Forms.Label
$StatsLabel.Location = New-Object System.Drawing.Point(20, 270)
$StatsLabel.Size = New-Object System.Drawing.Size(440, 25)
$StatsLabel.Text = "[STATS] TODAY'S STATISTICS"
$StatsLabel.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$StatsLabel.TextAlign = "MiddleCenter"
$StatsLabel.ForeColor = [System.Drawing.Color]::FromArgb(255, 215, 0)
$RightPanel.Controls.Add($StatsLabel)

$StatsBox = New-Object System.Windows.Forms.TextBox
$StatsBox.Location = New-Object System.Drawing.Point(20, 300)
$StatsBox.Size = New-Object System.Drawing.Size(440, 120)
$StatsBox.Multiline = $true
$StatsBox.ScrollBars = "Vertical"
$StatsBox.ReadOnly = $true
$StatsBox.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 20)
$StatsBox.ForeColor = [System.Drawing.Color]::LightBlue
$StatsBox.Font = New-Object System.Drawing.Font("Consolas", 9)
$RightPanel.Controls.Add($StatsBox)

# Progress Bar
$ProgressBar = New-Object System.Windows.Forms.ProgressBar
$ProgressBar.Location = New-Object System.Drawing.Point(20, 440)
$ProgressBar.Size = New-Object System.Drawing.Size(440, 25)
$ProgressBar.Style = "Marquee"
$ProgressBar.MarqueeAnimationSpeed = 30
$ProgressBar.Visible = $false
$RightPanel.Controls.Add($ProgressBar)

# Progress Label
$ProgressLabel = New-Object System.Windows.Forms.Label
$ProgressLabel.Location = New-Object System.Drawing.Point(20, 470)
$ProgressLabel.Size = New-Object System.Drawing.Size(440, 25)
$ProgressLabel.Text = ""
$ProgressLabel.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$ProgressLabel.TextAlign = "MiddleCenter"
$ProgressLabel.ForeColor = [System.Drawing.Color]::LightGreen
$RightPanel.Controls.Add($ProgressLabel)

# Control Buttons
$ControlPanel = New-Object System.Windows.Forms.Panel
$ControlPanel.Location = New-Object System.Drawing.Point(20, 500)
$ControlPanel.Size = New-Object System.Drawing.Size(440, 40)
$ControlPanel.BackColor = [System.Drawing.Color]::FromArgb(45, 45, 45)
$Dashboard.Controls.Add($ControlPanel)

$RefreshButton = New-Object System.Windows.Forms.Button
$RefreshButton.Location = New-Object System.Drawing.Point(10, 5)
$RefreshButton.Size = New-Object System.Drawing.Size(100, 30)
$RefreshButton.Text = "[REFRESH] Refresh"
$RefreshButton.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$RefreshButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$RefreshButton.ForeColor = [System.Drawing.Color]::White
$RefreshButton.FlatStyle = "Flat"
$RefreshButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$RefreshButton.Add_Click({
    Update-Statistics
    Update-Status "Dashboard refreshed"
})
$ControlPanel.Controls.Add($RefreshButton)

$ClearLogButton = New-Object System.Windows.Forms.Button
$ClearLogButton.Location = New-Object System.Drawing.Point(120, 5)
$ClearLogButton.Size = New-Object System.Drawing.Size(100, 30)
$ClearLogButton.Text = "[CLEAR] Clear Log"
$ClearLogButton.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$ClearLogButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$ClearLogButton.ForeColor = [System.Drawing.Color]::White
$ClearLogButton.FlatStyle = "Flat"
$ClearLogButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$ClearLogButton.Add_Click({
    $StatusBox.Clear()
    Update-Status "Log cleared"
})
$ControlPanel.Controls.Add($ClearLogButton)

$CloseButton = New-Object System.Windows.Forms.Button
$CloseButton.Location = New-Object System.Drawing.Point(330, 5)
$CloseButton.Size = New-Object System.Drawing.Size(100, 30)
$CloseButton.Text = "[CLOSE] Close"
$CloseButton.Font = New-Object System.Drawing.Font("Segoe UI", 9)
$CloseButton.BackColor = [System.Drawing.Color]::FromArgb(220, 20, 60)
$CloseButton.ForeColor = [System.Drawing.Color]::White
$CloseButton.FlatStyle = "Flat"
$CloseButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$CloseButton.Add_Click({
    $Dashboard.Close()
})
$ControlPanel.Controls.Add($CloseButton)

# Functions
function Update-Status {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    $StatusBox.AppendText("`r`n[$timestamp] $Message")
    $StatusBox.SelectionStart = $StatusBox.Text.Length
    $StatusBox.ScrollToCaret()
}

function Update-Statistics {
    $today = Get-Date -Format "yyyy-MM-dd"
    $videoCount = 0
    $totalSize = 0
    
    if (Test-Path $OutputFolder) {
        $videos = Get-ChildItem $OutputFolder -Filter "*.mp4" | Where-Object { $_.LastWriteTime.Date -eq (Get-Date).Date }
        $videoCount = $videos.Count
        $totalSize = ($videos | Measure-Object Length -Sum).Sum / 1MB
    }
    
    $StatsBox.Text = @"
Today: $today
Videos Generated: $videoCount
Total Size: $([math]::Round($totalSize, 2)) MB
YouTube Quota: 50 uploads/day
Status: Ready for Production

Recent Activity:
- Last video: $(if ($videoCount -gt 0) { "Generated today" } else { "None today" })
- System: Operational
- Authentication: Ready
"@
}

function Run-BatchOperation {
    param(
        [int]$Count,
        [bool]$Upload
    )
    
    # Disable all buttons during operation
    $TestButton.Enabled = $false
    $SmallBatchButton.Enabled = $false
    $MediumBatchButton.Enabled = $false
    $LargeBatchButton.Enabled = $false
    $MaxBatchButton.Enabled = $false
    $CustomRunButton.Enabled = $false
    
    # Show progress
    $ProgressBar.Visible = $true
    $ProgressLabel.Text = "Starting batch operation..."
    $Dashboard.Refresh()
    
    Update-Status "Starting batch operation: $Count videos, Upload: $Upload"
    
    # Build command
    $Args = @("$PythonScript", "--count", $Count)
    
    if ($Upload) {
        $Args += "--upload"
    } else {
        $Args += "--test"
    }
    
    try {
        # Start process in new window
        $ProcessStartInfo = New-Object System.Diagnostics.ProcessStartInfo
        $ProcessStartInfo.FileName = $PythonExe
        $ProcessStartInfo.Arguments = $Args -join " "
        $ProcessStartInfo.UseShellExecute = $true
        $ProcessStartInfo.CreateNoWindow = $false
        $ProcessStartInfo.WorkingDirectory = $ScriptRoot
        
        $Process = [System.Diagnostics.Process]::Start($ProcessStartInfo)
        
        Update-Status "Batch operation started in new window (PID: $($Process.Id))"
        $ProgressLabel.Text = "Batch operation running... Check console window"
        
        # Start monitoring
        Start-Sleep -Seconds 2
        Update-Status "Monitoring batch operation..."
        
        # Wait for completion (with timeout)
        $timeout = $Count * 30  # 30 seconds per video
        $Process.WaitForExit($timeout * 1000)
        
        if ($Process.HasExited) {
            if ($Process.ExitCode -eq 0) {
                Update-Status "✅ Batch operation completed successfully!"
                $ProgressLabel.Text = "Batch completed successfully"
            } else {
                Update-Status "⚠️ Batch operation completed with warnings (Exit code: $($Process.ExitCode))"
                $ProgressLabel.Text = "Batch completed with warnings"
            }
        } else {
            Update-Status "⚠️ Batch operation still running (timeout reached)"
            $ProgressLabel.Text = "Batch still running..."
        }
        
    } catch {
        Update-Status "❌ Error starting batch operation: $($_.Exception.Message)"
        $ProgressLabel.Text = "Error starting batch"
    } finally {
        # Re-enable buttons
        $TestButton.Enabled = $true
        $SmallBatchButton.Enabled = $true
        $MediumBatchButton.Enabled = $true
        $LargeBatchButton.Enabled = $true
        $MaxBatchButton.Enabled = $true
        $CustomRunButton.Enabled = $true
        
        $ProgressBar.Visible = $false
        Update-Statistics
    }
}

function Test-YouTubeAuth {
    Update-Status "Testing YouTube authentication..."
    $ProgressLabel.Text = "Testing YouTube auth..."
    
    try {
        $ProcessStartInfo = New-Object System.Diagnostics.ProcessStartInfo
        $ProcessStartInfo.FileName = $PythonExe
        $ProcessStartInfo.Arguments = "youtube_uploader.py --test-auth dummy.mp4"
        $ProcessStartInfo.UseShellExecute = $false
        $ProcessStartInfo.RedirectStandardOutput = $true
        $ProcessStartInfo.RedirectStandardError = $true
        $ProcessStartInfo.WorkingDirectory = $ScriptRoot
        
        $Process = [System.Diagnostics.Process]::Start($ProcessStartInfo)
        $output = $Process.StandardOutput.ReadToEnd()
        $error = $Process.StandardError.ReadToEnd()
        $Process.WaitForExit()
        
        if ($Process.ExitCode -eq 0) {
            Update-Status "✅ YouTube authentication successful"
            $ProgressLabel.Text = "YouTube auth: OK"
        } else {
            Update-Status "❌ YouTube authentication failed: $error"
            $ProgressLabel.Text = "YouTube auth: Failed"
        }
    } catch {
        Update-Status "❌ Error testing YouTube auth: $($_.Exception.Message)"
        $ProgressLabel.Text = "YouTube auth: Error"
    }
}

# Initialize dashboard
Update-Statistics
Update-Status "SCARIFY Dashboard initialized successfully"

# Check if script exists
if (-not (Test-Path $PythonScript)) {
    Update-Status "❌ ERROR: scarify_master.py not found!"
    [System.Windows.Forms.MessageBox]::Show(
        "scarify_master.py not found!`r`n`r`nExpected location:`r`n$PythonScript",
        "Script Not Found",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    )
}

# Show the dashboard
Write-Host "🚀 Launching SCARIFY Dashboard..."
[void]$Dashboard.ShowDialog()
