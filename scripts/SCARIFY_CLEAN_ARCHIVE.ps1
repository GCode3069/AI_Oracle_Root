<#
SCARIFY_CLEAN_ARCHIVE.ps1
Safely archives legacy / versioned / clutter files for the SCARIFY project.

Usage:
  .\scripts\SCARIFY_CLEAN_ARCHIVE.ps1 -DryRun
  .\scripts\SCARIFY_CLEAN_ARCHIVE.ps1          (commit moves)

Parameters:
  -Root          Root path (default: current)
  -DryRun        Show actions only
  -IncludeExtra  Apply more aggressive patterns
  -KeepLatestN   Retain newest N per pattern (default 1)
#>

param(
    [string]$Root = (Get-Location).Path,
    [switch]$DryRun,
    [switch]$IncludeExtra,
    [int]$KeepLatestN = 1
)

$ErrorActionPreference = "Stop"

function Info($m){ Write-Host "[INFO] $m" -ForegroundColor Cyan }
function Warn($m){ Write-Host "[WARN] $m" -ForegroundColor Yellow }
function Act($m){ Write-Host "[MOVE] $m" -ForegroundColor Green }
function Sim($m){ Write-Host "[DRY ] $m" -ForegroundColor Gray }
function Skip($m){ Write-Host "[SKIP] $m" -ForegroundColor Magenta }

$Root = (Resolve-Path $Root).Path
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$ArchiveBase = Join-Path $Root "archive_cleanup"
$ArchiveFolder = Join-Path $ArchiveBase ("archive_{0}" -f $ts)
$LogFile = Join-Path $ArchiveBase ("cleanup_log_{0}.txt" -f $ts)

if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $ArchiveFolder | Out-Null
    New-Item -ItemType Directory -Force -Path $ArchiveBase | Out-Null
    Add-Content $LogFile "=== SCARIFY CLEANUP START $(Get-Date) ==="
    Add-Content $LogFile "Root=$Root"
}

# Primary patterns
$patterns = @(
    "scarify_arg_pipeline_Version*.py",
    "scarify.pipeline_scarify_arg_pipeline_Version*.py",
    "scarify_full_pipeline*.py",
    "scenes_Version*.json",
    "SCARIFY_QUICK_LAUNCH_Version*.ps1",
    "*_Version*.ps1",
    "*_backup*.json",
    "*_old*.ps1",
    "*mini_test_Version*.py",
    "*first_batch*.ps1"
)

if ($IncludeExtra) {
    $patterns += @(
        "place_google_oauth_credentials_Version*.ps1",
        "Upload-*Version*.ps1"
    )
}

$candidates = @()
foreach ($pat in $patterns) {
    $found = Get-ChildItem -Path $Root -Filter $pat -Recurse -File -ErrorAction SilentlyContinue
    if ($found) { $candidates += $found }
}

if (-not $candidates) {
    Warn "No matching legacy files found."
    return
}

# Group by normalized name (strip long numbers)
$grouped = $candidates | Group-Object { $_.Name -replace '\d{8,}','' }

$planned = @()
foreach ($grp in $grouped) {
    $ordered = $grp.Group | Sort-Object LastWriteTime -Descending
    $keep = $ordered | Select-Object -First $KeepLatestN
    $archiveThese = $ordered | Where-Object { $keep -notcontains $_ }
    foreach ($file in $archiveThese) {
        # Double-check file still exists before planning the move
        if (Test-Path $file.FullName) {
            $rel = $file.FullName.Substring($Root.Length).TrimStart("\", "/")
            $destName = $rel -replace '[\\/]', '_'
            $dest = Join-Path $ArchiveFolder $destName
            $planned += [PSCustomObject]@{
                Source = $file.FullName
                Destination = $dest
                Size = $file.Length
                Modified = $file.LastWriteTime
            }
        } else {
            Warn "File no longer exists, skipping: $($file.FullName)"
        }
    }
}

if (-not $planned) {
    Info "Nothing to archive (KeepLatestN=$KeepLatestN)."
    return
}

$totalSize = ($planned | Measure-Object -Property Size -Sum).Sum
Info ("Files to archive: {0}  Total: {1:N0} bytes (~{2:N2} MB)" -f $planned.Count, $totalSize, ($totalSize/1MB))

$moved = 0
$skipped = 0

foreach ($p in $planned) {
    # Final check before move - file may have been deleted since planning
    if (-not (Test-Path $p.Source)) {
        Skip "File no longer exists: $($p.Source)"
        $skipped++
        if (-not $DryRun) {
            Add-Content $LogFile "SKIPPED|$($p.Source)|FILE_NOT_FOUND|$(Get-Date -Format 'o')"
        }
        continue
    }
    
    if ($DryRun) {
        Sim "$($p.Source) -> $($p.Destination)"
    } else {
        try {
            $destDir = Split-Path $p.Destination
            New-Item -ItemType Directory -Force -Path $destDir | Out-Null
            Move-Item -Path $p.Source -Destination $p.Destination -Force
            Act "$($p.Source) -> $($p.Destination)"
            Add-Content $LogFile "$($p.Source)|$($p.Destination)|$($p.Size)|$($p.Modified.ToString('o'))"
            $moved++
        }
        catch {
            Warn "Failed to move $($p.Source): $($_.Exception.Message)"
            Add-Content $LogFile "ERROR|$($p.Source)|$($_.Exception.Message)|$(Get-Date -Format 'o')"
            $skipped++
        }
    }
}

if (-not $DryRun) {
    Add-Content $LogFile "=== CLEANUP COMPLETE $(Get-Date) ==="
    Add-Content $LogFile "FILES_MOVED=$moved"
    Add-Content $LogFile "FILES_SKIPPED=$skipped"
    Info "Archive folder: $ArchiveFolder"
    Info "Log file: $LogFile"
    Info "Successfully moved: $moved files, Skipped: $skipped files"
} else {
    Warn "Dry run only. Re-run WITHOUT -DryRun to commit."
    Info "Would move: $($planned.Count) files, Would skip: $skipped files"
}