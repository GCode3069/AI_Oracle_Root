# SCARIFY - Credential Extractor & Organizer (FIXED VERSION)
param(
    [string]$OutputDir = "F:\AI_Oracle_Root\scarify\config\credentials",
    [switch]$BackupOriginal = $true
)

Write-Host "🔐 SCARIFY CREDENTIAL ORGANIZER" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    Write-Host "📁 Created output directory: $OutputDir" -ForegroundColor Green
}

# Focus on the important credential files you found
$importantCreds = @(
    "C:\AI_Oracle_Root\AI_Oracle_Root\credentials\Claude.key",
    "C:\AI_Oracle_Root\AI_Oracle_Root\credentials\ElevenLabs.key",
    "C:\AI_Oracle_Root\AI_Oracle_Root\Useful_Extracted\credentials\Claude.key",
    "C:\AI_Oracle_Root\AI_Oracle_Root\Useful_Extracted\credentials\ElevenLabs.key",
    "C:\AI_Oracle_Root\AI_Oracle_Root\Useful_Extracted\Claude.key",
    "C:\AI_Oracle_Root\AI_Oracle_Root\Useful_Extracted\ElevenLabs.key"
)

Write-Host "`n🎯 EXTRACTING CREDENTIALS FOR SCARIFY SYSTEM..." -ForegroundColor Green

$extractedCount = 0
$organizedCreds = @{}

foreach ($credFile in $importantCreds) {
    if (Test-Path $credFile) {
        Write-Host "`n📖 Reading: $credFile" -ForegroundColor Cyan
        
        try {
            $content = Get-Content -Path $credFile -Raw -ErrorAction Stop
            
            # Determine credential type
            if ($credFile -match "Claude") {
                $credType = "Claude"
                $organizedCreds["Claude"] = $content.Trim()
                $outputFile = "claude_api.key"
            }
            elseif ($credFile -match "ElevenLabs") {
                $credType = "ElevenLabs"
                $organizedCreds["ElevenLabs"] = $content.Trim()
                $outputFile = "elevenlabs_api.key"
            }
            else {
                $credType = "Unknown"
                $outputFile = "unknown.key"
            }
            
            # Save to organized location
            $outputPath = Join-Path $OutputDir $outputFile
            $content.Trim() | Out-File -FilePath $outputPath -Encoding UTF8 -NoNewline
            
            Write-Host "  ✅ Extracted: $credType API Key" -ForegroundColor Green
            Write-Host "  💾 Saved to: $outputPath" -ForegroundColor Gray
            
            # Backup original if requested
            if ($BackupOriginal) {
                $backupDir = Join-Path $OutputDir "backup_original"
                if (-not (Test-Path $backupDir)) {
                    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
                }
                Copy-Item -Path $credFile -Destination (Join-Path $backupDir (Split-Path $credFile -Leaf)) -Force
                Write-Host "  📦 Backed up original" -ForegroundColor Gray
            }
            
            $extractedCount++
        }
        catch {
            Write-Host "  ❌ Failed to read: $credFile" -ForegroundColor Red
            Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
    else {
        Write-Host "  ⚠️  Not found: $credFile" -ForegroundColor Yellow
    }
}

# Create environment template with FIXED syntax
Write-Host "`n🔧 CREATING SCARIFY CONFIGURATION..." -ForegroundColor Cyan

# Handle the null coalescing manually
$elevenLabsValue = "your_elevenlabs_api_key_here"
$claudeValue = "your_claude_api_key_here"

if ($organizedCreds["ElevenLabs"]) {
    $elevenLabsValue = $organizedCreds["ElevenLabs"]
}

if ($organizedCreds["Claude"]) {
    $claudeValue = $organizedCreds["Claude"]
}

$envTemplate = @"
# SCARIFY Environment Variables
# Copy this to .env file and fill in your actual API keys

# AI Services
ELEVENLABS_API_KEY=$elevenLabsValue
CLAUDE_API_KEY=$claudeValue
OPENAI_API_KEY=your_openai_api_key_here
RUNWAY_API_KEY=your_runway_api_key_here

# YouTube OAuth2
YT_CLIENT_SECRETS_PATH=config/credentials/client_secrets.json
YT_CREDENTIALS_PATH=config/credentials/youtube_oauth_credentials.json

# System Paths
SCARIFY_ROOT=F:\AI_Oracle_Root\scarify
CONTENT_SOURCE=F:\Extreme SSD\SCARIFY_CONSOLIDATED
OUTPUT_DIR=output

# Upload Settings
UPLOAD_METHOD=standard
DEFAULT_ARCHETYPE=Mystic
"@

$envTemplatePath = Join-Path $OutputDir ".env.template"
$envTemplate | Out-File -FilePath $envTemplatePath -Encoding UTF8

Write-Host "  ✅ Environment template: $envTemplatePath" -ForegroundColor Green

# Create actual .env file with extracted keys
if ($organizedCreds["ElevenLabs"] -or $organizedCreds["Claude"]) {
    $actualEnv = @"
# SCARIFY Environment Variables - ACTUAL KEYS
# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')

# AI Services
ELEVENLABS_API_KEY=$($organizedCreds['ElevenLabs'] ?? '')
CLAUDE_API_KEY=$($organizedCreds['Claude'] ?? '')
OPENAI_API_KEY=your_openai_api_key_here
RUNWAY_API_KEY=your_runway_api_key_here

# System Paths
SCARIFY_ROOT=F:\AI_Oracle_Root\scarify
CONTENT_SOURCE=F:\Extreme SSD\SCARIFY_CONSOLIDATED
OUTPUT_DIR=output
"@

    $actualEnvPath = Join-Path $OutputDir ".env"
    $actualEnv | Out-File -FilePath $actualEnvPath -Encoding UTF8
    Write-Host "  ✅ Actual .env file created: $actualEnvPath" -ForegroundColor Green
}

# Summary
Write-Host "`n🎉 CREDENTIAL EXTRACTION COMPLETE!" -ForegroundColor Green
Write-Host "=" * 40 -ForegroundColor Green
Write-Host "📊 Extraction Summary:" -ForegroundColor Cyan
Write-Host "  ✅ Files processed: $extractedCount" -ForegroundColor White

if ($organizedCreds['ElevenLabs']) {
    Write-Host "  🔑 ElevenLabs API: EXTRACTED" -ForegroundColor Green
    Write-Host "     Key: $($organizedCreds['ElevenLabs'].Substring(0, [Math]::Min(10, $organizedCreds['ElevenLabs'].Length)))..." -ForegroundColor Gray
} else {
    Write-Host "  🔑 ElevenLabs API: MISSING" -ForegroundColor Red
}

if ($organizedCreds['Claude']) {
    Write-Host "  🧠 Claude API: EXTRACTED" -ForegroundColor Green
    Write-Host "     Key: $($organizedCreds['Claude'].Substring(0, [Math]::Min(10, $organizedCreds['Claude'].Length)))..." -ForegroundColor Gray
} else {
    Write-Host "  🧠 Claude API: MISSING" -ForegroundColor Red
}

Write-Host "  📁 Output location: $OutputDir" -ForegroundColor White

Write-Host "`n🚀 NEXT STEPS FOR SCARIFY:" -ForegroundColor Yellow
Write-Host "  1. Review extracted keys in: $OutputDir" -ForegroundColor Gray
Write-Host "  2. Add missing API keys (RunwayML, YouTube OAuth)" -ForegroundColor Gray
Write-Host "  3. Test AI services with extracted credentials" -ForegroundColor Gray
Write-Host "  4. Run first real SCARIFY upload!" -ForegroundColor Green

# Show what we extracted
if ($organizedCreds.Count -gt 0) {
    Write-Host "`n📋 EXTRACTED CREDENTIALS:" -ForegroundColor Cyan
    foreach ($key in $organizedCreds.Keys) {
        Write-Host "  $key : $($organizedCreds[$key].Substring(0, [Math]::Min(15, $organizedCreds[$key].Length)))..." -ForegroundColor Gray
    }
}
