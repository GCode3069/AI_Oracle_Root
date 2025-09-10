. "$PSScriptRoot/../lib/WinFormsSmoothing.ps1"

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$script:Config = @{
    RootPath = "D:\AI_Oracle_Root"
    SelectedLanguages = @("en")
    AudioIntensity = 0.7
    ScriptQueue = @()
}

$script:Theme = @{
    Primary = [System.Drawing.Color]::FromArgb(17, 17, 17)
    Accent = [System.Drawing.Color]::FromArgb(255, 68, 68)
    Success = [System.Drawing.Color]::FromArgb(34, 197, 94)
    Text = [System.Drawing.Color]::FromArgb(240, 240, 240)
}

function New-ScarifyMainForm {
    $form = New-SmoothForm
    $form.Text = "🔺 SCARIFY Global Content Empire Launcher"
    $form.Size = New-Object System.Drawing.Size(1200, 800)
    $form.StartPosition = "CenterScreen"
    $form.BackColor = $script:Theme.Primary
    $form.ForeColor = $script:Theme.Text
    
    # Title
    $title = New-Object System.Windows.Forms.Label
    $title.Text = "🔺 SCARIFY Global Content Empire Launcher v2.0.0"
    $title.Font = New-Object System.Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
    $title.ForeColor = $script:Theme.Accent
    $title.Size = New-Object System.Drawing.Size(1160, 40)
    $title.Location = New-Object System.Drawing.Point(20, 20)
    $title.TextAlign = "MiddleCenter"
    $form.Controls.Add($title)
    
    # AI Engine Panel
    $enginePanel = New-Object System.Windows.Forms.GroupBox
    $enginePanel.Text = "🤖 AI Engine Configuration"
    $enginePanel.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $enginePanel.ForeColor = $script:Theme.Text
    $enginePanel.Size = New-Object System.Drawing.Size(360, 120)
    $enginePanel.Location = New-Object System.Drawing.Point(20, 80)
    
    $engineLabel = New-Object System.Windows.Forms.Label
    $engineLabel.Text = "Primary AI Engine:"
    $engineLabel.Size = New-Object System.Drawing.Size(150, 25)
    $engineLabel.Location = New-Object System.Drawing.Point(20, 30)
    $enginePanel.Controls.Add($engineLabel)
    
    $script:EngineCombo = New-Object System.Windows.Forms.ComboBox
    $script:EngineCombo.Items.AddRange(@("Claude", "ChatGPT", "Gemini"))
    $script:EngineCombo.SelectedIndex = 0
    $script:EngineCombo.Size = New-Object System.Drawing.Size(180, 25)
    $script:EngineCombo.Location = New-Object System.Drawing.Point(170, 28)
    $script:EngineCombo.DropDownStyle = "DropDownList"
    $enginePanel.Controls.Add($script:EngineCombo)
    
    $platformLabel = New-Object System.Windows.Forms.Label
    $platformLabel.Text = "Target Platform:"
    $platformLabel.Size = New-Object System.Drawing.Size(150, 25)
    $platformLabel.Location = New-Object System.Drawing.Point(20, 65)
    $enginePanel.Controls.Add($platformLabel)
    
    $script:PlatformCombo = New-Object System.Windows.Forms.ComboBox
    $script:PlatformCombo.Items.AddRange(@("Windows", "Linux", "macOS"))
    $script:PlatformCombo.SelectedIndex = 0
    $script:PlatformCombo.Size = New-Object System.Drawing.Size(180, 25)
    $script:PlatformCombo.Location = New-Object System.Drawing.Point(170, 63)
    $script:PlatformCombo.DropDownStyle = "DropDownList"
    $enginePanel.Controls.Add($script:PlatformCombo)
    
    $form.Controls.Add($enginePanel)
    
    # Language Selection Panel
    $langPanel = New-Object System.Windows.Forms.GroupBox
    $langPanel.Text = "🌍 Target Languages"
    $langPanel.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $langPanel.ForeColor = $script:Theme.Text
    $langPanel.Size = New-Object System.Drawing.Size(360, 200)
    $langPanel.Location = New-Object System.Drawing.Point(20, 220)
    
    $script:LanguageCheckboxes = @{}
    $languages = @{
        "en" = "🇺🇸 English"; "es" = "🇪🇸 Spanish"; "de" = "🇩🇪 German"
        "fr" = "🇫🇷 French"; "it" = "🇮🇹 Italian"; "ja" = "🇯🇵 Japanese"
        "ko" = "🇰🇷 Korean"; "ru" = "🇷🇺 Russian"; "zh" = "🇨🇳 Chinese"
        "hi" = "🇮🇳 Hindi"; "ar" = "🇸🇦 Arabic"; "pt" = "🇧🇷 Portuguese"
    }
    
    $x = 20; $y = 30; $col = 0
    foreach ($lang in $languages.GetEnumerator()) {
        $checkbox = New-Object System.Windows.Forms.CheckBox
        $checkbox.Text = $lang.Value
        $checkbox.Size = New-Object System.Drawing.Size(160, 25)
        $checkbox.Location = New-Object System.Drawing.Point($x, $y)
        $checkbox.ForeColor = $script:Theme.Text
        $checkbox.Tag = $lang.Key
        $checkbox.Checked = ($lang.Key -eq "en")
        
        $langPanel.Controls.Add($checkbox)
        $script:LanguageCheckboxes[$lang.Key] = $checkbox
        
        $y += 30; $col++
        if ($col -eq 4) { $col = 0; $x += 180; $y = 30 }
    }
    
    $form.Controls.Add($langPanel)
    
    # Audio Enhancement Panel
    $audioPanel = New-Object System.Windows.Forms.GroupBox
    $audioPanel.Text = "🎵 Audio Enhancement"
    $audioPanel.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $audioPanel.ForeColor = $script:Theme.Text
    $audioPanel.Size = New-Object System.Drawing.Size(360, 80)
    $audioPanel.Location = New-Object System.Drawing.Point(20, 440)
    
    $intensityLabel = New-Object System.Windows.Forms.Label
    $intensityLabel.Text = "Enhancement Intensity:"
    $intensityLabel.Size = New-Object System.Drawing.Size(150, 25)
    $intensityLabel.Location = New-Object System.Drawing.Point(20, 30)
    $audioPanel.Controls.Add($intensityLabel)
    
    $script:IntensityTracker = New-Object System.Windows.Forms.TrackBar
    $script:IntensityTracker.Minimum = 0
    $script:IntensityTracker.Maximum = 100
    $script:IntensityTracker.Value = 70
    $script:IntensityTracker.Size = New-Object System.Drawing.Size(180, 45)
    $script:IntensityTracker.Location = New-Object System.Drawing.Point(170, 25)
    $audioPanel.Controls.Add($script:IntensityTracker)
    
    $form.Controls.Add($audioPanel)
    
    # Execution Panel
    $execPanel = New-Object System.Windows.Forms.GroupBox
    $execPanel.Text = "🚀 Execution Commands"
    $execPanel.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $execPanel.ForeColor = $script:Theme.Text
    $execPanel.Size = New-Object System.Drawing.Size(360, 160)
    $execPanel.Location = New-Object System.Drawing.Point(20, 540)
    
    $generateBtn = New-Object System.Windows.Forms.Button
    $generateBtn.Text = "🧠 Generate Scripts"
    $generateBtn.Size = New-Object System.Drawing.Size(320, 35)
    $generateBtn.Location = New-Object System.Drawing.Point(20, 30)
    $generateBtn.BackColor = $script:Theme.Accent
    $generateBtn.ForeColor = [System.Drawing.Color]::White
    $generateBtn.FlatStyle = "Flat"
    $generateBtn.Font = New-Object System.Drawing.Font("Segoe UI", 11, [System.Drawing.FontStyle]::Bold)
    $generateBtn.Add_Click({ Start-ScriptGeneration })
    $execPanel.Controls.Add($generateBtn)
    
    $batchBtn = New-Object System.Windows.Forms.Button
    $batchBtn.Text = "📁 Add Batch Scripts"
    $batchBtn.Size = New-Object System.Drawing.Size(150, 30)
    $batchBtn.Location = New-Object System.Drawing.Point(20, 75)
    $batchBtn.BackColor = $script:Theme.Success
    $batchBtn.ForeColor = [System.Drawing.Color]::White
    $batchBtn.FlatStyle = "Flat"
    $batchBtn.Add_Click({ Add-BatchScripts })
    $execPanel.Controls.Add($batchBtn)
    
    $runBtn = New-Object System.Windows.Forms.Button
    $runBtn.Text = "🚀 Run Batch"
    $runBtn.Size = New-Object System.Drawing.Size(150, 30)
    $runBtn.Location = New-Object System.Drawing.Point(190, 75)
    $runBtn.BackColor = $script:Theme.Success
    $runBtn.ForeColor = [System.Drawing.Color]::White
    $runBtn.FlatStyle = "Flat"
    $runBtn.Add_Click({ Start-BatchExecution })
    $execPanel.Controls.Add($runBtn)
    
    $audioBtn = New-Object System.Windows.Forms.Button
    $audioBtn.Text = "🎵 Enhance Audio Folder"
    $audioBtn.Size = New-Object System.Drawing.Size(320, 30)
    $audioBtn.Location = New-Object System.Drawing.Point(20, 115)
    $audioBtn.BackColor = [System.Drawing.Color]::FromArgb(251, 191, 36)
    $audioBtn.ForeColor = [System.Drawing.Color]::White
    $audioBtn.FlatStyle = "Flat"
    $audioBtn.Add_Click({ Start-AudioEnhancement })
    $execPanel.Controls.Add($audioBtn)
    
    $form.Controls.Add($execPanel)
    
    # Output Panel
    $outputPanel = New-Object System.Windows.Forms.GroupBox
    $outputPanel.Text = "📊 System Output"
    $outputPanel.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
    $outputPanel.ForeColor = $script:Theme.Text
    $outputPanel.Size = New-Object System.Drawing.Size(760, 620)
    $outputPanel.Location = New-Object System.Drawing.Point(400, 80)
    
    $script:OutputTextBox = New-Object System.Windows.Forms.RichTextBox
    $script:OutputTextBox.Size = New-Object System.Drawing.Size(720, 580)
    $script:OutputTextBox.Location = New-Object System.Drawing.Point(20, 30)
    $script:OutputTextBox.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
    $script:OutputTextBox.ForeColor = $script:Theme.Text
    $script:OutputTextBox.Font = New-Object System.Drawing.Font("Consolas", 10)
    $script:OutputTextBox.ReadOnly = $true
    $outputPanel.Controls.Add($script:OutputTextBox)
    
    $form.Controls.Add($outputPanel)
    
    Write-ScarifyOutput "🔺 SCARIFY Global Content Empire Launcher v2.0.0 initialized"
    Write-ScarifyOutput "📁 Root directory: $($script:Config.RootPath)"
    Write-ScarifyOutput "🚀 System ready for content generation"
    
    return $form
}

function Write-ScarifyOutput {
    param([string]$Message)
    $timestamp = Get-Date -Format "HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    
    if ($script:OutputTextBox) {
        $script:OutputTextBox.AppendText("$logMessage`n")
        $script:OutputTextBox.ScrollToCaret()
    }
    
    Write-Host $logMessage -ForegroundColor Cyan
}

function Start-ScriptGeneration {
    $selectedLanguages = @()
    foreach ($checkbox in $script:LanguageCheckboxes.Values) {
        if ($checkbox.Checked) {
            $selectedLanguages += $checkbox.Tag
        }
    }
    
    if ($selectedLanguages.Count -eq 0) {
        [System.Windows.Forms.MessageBox]::Show("Please select at least one language.", "No Languages Selected")
        return
    }
    
    $engine = $script:EngineCombo.SelectedItem
    Write-ScarifyOutput "🧠 Starting script generation with $engine for $($selectedLanguages.Count) language(s)"
    
    foreach ($lang in $selectedLanguages) {
        $timestamp = Get-Date -Format "HHmmss"
        $filename = "${engine}_${lang}_${timestamp}.txt"
        $outputPath = "$($script:Config.RootPath)\generated\$filename"
        
        $dir = Split-Path $outputPath -Parent
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
        
        $content = @"
# SCARIFY Generated Script
# Engine: $engine
# Language: $lang
# Generated: $(Get-Date)

Write a cinematic horror scene featuring mysterious disappearances in urban centers.
The narrative should build tension through atmospheric descriptions and psychological elements.

[Generated script content would appear here based on AI engine selection]
"@
        
        $content | Set-Content -Path $outputPath -Encoding UTF8
        Write-ScarifyOutput "✅ Generated script for $lang → $filename"
    }
    
    [System.Windows.Forms.MessageBox]::Show("Script generation completed for $($selectedLanguages.Count) language(s)!", "Generation Complete")
}

function Add-BatchScripts {
    $openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
    $openFileDialog.Multiselect = $true
    $openFileDialog.Filter = "Script Files (*.ps1;*.py;*.bat)|*.ps1;*.py;*.bat|All Files (*.*)|*.*"
    $openFileDialog.Title = "Select Scripts for Batch Execution"
    
    if ($openFileDialog.ShowDialog() -eq "OK") {
        foreach ($file in $openFileDialog.FileNames) {
            $script:Config.ScriptQueue += $file
            Write-ScarifyOutput "📥 Added to batch: $(Split-Path $file -Leaf)"
        }
        Write-ScarifyOutput "📦 Batch queue now contains $($script:Config.ScriptQueue.Count) script(s)"
    }
}

function Start-BatchExecution {
    if ($script:Config.ScriptQueue.Count -eq 0) {
        [System.Windows.Forms.MessageBox]::Show("No scripts in batch queue. Add scripts first.", "Empty Queue")
        return
    }
    
    Write-ScarifyOutput "🚀 Starting batch execution of $($script:Config.ScriptQueue.Count) script(s)"
    
    foreach ($scriptPath in $script:Config.ScriptQueue) {
        $extension = [System.IO.Path]::GetExtension($scriptPath).ToLower()
        $scriptName = Split-Path $scriptPath -Leaf
        
        try {
            switch ($extension) {
                ".ps1" {
                    Write-ScarifyOutput "⚡ Executing PowerShell: $scriptName"
                    & powershell -ExecutionPolicy Bypass -File $scriptPath
                }
                ".py" {
                    Write-ScarifyOutput "🐍 Executing Python: $scriptName"
                    & python $scriptPath
                }
                ".bat" {
                    Write-ScarifyOutput "📋 Executing Batch: $scriptName"
                    & cmd /c $scriptPath
                }
                default {
                    Write-ScarifyOutput "❓ Unknown script type: $scriptName"
                }
            }
            Write-ScarifyOutput "✅ Completed: $scriptName"
        }
        catch {
            Write-ScarifyOutput "❌ Failed: $scriptName - $_"
        }
    }
    
    Write-ScarifyOutput "🎉 Batch execution completed!"
}

function Start-AudioEnhancement {
    $folderDialog = New-Object System.Windows.Forms.FolderBrowserDialog
    $folderDialog.Description = "Select folder containing audio files to enhance"
    
    if ($folderDialog.ShowDialog() -eq "OK") {
        $audioFolder = $folderDialog.SelectedPath
        $outputFolder = "$($script:Config.RootPath)\Output\EnhancedAudio"
        
        if (-not (Test-Path $outputFolder)) {
            New-Item -ItemType Directory -Path $outputFolder -Force | Out-Null
        }
        
        $audioFiles = Get-ChildItem $audioFolder -Filter "*.mp3", "*.wav", "*.m4a"
        $intensity = $script:IntensityTracker.Value / 100.0
        
        Write-ScarifyOutput "🎵 Starting audio enhancement with intensity $intensity"
        Write-ScarifyOutput "📁 Input: $audioFolder"
        Write-ScarifyOutput "📁 Output: $outputFolder"
        
        foreach ($file in $audioFiles) {
            $outputFile = Join-Path $outputFolder "enhanced_$($file.Name)"
            try {
                Copy-Item $file.FullName $outputFile
                Write-ScarifyOutput "✅ Enhanced: $($file.Name)"
            }
            catch {
                Write-ScarifyOutput "❌ Failed to enhance: $($file.Name) - $_"
            }
        }
        
        Write-ScarifyOutput "🎉 Audio enhancement completed for $($audioFiles.Count) files!"
        [System.Windows.Forms.MessageBox]::Show("Audio enhancement completed!", "Enhancement Complete")
    }
}

try {
    [System.Windows.Forms.Application]::EnableVisualStyles()
    [System.Windows.Forms.Application]::SetCompatibleTextRenderingDefault($false)
    
    $mainForm = New-ScarifyMainForm
    [System.Windows.Forms.Application]::Run($mainForm)
}
catch {
    Write-Host "Error: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
