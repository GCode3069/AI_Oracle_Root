<#
.SYNOPSIS
MasterLaunch.ps1 - Unified end-to-end orchestrator for Oracle Horror Production System.

.DESCRIPTION
Runs the full pipeline: dependency checks, content generation (MasterControl.ps1),
picks the produced video, and deploys it via Deploy_Content.ps1.
Provides robust logging, retries, timestamps, and optional cleanup.

USAGE

# Full run: build + deploy

.\MasterLaunch.ps1 -Mode full -Campaign awakening -Deploy

# Build only (no deploy)

.\MasterLaunch.ps1 -Mode full -Campaign awakening -Deploy:$false

# Skip installer steps (useful for CI or already-provisioned systems)

.\MasterLaunch.ps1 -Mode full -Campaign awakening -SkipInstall

PARAMETERS
-Mode        : shorts | full | viral
-Campaign    : awakening | memory_merchants | digital_possession
-Count       : Number of videos to generate (default 1)
-Deploy      : Switch to run Deploy_Content.ps1 after successful build
-Force       : Force rebuild / overwrite outputs
-SkipInstall : Skip dependency installation steps
-Cleanup     : Remove temp artifacts after successful run
#>

param(
[Parameter(Mandatory=$true)][ValidateSet("shorts","full","viral")][string]$Mode,
[Parameter(Mandatory=$true)][ValidateSet("awakening","memory_merchants","digital_possession")][string]$Campaign,
[int]$Count = 1,
[switch]$Deploy = $true,
[switch]$Force,
[switch]$SkipInstall,
[switch]$Cleanup
)

# -------------------------
# Environment / Paths
# -------------------------

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path -LiteralPath ".").Path
$Timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$RunFolder = Join-Path $RepoRoot "Output\Runs\$($Campaign)_$($Timestamp)"
$LogPath = Join-Path $RunFolder "masterlaunch_$($Timestamp).log"
$MasterControl = Join-Path $RepoRoot "MasterControl.ps1"
$DeployScript = Join-Path $RepoRoot "Deploy_Content.ps1"

# Ensure run folder exists
New-Item -ItemType Directory -Force -Path $RunFolder | Out-Null

# -------------------------
# Logging helper
# -------------------------

function Write-RunLog {
param([string]$msg, [string]$level = "INFO")
$ts = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
$line = "[$ts][$level] $msg"
Write-Host $line
Add-Content -Path $LogPath -Value $line
}

# Start transcript (captures console + verbose output)
try {
Start-Transcript -Path $LogPath -Append -ErrorAction SilentlyContinue
} catch {
Write-RunLog "Warning: Could not start transcript: $_" "WARN"
}

Write-RunLog "MASTERLAUNCH START: Mode=$Mode Campaign=$Campaign Count=$Count Force=$Force SkipInstall=$SkipInstall Cleanup=$Cleanup"

# -------------------------
# Basic checks
# -------------------------

if (-not (Test-Path $MasterControl)) {
Write-RunLog "MasterControl.ps1 not found at $MasterControl" "ERROR"
throw "MasterControl.ps1 missing"
}
if (-not (Test-Path $DeployScript)) {
Write-RunLog "Deploy_Content.ps1 not found at $DeployScript. Deploy functionality will be disabled." "WARN"
$Deploy = $false
}

# -------------------------
# Run MasterControl (build)
# -------------------------

$mcArgs = @(
"-Mode", $Mode,
"-Campaign", $Campaign,
"-Count", $Count
)
if ($Force) { $mcArgs += "-Force" }
if ($SkipInstall) { $mcArgs += "-SkipInstall" }

Write-RunLog "Invoking MasterControl.ps1 with args: $($mcArgs -join ' ')"
$mcStart = Get-Date

# Execute with PowerShell to avoid breaking current session policies
$mcInvocation = @{
FilePath = "powershell"
ArgumentList = @("-NoProfile","-ExecutionPolicy","Bypass","-File",$MasterControl) + $mcArgs
NoNewWindow = $true
Wait = $true
PassThru = $true
}
$mcProc = Start-Process @mcInvocation
if ($mcProc.ExitCode -ne 0) {
Write-RunLog "MasterControl failed with exit code $($mcProc.ExitCode)" "ERROR"
Stop-Transcript -ErrorAction SilentlyContinue
throw "MasterControl failed"
}
$mcEnd = Get-Date
Write-RunLog "MasterControl completed in $((New-TimeSpan $mcStart $mcEnd).ToString())"

# -------------------------
# Locate produced video(s)
# -------------------------

Write-RunLog "Searching for produced videos..."
$videoRepoOut = Join-Path $RepoRoot "Output\Videos"
if (-not (Test-Path $videoRepoOut)) {
Write-RunLog "Output\Videos not found: $videoRepoOut" "ERROR"
throw "No Output\Videos directory"
}

# Get newest mp4 files matching campaign prefix
$pattern = "*$Campaign*oracle_horror*.mp4"
$produced = Get-ChildItem -Path $videoRepoOut -Filter "$pattern" -File -ErrorAction SilentlyContinue |
Sort-Object LastWriteTime -Descending

if (-not $produced -or $produced.Count -eq 0) {
# fallback: any mp4
Write-RunLog "No campaign-matching files found. Trying any recent mp4..."
$produced = Get-ChildItem -Path $videoRepoOut -Filter "*.mp4" -File |
Sort-Object LastWriteTime -Descending
if (-not $produced -or $produced.Count -eq 0) {
Write-RunLog "No mp4 files found in $videoRepoOut" "ERROR"
throw "No produced videos"
}
}

# Select top $Count videos
$selected = $produced | Select-Object -First $Count
Write-RunLog "Selected $($selected.Count) video(s) for post-processing:"
foreach ($v in $selected) { Write-RunLog "  - $($v.Name) ($([math]::Round($v.Length/1MB,2)) MB)" }

# Copy selected videos to run folder (atomic snapshot)
$copiedVideos = @()
foreach ($v in $selected) {
$dest = Join-Path $RunFolder $v.Name
Copy-Item -Path $v.FullName -Destination $dest -Force
$copiedVideos += (Get-Item $dest)
}

# -------------------------
# Optional: Perform quick verification (size/duration)
# -------------------------

function Get-VideoDuration {
param([string]$path)
try {
$out = & ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $path 2>$null
return [double]::Parse($out.Trim())
} catch {
return $null
}
}

foreach ($cv in $copiedVideos) {
Write-RunLog "Verifying $($cv.Name) size=$([math]::Round($cv.Length/1MB,2)) MB"
$dur = Get-VideoDuration -path $cv.FullName
if ($dur) {
Write-RunLog "  duration: $([math]::Round($dur,2))s"
} else {
Write-RunLog "  duration: unknown (ffprobe not available or failed)" "WARN"
}
if ($cv.Length -lt 1MB) {
Write-RunLog "  WARNING: file smaller than 1MB - likely a failed render" "WARN"
}
}

# -------------------------
# Deploy step (optional)
# -------------------------

if ($Deploy -and (Test-Path $DeployScript)) {
foreach ($cv in $copiedVideos) {
Write-RunLog "Invoking Deploy_Content.ps1 for $($cv.Name)"
$deployArgs = @(
"-Campaign", $Campaign,
"-Mode", $Mode,
"-OutputDir", (Split-Path -Parent $cv.FullName)
)
$deployInvocation = @{
FilePath = "powershell"
ArgumentList = @("-NoProfile","-ExecutionPolicy","Bypass","-File",$DeployScript) + $deployArgs
NoNewWindow = $true
Wait = $true
PassThru = $true
}
$dproc = Start-Process @deployInvocation
if ($dproc.ExitCode -ne 0) {
Write-RunLog "Deploy script failed for $($cv.Name) with exit code $($dproc.ExitCode)" "ERROR"
# decide whether to continue on error or abort — default: continue to next video
} else {
Write-RunLog "Deploy completed for $($cv.Name)"
}
}
} else {
Write-RunLog "Deploy skipped (Deploy flag false or deploy script missing)."
}

# -------------------------
# Cleanup (optional)
# -------------------------

if ($Cleanup) {
try {
Write-RunLog "Cleanup requested. Removing temp artifacts in $RunFolder older than 1 day..."
Get-ChildItem -Path (Join-Path $RepoRoot "Output\Temp") -Recurse -ErrorAction SilentlyContinue |
Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-1) } |
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-RunLog "Cleanup complete."
} catch {
Write-RunLog "Cleanup failed: $_" "WARN"
}
}

Write-RunLog "MASTERLAUNCH COMPLETED SUCCESSFULLY"
Stop-Transcript -ErrorAction SilentlyContinue
