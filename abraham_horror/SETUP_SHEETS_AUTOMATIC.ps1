# ONE-CLICK GOOGLE SHEETS SETUP
# This script will help you set up service account authentication

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GOOGLE SHEETS AUTOMATIC SETUP" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$CREDS_DIR = "F:\AI_Oracle_Root\scarify\config\credentials\google"
$CREDS_FILE = "$CREDS_DIR\service_account.json"
$SHEET_ID = "1jvWP95U0ksaHw97PrPZsrh6ZVllviJJof7kQ2dV0ka0"
$SERVICE_ACCOUNTS = @(
    "ai-oracle-automation@fourth-memento-454609-p5.iam.gserviceaccount.com",
    "ssml-automation@fourth-memento-454609-p5.iam.gserviceaccount.com"
)

# Create directory if it doesn't exist
if (-not (Test-Path $CREDS_DIR)) {
    New-Item -ItemType Directory -Path $CREDS_DIR -Force | Out-Null
    Write-Host "[OK] Created credentials directory" -ForegroundColor Green
}

# Check if credentials already exist
if (Test-Path $CREDS_FILE) {
    Write-Host "[OK] Service account JSON already exists!" -ForegroundColor Green
    Write-Host "    Location: $CREDS_FILE" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Do you want to use the existing file? (Y/N)"
    if ($choice -eq "Y" -or $choice -eq "y") {
        Write-Host "[INFO] Using existing credentials" -ForegroundColor Cyan
        Write-Host ""
        
        # Read service account email from JSON
        try {
            $json = Get-Content $CREDS_FILE | ConvertFrom-Json
            $service_email = $json.client_email
            Write-Host "[NEXT STEP] Share your Google Sheet with this email:" -ForegroundColor Yellow
            Write-Host "    $service_email" -ForegroundColor White
            Write-Host ""
            Write-Host "    Sheet URL: https://docs.google.com/spreadsheets/d/$SHEET_ID/edit?usp=sharing" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "    1. Click 'Share' button on the sheet" -ForegroundColor White
            Write-Host "    2. Paste: $service_email" -ForegroundColor White
            Write-Host "    3. Set permission to 'Editor'" -ForegroundColor White
            Write-Host "    4. Click 'Send'" -ForegroundColor White
            Write-Host ""
            $ready = Read-Host "Press Enter after you've shared the sheet"
            
            # Test connection
            Write-Host ""
            Write-Host "[TESTING] Connecting to Google Sheets..." -ForegroundColor Cyan
            python "$PSScriptRoot\INIT_SHEETS_TEST.py"
            exit
        } catch {
            Write-Host "[ERROR] Could not read JSON file" -ForegroundColor Red
        }
    }
}

Write-Host "[STEP 1] Download Service Account Key" -ForegroundColor Yellow
Write-Host ""
Write-Host "Opening Google Cloud Console..." -ForegroundColor Cyan
Write-Host ""
Write-Host "1. The browser will open to Service Accounts page" -ForegroundColor White
Write-Host "2. Click on one of these service accounts:" -ForegroundColor White
foreach ($email in $SERVICE_ACCOUNTS) {
    Write-Host "   - $email" -ForegroundColor Cyan
}
Write-Host ""
Write-Host "3. Click 'KEYS' tab" -ForegroundColor White
Write-Host "4. Click 'ADD KEY' -> 'Create new key'" -ForegroundColor White
Write-Host "5. Choose 'JSON' format" -ForegroundColor White
Write-Host "6. Click 'CREATE' - it will download a JSON file" -ForegroundColor White
Write-Host ""

$openConsole = Read-Host "Open Google Cloud Console now? (Y/N)"
if ($openConsole -eq "Y" -or $openConsole -eq "y") {
    Start-Process "https://console.cloud.google.com/iam-admin/serviceaccounts?project=fourth-memento-454609-p5"
}

Write-Host ""
Write-Host "[STEP 2] Move JSON File" -ForegroundColor Yellow
Write-Host ""
Write-Host "After the JSON file downloads:" -ForegroundColor White
Write-Host ""
Write-Host "The file will be in your Downloads folder with a name like:" -ForegroundColor White
Write-Host "   fourth-memento-454609-p5-xxxxx.json" -ForegroundColor Cyan
Write-Host ""

# Wait for user to download
Write-Host "Press Enter after you've downloaded the JSON file..." -ForegroundColor Yellow
Read-Host

# Find JSON file in Downloads
$downloadsPath = "$env:USERPROFILE\Downloads"
$jsonFiles = Get-ChildItem -Path $downloadsPath -Filter "*.json" | Where-Object {
    $_.Name -match "fourth-memento|service|key" -or 
    $_.LastWriteTime -gt (Get-Date).AddMinutes(-5)
} | Sort-Object LastWriteTime -Descending

if ($jsonFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "Found JSON files in Downloads:" -ForegroundColor Green
    for ($i = 0; $i -lt [Math]::Min($jsonFiles.Count, 5); $i++) {
        Write-Host "   [$i] $($jsonFiles[$i].Name) (Modified: $($jsonFiles[$i].LastWriteTime))" -ForegroundColor White
    }
    Write-Host ""
    
    $selected = Read-Host "Enter number of the service account JSON file (or press Enter for most recent)"
    if ([string]::IsNullOrWhiteSpace($selected)) {
        $selectedFile = $jsonFiles[0]
    } else {
        $selectedFile = $jsonFiles[[int]$selected]
    }
    
    Write-Host ""
    Write-Host "[COPYING] Moving file to credentials directory..." -ForegroundColor Cyan
    Copy-Item $selectedFile.FullName -Destination $CREDS_FILE -Force
    Write-Host "[OK] Saved to: $CREDS_FILE" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[MANUAL] No JSON file found automatically" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please manually copy your service account JSON file to:" -ForegroundColor White
    Write-Host "    $CREDS_FILE" -ForegroundColor Cyan
    Write-Host ""
    $manual = Read-Host "Press Enter after you've copied the file"
}

# Verify file exists
if (-not (Test-Path $CREDS_FILE)) {
    Write-Host "[ERROR] Credentials file not found at: $CREDS_FILE" -ForegroundColor Red
    Write-Host "Please copy the JSON file manually and run this script again." -ForegroundColor Yellow
    exit 1
}

# Read service account email
try {
    $json = Get-Content $CREDS_FILE | ConvertFrom-Json
    $service_email = $json.client_email
    Write-Host ""
    Write-Host "[OK] Credentials file loaded!" -ForegroundColor Green
    Write-Host "    Service Account: $service_email" -ForegroundColor White
    Write-Host ""
} catch {
    Write-Host "[ERROR] Invalid JSON file" -ForegroundColor Red
    exit 1
}

# Step 3: Share Sheet
Write-Host "[STEP 3] Share Google Sheet" -ForegroundColor Yellow
Write-Host ""
Write-Host "You need to share your Google Sheet with the service account:" -ForegroundColor White
Write-Host ""
Write-Host "    Email: $service_email" -ForegroundColor Cyan
Write-Host ""
Write-Host "Opening Google Sheet..." -ForegroundColor Cyan
Start-Process "https://docs.google.com/spreadsheets/d/$SHEET_ID/edit?usp=sharing"
Write-Host ""
Write-Host "Instructions:" -ForegroundColor Yellow
Write-Host "  1. Click 'Share' button (top right)" -ForegroundColor White
Write-Host "  2. Paste this email: $service_email" -ForegroundColor Cyan
Write-Host "  3. Set permission to 'Editor'" -ForegroundColor White
Write-Host "  4. Click 'Send'" -ForegroundColor White
Write-Host ""
$ready = Read-Host "Press Enter after you've shared the sheet"

# Step 4: Test
Write-Host ""
Write-Host "[STEP 4] Testing Connection..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Writing headers and sample rows to your sheet..." -ForegroundColor Cyan
Write-Host ""

python "$PSScriptRoot\INIT_SHEETS_TEST.py"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "SUCCESS! Google Sheets is now connected!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Check your sheet:" -ForegroundColor White
    Write-Host "https://docs.google.com/spreadsheets/d/$SHEET_ID/edit?usp=sharing" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You should see:" -ForegroundColor White
    Write-Host "  - Headers in row 1: headline | prompt | tags" -ForegroundColor White
    Write-Host "  - Sample rows below with test data" -ForegroundColor White
    Write-Host ""
    Write-Host "Your video generators will now read from this sheet!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERROR] Connection test failed" -ForegroundColor Red
    Write-Host "Make sure:" -ForegroundColor Yellow
    Write-Host "  1. Service account JSON is in the right place" -ForegroundColor White
    Write-Host "  2. Sheet is shared with: $service_email" -ForegroundColor White
    Write-Host "  3. Permission is set to 'Editor'" -ForegroundColor White
}

Write-Host ""

