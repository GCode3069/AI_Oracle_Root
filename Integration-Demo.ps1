<#
.SYNOPSIS
Integration-Demo.ps1 - Demonstrates integration with existing MasterControl/MasterLaunch

.DESCRIPTION
Shows how the new GlobalLauncher system can work alongside the existing infrastructure.
#>

# Simulate integration with MasterControl.ps1
function Test-Integration {
    Write-Host "🔗 Testing Integration with Existing Scripts" -ForegroundColor Cyan
    Write-Host "=" * 50 -ForegroundColor Cyan
    
    # 1. Check if existing scripts are available
    $masterControl = ".\MasterControl.ps1"
    $masterLaunch = ".\MasterLaunch.ps1"
    
    Write-Host "Checking existing infrastructure:" -ForegroundColor Yellow
    Write-Host "  MasterControl.ps1: $(if (Test-Path $masterControl) { '✅ Found' } else { '❌ Missing' })" -ForegroundColor White
    Write-Host "  MasterLaunch.ps1:  $(if (Test-Path $masterLaunch) { '✅ Found' } else { '❌ Missing' })" -ForegroundColor White
    Write-Host ""
    
    # 2. Load our GlobalLauncher functions
    . .\GlobalLauncher-Test.ps1
    
    # 3. Generate content using our system
    Write-Host "Generating sample content with GlobalLauncher system..." -ForegroundColor Yellow
    
    $generator = [GlobalContentGenerator]::new("en", "Horror", "GPT-4")
    $alert = @{ Text = "integration test SIGNAL_DETECTED"; Location = "Integration City" }
    $content = $generator.GenerateMultiLanguageContent($alert.Text, $alert.Location)
    
    # 4. Create output in format compatible with existing scripts
    $outputPath = Ensure-Dir ".\Output\Integration\en\YouTube"
    
    # Generate monetization content
    Invoke-MonetizationForItem -Language "en" -Platform "YouTube" -Theme "Integration Test" `
        -OutputPath $outputPath -StoryText $content["en"].Story
    
    Write-Host "✅ Generated content compatible with existing pipeline" -ForegroundColor Green
    
    # 5. Show how this could integrate with MasterLaunch
    Write-Host ""
    Write-Host "Integration workflow:" -ForegroundColor Cyan
    Write-Host "  1. User runs GlobalLauncher.ps1 for content generation" -ForegroundColor White
    Write-Host "  2. Generated manifests and content are placed in Output/Global/" -ForegroundColor White
    Write-Host "  3. MasterLaunch.ps1 can be modified to pick up generated content" -ForegroundColor White
    Write-Host "  4. Deploy_Content.ps1 uses the manifests for automated uploading" -ForegroundColor White
    
    # 6. Sample integration code for MasterLaunch
    Write-Host ""
    Write-Host "Sample integration code for MasterLaunch.ps1:" -ForegroundColor Yellow
    Write-Host @"
# In MasterLaunch.ps1, add this section:
if (Test-Path ".\Output\Global") {
    Write-RunLog "Found GlobalLauncher content, integrating..."
    
    `$globalContent = Get-ChildItem -Path ".\Output\Global" -Recurse -Filter "*.json"
    foreach (`$manifest in `$globalContent) {
        Write-RunLog "Processing manifest: `$(`$manifest.Name)"
        # Use manifest data for deployment
    }
}
"@ -ForegroundColor Gray
    
    Write-Host ""
    Write-Host "✅ Integration demonstration complete!" -ForegroundColor Green
    Write-Host "📁 Check Output/Integration/ for generated files" -ForegroundColor Green
}

# Run the demonstration
Test-Integration