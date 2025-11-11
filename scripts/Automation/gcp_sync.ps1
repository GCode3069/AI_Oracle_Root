# GCP Cloud Sync Script
# Requires: gsutil installed and authenticated
# Bucket: gs://ai-oracle-root-backups (to be created)

param(
    [string]$SourcePath = "F:\AI_Oracle_Root",
    [string]$BucketName = "ai-oracle-root-backups",
    [string]$LogFile = "F:\AI_Oracle_Root\Logs\Automation\gcp_sync.log",
    [switch]$DryRun
)

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$timestamp] $Message"
    Write-Output $entry
    if ($LogFile) {
        $entry | Out-File -FilePath $LogFile -Append -Encoding UTF8
    }
}

# Check if gsutil is available
$gsutilPath = Get-Command gsutil -ErrorAction SilentlyContinue
if (-not $gsutilPath) {
    Write-Log "ERROR: gsutil not found. Install Google Cloud SDK first."
    exit 1
}

if (-not (Test-Path -Path $SourcePath)) {
    Write-Log "ERROR: Source path '$SourcePath' not found."
    exit 1
}

$bucketUri = "gs://$BucketName"

# Check if bucket exists
$bucketCheck = & gsutil ls $bucketUri 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Log "WARNING: Bucket '$bucketUri' may not exist. Create it first:"
    Write-Log "  gsutil mb -l us-central1 $bucketUri"
    Write-Log "  gsutil versioning set on $bucketUri"
    if (-not $DryRun) {
        exit 1
    }
}

Write-Log "Starting GCP sync from '$SourcePath' to '$bucketUri'"

# Exclusion patterns for gsutil rsync
$excludePatterns = @(
    ".git/**",
    "Backups/**",
    ".venv*/**",
    "venv*/**",
    "node_modules/**",
    "*.log",
    "*.tmp",
    "thumbs.db"
)

$rsyncArgs = @("rsync", "-r", "-d")
foreach ($pattern in $excludePatterns) {
    $rsyncArgs += "-x"
    $rsyncArgs += $pattern
}

if ($DryRun) {
    $rsyncArgs += "-n"
    Write-Log "DRY RUN: Would sync (no changes will be made)"
}

$rsyncArgs += $SourcePath
$rsyncArgs += $bucketUri

Write-Log "Executing: gsutil $($rsyncArgs -join ' ')"

try {
    $output = & gsutil $rsyncArgs 2>&1
    $output | ForEach-Object { Write-Log $_ }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Log "GCP sync completed successfully"
    } else {
        Write-Log "GCP sync completed with warnings (exit code: $LASTEXITCODE)"
    }
} catch {
    Write-Log "ERROR: GCP sync failed: $_"
    exit 1
}

