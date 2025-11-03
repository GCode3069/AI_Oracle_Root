# SCARIFY Recovery Script

# Variables
$baseDir = "scarify"
$analysisDir = "${baseDir}/analysis"
$exportDir = "${baseDir}/export"

# Function for logging
function Log {
    param([string]$message)
    Write-Host "[INFO] $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - $message"
}

# Create directories
try {
    Log "Creating missing directories..."
    if (-not (Test-Path $analysisDir)) {
        New-Item -ItemType Directory -Path $analysisDir -Force
        Log "Created directory: $analysisDir"
    } else {
        Log "Directory already exists: $analysisDir"
    }

    if (-not (Test-Path $exportDir)) {
        New-Item -ItemType Directory -Path $exportDir -Force
        Log "Created directory: $exportDir"
    } else {
        Log "Directory already exists: $exportDir"
    }
} catch {
    Write-Host "[ERROR] Failed to create directories: $_"
}

# Create missing Python files
$files = @(
    @{Path="scarify/utils/complete_pipeline.py"; Content=""},
    @{Path="scarify/core/scanner.py"; Content=""},
    @{Path="scarify/utils/report_generator.py"; Content=""},
    @{Path="test_scarify_production.py"; Content=""}
)

foreach ($file in $files) {
    try {
        $filePath = $file.Path
        if (-not (Test-Path $filePath)) {
            New-Item -ItemType File -Path $filePath -Force
            Log "Created file: $filePath"
        } else {
            Log "File already exists: $filePath"
        }
    } catch {
        Write-Host "[ERROR] Failed to create file: $filePath - $_"
    }
}