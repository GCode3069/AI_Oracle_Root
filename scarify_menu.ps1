# SCARIFY Launcher Menu
# Choose between Simple Launcher and Full Dashboard

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create the menu form
$MenuForm = New-Object System.Windows.Forms.Form
$MenuForm.Text = "SCARIFY Launcher Menu"
$MenuForm.Size = New-Object System.Drawing.Size(500, 400)
$MenuForm.StartPosition = "CenterScreen"
$MenuForm.FormBorderStyle = "FixedDialog"
$MenuForm.MaximizeBox = $false
$MenuForm.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
$MenuForm.ForeColor = [System.Drawing.Color]::White

# Title
$TitleLabel = New-Object System.Windows.Forms.Label
$TitleLabel.Location = New-Object System.Drawing.Point(20, 20)
$TitleLabel.Size = New-Object System.Drawing.Size(460, 40)
$TitleLabel.Text = "[SCARIFY] LAUNCHER MENU"
$TitleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
$TitleLabel.TextAlign = "MiddleCenter"
$TitleLabel.ForeColor = [System.Drawing.Color]::FromArgb(255, 215, 0)
$MenuForm.Controls.Add($TitleLabel)

# Subtitle
$SubtitleLabel = New-Object System.Windows.Forms.Label
$SubtitleLabel.Location = New-Object System.Drawing.Point(20, 70)
$SubtitleLabel.Size = New-Object System.Drawing.Size(460, 30)
$SubtitleLabel.Text = "Choose your SCARIFY experience:"
$SubtitleLabel.Font = New-Object System.Drawing.Font("Segoe UI", 12)
$SubtitleLabel.TextAlign = "MiddleCenter"
$SubtitleLabel.ForeColor = [System.Drawing.Color]::LightGray
$MenuForm.Controls.Add($SubtitleLabel)

# Dashboard Button
$DashboardButton = New-Object System.Windows.Forms.Button
$DashboardButton.Location = New-Object System.Drawing.Point(50, 120)
$DashboardButton.Size = New-Object System.Drawing.Size(400, 80)
$DashboardButton.Text = "[DASHBOARD] FULL DASHBOARD`r`n`r`nAdvanced control center with batch operations,`r`nmonitoring, statistics, and system controls"
$DashboardButton.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
$DashboardButton.BackColor = [System.Drawing.Color]::FromArgb(34, 139, 34)
$DashboardButton.ForeColor = [System.Drawing.Color]::White
$DashboardButton.FlatStyle = "Flat"
$DashboardButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$DashboardButton.FlatAppearance.BorderSize = 0
$DashboardButton.Add_Click({
    $MenuForm.Hide()
    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$PSScriptRoot\scarify_dashboard.ps1`""
    $MenuForm.Close()
})
$MenuForm.Controls.Add($DashboardButton)

# Simple Launcher Button
$SimpleButton = New-Object System.Windows.Forms.Button
$SimpleButton.Location = New-Object System.Drawing.Point(50, 220)
$SimpleButton.Size = New-Object System.Drawing.Size(400, 80)
$SimpleButton.Text = "[SIMPLE] SIMPLE LAUNCHER`r`n`r`nQuick access with basic generation buttons`r`nfor fast video creation"
$SimpleButton.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
$SimpleButton.BackColor = [System.Drawing.Color]::FromArgb(70, 130, 180)
$SimpleButton.ForeColor = [System.Drawing.Color]::White
$SimpleButton.FlatStyle = "Flat"
$SimpleButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$SimpleButton.FlatAppearance.BorderSize = 0
$SimpleButton.Add_Click({
    $MenuForm.Hide()
    Start-Process powershell -ArgumentList "-ExecutionPolicy Bypass -File `"$PSScriptRoot\scarify_launcher.ps1`""
    $MenuForm.Close()
})
$MenuForm.Controls.Add($SimpleButton)

# Close Button
$CloseButton = New-Object System.Windows.Forms.Button
$CloseButton.Location = New-Object System.Drawing.Point(200, 320)
$CloseButton.Size = New-Object System.Drawing.Size(100, 40)
$CloseButton.Text = "[CLOSE] Close"
$CloseButton.Font = New-Object System.Drawing.Font("Segoe UI", 10)
$CloseButton.BackColor = [System.Drawing.Color]::FromArgb(220, 20, 60)
$CloseButton.ForeColor = [System.Drawing.Color]::White
$CloseButton.FlatStyle = "Flat"
$CloseButton.Cursor = [System.Windows.Forms.Cursors]::Hand
$CloseButton.Add_Click({
    $MenuForm.Close()
})
$MenuForm.Controls.Add($CloseButton)

# Show the menu
Write-Host "🚀 Launching SCARIFY Menu..."
[void]$MenuForm.ShowDialog()
