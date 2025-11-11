param(
    [string]$SourcePath = "F:\AI_Oracle_Root",
    [string]$BackupRoot = "F:\Backups\scarify",
    [int]$RetentionDays = 14,
    [string[]]$ExcludeDirs = @(".git", "Backups", ".venv", ".venv_animdiff", ".venv_clean", ".venv_scarify", ".venv311", "node_modules", "tmp", "temp"),
    [string[]]$ExcludeFiles = @("*.log", "*.tmp", "thumbs.db")
)

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $entry = "[$timestamp] $Message"
    Write-Output $entry
    $logFile = "F:\AI_Oracle_Root\Logs\Automation\nightly_backup.log"
    $entry | Out-File -FilePath $logFile -Append -Encoding UTF8
}

if (-not (Test-Path -Path $SourcePath)) {
    Write-Log "Source path '$SourcePath' not found."
    exit 1
}

if (-not (Test-Path -Path $BackupRoot)) {
    try {
        New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null
        Write-Log "Created backup root at '$BackupRoot'."
    } catch {
        Write-Log "Failed to create backup root '$BackupRoot': $_"
        exit 1
    }
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmm"
$targetPath = Join-Path $BackupRoot "scarify_$timestamp"

try {
    New-Item -ItemType Directory -Path $targetPath -Force | Out-Null
} catch {
    Write-Log "Failed to create backup target '$targetPath': $_"
    exit 1
}

$robocopyArgs = @($SourcePath, $targetPath, "/MIR", "/R:1", "/W:3", "/NFL", "/NDL", "/NP", "/XO")

foreach ($dir in $ExcludeDirs) {
    $fullPath = Join-Path $SourcePath $dir
    $robocopyArgs += "/XD"
    $robocopyArgs += $fullPath
}

foreach ($filePattern in $ExcludeFiles) {
    $robocopyArgs += "/XF"
    $robocopyArgs += $filePattern
}

Write-Log "Starting robocopy to '$targetPath'."
$process = Start-Process -FilePath "robocopy" -ArgumentList $robocopyArgs -Wait -NoNewWindow -PassThru
$exitCode = $process.ExitCode

if ($exitCode -ge 8) {
    Write-Log "Robocopy failed with exit code $exitCode."
    exit $exitCode
}

Write-Log "Backup completed with robocopy exit code $exitCode."

# Retention cleanup
$threshold = (Get-Date).AddDays(-$RetentionDays)
$olderBackups = Get-ChildItem -Path $BackupRoot -Directory | Where-Object { $_.LastWriteTime -lt $threshold }

foreach ($old in $olderBackups) {
    try {
        Remove-Item -Path $old.FullName -Recurse -Force
        Write-Log "Removed old backup '$($old.FullName)'."
    } catch {
        Write-Log "Failed to remove old backup '$($old.FullName)': $_"
    }
}

Write-Log "Backup job finished."

