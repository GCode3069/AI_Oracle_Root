# SCARIFY Video Generator - GUI Launcher
# PowerShell GUI with one-click generation and upload

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Project settings
$ScriptRoot = $PSScriptRoot
$PythonScript = Join-Path $ScriptRoot "scarify_master.py"
$OutputFolder = Join-Path $ScriptRoot "output\videos"
$VenvPath = Join-Path $ScriptRoot "scarify_venv\Scripts\python.exe"

# Check if Python exists (try venv first, then system Python)
if (Test-Path $VenvPath) {
    $PythonExe = $VenvPath
    Write-Host "✅ Using virtual environment Python"
} else {
    $PythonExe = "python"
    Write-Host "⚠️  Virtual environment not found, using system Python"
}

# Create the form
$Form = New-Object System.Windows.Forms.Form
$Form.Text = "SCARIFY Video Generator"
$Form.Size = New-Object System.Drawing.Size(600, 500)
$Form.StartPosition = "CenterScreen"
$Form.FormBorderStyle = "FixedDialog"
$Form.MaximizeBox = $false
$Form.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$Form.ForeColor = [System.Drawing.Color]::White

# Title Label
$TitleLabel = New-Object System.Windows.Forms.Label
$TitleLabel.Location = New-Object System.Drawing.Point(20, 20)
$TitleLabel.Size = New-Object System.Drawing.Size(560, 40)
$TitleLabel.Text = "🔥 SCARIFY - YouTube Shorts Generator 🔥"
$TitleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
$TitleLabel.TextAlign = "MiddleCenter"
$Form.Controls.Add($TitleLabel)

# Subtitle
$SubtitleLabel = New-Object System.Windows.Forms.Label
$SubtitleLabel.Location = New-Object System.Drawing.Point(20, 70)
$SubtitleLabel.Size = New-Object System.Drawing.Size(560, 30)
$SubtitleLabel.Text = "Ex-Vet Emergency Kit Marketing Videos"
$SubtitleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$SubtitleLabel.TextAlign = "MiddleCenter"
$SubtitleLabel.ForeColor = [System.Drawing.Color]::LightGray
$Form.Controls.Add($SubtitleLabel)

# Separator
$Separator1 = New-Object System.Windows.Forms.Label
$Separator1.Location = New-Object System.Drawing.Point(50, 110)
$Separator1.Size = New-Object System.Drawing.Size(500, 2)
$Separator1.BorderStyle = "Fixed3D"
$Form.Controls.Add($Separator1)

# Button styling function
function New-StyledButton {
    param(
        [int]$X,
        [int]$Y,
        [string]$Text,
        [System.Drawing.Color]$BackColor
    )
    
    $Button = New-Object System.Windows.Forms.Button
    $Button.Location = New-Object System.Drawing.Point($X, $Y)
    $Button.Size = New-Object System.Drawing.Size(540, 60)
    $Button.Text = $Text
    $Button.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $Button.BackColor = $BackColor
    $Button.ForeColor = [System.Drawing.Color]::White
    $Button.FlatStyle = "Flat"
    $Button.Cursor = [System.Windows.Forms.Cursors]::Hand
    $Button.FlatAppearance.BorderSize = 0
    
    return $Button
}

# Button 1: Generate Test Video
$ButtonTest = New-StyledButton -X 30 -Y 130 -Text "📹 Generate 1 Test Video (No Upload)" -BackColor ([System.Drawing.Color]::FromArgb(70, 130, 180))
$ButtonTest.Add_Click({
    Run-ScarifyCommand -Count 1 -TestMode $true -Upload $false
})
$Form.Controls.Add($ButtonTest)

# Button 2: Generate 5 + Upload
$Button5 = New-StyledButton -X 30 -Y 200 -Text "🚀 Generate 5 Videos + Upload to YouTube" -BackColor ([System.Drawing.Color]::FromArgb(34, 139, 34))
$Button5.Add_Click({
    Run-ScarifyCommand -Count 5 -TestMode $false -Upload $true
})
$Form.Controls.Add($Button5)

# Button 3: Generate 20 + Upload
$Button20 = New-StyledButton -X 30 -Y 270 -Text "💥 Generate 20 Videos + Upload to YouTube" -BackColor ([System.Drawing.Color]::FromArgb(220, 20, 60))
$Button20.Add_Click({
    Run-ScarifyCommand -Count 20 -TestMode $false -Upload $true
})
$Form.Controls.Add($Button20)

# Output TextBox
$OutputBox = New-Object System.Windows.Forms.TextBox
$OutputBox.Location = New-Object System.Drawing.Point(30, 340)
$OutputBox.Size = New-Object System.Drawing.Size(540, 60)
$OutputBox.Multiline = $true
$OutputBox.ScrollBars = "Vertical"
$OutputBox.ReadOnly = $true
$OutputBox.BackColor = [System.Drawing.Color]::FromArgb(20, 20, 20)
$OutputBox.ForeColor = [System.Drawing.Color]::LightGreen
$OutputBox.Font = New-Object System.Drawing.Font("Consolas", 9)
$OutputBox.Text = "Ready to generate videos...`r`n"
$Form.Controls.Add($OutputBox)

# Open Output Folder Button
$OpenFolderButton = New-Object System.Windows.Forms.Button
$OpenFolderButton.Location = New-Object System.Drawing.Point(30, 410)
$OpenFolderButton.Size = New-Object System.Drawing.Size(260, 40)
$OpenFolderButton.Text = "📁 Open Output Folder"
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

# Close Button
$CloseButton = New-Object System.Windows.Forms.Button
$CloseButton.Location = New-Object System.Drawing.Point(310, 410)
$CloseButton.Size = New-Object System.Drawing.Size(260, 40)
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
    $ButtonTest.Enabled = $false
    $Button5.Enabled = $false
    $Button20.Enabled = $false
    
    # Build command
    $Args = @("$PythonScript", "--count", $Count)
    
    if ($TestMode) {
        $Args += "--test"
    }
    
    if ($Upload) {
        $Args += "--upload"
    }
    
    $OutputBox.Clear()
    $OutputBox.AppendText("🔥 Starting SCARIFY Generator...`r`n")
    $OutputBox.AppendText("Command: python $($Args -join ' ')`r`n")
    $OutputBox.AppendText("`r`n")
    
    $Form.Refresh()
    
    try {
        # Create a new PowerShell window to show progress
        $ProcessStartInfo = New-Object System.Diagnostics.ProcessStartInfo
        $ProcessStartInfo.FileName = $PythonExe
        $ProcessStartInfo.Arguments = $Args -join " "
        $ProcessStartInfo.UseShellExecute = $false
        $ProcessStartInfo.RedirectStandardOutput = $true
        $ProcessStartInfo.RedirectStandardError = $true
        $ProcessStartInfo.CreateNoWindow = $false
        $ProcessStartInfo.WorkingDirectory = $ScriptRoot
        
        # Start in a new visible console window
        $ProcessStartInfo.UseShellExecute = $true
        $ProcessStartInfo.CreateNoWindow = $false
        
        $Process = [System.Diagnostics.Process]::Start($ProcessStartInfo)
        
        $OutputBox.AppendText("✅ Process started in new window...`r`n")
        $OutputBox.AppendText("⏳ Check the console window for real-time progress`r`n")
        
        # Wait for completion
        $Process.WaitForExit()
        
        $ExitCode = $Process.ExitCode
        
        if ($ExitCode -eq 0) {
            $OutputBox.AppendText("`r`n✅ COMPLETE! Check output folder.`r`n")
            
            # Offer to open folder
            $Result = [System.Windows.Forms.MessageBox]::Show(
                "Video generation complete!`r`n`r`nOpen output folder?",
                "Success",
                [System.Windows.Forms.MessageBoxButtons]::YesNo,
                [System.Windows.Forms.MessageBoxIcon]::Information
            )
            
            if ($Result -eq [System.Windows.Forms.DialogResult]::Yes) {
                if (Test-Path $OutputFolder) {
                    Start-Process explorer.exe -ArgumentList $OutputFolder
                }
            }
        } else {
            $OutputBox.AppendText("`r`n❌ Process failed with exit code: $ExitCode`r`n")
            
            [System.Windows.Forms.MessageBox]::Show(
                "Video generation encountered errors.`r`nCheck the console output.",
                "Error",
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Error
            )
        }
        
    } catch {
        $OutputBox.AppendText("`r`n❌ ERROR: $($_.Exception.Message)`r`n")
        
        [System.Windows.Forms.MessageBox]::Show(
            "Failed to start video generator:`r`n`r`n$($_.Exception.Message)",
            "Error",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
    } finally {
        # Re-enable buttons
        $ButtonTest.Enabled = $true
        $Button5.Enabled = $true
        $Button20.Enabled = $true
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
Write-Host "🚀 Launching SCARIFY GUI..."
[void]$Form.ShowDialog()


