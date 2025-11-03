# =========================================
# ??  SCARIFY: Save & Resume PowerShell Session
# =========================================
# Automatically captures session state on exit
# and enables one-click restore later.

# --- CONFIGURATION ---
$sessionDir = "F:\AI_Oracle_Root\scarify\session_state"
if (!(Test-Path $sessionDir)) { New-Item -ItemType Directory -Path $sessionDir | Out-Null }

# --- CAPTURE ENVIRONMENT ---
$lastDir = Get-Location
$history = Get-History
$variables = Get-Variable | Where-Object { $_.Name -notmatch '^(PWD|host|error|?)$' }

# --- SAVE STATE ---
$lastDir.Path | Set-Content "$sessionDir\last_dir.txt"
$history | Export-Clixml "$sessionDir\command_history.xml"
$variables | Export-Clixml "$sessionDir\variables.xml"

# --- LOGGING ---
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
"Session saved at $timestamp from $lastDir" | Out-File "$sessionDir\session_log.txt" -Append

Write-Host "`n?? SCARIFY session saved successfully at $timestamp" -ForegroundColor Green
