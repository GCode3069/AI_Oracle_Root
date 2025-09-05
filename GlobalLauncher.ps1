<#
.SYNOPSIS
GlobalLauncher.ps1 - GUI-based content generation system with cancellation and monetization support

.DESCRIPTION
Provides a Windows Forms GUI for global content generation across multiple languages and platforms.
Features cancellation support, monetization macro integration, and batch processing capabilities.

.USAGE
.\GlobalLauncher.ps1

FEATURES
- Multi-language content generation
- Platform selection (YouTube, TikTok, Instagram)
- Batch processing with progress tracking
- Graceful cancellation support
- Automated monetization content generation
- Manifest creation for upload automation
#>

param()

# Add Windows Forms and Drawing assemblies
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Threading

# --- helpers & globals ---
function New-Point([int]$x,[int]$y){ New-Object System.Drawing.Point -ArgumentList $x,$y }
function New-Size ([int]$w,[int]$h){ New-Object System.Drawing.Size  -ArgumentList $w,$h }
function Ensure-Dir([string]$p){ if(-not(Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } $p }

# session + cancel state
$script:SessionStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$script:CancelCts    = $null   # [System.Threading.CancellationTokenSource]
$script:MonetizeLoaded = $false

# Global configuration for supported languages and platforms
$Global:Config = @{
    SupportedLanguages = @{
        "en" = @{ Name = "English"; Flag = "🇺🇸"; Voice = "en-US-Neural2-D" }
        "es" = @{ Name = "Spanish"; Flag = "🇪🇸"; Voice = "es-ES-Neural2-B" }
        "fr" = @{ Name = "French"; Flag = "🇫🇷"; Voice = "fr-FR-Neural2-A" }
        "de" = @{ Name = "German"; Flag = "🇩🇪"; Voice = "de-DE-Neural2-F" }
        "it" = @{ Name = "Italian"; Flag = "🇮🇹"; Voice = "it-IT-Neural2-A" }
        "pt" = @{ Name = "Portuguese"; Flag = "🇵🇹"; Voice = "pt-PT-Neural2-A" }
        "ru" = @{ Name = "Russian"; Flag = "🇷🇺"; Voice = "ru-RU-Neural2-A" }
        "ja" = @{ Name = "Japanese"; Flag = "🇯🇵"; Voice = "ja-JP-Neural2-B" }
        "ko" = @{ Name = "Korean"; Flag = "🇰🇷"; Voice = "ko-KR-Neural2-A" }
        "zh" = @{ Name = "Chinese"; Flag = "🇨🇳"; Voice = "zh-CN-Neural2-A" }
    }
    SupportedPlatforms = @("YouTube", "TikTok", "Instagram")
    SupportedGenres = @("Horror", "Thriller", "Mystery", "Sci-Fi", "Suspense")
    SupportedModels = @("GPT-4", "Claude-3", "Gemini-Pro")
}

# --- Monetization helpers ---
function Ensure-MonetizationMacros {
    param([string]$Path = $null)
    if (Get-Command New-DescriptionText -ErrorAction SilentlyContinue) { $script:MonetizeLoaded = $true; return $true }

    try {
        if (-not $Path) {
            $scriptDir   = Split-Path -Parent $PSCommandPath
            $scarifyRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path  # ..\scarify\
            $default     = Join-Path $scarifyRoot "cli\SCARIFY-Monetize-Macros.ps1"
            $Path        = (Get-Item $env:SCARIFY_MACROS_PATH -ErrorAction SilentlyContinue)?.FullName ?? $default
        }
        if (-not (Test-Path $Path)) { Write-Host "[monetize] macros not found at $Path" -ForegroundColor Yellow; return $false }
        . $Path
        $script:MonetizeLoaded = $true
        Write-Host "[monetize] macros loaded: $Path" -ForegroundColor Green
        return $true
    } catch {
        Write-Warning "[monetize] load failed: $($_.Exception.Message)"
        return $false
    }
}

function Invoke-MonetizationForItem {
    param(
        [string]$Language,
        [string]$Platform,
        [string]$Theme,
        [string]$OutputPath,
        [string]$StoryText
    )
    if (-not $script:MonetizeLoaded) { if (-not (Ensure-MonetizationMacros)) { return } }

    $campaign = "SCARIFY_${($script:SessionStamp)}"
    $slug     = ($Theme -replace '\W+','_').ToUpperInvariant()

    # Defaults (swap to your real links anytime)
    $title       = "SCARIFY — $Theme ($Language/$Platform)"
    $hook        = "🔴 Decode tonight's clue. It's in the noise."
    $nextEp      = "https://youtube.com/watch?v=NEXT_EP_PLACEHOLDER"
    $sponsorName = "ShadowVPN"
    $sponsorUrl  = "https://shadowvpn.example.com/aioracle"
    $sponsorCode = "ORACLE20"
    $digitalPack = "https://gum.co/scream-pack-100"
    $affiliate   = "https://amzn.to/your-haunt-kit"
    $patreon     = "https://patreon.com/SignalGhost"
    $discord     = "https://discord.gg/YOURCODE"
    $merch       = "https://shop.signalghost.com/collections/oracle"

    try {
        $desc = if (Get-Command New-DescriptionText -ErrorAction SilentlyContinue) {
            New-DescriptionText -Title $title -HookOneLiner $hook -Campaign $campaign -ContentSlug $slug `
                -NextEpisodeUrl $nextEp -SponsorName $sponsorName -SponsorUrl $sponsorUrl -SponsorCode $sponsorCode `
                -DigitalPackUrl $digitalPack -AffiliateBundleUrl $affiliate -PatreonUrl $patreon -DiscordUrl $discord -MerchUrl $merch
        } else {
            # Fallback description
            @"
$title

$hook

🎯 Campaign: $campaign
📍 Content: $slug

🔗 Links:
▶️ Next Episode: $nextEp
🛡️ Sponsor ($sponsorName): $sponsorUrl (Code: $sponsorCode)
💎 Digital Pack: $digitalPack
🛒 Affiliate Bundle: $affiliate
☕ Support us: $patreon
💬 Discord: $discord
👕 Merch: $merch

#horror #arg #scarify #$($Language.ToLowerInvariant()) #$($Platform.ToLowerInvariant())
"@
        }

        $pin = if (Get-Command New-PinnedCommentText -ErrorAction SilentlyContinue) {
            New-PinnedCommentText -Campaign $campaign -ContentSlug $slug -NextEpisodeUrl $nextEp `
                -SponsorName $sponsorName -SponsorUrl $sponsorUrl -SponsorCode $sponsorCode -DigitalPackUrl $digitalPack
        } else {
            # Fallback pinned comment
            @"
👋 Welcome to $title! 

🔴 Tonight's transmission: $hook

🎯 Use code $sponsorCode at $sponsorUrl for exclusive access
💎 Download the digital pack: $digitalPack
▶️ Next episode: $nextEp

#$campaign #$slug
"@
        }

        $manDir  = Ensure-Dir (Join-Path $OutputPath "manifests")
        $tagList = @("horror","arg","scarify",$Language.ToLowerInvariant(),$Platform.ToLowerInvariant(),$slug.ToLowerInvariant())
        $manifestPath = Join-Path $manDir ("upload_{0}_{1}_{2}.json" -f $Language,$Platform,$script:SessionStamp)

        $links = @{
            "next_episode" = $nextEp
            "sponsor"      = $sponsorUrl
            "digital_pack" = $digitalPack
            "affiliate"    = $affiliate
            "patreon"      = $patreon
            "discord"      = $discord
            "merch"        = $merch
        }

        if (Get-Command Update-UploadManifest -ErrorAction SilentlyContinue) {
            Update-UploadManifest -ManifestPath $manifestPath -Title $title -DescriptionText $desc -PinnedCommentText $pin `
                -Links $links -Tags $tagList -Privacy "unlisted" | Out-Null
        } else {
            # lightweight fallback
            $m = @{
                title       = $title
                description = $desc
                pinned_comment = $pin
                tags        = $tagList
                links       = $links
                privacy     = "unlisted"
                story_snippet = ($StoryText.Substring(0,[Math]::Min(180,$StoryText.Length)))
                last_updated_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
            }
            $m | ConvertTo-Json -Depth 8 | Set-Content -Path $manifestPath -Encoding UTF8
        }

        # also save plain text for uploaders
        $descTxt = Join-Path $manDir ("description_{0}_{1}_{2}.txt" -f $Language,$Platform,$script:SessionStamp)
        $pinTxt  = Join-Path $manDir ("pinned_{0}_{1}_{2}.txt"      -f $Language,$Platform,$script:SessionStamp)
        $desc | Set-Content -Path $descTxt -Encoding UTF8
        $pin  | Set-Content -Path $pinTxt  -Encoding UTF8
        Write-Host "[monetize] wrote: $manifestPath" -ForegroundColor DarkGreen
    }
    catch {
        Write-Warning "[monetize] generation failed: $($_.Exception.Message)"
    }
}

# --- Content Generation Classes ---
class GlobalContentGenerator {
    [string]$Language
    [string]$Genre
    [string]$Model

    GlobalContentGenerator([string]$language, [string]$genre, [string]$model) {
        $this.Language = $language
        $this.Genre = $genre
        $this.Model = $model
    }

    [hashtable] GenerateMultiLanguageContent([string]$alertText, [string]$location) {
        # Simulate content generation for different languages
        $baseStory = $this.GenerateBaseStory($alertText, $location)
        
        $content = @{}
        foreach ($lang in $Global:Config.SupportedLanguages.Keys) {
            $localizedStory = $this.LocalizeStory($baseStory, $lang, $location)
            $content[$lang] = @{
                Story = $localizedStory
                Title = "Oracle Alert: $location"
                Description = "Emergency transmission from $location"
            }
        }
        
        return $content
    }

    [string] GenerateBaseStory([string]$alertText, [string]$location) {
        # Base story generation logic
        return @"
EMERGENCY TRANSMISSION - $location

Signal intercepted at coordinates: $location
Alert content: $alertText

The Oracle has detected anomalous activity in the region. Citizens are advised to remain vigilant and report any unusual phenomena to local authorities.

This transmission will repeat every 15 minutes until further notice.

END TRANSMISSION
"@
    }

    [string] LocalizeStory([string]$baseStory, [string]$language, [string]$location) {
        # Simulate localization (in real implementation, this would use translation APIs)
        $langInfo = $Global:Config.SupportedLanguages[$language]
        return "$($langInfo.Flag) [$($langInfo.Name)] $baseStory"
    }
}

# --- Main Content Generation Function ---
function Start-GlobalContentGeneration {
    param(
        [string[]]$Languages,
        [string[]]$Platforms,
        [string]$Genre,
        [string]$Model,
        [System.Windows.Forms.ProgressBar]$ProgressBar,
        [System.Windows.Forms.Label]$StatusLabel,
        [int]$BatchSize,
        [bool]$BurnCaptions,
        [bool]$Upload,
        [System.Windows.Forms.Button]$LaunchButton,
        [System.Windows.Forms.Button]$CancelButton
    )

    # prepare cancel token
    if ($script:CancelCts) { try { $script:CancelCts.Dispose() } catch {} }
    $script:CancelCts = [System.Threading.CancellationTokenSource]::new()
    $token = $script:CancelCts.Token

    # set UI initial state
    $LaunchButton.Enabled = $false
    $CancelButton.Enabled = $true
    $StatusLabel.ForeColor = [System.Drawing.Color]::Gold
    $StatusLabel.Text = "Preparing…"
    [System.Windows.Forms.Application]::DoEvents()

    $totalSteps = [math]::Max(1, $Languages.Count * $Platforms.Count * $BatchSize)
    $ProgressBar.Minimum = 0; $ProgressBar.Maximum = $totalSteps; $ProgressBar.Value = 0
    $currentStep = 0
    $cancelled = $false

    $generator = [GlobalContentGenerator]::new(($Languages | Select-Object -First 1), $Genre, $Model)

    # sample alert data (stub)
    $sampleAlerts = @(
        @{ Text = "petersburg healthcare DISTANT_BEEP"; Location = "Petersburg VA" }
        @{ Text = "miami logistics FAINT_ALARM";        Location = "Miami FL" }
        @{ Text = "london finance STATIC_HISS";         Location = "London UK" }
        @{ Text = "tokyo healthcare DISTANT_BEEP";      Location = "Tokyo JP" }
        @{ Text = "berlin logistics FAINT_ALARM";       Location = "Berlin DE" }
    )

    foreach ($language in $Languages) {
        if ($token.IsCancellationRequested) { $cancelled = $true; break }
        $StatusLabel.Text = "Generating for $($Global:Config.SupportedLanguages[$language].Name)…"
        [System.Windows.Forms.Application]::DoEvents()

        foreach ($platform in $Platforms) {
            if ($token.IsCancellationRequested) { $cancelled = $true; break }
            for ($i = 0; $i -lt $BatchSize; $i++) {
                if ($token.IsCancellationRequested) { $cancelled = $true; break }

                try {
                    $alert = $sampleAlerts[$i % $sampleAlerts.Count]
                    $StatusLabel.Text = "Processing $($Global:Config.SupportedLanguages[$language].Flag)  $($alert.Location)  →  $platform ($($i+1)/$BatchSize)…"
                    [System.Windows.Forms.Application]::DoEvents()

                    # generate multilingual content
                    $content = $generator.GenerateMultiLanguageContent($alert.Text, $alert.Location)

                    # platform output dir (portable)
                    $outPath = Ensure-Dir (Join-Path (Join-Path (Join-Path "Output" "Global") $language) $platform)

                    # (your per-platform handling here)
                    switch ($platform) {
                        "YouTube" {
                            $params = @{
                                Theme        = "$($alert.Location)_Horror_$language"
                                VoiceStyle   = $Global:Config.SupportedLanguages[$language].Voice
                                Language     = $language
                                Story        = $content[$language].Story
                                OutputPath   = $outPath
                                BurnCaptions = $BurnCaptions
                                Platform     = $platform
                                Upload       = $Upload
                            }
                            # Generate-PlatformSpecificContent $params
                        }
                        default { } # TikTok/Instagram stubs
                    }

                    # 🔗 Monetization per batch item
                    Invoke-MonetizationForItem -Language $language -Platform $platform -Theme "$($alert.Location) Horror" `
                        -OutputPath $outPath -StoryText $content[$language].Story
                }
                catch {
                    $StatusLabel.Text = "Error: $($_.Exception.Message)"
                }
                finally {
                    $currentStep++
                    if ($currentStep -le $ProgressBar.Maximum) { $ProgressBar.Value = $currentStep }
                    [System.Windows.Forms.Application]::DoEvents()
                    Start-Sleep -Milliseconds 150
                }
            }
            if ($cancelled) { break }
        }
        if ($cancelled) { break }
    }

    # finalize UI
    if ($cancelled) {
        $StatusLabel.Text = "⏹️ Cancelled by user."
        $StatusLabel.ForeColor = [System.Drawing.Color]::Orange
    } else {
        $StatusLabel.Text = "✅ Complete! $currentStep items processed."
        $StatusLabel.ForeColor = [System.Drawing.Color]::LightGreen
    }
    $CancelButton.Enabled = $false
    $LaunchButton.Enabled = $true
    [System.Windows.Forms.Application]::DoEvents()
}

# --- Preview Functions ---
function Show-ContentPreview {
    param(
        [hashtable]$LanguageCheckboxes,
        [string]$Genre
    )
    
    $selectedLanguages = @()
    foreach ($langCode in $LanguageCheckboxes.Keys) {
        if ($LanguageCheckboxes[$langCode].Checked) {
            $selectedLanguages += $Global:Config.SupportedLanguages[$langCode].Name
        }
    }
    
    $previewText = "Content Preview`n`n"
    $previewText += "Selected Languages: $($selectedLanguages -join ', ')`n"
    $previewText += "Genre: $Genre`n`n"
    $previewText += "Sample content would be generated for each language/platform combination..."
    
    [System.Windows.Forms.MessageBox]::Show($previewText, "Content Preview", [System.Windows.Forms.MessageBoxButtons]::OK)
}

function Export-LauncherConfig {
    param([System.Windows.Forms.Form]$Form)
    
    $configData = @{
        SessionStamp = $script:SessionStamp
        ExportTime = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ssZ")
        SupportedLanguages = $Global:Config.SupportedLanguages.Keys
        SupportedPlatforms = $Global:Config.SupportedPlatforms
        SupportedGenres = $Global:Config.SupportedGenres
    }
    
    $configPath = "Output\launcher_config_$($script:SessionStamp).json"
    Ensure-Dir (Split-Path -Parent $configPath)
    $configData | ConvertTo-Json -Depth 3 | Set-Content -Path $configPath -Encoding UTF8
    
    [System.Windows.Forms.MessageBox]::Show("Configuration exported to: $configPath", "Export Complete", [System.Windows.Forms.MessageBoxButtons]::OK)
}

# --- Main GUI Function ---
function Show-GlobalLauncher {
    # Initialize monetization macros
    Ensure-MonetizationMacros | Out-Null
    
    # Create main form
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "🌐 Global Content Generation Launcher"
    $form.Size = New-Size 800 720
    $form.StartPosition = [System.Windows.Forms.FormStartPosition]::CenterScreen
    $form.BackColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
    $form.ForeColor = [System.Drawing.Color]::White

    # Title Label
    $titleLabel = New-Object System.Windows.Forms.Label
    $titleLabel.Text = "🌐 GLOBAL CONTENT GENERATION SYSTEM"
    $titleLabel.Location = New-Point 20 20
    $titleLabel.Size = New-Size 750 30
    $titleLabel.Font = New-Object System.Drawing.Font -ArgumentList "Arial", 16, ([System.Drawing.FontStyle]::Bold)
    $titleLabel.ForeColor = [System.Drawing.Color]::Cyan
    $titleLabel.TextAlign = [System.Drawing.ContentAlignment]::TopCenter

    # Language Selection Group
    $langGroupBox = New-Object System.Windows.Forms.GroupBox
    $langGroupBox.Text = "🌍 Language Selection"
    $langGroupBox.Location = New-Point 20 60
    $langGroupBox.Size = New-Size 360 200
    $langGroupBox.ForeColor = [System.Drawing.Color]::LightGreen

    $languageCheckboxes = @{}
    $yOffset = 25
    foreach ($langCode in $Global:Config.SupportedLanguages.Keys) {
        $langInfo = $Global:Config.SupportedLanguages[$langCode]
        $checkbox = New-Object System.Windows.Forms.CheckBox
        $checkbox.Text = "$($langInfo.Flag) $($langInfo.Name)"
        $checkbox.Location = New-Point 15 $yOffset
        $checkbox.Size = New-Size 150 20
        $checkbox.ForeColor = [System.Drawing.Color]::White
        $languageCheckboxes[$langCode] = $checkbox
        $langGroupBox.Controls.Add($checkbox)
        $yOffset += 25
        if ($yOffset -gt 175) {
            $yOffset = 25
            $checkbox.Location = New-Point 180 $yOffset
        }
    }

    # Genre Selection Group
    $genreGroupBox = New-Object System.Windows.Forms.GroupBox
    $genreGroupBox.Text = "🎭 Genre Selection"
    $genreGroupBox.Location = New-Point 400 60
    $genreGroupBox.Size = New-Size 360 100
    $genreGroupBox.ForeColor = [System.Drawing.Color]::LightBlue

    $genreComboBox = New-Object System.Windows.Forms.ComboBox
    $genreComboBox.Location = New-Point 20 30
    $genreComboBox.Size = New-Size 320 25
    $genreComboBox.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDownList
    $Global:Config.SupportedGenres | ForEach-Object { $genreComboBox.Items.Add($_) }
    $genreComboBox.SelectedIndex = 0
    $genreGroupBox.Controls.Add($genreComboBox)

    # Model Selection
    $modelLabel = New-Object System.Windows.Forms.Label
    $modelLabel.Text = "🤖 AI Model:"
    $modelLabel.Location = New-Point 20 65
    $modelLabel.Size = New-Size 80 20
    $modelLabel.ForeColor = [System.Drawing.Color]::White
    $genreGroupBox.Controls.Add($modelLabel)

    $modelComboBox = New-Object System.Windows.Forms.ComboBox
    $modelComboBox.Location = New-Point 110 63
    $modelComboBox.Size = New-Size 230 25
    $modelComboBox.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDownList
    $Global:Config.SupportedModels | ForEach-Object { $modelComboBox.Items.Add($_) }
    $modelComboBox.SelectedIndex = 0
    $genreGroupBox.Controls.Add($modelComboBox)

    # Platform Selection Group
    $platformGroupBox = New-Object System.Windows.Forms.GroupBox
    $platformGroupBox.Text = "📱 Platform Selection"
    $platformGroupBox.Location = New-Point 20 280
    $platformGroupBox.Size = New-Size 360 120
    $platformGroupBox.ForeColor = [System.Drawing.Color]::Orange

    $platformCheckboxes = @{}
    $yOffset = 25
    foreach ($platform in $Global:Config.SupportedPlatforms) {
        $checkbox = New-Object System.Windows.Forms.CheckBox
        $checkbox.Text = $platform
        $checkbox.Location = New-Point 15 $yOffset
        $checkbox.Size = New-Size 150 20
        $checkbox.ForeColor = [System.Drawing.Color]::White
        $checkbox.Checked = ($platform -eq "YouTube") # Default to YouTube
        $platformCheckboxes[$platform] = $checkbox
        $platformGroupBox.Controls.Add($checkbox)
        $yOffset += 25
    }

    # Data & Processing Group
    $dataGroupBox = New-Object System.Windows.Forms.GroupBox
    $dataGroupBox.Text = "⚙️ Processing Options"
    $dataGroupBox.Location = New-Point 400 180
    $dataGroupBox.Size = New-Size 360 220
    $dataGroupBox.ForeColor = [System.Drawing.Color]::Yellow

    # Batch Size
    $batchSizeLabel = New-Object System.Windows.Forms.Label
    $batchSizeLabel.Text = "Batch Size:"
    $batchSizeLabel.Location = New-Point 20 30
    $batchSizeLabel.Size = New-Size 80 20
    $batchSizeLabel.ForeColor = [System.Drawing.Color]::White
    $dataGroupBox.Controls.Add($batchSizeLabel)

    $batchSizeNumeric = New-Object System.Windows.Forms.NumericUpDown
    $batchSizeNumeric.Location = New-Point 110 28
    $batchSizeNumeric.Size = New-Size 80 25
    $batchSizeNumeric.Minimum = 1
    $batchSizeNumeric.Maximum = 50
    $batchSizeNumeric.Value = 5
    $dataGroupBox.Controls.Add($batchSizeNumeric)

    # Options checkboxes
    $burnCaptionsCheckBox = New-Object System.Windows.Forms.CheckBox
    $burnCaptionsCheckBox.Text = "Burn Captions"
    $burnCaptionsCheckBox.Location = New-Point 20 65
    $burnCaptionsCheckBox.Size = New-Size 150 20
    $burnCaptionsCheckBox.ForeColor = [System.Drawing.Color]::White
    $dataGroupBox.Controls.Add($burnCaptionsCheckBox)

    $uploadCheckBox = New-Object System.Windows.Forms.CheckBox
    $uploadCheckBox.Text = "Auto-Upload"
    $uploadCheckBox.Location = New-Point 20 95
    $uploadCheckBox.Size = New-Size 150 20
    $uploadCheckBox.ForeColor = [System.Drawing.Color]::White
    $dataGroupBox.Controls.Add($uploadCheckBox)

    # Output Group
    $outputGroupBox = New-Object System.Windows.Forms.GroupBox
    $outputGroupBox.Text = "📊 Progress & Status"
    $outputGroupBox.Location = New-Point 20 420
    $outputGroupBox.Size = New-Size 740 180
    $outputGroupBox.ForeColor = [System.Drawing.Color]::Magenta

    # Progress Bar
    $progressBar = New-Object System.Windows.Forms.ProgressBar
    $progressBar.Location = New-Point 20 30
    $progressBar.Size = New-Size 700 25
    $progressBar.Style = [System.Windows.Forms.ProgressBarStyle]::Continuous
    $outputGroupBox.Controls.Add($progressBar)

    # Status Label
    $statusLabel = New-Object System.Windows.Forms.Label
    $statusLabel.Text = "Ready to launch global content generation..."
    $statusLabel.Location = New-Point 20 65
    $statusLabel.Size = New-Size 700 20
    $statusLabel.ForeColor = [System.Drawing.Color]::LightGreen
    $outputGroupBox.Controls.Add($statusLabel)

    # Launch Button
    $launchButton = New-Object System.Windows.Forms.Button
    $launchButton.Text = "🚀 Launch Global Content Generation"
    $launchButton.Location = New-Point 20 620
    $launchButton.Size = New-Size 300 40
    $launchButton.BackColor = [System.Drawing.Color]::FromArgb(255, 100, 100)
    $launchButton.ForeColor = [System.Drawing.Color]::White
    $launchButton.Font = New-Object System.Drawing.Font -ArgumentList "Arial", 12, ([System.Drawing.FontStyle]::Bold)

    # Cancel Button (new)
    $cancelButton = New-Object System.Windows.Forms.Button
    $cancelButton.Text = "⏹️ Cancel"
    $cancelButton.Location = New-Point 330 620
    $cancelButton.Size = New-Size 120 40
    $cancelButton.BackColor = [System.Drawing.Color]::FromArgb(90, 90, 90)
    $cancelButton.ForeColor = [System.Drawing.Color]::White
    $cancelButton.Enabled = $false

    # Preview Button
    $previewButton = New-Object System.Windows.Forms.Button
    $previewButton.Text = "👁️ Preview Content"
    $previewButton.Location = New-Point 460 620
    $previewButton.Size = New-Size 150 40
    $previewButton.BackColor = [System.Drawing.Color]::FromArgb(100, 100, 255)
    $previewButton.ForeColor = [System.Drawing.Color]::White

    # Export Config Button
    $exportButton = New-Object System.Windows.Forms.Button
    $exportButton.Text = "💾 Export Config"
    $exportButton.Location = New-Point 620 620
    $exportButton.Size = New-Size 150 40
    $exportButton.BackColor = [System.Drawing.Color]::FromArgb(100, 255, 100)
    $exportButton.ForeColor = [System.Drawing.Color]::Black

    # Event Handlers
    $launchButton.Add_Click({
        $selectedLanguages = @()
        foreach ($langCode in $languageCheckboxes.Keys) {
            if ($languageCheckboxes[$langCode].Checked) { $selectedLanguages += $langCode }
        }
        if ($selectedLanguages.Count -eq 0) {
            [System.Windows.Forms.MessageBox]::Show("Please select at least one language.", "No Languages Selected")
            return
        }
        $selectedPlatforms = @()
        foreach ($platform in $platformCheckboxes.Keys) {
            if ($platformCheckboxes[$platform].Checked) { $selectedPlatforms += $platform }
        }

        Start-GlobalContentGeneration `
            -Languages $selectedLanguages `
            -Platforms $selectedPlatforms `
            -Genre $genreComboBox.SelectedItem `
            -Model $modelComboBox.SelectedItem `
            -ProgressBar $progressBar `
            -StatusLabel $statusLabel `
            -BatchSize $batchSizeNumeric.Value `
            -BurnCaptions $burnCaptionsCheckBox.Checked `
            -Upload $uploadCheckBox.Checked `
            -LaunchButton $launchButton `
            -CancelButton $cancelButton
    })

    $cancelButton.Add_Click({
        if ($script:CancelCts -and -not $script:CancelCts.IsCancellationRequested) {
            $statusLabel.Text = "Cancelling…"
            $statusLabel.ForeColor = [System.Drawing.Color]::Orange
            try { $script:CancelCts.Cancel() } catch {}
            $cancelButton.Enabled = $false
        }
    })

    $previewButton.Add_Click({ Show-ContentPreview -LanguageCheckboxes $languageCheckboxes -Genre $genreComboBox.SelectedItem })
    $exportButton.Add_Click({ Export-LauncherConfig -Form $form })

    # Add controls to form (include Cancel now)
    $form.Controls.AddRange(@(
        $titleLabel, $langGroupBox, $genreGroupBox, $platformGroupBox,
        $dataGroupBox, $outputGroupBox, $progressBar, $statusLabel,
        $launchButton, $cancelButton, $previewButton, $exportButton
    ))

    # Show the form
    $form.ShowDialog() | Out-Null
}

# --- Main Execution ---
if ($MyInvocation.InvocationName -ne '.') {
    Show-GlobalLauncher
}