<#
.SYNOPSIS
GlobalLauncher-Test.ps1 - Test version for non-Windows platforms

.DESCRIPTION
Tests the core functionality of GlobalLauncher.ps1 without GUI components.
This demonstrates the helper functions, monetization macros, and content generation logic.
#>

# Skip Windows Forms on non-Windows platforms
if ($PSVersionTable.Platform -ne "Win32NT") {
    Write-Host "Non-Windows platform detected. Testing core functionality only." -ForegroundColor Yellow
    Write-Host "Windows Forms GUI will work on Windows platforms." -ForegroundColor Yellow
}

# --- helpers & globals (same as main script) ---
function New-Point([int]$x,[int]$y){ New-Object System.Drawing.Point -ArgumentList $x,$y }
function New-Size ([int]$w,[int]$h){ New-Object System.Drawing.Size  -ArgumentList $w,$h }
function Ensure-Dir([string]$p){ if(-not(Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } $p }

# session + cancel state
$script:SessionStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$script:CancelCts    = $null   # [System.Threading.CancellationTokenSource]
$script:MonetizeLoaded = $false

# Test Configuration
$Global:Config = @{
    SupportedLanguages = @{
        "en" = @{ Name = "English"; Flag = "🇺🇸"; Voice = "en-US-Neural2-D" }
        "es" = @{ Name = "Spanish"; Flag = "🇪🇸"; Voice = "es-ES-Neural2-B" }
        "fr" = @{ Name = "French"; Flag = "🇫🇷"; Voice = "fr-FR-Neural2-A" }
    }
    SupportedPlatforms = @("YouTube", "TikTok", "Instagram")
    SupportedGenres = @("Horror", "Thriller", "Mystery")
    SupportedModels = @("GPT-4", "Claude-3", "Gemini-Pro")
}

# --- Monetization helpers (same as main script) ---
function Ensure-MonetizationMacros {
    param([string]$Path = $null)
    Write-Host "[monetize] Simulating macro loading (no actual macros file)" -ForegroundColor Yellow
    $script:MonetizeLoaded = $true
    return $true
}

function Invoke-MonetizationForItem {
    param(
        [string]$Language,
        [string]$Platform,
        [string]$Theme,
        [string]$OutputPath,
        [string]$StoryText
    )
    
    $campaign = "SCARIFY_${($script:SessionStamp)}"
    $slug     = ($Theme -replace '\W+','_').ToUpperInvariant()
    $title    = "SCARIFY — $Theme ($Language/$Platform)"
    
    # Create manifest directory
    $manDir = Ensure-Dir (Join-Path $OutputPath "manifests")
    $manifestPath = Join-Path $manDir ("upload_{0}_{1}_{2}.json" -f $Language,$Platform,$script:SessionStamp)
    
    # Generate sample description
    $desc = @"
$title

🔴 Decode tonight's clue. It's in the noise.

🎯 Campaign: $campaign
📍 Content: $slug

#horror #arg #scarify #$($Language.ToLowerInvariant()) #$($Platform.ToLowerInvariant())
"@
    
    # Generate sample pinned comment
    $pin = @"
👋 Welcome to $title! 

🔴 Tonight's transmission: Decode tonight's clue. It's in the noise.

#$campaign #$slug
"@
    
    # Create manifest
    $manifest = @{
        title = $title
        description = $desc
        pinned_comment = $pin
        tags = @("horror","arg","scarify",$Language.ToLowerInvariant(),$Platform.ToLowerInvariant(),$slug.ToLowerInvariant())
        privacy = "unlisted"
        story_snippet = ($StoryText.Substring(0,[Math]::Min(180,$StoryText.Length)))
        last_updated_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    }
    
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -Path $manifestPath -Encoding UTF8
    
    # Save plain text files
    $descTxt = Join-Path $manDir ("description_{0}_{1}_{2}.txt" -f $Language,$Platform,$script:SessionStamp)
    $pinTxt  = Join-Path $manDir ("pinned_{0}_{1}_{2}.txt"      -f $Language,$Platform,$script:SessionStamp)
    $desc | Set-Content -Path $descTxt -Encoding UTF8
    $pin  | Set-Content -Path $pinTxt  -Encoding UTF8
    
    Write-Host "[monetize] wrote: $manifestPath" -ForegroundColor Green
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
        $langInfo = $Global:Config.SupportedLanguages[$language]
        return "$($langInfo.Flag) [$($langInfo.Name)] $baseStory"
    }
}

# --- Test Function ---
function Test-ContentGeneration {
    Write-Host "🧪 Testing Global Content Generation System" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Cyan
    
    # Initialize
    Ensure-MonetizationMacros | Out-Null
    
    # Test parameters
    $languages = @("en", "es")
    $platforms = @("YouTube", "TikTok")
    $genre = "Horror"
    $model = "GPT-4"
    $batchSize = 2
    
    Write-Host "Languages: $($languages -join ', ')" -ForegroundColor White
    Write-Host "Platforms: $($platforms -join ', ')" -ForegroundColor White
    Write-Host "Genre: $genre" -ForegroundColor White
    Write-Host "Model: $model" -ForegroundColor White
    Write-Host "Batch Size: $batchSize" -ForegroundColor White
    Write-Host ""
    
    # Simulate cancellation token
    $script:CancelCts = [System.Threading.CancellationTokenSource]::new()
    $token = $script:CancelCts.Token
    
    $generator = [GlobalContentGenerator]::new($languages[0], $genre, $model)
    
    # Sample alerts
    $sampleAlerts = @(
        @{ Text = "petersburg healthcare DISTANT_BEEP"; Location = "Petersburg VA" }
        @{ Text = "miami logistics FAINT_ALARM";        Location = "Miami FL" }
    )
    
    $currentStep = 0
    $totalSteps = $languages.Count * $platforms.Count * $batchSize
    
    foreach ($language in $languages) {
        if ($token.IsCancellationRequested) { break }
        Write-Host "Processing language: $($Global:Config.SupportedLanguages[$language].Name)" -ForegroundColor Yellow
        
        foreach ($platform in $platforms) {
            if ($token.IsCancellationRequested) { break }
            for ($i = 0; $i -lt $batchSize; $i++) {
                if ($token.IsCancellationRequested) { break }
                
                $alert = $sampleAlerts[$i % $sampleAlerts.Count]
                $currentStep++
                
                Write-Host "  Step $currentStep/$totalSteps : $($Global:Config.SupportedLanguages[$language].Flag) $($alert.Location) → $platform" -ForegroundColor Cyan
                
                # Generate content
                $content = $generator.GenerateMultiLanguageContent($alert.Text, $alert.Location)
                
                # Create output directory
                $outPath = Ensure-Dir (Join-Path (Join-Path (Join-Path "Output" "Global") $language) $platform)
                
                # Generate monetization content
                Invoke-MonetizationForItem -Language $language -Platform $platform -Theme "$($alert.Location) Horror" `
                    -OutputPath $outPath -StoryText $content[$language].Story
                
                Start-Sleep -Milliseconds 100  # Simulate processing time
            }
        }
    }
    
    Write-Host ""
    Write-Host "✅ Test completed! Generated content for $currentStep items." -ForegroundColor Green
    Write-Host "📁 Check the Output/Global directory for generated files." -ForegroundColor Green
}

# --- Main Execution ---
if ($MyInvocation.InvocationName -ne '.') {
    Test-ContentGeneration
}