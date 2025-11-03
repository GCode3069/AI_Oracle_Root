# Copy Google service account JSON to the correct location
# Run: powershell -ExecutionPolicy Bypass -File .\COPY_SA_JSON.ps1

param(
    [switch]$Test
)

$TargetDir  = "F:\AI_Oracle_Root\scarify\config\credentials\google"
$TargetFile = Join-Path $TargetDir "service_account.json"

# Ensure target directory
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

# Open file picker
Add-Type -AssemblyName System.Windows.Forms | Out-Null
$dlg = New-Object System.Windows.Forms.OpenFileDialog
$dlg.Title = "Select Google Service Account JSON"
$dlg.InitialDirectory = Join-Path $env:USERPROFILE "Downloads"
$dlg.Filter = "JSON files (*.json)|*.json|All files (*.*)|*.*"
$dlg.Multiselect = $false

$src = $null
if ($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $src = $dlg.FileName
} else {
    Write-Host "[CANCELLED] No file selected" -ForegroundColor Yellow
    exit 1
}

# Copy to target
Copy-Item -Path $src -Destination $TargetFile -Force
Write-Host "[OK] Copied to: $TargetFile" -ForegroundColor Green

# Show service account email for sharing step
try {
    $json = Get-Content $TargetFile | ConvertFrom-Json
    if ($json.client_email) {
        Write-Host "[INFO] Service Account Email:" -ForegroundColor Cyan
        Write-Host "  $($json.client_email)" -ForegroundColor White
    }
} catch {}

# Optional test
if ($Test.IsPresent) {
    Write-Host "[TEST] Writing headers/sample rows to your sheet..." -ForegroundColor Cyan
    try {
        Set-Location $PSScriptRoot
        python INIT_SHEETS_TEST.py
    } catch {
        Write-Host "[WARN] Test run failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}



