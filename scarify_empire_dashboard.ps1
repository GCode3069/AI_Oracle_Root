# SCARIFY EMPIRE DASHBOARD - ONE-CLICK YOUTUBE UPLOAD
# Professional GUI with all four features + direct upload

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Project settings
$ScriptRoot = $PSScriptRoot
$PythonScript = Join-Path $ScriptRoot "scarify_master.py"
$OutputFolder = Join-Path $ScriptRoot "output\videos"
$VenvPath = Join-Path $ScriptRoot "scarify_venv\Scripts\python.exe"

# Check if Python exists
if (Test-Path $VenvPath) {
    $PythonExe = $VenvPath
    Write-Host "✅ Using virtual environment Python"
} else {
    $PythonExe = "python"
    Write-Host "⚠️  Virtual environment not found, using system Python"
}

# Create the form
$Form = New-Object System.Windows.Forms.Form
$Form.Text = "🔥 SCARIFY EMPIRE DASHBOARD 🔥"
$Form.Size = New-Object System.Drawing.Size(800, 700)
$Form.StartPosition = "CenterScreen"
$Form.FormBorderStyle = "FixedDialog"
$Form.MaximizeBox = $false
$Form.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 20)
$Form.ForeColor = [System.Drawing.Color]::White

# Title Label
$TitleLabel = New-Object System.Windows.Forms.Label
$TitleLabel.Location = New-Object System.Drawing.Point(20, 20)
$TitleLabel.Size = New-Object System.Drawing.Size(760, 50)
$TitleLabel.Text = "🔥 SCARIFY EMPIRE DASHBOARD 🔥"
$TitleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 18, [System.Drawing.FontStyle]::Bold)
$TitleLabel.TextAlign = "MiddleCenter"
$TitleLabel.ForeColor = [System.Drawing.Color]::FromArgb(255, 100, 100)
$Form.Controls.Add($TitleLabel)

# Subtitle
$SubtitleLabel = New-Object System.Windows.Forms.Label
$SubtitleLabel.Location = New-Object System.Drawing.Point(20, 80)
$SubtitleLabel.Size = New-Object System.Drawing.Size(760, 30)
$SubtitleLabel.Text = "BTC QR + Theta Audio + Chapman Fear + Multi-Channel + Direct Upload"
$SubtitleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$SubtitleLabel.TextAlign = "MiddleCenter"
$SubtitleLabel.ForeColor = [System.Drawing.Color]::LightGray
$Form.Controls.Add($SubtitleLabel)

# Separator
$Separator1 = New-Object System.Windows.Forms.Label
$Separator1.Location = New-Object System.Drawing.Point(50, 120)
$Separator1.Size = New-Object System.Drawing.Size(700, 2)
$Separator1.BorderStyle = "Fixed3D"
$Form.Controls.Add($Separator1)

# Features Status Panel
$FeaturesPanel = New-Object System.Windows.Forms.Panel
$FeaturesPanel.Location = New-Object System.Drawing.Point(30, 140)
$FeaturesPanel.Size = New-Object System.Drawing.Size(740, 120)
$FeaturesPanel.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$FeaturesPanel.BorderStyle = "FixedSingle"

$FeaturesTitle = New-Object System.Windows.Forms.Label
$FeaturesTitle.Location = New-Object System.Drawing.Point(10, 10)
$FeaturesTitle.Size = New-Object System.Drawing.Size(720, 25)
$FeaturesTitle.Text = "🚀 FEATURES STATUS"
$FeaturesTitle.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$FeaturesTitle.ForeColor = [System.Drawing.Color]::FromArgb(100, 255, 100)
$FeaturesPanel.Controls.Add($FeaturesTitle)

# Feature status labels
$BTCStatus = New-Object System.Windows.Forms.Label
$BTCStatus.Location = New-Object System.Drawing.Point(20, 40)
$BTCStatus.Size = New-Object System.Drawing.Size(200, 20)
$BTCStatus.Text = "💰 BTC QR Overlays: ✅ READY"
$BTCStatus.ForeColor = [System.Drawing.Color]::LightGreen
$FeaturesPanel.Controls.Add($BTCStatus)

$ThetaStatus = New-Object System.Windows.Forms.Label
$ThetaStatus.Location = New-Object System.Drawing.Point(20, 60)
$ThetaStatus.Size = New-Object System.Drawing.Size(200, 20)
$ThetaStatus.Text = "🎵 Theta Audio: ✅ READY"
$ThetaStatus.ForeColor = [System.Drawing.Color]::LightGreen
$FeaturesPanel.Controls.Add($ThetaStatus)

$FearStatus = New-Object System.Windows.Forms.Label
$FearStatus.Location = New-Object System.Drawing.Point(20, 80)
$FearStatus.Size = New-Object System.Drawing.Size(200, 20)
$FearStatus.Text = "😨 Chapman Fear: ✅ READY"
$FearStatus.ForeColor = [System.Drawing.Color]::LightGreen
$FeaturesPanel.Controls.Add($FearStatus)

$ChannelStatus = New-Object System.Windows.Forms.Label
$ChannelStatus.Location = New-Object System.Drawing.Point(250, 40)
$ChannelStatus.Size = New-Object System.Drawing.Size(200, 20)
$ChannelStatus.Text = "🔄 Multi-Channel: ✅ READY"
$ChannelStatus.ForeColor = [System.Drawing.Color]::LightGreen
$FeaturesPanel.Controls.Add($ChannelStatus)

$UploadStatus = New-Object System.Windows.Forms.Label
$UploadStatus.Location = New-Object System.Drawing.Point(250, 60)
$UploadStatus.Size = New-Object System.Drawing.Size(200, 20)
$UploadStatus.Text = "📤 Direct Upload: ✅ READY"
$UploadStatus.ForeColor = [System.Drawing.Color]::LightGreen
$FeaturesPanel.Controls.Add($UploadStatus)

$TextStatus = New-Object System.Windows.Forms.Label
$TextStatus.Location = New-Object System.Drawing.Point(250, 80)
$TextStatus.Size = New-Object System.Drawing.Size(200, 20)
$TextStatus.Text = "📝 Text Overlays: ✅ READY"
$TextStatus.ForeColor = [System.Drawing.Color]::LightGreen
$FeaturesPanel.Controls.Add($TextStatus)

$Form.Controls.Add($FeaturesPanel)

# Button styling function
function New-EmpireButton {
    param(
        [int]$X,
        [int]$Y,
        [int]$Width,
        [int]$Height,
        [string]$Text,
        [System.Drawing.Color]$BackColor
    )
    
    $Button = New-Object System.Windows.Forms.Button
    $Button.Location = New-Object System.Drawing.Point($X, $Y)
    $Button.Size = New-Object System.Drawing.Size($Width, $Height)
    $Button.Text = $Text
    $Button.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $Button.BackColor = $BackColor
    $Button.ForeColor = [System.Drawing.Color]::White
    $Button.FlatStyle = "Flat"
    $Button.Cursor = [System.Windows.Forms.Cursors]::Hand
    $Button.FlatAppearance.BorderSize = 0
    
    return $Button
}

# Main Action Buttons
$TestButton = New-EmpireButton -X 30 -Y 280 -Width 180 -Height 60 -Text "🧪 TEST (1 Video)" -BackColor ([System.Drawing.Color]::FromArgb(70, 130, 180))
$TestButton.Add_Click({
    Run-ScarifyCommand -Count 1 -TestMode $true -Upload $false
})
$Form.Controls.Add($TestButton)

$Upload1Button = New-EmpireButton -X 230 -Y 280 -Width 180 -Height 60 -Text "🚀 UPLOAD 1" -BackColor ([System.Drawing.Color]::FromArgb(34, 139, 34))
$Upload1Button.Add_Click({
    Run-ScarifyCommand -Count 1 -TestMode $false -Upload $true
})
$Form.Controls.Add($Upload1Button)

$Upload5Button = New-EmpireButton -X 430 -Y 280 -Width 180 -Height 60 -Text "💥 UPLOAD 5" -BackColor ([System.Drawing.Color]::FromArgb(220, 20, 60))
$Upload5Button.Add_Click({
    Run-ScarifyCommand -Count 5 -TestMode $false -Upload $true
})
$Form.Controls.Add($Upload5Button)

$Upload20Button = New-EmpireButton -X 630 -Y 280 -Width 140 -Height 60 -Text "🔥 UPLOAD 20" -BackColor ([System.Drawing.Color]::FromArgb(139, 0, 139))
$Upload20Button.Add_Click({
    Run-ScarifyCommand -Count 20 -TestMode $false -Upload $true
})
$Form.Controls.Add($Upload20Button)

# Channel Selection
$ChannelPanel = New-Object System.Windows.Forms.Panel
$ChannelPanel.Location = New-Object System.Drawing.Point(30, 360)
$ChannelPanel.Size = New-Object System.Drawing.Size(740, 80)
$ChannelPanel.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$ChannelPanel.BorderStyle = "FixedSingle"

$ChannelTitle = New-Object System.Windows.Forms.Label
$ChannelTitle.Location = New-Object System.Drawing.Point(10, 10)
$ChannelTitle.Size = New-Object System.Drawing.Size(720, 25)
$ChannelTitle.Text = "📺 CHANNEL SELECTION"
$ChannelTitle.Font = New-Object System.Drawing.Font("Segoe UI", 12, [System.Drawing.FontStyle]::Bold)
$ChannelTitle.ForeColor = [System.Drawing.Color]::FromArgb(100, 255, 100)
$ChannelPanel.Controls.Add($ChannelTitle)

$VetEdgeRadio = New-Object System.Windows.Forms.RadioButton
$VetEdgeRadio.Location = New-Object System.Drawing.Point(20, 40)
$VetEdgeRadio.Size = New-Object System.Drawing.Size(200, 20)
$VetEdgeRadio.Text = "The Vet Edge (Main)"
$VetEdgeRadio.ForeColor = [System.Drawing.Color]::White
$VetEdgeRadio.Checked = $true
$ChannelPanel.Controls.Add($VetEdgeRadio)

$ArchiveRadio = New-Object System.Windows.Forms.RadioButton
$ArchiveRadio.Location = New-Object System.Drawing.Point(250, 40)
$ArchiveRadio.Size = New-Object System.Drawing.Size(200, 20)
$ArchiveRadio.Text = "SCARIFY Archive"
$ArchiveRadio.ForeColor = [System.Drawing.Color]::White
$ChannelPanel.Controls.Add($ArchiveRadio)

$BTCRadio = New-Object System.Windows.Forms.RadioButton
$BTCRadio.Location = New-Object System.Drawing.Point(480, 40)
$BTCRadio.Size = New-Object System.Drawing.Size(200, 20)
$BTCRadio.Text = "BTC Empire"
$BTCRadio.ForeColor = [System.Drawing.Color]::White
$ChannelPanel.Controls.Add($BTCRadio)

$Form.Controls.Add($ChannelPanel)

# Output TextBox
$OutputBox = New-Object System.Windows.Forms.TextBox
$OutputBox.Location = New-Object System.Drawing.Point(30, 460)
$OutputBox.Size = New-Object System.Drawing.Size(740, 120)
$OutputBox.Multiline = $true
$OutputBox.ScrollBars = "Vertical"
$OutputBox.ReadOnly = $true
$OutputBox.BackColor = [System.Drawing.Color]::FromArgb(10, 10, 10)
$OutputBox.ForeColor = [System.Drawing.Color]::LightGreen
$OutputBox.Font = New-Object System.Drawing.Font("Consolas", 9)
$OutputBox.Text = "🔥 SCARIFY EMPIRE DASHBOARD READY 🔥`r`n`r`nFeatures:`r`n✅ BTC QR Overlays (Direct crypto payments)`r`n✅ Theta Audio (Brainwave retention)`r`n✅ Chapman Fear Prompts (Psychology-based)`r`n✅ Multi-Channel Rotation (Scale without limits)`r`n✅ Direct YouTube Upload (One-click)`r`n`r`nReady to build the empire...`r`n"
$Form.Controls.Add($OutputBox)

# Control Buttons
$OpenFolderButton = New-Object System.Windows.Forms.Button
$OpenFolderButton.Location = New-Object System.Drawing.Point(30, 600)
$OpenFolderButton.Size = New-Object System.Drawing.Size(150, 40)
$OpenFolderButton.Text = "📁 Open Videos"
$OpenFolderButton.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$OpenFolderButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$OpenFolderButton.ForeColor = [System.Drawing.Color]::White
$OpenFolderButton.FlatStyle = "Flat"
$OpenFolderButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$OpenFolderButton.Add_Click({
    if (Test-Path $OutputFolder) {
        Start-Process explorer.exe -ArgumentList $OutputFolder
        $OutputBox.AppendText("✅ Opened output folder`r`n")
    } else {
        [System.Windows.Forms.MessageBox]::Show(
            "Output folder not found. Generate a video first!",
            "Folder Not Found",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Warning
        )
    }
})
$Form.Controls.Add($OpenFolderButton)

$YouTubeStudioButton = New-Object System.Windows.Forms.Button
$YouTubeStudioButton.Location = New-Object System.Drawing.Point(200, 600)
$YouTubeStudioButton.Size = New-Object System.Drawing.Size(150, 40)
$YouTubeStudioButton.Text = "📺 YouTube Studio"
$YouTubeStudioButton.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$YouTubeStudioButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$YouTubeStudioButton.ForeColor = [System.Drawing.Color]::White
$YouTubeStudioButton.FlatStyle = "Flat"
$YouTubeStudioButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$YouTubeStudioButton.Add_Click({
    Start-Process "https://studio.youtube.com/"
    $OutputBox.AppendText("✅ Opened YouTube Studio`r`n")
})
$Form.Controls.Add($YouTubeStudioButton)

$CloseButton = New-Object System.Windows.Forms.Button
$CloseButton.Location = New-Object System.Drawing.Point(620, 600)
$CloseButton.Size = New-Object System.Drawing.Size(150, 40)
$CloseButton.Text = "❌ Close"
$CloseButton.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$CloseButton.BackColor = [System.Drawing.Color]::FromArgb(60, 60, 60)
$CloseButton.ForeColor = [System.Drawing.Color]::White
$CloseButton.FlatStyle = "Flat"
$CloseButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$CloseButton.Add_Click({
    $Form.Close()
})
$Form.Controls.Add($CloseButton)

# Function to run SCARIFY command
function Run-ScarifyCommand {
    param(
        [int]$Count,
        [bool]$TestMode,
        [bool]$Upload
    )
    
    # Disable buttons during execution
    $TestButton.Enabled = $false
    $Upload1Button.Enabled = $false
    $Upload5Button.Enabled = $false
    $Upload20Button.Enabled = $false
    
    # Get selected channel
    $SelectedChannel = "the_vet_edge"
    if ($ArchiveRadio.Checked) { $SelectedChannel = "scarify_archive" }
    if ($BTCRadio.Checked) { $SelectedChannel = "btc_empire" }
    
    # Build command
    $Args = @("$PythonScript", "--count", $Count)
    
    if ($TestMode) {
        $Args += "--test"
    }
    
    if ($Upload) {
        $Args += "--upload"
    }
    
    $OutputBox.Clear()
    $OutputBox.AppendText("🔥 SCARIFY EMPIRE ACTIVATED 🔥`r`n")
    $OutputBox.AppendText("=" * 50 + "`r`n")
    $OutputBox.AppendText("Command: python $($Args -join ' ')`r`n")
    $OutputBox.AppendText("Channel: $SelectedChannel`r`n")
    $OutputBox.AppendText("Mode: $(if($TestMode){'TEST'}else{'PRODUCTION'})`r`n")
    $OutputBox.AppendText("Upload: $(if($Upload){'YES'}else{'NO'})`r`n")
    $OutputBox.AppendText("=" * 50 + "`r`n`r`n")
    
    $Form.Refresh()
    
    try {
        # Set environment variables
        $env:IMAGEMAGICK_BINARY = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"
        $env:SCARIFY_CHANNEL = $SelectedChannel
        
        # Create a new PowerShell window to show progress
        $ProcessStartInfo = New-Object System.Diagnostics.ProcessStartInfo
        $ProcessStartInfo.FileName = $PythonExe
        $ProcessStartInfo.Arguments = $Args -join " "
        $ProcessStartInfo.UseShellExecute = $true
        $ProcessStartInfo.CreateNoWindow = $false
        $ProcessStartInfo.WorkingDirectory = $ScriptRoot
        
        $Process = [System.Diagnostics.Process]::Start($ProcessStartInfo)
        
        $OutputBox.AppendText("✅ Process started in new window...`r`n")
        $OutputBox.AppendText("⏳ Check the console window for real-time progress`r`n")
        $OutputBox.AppendText("`r`nFeatures active:`r`n")
        $OutputBox.AppendText("💰 BTC QR Overlays`r`n")
        $OutputBox.AppendText("🎵 Theta Audio Background`r`n")
        $OutputBox.AppendText("😨 Chapman Fear Psychology`r`n")
        $OutputBox.AppendText("📝 Professional Text Overlays`r`n")
        if ($Upload) {
            $OutputBox.AppendText("📤 Direct YouTube Upload`r`n")
        }
        
        # Wait for completion
        $Process.WaitForExit()
        
        $ExitCode = $Process.ExitCode
        
        if ($ExitCode -eq 0) {
            $OutputBox.AppendText("`r`n" + "=" * 50 + "`r`n")
            $OutputBox.AppendText("🎉 EMPIRE BUILDING COMPLETE! 🎉`r`n")
            $OutputBox.AppendText("=" * 50 + "`r`n")
            
            if ($Upload) {
                $OutputBox.AppendText("✅ Videos uploaded to YouTube!`r`n")
                $OutputBox.AppendText("📺 Check YouTube Studio for results`r`n")
            } else {
                $OutputBox.AppendText("✅ Videos generated successfully!`r`n")
                $OutputBox.AppendText("📁 Check output folder for videos`r`n")
            }
            
            # Offer to open relevant location
            if ($Upload) {
                $Result = [System.Windows.Forms.MessageBox]::Show(
                    "Videos uploaded to YouTube!`r`n`r`nOpen YouTube Studio?",
                    "Empire Building Complete",
                    [System.Windows.Forms.MessageBoxButtons]::YesNo,
                    [System.Windows.Forms.MessageBoxIcon]::Information
                )
                
                if ($Result -eq [System.Windows.Forms.DialogResult]::Yes) {
                    Start-Process "https://studio.youtube.com/"
                }
            } else {
                $Result = [System.Windows.Forms.MessageBox]::Show(
                    "Videos generated successfully!`r`n`r`nOpen output folder?",
                    "Empire Building Complete",
                    [System.Windows.Forms.MessageBoxButtons]::YesNo,
                    [System.Windows.Forms.MessageBoxIcon]::Information
                )
                
                if ($Result -eq [System.Windows.Forms.DialogResult]::Yes) {
                    if (Test-Path $OutputFolder) {
                        Start-Process explorer.exe -ArgumentList $OutputFolder
                    }
                }
            }
        } else {
            $OutputBox.AppendText("`r`n❌ Process failed with exit code: $ExitCode`r`n")
            
            [System.Windows.Forms.MessageBox]::Show(
                "Video generation encountered errors.`r`nCheck the console output.",
                "Empire Building Error",
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Error
            )
        }
        
    } catch {
        $OutputBox.AppendText("`r`n❌ ERROR: $($_.Exception.Message)`r`n")
        
        [System.Windows.Forms.MessageBox]::Show(
            "Failed to start video generator:`r`n`r`n$($_.Exception.Message)",
            "Empire Building Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
    } finally {
        # Re-enable buttons
        $TestButton.Enabled = $true
        $Upload1Button.Enabled = $true
        $Upload5Button.Enabled = $true
        $Upload20Button.Enabled = $true
    }
}

# Check if script exists
if (-not (Test-Path $PythonScript)) {
    [System.Windows.Forms.MessageBox]::Show(
        "scarify_master.py not found!`r`n`r`nExpected location:`r`n$PythonScript",
        "Script Not Found",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    )
    exit 1
}

# Show the form
Write-Host "🔥 Launching SCARIFY EMPIRE DASHBOARD..."
[void]$Form.ShowDialog()
