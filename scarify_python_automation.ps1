# SCARIFY PowerShell Template: Automate Python Script Creation and Execution
# Author: GCode3069 | AI Oracle Series

param (
    [string]$PyScriptName = "scarify_temp.py",
    [string]$PyCode = @"
import sys
print('Hello from SCARIFY automated Python!')
sys.exit(0)
"@
)

# Define the script path (default: current directory)
$PyScriptPath = Join-Path (Get-Location) $PyScriptName

# Write Python code to file
$PyCode | Set-Content -Path $PyScriptPath -Encoding UTF8
Write-Host "✅ Python script written to $PyScriptPath" -ForegroundColor Green

# Run the Python script and capture output
Write-Host "🚀 Running Python script..." -ForegroundColor Cyan
try {
    $result = & python $PyScriptPath 2>&1
    Write-Host $result
    Write-Host "✅ Python script finished." -ForegroundColor Green
} catch {
    Write-Host "❌ Error running Python script: $_" -ForegroundColor Red
}

# Optionally delete the script after run (uncomment if desired)
# Remove-Item -Path $PyScriptPath -Force