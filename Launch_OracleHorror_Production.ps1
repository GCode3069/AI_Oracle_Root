# Launch_OracleHorror_Production.ps1
# Oracle Horror Real Video Generation Engine Launcher
# Integrates with MasterControl.ps1 system
# Commander: GCode3069 | Horror Production Module

param(
    [string]$Campaign = "awakening",
    [string]$Format = "shorts", 
    [int]$Count = 1,
    [string]$OutputDir = "output",
    [switch]$Test,
    [switch]$All,
    [switch]$Verbose
)

# Enhanced logging for Oracle Horror
function Write-HorrorLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch ($Level) {
        "INFO" { "Cyan" }
        "SUCCESS" { "Green" }
        "WARNING" { "Yellow" }
        "ERROR" { "Red" }
        "HORROR" { "Magenta" }
        default { "White" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

# Oracle Horror Header
function Show-HorrorHeader {
    Write-Host ""
    Write-Host "=" * 80 -ForegroundColor Magenta
    Write-Host "🔮 ORACLE HORROR REAL VIDEO GENERATION ENGINE" -ForegroundColor Magenta
    Write-Host "   Real MP4 files • ElevenLabs Voice • FFmpeg Rendering" -ForegroundColor Cyan
    Write-Host "=" * 80 -ForegroundColor Magenta
    Write-Host ""
}

# Check Python and dependencies
function Test-Dependencies {
    Write-HorrorLog "🔍 Checking Oracle Horror dependencies..." "HORROR"
    
    # Check Python
    try {
        $pythonVersion = python3 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-HorrorLog "✅ Python: $pythonVersion" "SUCCESS"
        } else {
            Write-HorrorLog "❌ Python 3 not found" "ERROR"
            return $false
        }
    } catch {
        Write-HorrorLog "❌ Python 3 not available" "ERROR"
        return $false
    }
    
    # Check if requirements.txt exists
    if (Test-Path "requirements.txt") {
        Write-HorrorLog "✅ Requirements file found" "SUCCESS"
        
        # Install dependencies if needed
        Write-HorrorLog "📦 Installing/updating dependencies..." "INFO"
        python3 -m pip install -r requirements.txt --quiet
        
        if ($LASTEXITCODE -eq 0) {
            Write-HorrorLog "✅ Dependencies installed successfully" "SUCCESS"
        } else {
            Write-HorrorLog "⚠️ Some dependencies may have failed to install" "WARNING"
        }
    } else {
        Write-HorrorLog "❌ requirements.txt not found" "ERROR"
        return $false
    }
    
    # Check Oracle Horror CLI
    if (Test-Path "oracle_horror_cli.py") {
        Write-HorrorLog "✅ Oracle Horror CLI found" "SUCCESS"
        return $true
    } else {
        Write-HorrorLog "❌ oracle_horror_cli.py not found" "ERROR"
        return $false
    }
}

# Run Oracle Horror system test
function Invoke-HorrorSystemTest {
    Write-HorrorLog "🧪 Running Oracle Horror system test..." "HORROR"
    
    try {
        $testResult = python3 oracle_horror_cli.py test
        
        if ($LASTEXITCODE -eq 0) {
            Write-HorrorLog "✅ System test PASSED - Oracle Horror ready!" "SUCCESS"
            return $true
        } else {
            Write-HorrorLog "❌ System test FAILED" "ERROR"
            Write-HorrorLog "Test output: $testResult" "ERROR"
            return $false
        }
    } catch {
        Write-HorrorLog "❌ System test error: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Generate single horror video
function Invoke-HorrorGeneration {
    param([string]$CampaignType, [string]$FormatType, [string]$Output)
    
    Write-HorrorLog "🎬 Generating Oracle Horror video..." "HORROR"
    Write-HorrorLog "   Campaign: $CampaignType | Format: $FormatType" "INFO"
    
    try {
        $generateCmd = "python3 oracle_horror_cli.py generate --campaign $CampaignType --format $FormatType --output $Output"
        
        if ($Verbose) {
            Write-HorrorLog "Executing: $generateCmd" "INFO"
        }
        
        Invoke-Expression $generateCmd
        
        if ($LASTEXITCODE -eq 0) {
            Write-HorrorLog "✅ Horror video generated successfully!" "SUCCESS"
            
            # Check if output directory has new files
            if (Test-Path $Output) {
                $outputFiles = Get-ChildItem $Output -Recurse | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-5) }
                
                Write-HorrorLog "📁 Generated files:" "SUCCESS"
                foreach ($file in $outputFiles) {
                    Write-HorrorLog "   $($file.FullName)" "SUCCESS"
                }
            }
            
            return $true
        } else {
            Write-HorrorLog "❌ Horror video generation failed" "ERROR"
            return $false
        }
    } catch {
        Write-HorrorLog "❌ Generation error: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Generate multiple horror videos
function Invoke-HorrorBatch {
    param([int]$VideoCount, [string]$Output)
    
    Write-HorrorLog "🎬 Generating $VideoCount Oracle Horror videos..." "HORROR"
    
    try {
        $batchCmd = "python3 oracle_horror_cli.py all --count $VideoCount --output $Output"
        
        if ($Verbose) {
            Write-HorrorLog "Executing: $batchCmd" "INFO"
        }
        
        Invoke-Expression $batchCmd
        
        if ($LASTEXITCODE -eq 0) {
            Write-HorrorLog "✅ Batch generation completed!" "SUCCESS"
            
            # Show generated files
            if (Test-Path $Output) {
                $outputFiles = Get-ChildItem $Output -Recurse -File | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-10) }
                
                Write-HorrorLog "📁 Generated $($outputFiles.Count) files:" "SUCCESS"
                foreach ($file in $outputFiles) {
                    $sizeKB = [math]::Round($file.Length / 1KB, 2)
                    Write-HorrorLog "   $($file.Name) ($sizeKB KB)" "SUCCESS"
                }
            }
            
            return $true
        } else {
            Write-HorrorLog "❌ Batch generation failed" "ERROR"
            return $false
        }
    } catch {
        Write-HorrorLog "❌ Batch error: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Integration with MasterControl.ps1
function Register-WithMasterControl {
    Write-HorrorLog "🔗 Registering Oracle Horror with MasterControl..." "INFO"
    
    # Check if MasterControl.ps1 exists
    if (Test-Path "MasterControl.ps1") {
        Write-HorrorLog "✅ MasterControl.ps1 found - Integration available" "SUCCESS"
        
        # Could add more integration logic here in the future
        return $true
    } else {
        Write-HorrorLog "⚠️ MasterControl.ps1 not found - Standalone mode" "WARNING"
        return $false
    }
}

# Main execution
Show-HorrorHeader

Write-HorrorLog "🚀 Oracle Horror Production System Starting..." "HORROR"
Write-HorrorLog "Commander: GCode3069 | Timestamp: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')" "HORROR"

# Register with MasterControl
Register-WithMasterControl | Out-Null

# Check dependencies
if (-not (Test-Dependencies)) {
    Write-HorrorLog "❌ Dependency check failed - Cannot proceed" "ERROR"
    exit 1
}

# Handle different operation modes
if ($Test) {
    Write-HorrorLog "🧪 TEST MODE: Running system diagnostics" "HORROR"
    
    if (Invoke-HorrorSystemTest) {
        Write-HorrorLog "🎯 TEST COMPLETE: All systems operational" "SUCCESS"
        exit 0
    } else {
        Write-HorrorLog "❌ TEST FAILED: System not ready" "ERROR"
        exit 1
    }
}
elseif ($All) {
    Write-HorrorLog "🎭 BATCH MODE: Generating multiple horror videos" "HORROR"
    
    if (Invoke-HorrorBatch -VideoCount $Count -Output $OutputDir) {
        Write-HorrorLog "🌟 BATCH COMPLETE: Horror content ready for deployment" "SUCCESS"
        exit 0
    } else {
        Write-HorrorLog "❌ BATCH FAILED: Production incomplete" "ERROR"
        exit 1
    }
}
else {
    Write-HorrorLog "🎬 SINGLE MODE: Generating one horror video" "HORROR"
    
    if (Invoke-HorrorGeneration -CampaignType $Campaign -FormatType $Format -Output $OutputDir) {
        Write-HorrorLog "🎯 GENERATION COMPLETE: Horror video ready" "SUCCESS"
        exit 0
    } else {
        Write-HorrorLog "❌ GENERATION FAILED: Video not created" "ERROR"
        exit 1
    }
}

Write-Host ""
Write-Host "=" * 80 -ForegroundColor Magenta
Write-HorrorLog "🧬 Oracle Horror Production Session Complete" "HORROR"
Write-Host "=" * 80 -ForegroundColor Magenta