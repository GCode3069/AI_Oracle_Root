# Refined PowerShell Script to Execute Python Script Without Exiting PowerShell
param (
    [string]$PythonPath = "python",  # Path to Python executable
    [string]$ScriptPath = "F:\AI_Oracle_Root\scarify\multi_platform_phantom.py",  # Path to Python script
    [string]$LogFile = "F:\AI_Oracle_Root\scarify\phantom_upload.log"  # Path to log file
)

Write-Host "🚀 Starting Multi-Platform Phantom Uploader..." -ForegroundColor Cyan

# Check if Python is installed
if (-not (Get-Command $PythonPath -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python executable not found. Please install Python or check your path." -ForegroundColor Red
    return
}

# Check if the Python script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "❌ Python script not found at $ScriptPath. Please verify the path." -ForegroundColor Red
    return
}

# Execute the Python script and log output
try {
    & $PythonPath $ScriptPath *>&1 | Tee-Object -FilePath $LogFile
    Write-Host "✅ Execution complete. Log file saved at $LogFile" -ForegroundColor Green
} catch {
    # Log the error without terminating the PowerShell session
    $ErrorMessage = $_.Exception.Message
    Write-Host "❌ Error during execution: $ErrorMessage" -ForegroundColor Red
    Add-Content -Path $LogFile -Value "Error: $ErrorMessage"
}

Write-Host "💡 If the issue persists, check the log file for details: $LogFile" -ForegroundColor Yellow