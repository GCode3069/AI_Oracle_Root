# PowerShell Script to Locate Files Containing "scarify" or "ai oracle" API Keys

param (
    [string]$SearchRoot = "C:\"  # Root directory to start the search, default is C:
)

$ErrorActionPreference = "Stop"

Write-Host "🔍 Searching for files containing 'scarify' or 'ai oracle' API keys..." -ForegroundColor Cyan

# Define search patterns for API keys
$searchPatterns = @("scarify", "ai oracle")

# Create a log file to store results
$LogFile = "$env:USERPROFILE\Desktop\API_Key_Search_Log.txt"
if (Test-Path $LogFile) {
    Remove-Item -Path $LogFile -Force
}
New-Item -ItemType File -Path $LogFile -Force | Out-Null
Write-Host "📄 Log file created at: $LogFile" -ForegroundColor Green

# Perform search
foreach ($pattern in $searchPatterns) {
    Write-Host "Searching for pattern: $pattern" -ForegroundColor Yellow
    $results = Get-ChildItem -Path $SearchRoot -Recurse -ErrorAction SilentlyContinue | Where-Object {
        $_.Name -match $pattern -or Select-String -Path $_.FullName -Pattern $pattern -ErrorAction SilentlyContinue
    }
    foreach ($result in $results) {
        $logEntry = "[FOUND] Pattern: $pattern | File: $($result.FullName)"
        Add-Content -Path $LogFile -Value $logEntry
        Write-Host $logEntry -ForegroundColor Green
    }
}

Write-Host "✅ Search completed. Check log file for details." -ForegroundColor Cyan