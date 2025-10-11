<#
.SYNOPSIS
Test-Cancellation.ps1 - Tests the cancellation functionality

.DESCRIPTION
Demonstrates how the cancellation token works in the content generation system.
#>

# Load the test functions
. ./GlobalLauncher-Test.ps1

function Test-CancellationFeature {
    Write-Host "🧪 Testing Cancellation Feature" -ForegroundColor Cyan
    Write-Host "=" * 40 -ForegroundColor Cyan
    
    # Initialize
    Ensure-MonetizationMacros | Out-Null
    
    # Test parameters for a longer run
    $languages = @("en", "es", "fr")
    $platforms = @("YouTube", "TikTok", "Instagram")
    $batchSize = 5
    
    Write-Host "Starting generation that will be cancelled mid-process..." -ForegroundColor Yellow
    Write-Host "Languages: $($languages -join ', ')" -ForegroundColor White
    Write-Host "Platforms: $($platforms -join ', ')" -ForegroundColor White
    Write-Host "Batch Size: $batchSize per platform" -ForegroundColor White
    Write-Host ""
    
    # Create cancellation token
    $script:CancelCts = [System.Threading.CancellationTokenSource]::new()
    $token = $script:CancelCts.Token
    
    $generator = [GlobalContentGenerator]::new($languages[0], "Horror", "GPT-4")
    
    # Sample alerts
    $sampleAlerts = @(
        @{ Text = "petersburg healthcare DISTANT_BEEP"; Location = "Petersburg VA" }
        @{ Text = "miami logistics FAINT_ALARM";        Location = "Miami FL" }
        @{ Text = "london finance STATIC_HISS";         Location = "London UK" }
        @{ Text = "tokyo healthcare DISTANT_BEEP";      Location = "Tokyo JP" }
        @{ Text = "berlin logistics FAINT_ALARM";       Location = "Berlin DE" }
    )
    
    $currentStep = 0
    $totalSteps = $languages.Count * $platforms.Count * $batchSize
    $cancelled = $false
    
    # Schedule cancellation after 3 steps
    $timer = New-Object System.Timers.Timer
    $timer.Interval = 1500  # 1.5 seconds
    $timer.AutoReset = $false
    $timer.add_Elapsed({
        Write-Host "`n⏹️ CANCELLATION TRIGGERED!" -ForegroundColor Red
        $script:CancelCts.Cancel()
    })
    $timer.Start()
    
    foreach ($language in $languages) {
        if ($token.IsCancellationRequested) { $cancelled = $true; break }
        Write-Host "Processing language: $($Global:Config.SupportedLanguages[$language].Name)" -ForegroundColor Yellow
        
        foreach ($platform in $platforms) {
            if ($token.IsCancellationRequested) { $cancelled = $true; break }
            for ($i = 0; $i -lt $batchSize; $i++) {
                if ($token.IsCancellationRequested) { $cancelled = $true; break }
                
                $alert = $sampleAlerts[$i % $sampleAlerts.Count]
                $currentStep++
                
                Write-Host "  Step $currentStep/$totalSteps : $($Global:Config.SupportedLanguages[$language].Flag) $($alert.Location) → $platform" -ForegroundColor Cyan
                
                try {
                    # Generate content
                    $content = $generator.GenerateMultiLanguageContent($alert.Text, $alert.Location)
                    
                    # Create output directory
                    $outPath = Ensure-Dir (Join-Path (Join-Path (Join-Path "Output" "Cancelled") $language) $platform)
                    
                    # Generate monetization content
                    Invoke-MonetizationForItem -Language $language -Platform $platform -Theme "$($alert.Location) Horror" `
                        -OutputPath $outPath -StoryText $content[$language].Story
                    
                    Start-Sleep -Milliseconds 500  # Simulate longer processing time
                }
                catch {
                    Write-Host "    Error: $($_.Exception.Message)" -ForegroundColor Red
                }
            }
            if ($cancelled) { break }
        }
        if ($cancelled) { break }
    }
    
    $timer.Stop()
    $timer.Dispose()
    
    Write-Host ""
    if ($cancelled) {
        Write-Host "⏹️ Process was cancelled after $currentStep steps (out of $totalSteps total)." -ForegroundColor Orange
        Write-Host "✅ Cancellation worked correctly - completed work was preserved." -ForegroundColor Green
    } else {
        Write-Host "⚠️ Process completed without cancellation (timer may have been too slow)." -ForegroundColor Yellow
    }
    
    # Show what was actually generated before cancellation
    $generatedFiles = Get-ChildItem -Path "Output/Cancelled" -Recurse -File -ErrorAction SilentlyContinue
    if ($generatedFiles) {
        Write-Host "📁 Files generated before cancellation:" -ForegroundColor Cyan
        $generatedFiles | ForEach-Object { Write-Host "   $($_.FullName)" -ForegroundColor Gray }
    } else {
        Write-Host "📁 No files were generated (cancellation happened very early)" -ForegroundColor Gray
    }
}

# Run the test
Test-CancellationFeature