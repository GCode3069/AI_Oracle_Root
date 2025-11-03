# QUICK SETUP - Run this AFTER you download the JSON file
# Usage: .\QUICK_SETUP_SHEETS.ps1 "path\to\downloaded.json"

param(
    [Parameter(Mandatory=$false)]
    [string]$JsonPath = ""
)

$CREDS_DIR = "F:\AI_Oracle_Root\scarify\config\credentials\google"
$CREDS_FILE = "$CREDS_DIR\service_account.json"
$SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"

# Create directory
if (-not (Test-Path $CREDS_DIR)) {
    New-Item -ItemType Directory -Path $CREDS_DIR -Force | Out-Null
}

# Find JSON file if not provided
if ([string]::IsNullOrWhiteSpace($JsonPath)) {
    $downloads = Get-ChildItem "$env:USERPROFILE\Downloads\*.json" -ErrorAction SilentlyContinue | 
        Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(2) } |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if ($downloads) {
        $JsonPath = $downloads.FullName
        Write-Host "[FOUND] Using: $($downloads.Name)" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] No recent JSON file found in Downloads" -ForegroundColor Red
        Write-Host ""
        Write-Host "Usage:" -ForegroundColor Yellow
        Write-Host "  .\QUICK_SETUP_SHEETS.ps1 `"C:\Users\YourName\Downloads\fourth-memento-454609-p5-xxxxx.json`"" -ForegroundColor White
        Write-Host ""
        Write-Host "Or download the JSON file, then run this script again." -ForegroundColor Cyan
        exit 1
    }
}

# Copy JSON file
if (Test-Path $JsonPath) {
    Copy-Item $JsonPath -Destination $CREDS_FILE -Force
    Write-Host "[OK] Credentials saved to: $CREDS_FILE" -ForegroundColor Green
    
    # Read service account email
    try {
        $json = Get-Content $CREDS_FILE | ConvertFrom-Json
        $service_email = $json.client_email
        Write-Host "[OK] Service Account: $service_email" -ForegroundColor Green
        Write-Host ""
        
        # Open sheet for sharing
        Write-Host "[NEXT] Share your Google Sheet with this email:" -ForegroundColor Yellow
        Write-Host "  $service_email" -ForegroundColor Cyan
        Write-Host ""
        Start-Process "https://docs.google.com/spreadsheets/d/$SHEET_ID/edit?usp=sharing"
        Write-Host "Sheet opened in browser. Click 'Share' and add the email above as 'Editor'." -ForegroundColor White
        Write-Host ""
        $ready = Read-Host "Press Enter AFTER you've shared the sheet"
        
        # Test connection
        Write-Host ""
        Write-Host "[TESTING] Writing to your sheet..." -ForegroundColor Cyan
        Set-Location $PSScriptRoot
        python INIT_SHEETS_TEST.py
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "========================================" -ForegroundColor Green
            Write-Host "SUCCESS! Check your sheet:" -ForegroundColor Green
            Write-Host "https://docs.google.com/spreadsheets/d/$SHEET_ID/edit?usp=sharing" -ForegroundColor Cyan
            Write-Host "========================================" -ForegroundColor Green
        }
    } catch {
        Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "[ERROR] File not found: $JsonPath" -ForegroundColor Red
}

