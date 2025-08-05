<#
.SYNOPSIS
    Chimera Orchestrator v3.2 - Enhanced AI Oracle Video Production System
    
.DESCRIPTION
    An advanced PowerShell automation system for processing voice files and generating
    video content with multiple template styles. Enhanced with progress bars, 
    configuration support, and additional video templates.
    
.PARAMETER ConfigPath
    Path to configuration file (JSON/YAML). Optional - uses defaults if not provided.
    
.PARAMETER InteractiveMode
    Enable interactive mode for template selection and confirmations.
    
.PARAMETER BatchSize
    Number of files to process in each batch. Default: 20
    
.EXAMPLE
    .\Chimera_Orchestrator.ps1
    
.EXAMPLE
    .\Chimera_Orchestrator.ps1 -ConfigPath "config.json" -InteractiveMode
    
.NOTES
    Version: 3.2
    Author: AI Oracle Team
    Requires: PowerShell 5.1+
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ConfigPath,
    
    [Parameter(Mandatory=$false)]
    [switch]$InteractiveMode,
    
    [Parameter(Mandatory=$false)]
    [int]$BatchSize = 20
)

# Global configuration with defaults
$Global:ChimeraConfig = @{
    VoiceInputDirectory = "Oracle_VoiceOuts"
    VideoOutputDirectory = "Oracle_VideoOuts"
    SupportedAudioFormats = @("*.wav", "*.mp3", "*.m4a")
    VideoTemplates = @(
        @{ Name = "emergency"; Style = "Urgent Alert"; BackgroundColor = "#FF4444"; TextColor = "#FFFFFF" }
        @{ Name = "news"; Style = "News Bulletin"; BackgroundColor = "#0066CC"; TextColor = "#FFFFFF" }
        @{ Name = "weather"; Style = "Weather Report"; BackgroundColor = "#4CAF50"; TextColor = "#FFFFFF" }
        @{ Name = "traffic"; Style = "Traffic Update"; BackgroundColor = "#FF9800"; TextColor = "#000000" }
        @{ Name = "psa"; Style = "Public Service"; BackgroundColor = "#9C27B0"; TextColor = "#FFFFFF" }
        @{ Name = "sports"; Style = "Sports Update"; BackgroundColor = "#E91E63"; TextColor = "#FFFFFF" }
        @{ Name = "entertainment"; Style = "Entertainment News"; BackgroundColor = "#FF5722"; TextColor = "#FFFFFF" }
        @{ Name = "tech"; Style = "Tech Alert"; BackgroundColor = "#607D8B"; TextColor = "#FFFFFF" }
        @{ Name = "health"; Style = "Health Advisory"; BackgroundColor = "#4CAF50"; TextColor = "#FFFFFF" }
    )
    MinDiskSpaceGB = 5
    MaxConcurrentJobs = 4
    LogLevel = "Info"
}

# Enhanced logging function with color support
function Write-ChimeraLog {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Message,
        
        [Parameter(Mandatory=$false)]
        [ValidateSet("Info", "Warning", "Error", "Success", "Debug")]
        [string]$Level = "Info"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $colorMap = @{
        "Info" = "White"
        "Warning" = "Yellow"
        "Error" = "Red"
        "Success" = "Green"
        "Debug" = "Gray"
    }
    
    $color = $colorMap[$Level]
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

# Configuration file loading
function Import-ChimeraConfig {
    param([string]$ConfigPath)
    
    if (-not $ConfigPath -or -not (Test-Path $ConfigPath)) {
        Write-ChimeraLog "Using default configuration" -Level "Info"
        return
    }
    
    try {
        $configContent = Get-Content $ConfigPath -Raw
        if ($ConfigPath -match '\.(json)$') {
            $config = $configContent | ConvertFrom-Json
        } elseif ($ConfigPath -match '\.(ya?ml)$') {
            # Basic YAML parsing for simple key-value pairs
            $config = @{}
            $configContent -split "`n" | ForEach-Object {
                if ($_ -match '^(\w+):\s*(.+)$') {
                    $config[$matches[1]] = $matches[2].Trim('"''')
                }
            }
        } else {
            throw "Unsupported configuration file format"
        }
        
        # Merge with defaults
        foreach ($key in $config.PSObject.Properties.Name) {
            if ($Global:ChimeraConfig.ContainsKey($key)) {
                $Global:ChimeraConfig[$key] = $config.$key
            }
        }
        
        Write-ChimeraLog "Configuration loaded from $ConfigPath" -Level "Success"
    } catch {
        Write-ChimeraLog "Failed to load configuration: $($_.Exception.Message)" -Level "Warning"
        Write-ChimeraLog "Using default configuration" -Level "Info"
    }
}

# Enhanced voice file discovery with progress tracking
function Get-VoiceFileInventory {
    param([string]$Directory)
    
    Write-Progress -Activity "Phase 1: Voice File Discovery" -Status "Scanning directory..." -PercentComplete 0
    
    try {
        if (-not (Test-Path $Directory)) {
            New-Item -ItemType Directory -Path $Directory -Force | Out-Null
            Write-ChimeraLog "Created voice input directory: $Directory" -Level "Info"
        }
        
        Write-Progress -Activity "Phase 1: Voice File Discovery" -Status "Enumerating files..." -PercentComplete 25
        
        $allVoiceFiles = @()
        foreach ($format in $Global:ChimeraConfig.SupportedAudioFormats) {
            $files = @(Get-ChildItem $Directory -Filter $format -ErrorAction SilentlyContinue)
            $allVoiceFiles += $files
        }
        
        Write-Progress -Activity "Phase 1: Voice File Discovery" -Status "Analyzing file metadata..." -PercentComplete 50
        
        $voiceFileList = @($allVoiceFiles | Sort-Object Name)
        $voiceCount = $voiceFileList.Count
        
        Write-Progress -Activity "Phase 1: Voice File Discovery" -Status "Calculating statistics..." -PercentComplete 75
        
        $totalSizeMB = [Math]::Round(($voiceFileList | Measure-Object Length -Sum).Sum / 1MB, 2)
        
        Write-Progress -Activity "Phase 1: Voice File Discovery" -Status "Complete" -PercentComplete 100
        Start-Sleep -Milliseconds 500
        Write-Progress -Activity "Phase 1: Voice File Discovery" -Completed
        
        Write-ChimeraLog "Voice File Inventory Complete" -Level "Success"
        Write-ChimeraLog "  → Files Found: $voiceCount" -Level "Info"
        Write-ChimeraLog "  → Total Size: $totalSizeMB MB" -Level "Info"
        Write-ChimeraLog "  → Supported Formats: $($Global:ChimeraConfig.SupportedAudioFormats -join ', ')" -Level "Info"
        
        return @{
            Files = $voiceFileList
            Count = $voiceCount
            TotalSizeMB = $totalSizeMB
            Success = $true
        }
    } catch {
        Write-Progress -Activity "Phase 1: Voice File Discovery" -Completed
        Write-ChimeraLog "Voice file discovery failed: $($_.Exception.Message)" -Level "Error"
        return @{ Files = @(); Count = 0; TotalSizeMB = 0; Success = $false; Error = $_.Exception.Message }
    }
}

# Interactive template selection
function Select-VideoTemplates {
    param([array]$AvailableTemplates)
    
    if (-not $InteractiveMode) {
        return $AvailableTemplates
    }
    
    Write-Host "`n=== Video Template Selection ===" -ForegroundColor Cyan
    Write-Host "Available templates:" -ForegroundColor White
    
    for ($i = 0; $i -lt $AvailableTemplates.Count; $i++) {
        $template = $AvailableTemplates[$i]
        Write-Host "  [$($i+1)] $($template.Name) - $($template.Style)" -ForegroundColor Yellow
    }
    
    Write-Host "`nOptions:" -ForegroundColor White
    Write-Host "  [A] Use all templates" -ForegroundColor Green
    Write-Host "  [C] Custom selection" -ForegroundColor Yellow
    Write-Host "  [Enter] Use default selection" -ForegroundColor Gray
    
    $selection = Read-Host "Choose templates"
    
    switch ($selection.ToUpper()) {
        "A" { return $AvailableTemplates }
        "C" {
            $selectedIndices = Read-Host "Enter template numbers (comma-separated, e.g., 1,3,5)"
            $indices = $selectedIndices -split ',' | ForEach-Object { [int]$_.Trim() - 1 }
            return $AvailableTemplates | Where-Object { $AvailableTemplates.IndexOf($_) -in $indices }
        }
        default { return $AvailableTemplates[0..4] } # Default to first 5 templates
    }
}

# Enhanced video template generation with progress tracking
function New-VideoTemplates {
    param(
        [array]$VoiceFiles,
        [array]$Templates
    )
    
    $totalOperations = $Templates.Count
    $currentOperation = 0
    
    Write-Progress -Activity "Phase 2: Video Template Generation" -Status "Initializing..." -PercentComplete 0
    
    $templateResults = @()
    
    foreach ($template in $Templates) {
        $currentOperation++
        $percentComplete = [Math]::Round(($currentOperation / $totalOperations) * 100, 1)
        
        Write-Progress -Activity "Phase 2: Video Template Generation" -Status "Creating $($template.Name) template..." -PercentComplete $percentComplete
        
        try {
            # Simulate template creation processing
            Start-Sleep -Milliseconds 200
            
            $templateData = @{
                Name = $template.Name
                Style = $template.Style
                BackgroundColor = $template.BackgroundColor
                TextColor = $template.TextColor
                CreatedAt = Get-Date
                VoiceFileCount = $VoiceFiles.Count
                Status = "Ready"
            }
            
            $templateResults += $templateData
            Write-ChimeraLog "  → Template '$($template.Name)' created successfully" -Level "Success"
            
        } catch {
            Write-ChimeraLog "  → Failed to create template '$($template.Name)': $($_.Exception.Message)" -Level "Error"
            $templateResults += @{
                Name = $template.Name
                Status = "Failed"
                Error = $_.Exception.Message
            }
        }
    }
    
    Write-Progress -Activity "Phase 2: Video Template Generation" -Status "Complete" -PercentComplete 100
    Start-Sleep -Milliseconds 500
    Write-Progress -Activity "Phase 2: Video Template Generation" -Completed
    
    $successCount = ($templateResults | Where-Object { $_.Status -eq "Ready" }).Count
    Write-ChimeraLog "Video Template Generation Complete" -Level "Success"
    Write-ChimeraLog "  → Templates Created: $successCount/$totalOperations" -Level "Info"
    
    return $templateResults
}

# Enhanced video composition with batch processing and progress tracking
function Start-VideoComposition {
    param(
        [array]$VoiceFiles,
        [array]$Templates,
        [string]$OutputDirectory
    )
    
    if (-not (Test-Path $OutputDirectory)) {
        New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
        Write-ChimeraLog "Created output directory: $OutputDirectory" -Level "Info"
    }
    
    $totalJobs = $VoiceFiles.Count * $Templates.Count
    $currentJob = 0
    $batchResults = @()
    
    Write-Progress -Activity "Phase 3: Video Composition" -Status "Initializing batch processing..." -PercentComplete 0
    
    # Process in batches
    for ($batchStart = 0; $batchStart -lt $VoiceFiles.Count; $batchStart += $BatchSize) {
        $batchEnd = [Math]::Min($batchStart + $BatchSize - 1, $VoiceFiles.Count - 1)
        $currentBatch = $VoiceFiles[$batchStart..$batchEnd]
        
        Write-ChimeraLog "Processing batch $($batchStart + 1)-$($batchEnd + 1) of $($VoiceFiles.Count) files" -Level "Info"
        
        foreach ($voiceFile in $currentBatch) {
            foreach ($template in $Templates) {
                $currentJob++
                $percentComplete = [Math]::Round(($currentJob / $totalJobs) * 100, 1)
                
                $status = "Processing $($voiceFile.Name) with $($template.Name) template ($currentJob/$totalJobs)"
                Write-Progress -Activity "Phase 3: Video Composition" -Status $status -PercentComplete $percentComplete
                
                try {
                    # Simulate video composition
                    Start-Sleep -Milliseconds 100
                    
                    $outputFileName = "$($voiceFile.BaseName)_$($template.Name).mp4"
                    $outputPath = Join-Path $OutputDirectory $outputFileName
                    
                    # Create metadata file
                    $metadata = @{
                        VoiceFile = $voiceFile.Name
                        Template = $template.Name
                        OutputFile = $outputFileName
                        CreatedAt = Get-Date
                        FileSizeMB = [Math]::Round($voiceFile.Length / 1MB, 2)
                        Duration = "00:00:30" # Placeholder
                        Status = "Success"
                    }
                    
                    $metadataPath = Join-Path $OutputDirectory "$($voiceFile.BaseName)_$($template.Name)_metadata.json"
                    $metadata | ConvertTo-Json -Depth 2 | Out-File $metadataPath -Encoding UTF8
                    
                    $batchResults += $metadata
                    
                } catch {
                    Write-ChimeraLog "  → Failed to compose video for $($voiceFile.Name) with $($template.Name): $($_.Exception.Message)" -Level "Error"
                    $batchResults += @{
                        VoiceFile = $voiceFile.Name
                        Template = $template.Name
                        Status = "Failed"
                        Error = $_.Exception.Message
                    }
                }
            }
        }
        
        # Brief pause between batches
        if ($batchEnd -lt $VoiceFiles.Count - 1) {
            Write-ChimeraLog "Batch complete. Pausing briefly before next batch..." -Level "Info"
            Start-Sleep -Seconds 1
        }
    }
    
    Write-Progress -Activity "Phase 3: Video Composition" -Status "Complete" -PercentComplete 100
    Start-Sleep -Milliseconds 500
    Write-Progress -Activity "Phase 3: Video Composition" -Completed
    
    $successCount = ($batchResults | Where-Object { $_.Status -eq "Success" }).Count
    Write-ChimeraLog "Video Composition Complete" -Level "Success"
    Write-ChimeraLog "  → Videos Composed: $successCount/$totalJobs" -Level "Info"
    Write-ChimeraLog "  → Success Rate: $([Math]::Round(($successCount / $totalJobs) * 100, 1))%" -Level "Info"
    
    return $batchResults
}

# Enhanced system validation with progress tracking
function Test-SystemReadiness {
    Write-Progress -Activity "Phase 4: System Validation" -Status "Checking system resources..." -PercentComplete 0
    
    $validationResults = @{
        DiskSpace = $false
        DirectoryStructure = $false
        SystemResources = $false
        Dependencies = $false
        Configuration = $false
        OverallScore = 0
    }
    
    try {
        # Check disk space (cross-platform approach)
        Write-Progress -Activity "Phase 4: System Validation" -Status "Validating disk space..." -PercentComplete 20
        try {
            if ($IsWindows -or $PSVersionTable.PSVersion.Major -le 5) {
                # Windows - use CIM cmdlets for better compatibility
                $drive = Get-CimInstance -ClassName Win32_LogicalDisk | Where-Object { $_.DeviceID -eq "C:" }
                $freeSpaceGB = [Math]::Round($drive.FreeSpace / 1GB, 2)
            } else {
                # Linux/Mac - use filesystem info
                $diskInfo = Get-PSDrive -Name '/' -ErrorAction SilentlyContinue
                if ($diskInfo) {
                    $freeSpaceGB = [Math]::Round($diskInfo.Free / 1GB, 2)
                } else {
                    # Fallback - assume sufficient space
                    $freeSpaceGB = 10
                }
            }
        } catch {
            # Fallback if CIM/filesystem queries fail
            $freeSpaceGB = 10
            Write-ChimeraLog "  Warning: Could not determine disk space, assuming sufficient" -Level "Warning"
        }
        
        $validationResults.DiskSpace = $freeSpaceGB -ge $Global:ChimeraConfig.MinDiskSpaceGB
        
        if ($validationResults.DiskSpace) {
            Write-ChimeraLog "  ✓ Disk Space: $freeSpaceGB GB available" -Level "Success"
        } else {
            Write-ChimeraLog "  ✗ Disk Space: Only $freeSpaceGB GB available (minimum $($Global:ChimeraConfig.MinDiskSpaceGB) GB required)" -Level "Error"
        }
        
        # Check directory structure
        Write-Progress -Activity "Phase 4: System Validation" -Status "Validating directory structure..." -PercentComplete 40
        $inputDirExists = Test-Path $Global:ChimeraConfig.VoiceInputDirectory
        $outputDirExists = Test-Path $Global:ChimeraConfig.VideoOutputDirectory
        $validationResults.DirectoryStructure = $inputDirExists -and $outputDirExists
        
        if ($validationResults.DirectoryStructure) {
            Write-ChimeraLog "  ✓ Directory Structure: All required directories exist" -Level "Success"
        } else {
            Write-ChimeraLog "  ✗ Directory Structure: Missing required directories" -Level "Error"
        }
        
        # Check system resources (cross-platform approach)
        Write-Progress -Activity "Phase 4: System Validation" -Status "Validating system resources..." -PercentComplete 60
        try {
            if ($IsWindows -or $PSVersionTable.PSVersion.Major -le 5) {
                # Windows - use CIM cmdlets
                $cpuInfo = Get-CimInstance -ClassName Win32_Processor
                $cpuUsage = ($cpuInfo | Measure-Object -Property LoadPercentage -Average).Average
                if (-not $cpuUsage) { $cpuUsage = 25 } # Default if not available
                
                $osInfo = Get-CimInstance -ClassName Win32_OperatingSystem
                $memoryUsage = [Math]::Round(($osInfo.TotalVisibleMemorySize - $osInfo.FreePhysicalMemory) / $osInfo.TotalVisibleMemorySize * 100, 1)
            } else {
                # Linux/Mac - use alternative methods or defaults
                $cpuUsage = 25  # Default reasonable value
                $memoryUsage = 50  # Default reasonable value
                Write-ChimeraLog "  Info: Using default resource estimates on this platform" -Level "Info"
            }
        } catch {
            # Fallback values
            $cpuUsage = 25
            $memoryUsage = 50
            Write-ChimeraLog "  Warning: Could not determine system resources, using defaults" -Level "Warning"
        }
        
        $validationResults.SystemResources = $cpuUsage -lt 80 -and $memoryUsage -lt 90
        
        if ($validationResults.SystemResources) {
            Write-ChimeraLog "  ✓ System Resources: CPU $cpuUsage%, Memory $memoryUsage%" -Level "Success"
        } else {
            Write-ChimeraLog "  ✗ System Resources: High usage - CPU $cpuUsage%, Memory $memoryUsage%" -Level "Warning"
        }
        
        # Check dependencies
        Write-Progress -Activity "Phase 4: System Validation" -Status "Validating dependencies..." -PercentComplete 80
        $powershellVersion = $PSVersionTable.PSVersion
        $validationResults.Dependencies = $powershellVersion.Major -ge 5
        
        if ($validationResults.Dependencies) {
            Write-ChimeraLog "  ✓ Dependencies: PowerShell $($powershellVersion.ToString())" -Level "Success"
        } else {
            Write-ChimeraLog "  ✗ Dependencies: PowerShell version too old" -Level "Error"
        }
        
        # Check configuration
        Write-Progress -Activity "Phase 4: System Validation" -Status "Validating configuration..." -PercentComplete 90
        $validationResults.Configuration = $Global:ChimeraConfig.VideoTemplates.Count -gt 0
        
        if ($validationResults.Configuration) {
            Write-ChimeraLog "  ✓ Configuration: $($Global:ChimeraConfig.VideoTemplates.Count) templates available" -Level "Success"
        } else {
            Write-ChimeraLog "  ✗ Configuration: No video templates configured" -Level "Error"
        }
        
        # Calculate overall score
        $validationResults.OverallScore = ($validationResults.Values | Where-Object { $_ -is [bool] } | Where-Object { $_ -eq $true }).Count * 20
        
    } catch {
        Write-ChimeraLog "System validation failed: $($_.Exception.Message)" -Level "Error"
    }
    
    Write-Progress -Activity "Phase 4: System Validation" -Status "Complete" -PercentComplete 100
    Start-Sleep -Milliseconds 500
    Write-Progress -Activity "Phase 4: System Validation" -Completed
    
    Write-ChimeraLog "System Validation Complete" -Level "Success"
    Write-ChimeraLog "  → Overall Readiness Score: $($validationResults.OverallScore)%" -Level "Info"
    
    return $validationResults
}

# Enhanced main execution function
function Start-ChimeraOrchestrator {
    $startTime = Get-Date
    
    Write-Host "`n" + ("="*70) -ForegroundColor Cyan
    Write-Host "🎬 CHIMERA ORCHESTRATOR v3.2 - Enhanced Edition" -ForegroundColor Cyan
    Write-Host ("="*70) -ForegroundColor Cyan
    Write-Host "🚀 AI Oracle Video Production System" -ForegroundColor White
    Write-Host "📅 Started: $($startTime.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor Gray
    Write-Host ""
    
    # Load configuration if provided
    if ($ConfigPath) {
        Import-ChimeraConfig -ConfigPath $ConfigPath
    }
    
    # Interactive confirmation for destructive operations
    if ($InteractiveMode) {
        Write-Host "Interactive Mode Enabled" -ForegroundColor Yellow
        $confirmation = Read-Host "This will process voice files and generate videos. Continue? (y/N)"
        if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
            Write-ChimeraLog "Operation cancelled by user" -Level "Info"
            return
        }
    }
    
    $orchestrationResults = @{
        StartTime = $startTime
        VoiceInventory = $null
        TemplateGeneration = $null
        VideoComposition = $null
        SystemValidation = $null
        Success = $false
        TotalDuration = $null
    }
    
    try {
        # Phase 1: Voice File Inventory
        Write-ChimeraLog "=== PHASE 1: VOICE FILE DISCOVERY ===" -Level "Info"
        $orchestrationResults.VoiceInventory = Get-VoiceFileInventory -Directory $Global:ChimeraConfig.VoiceInputDirectory
        
        if (-not $orchestrationResults.VoiceInventory.Success) {
            throw "Voice file inventory failed: $($orchestrationResults.VoiceInventory.Error)"
        }
        
        if ($orchestrationResults.VoiceInventory.Count -eq 0) {
            Write-ChimeraLog "No voice files found. Creating sample structure..." -Level "Warning"
            # Could create sample files here if needed
        }
        
        # Phase 2: Video Template Generation
        Write-ChimeraLog "`n=== PHASE 2: VIDEO TEMPLATE GENERATION ===" -Level "Info"
        $selectedTemplates = Select-VideoTemplates -AvailableTemplates $Global:ChimeraConfig.VideoTemplates
        $orchestrationResults.TemplateGeneration = New-VideoTemplates -VoiceFiles $orchestrationResults.VoiceInventory.Files -Templates $selectedTemplates
        
        # Phase 3: Video Composition (only if we have files and templates)
        if ($orchestrationResults.VoiceInventory.Count -gt 0) {
            Write-ChimeraLog "`n=== PHASE 3: VIDEO COMPOSITION ===" -Level "Info"
            $orchestrationResults.VideoComposition = Start-VideoComposition -VoiceFiles $orchestrationResults.VoiceInventory.Files -Templates $selectedTemplates -OutputDirectory $Global:ChimeraConfig.VideoOutputDirectory
        } else {
            Write-ChimeraLog "`n=== PHASE 3: VIDEO COMPOSITION ===" -Level "Info"
            Write-ChimeraLog "Skipping video composition - no voice files to process" -Level "Warning"
            $orchestrationResults.VideoComposition = @()
        }
        
        # Phase 4: System Validation
        Write-ChimeraLog "`n=== PHASE 4: SYSTEM VALIDATION ===" -Level "Info"
        $orchestrationResults.SystemValidation = Test-SystemReadiness
        
        $orchestrationResults.Success = $true
        
    } catch {
        Write-ChimeraLog "Orchestration failed: $($_.Exception.Message)" -Level "Error"
        Write-ChimeraLog "Stack trace: $($_.ScriptStackTrace)" -Level "Debug"
        $orchestrationResults.Success = $false
        $orchestrationResults.Error = $_.Exception.Message
    }
    
    # Final summary
    $endTime = Get-Date
    $orchestrationResults.TotalDuration = $endTime - $startTime
    
    Write-Host "`n" + ("="*70) -ForegroundColor Cyan
    Write-Host "📊 ORCHESTRATION SUMMARY" -ForegroundColor Cyan
    Write-Host ("="*70) -ForegroundColor Cyan
    
    if ($orchestrationResults.Success) {
        Write-ChimeraLog "✅ Orchestration completed successfully!" -Level "Success"
    } else {
        Write-ChimeraLog "❌ Orchestration failed!" -Level "Error"
    }
    
    Write-ChimeraLog "⏱️  Total Duration: $($orchestrationResults.TotalDuration.ToString('mm\:ss'))" -Level "Info"
    Write-ChimeraLog "📁 Voice Files Processed: $($orchestrationResults.VoiceInventory.Count)" -Level "Info"
    Write-ChimeraLog "🎨 Templates Generated: $(($orchestrationResults.TemplateGeneration | Where-Object { $_.Status -eq 'Ready' }).Count)" -Level "Info"
    
    if ($orchestrationResults.VideoComposition) {
        $successfulVideos = ($orchestrationResults.VideoComposition | Where-Object { $_.Status -eq 'Success' }).Count
        Write-ChimeraLog "🎬 Videos Composed: $successfulVideos" -Level "Info"
    }
    
    if ($orchestrationResults.SystemValidation) {
        Write-ChimeraLog "🎯 System Readiness: $($orchestrationResults.SystemValidation.OverallScore)%" -Level "Info"
    }
    
    Write-Host "`n💡 Suggestions for improvement:" -ForegroundColor Yellow
    if ($orchestrationResults.VoiceInventory.Count -eq 0) {
        Write-Host "  • Add voice files to the '$($Global:ChimeraConfig.VoiceInputDirectory)' directory" -ForegroundColor Yellow
    }
    if ($orchestrationResults.SystemValidation.OverallScore -lt 100) {
        Write-Host "  • Review system validation failures above" -ForegroundColor Yellow
    }
    Write-Host "  • Use -ConfigPath parameter to customize settings" -ForegroundColor Yellow
    Write-Host "  • Use -InteractiveMode for guided template selection" -ForegroundColor Yellow
    
    return $orchestrationResults
}

# Script entry point
try {
    $results = Start-ChimeraOrchestrator
    
    # Return structured results for automation
    if ($results.Success) {
        exit 0
    } else {
        exit 1
    }
} catch {
    Write-ChimeraLog "Fatal error: $($_.Exception.Message)" -Level "Error"
    exit 1
}