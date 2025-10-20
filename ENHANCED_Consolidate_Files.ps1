# ENHANCED_Consolidate_Files.ps1
# Consolidates files from multiple source drives to a single target (Extreme SSD)
# Features: dry-run, backup before overwrite, categorization, duplicate handling, error handling

param(
    [string[]]$SourceDirs = @(
        "D:\Ai Oracle",
        "E:\scarify",
        "E:\SCARIFY_COMPLETE_20251008_135202",
        "E:\My Passport\scarify",
        "F:\AI_Oracle_Root"
    ),
    [string]$TargetRoot = "F:\Extreme SSD",
    [switch]$DryRun,
    [switch]$Verbose,
    [switch]$BackupBeforeMove
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Folder mapping by extension
$FolderMap = @{ 
    'Scripts' = @('.ps1','.py','.bat','.cmd')
    'Assets'  = @('.jpg','.jpeg','.png','.gif','.bmp','.mp4','.avi','.mov','.wav','.mp3','.aac')
    'Config'  = @('.json','.toml','.yaml','.yml','.config','.ini')
    'Documents' = @('.pdf','.doc','.docx','.txt','.md','.rtf')
    'Data'    = @('.csv','.xlsx','.db','.sqlite')
    'Logs'    = @('.log','.tmp')
    'Archives' = @('.zip','.rar','.7z','.tar')
}

function Get-Category([string]$ext) {
    foreach ($k in $FolderMap.Keys) {
        if ($FolderMap[$k] -contains $ext.ToLower()) { return $k }
    }
    return 'Generated'
}

function Safe-Copy([string]$sourcePath, [string]$destPath) {
    if ($DryRun) { Write-Host "DRYRUN: Would copy $sourcePath -> $destPath" -ForegroundColor Yellow; return }
    $destDir = Split-Path $destPath -Parent
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }

    if (Test-Path $destPath) {
        # If file exists, create backup if requested, otherwise create unique name
        if ($BackupBeforeMove) {
            $bak = "$destPath.bak.$((Get-Date).ToString('yyyyMMddHHmmss'))"
            Write-Host "Backing up existing: $destPath -> $bak" -ForegroundColor Cyan
            Copy-Item -Path $destPath -Destination $bak -Force
        }
        $base = [System.IO.Path]::GetFileNameWithoutExtension($destPath)
        $ext = [System.IO.Path]::GetExtension($destPath)
        $i = 1
        do {
            $candidate = Join-Path -Path $destDir -ChildPath ("{0}_{1}{2}" -f $base, $i, $ext)
            $i++
        } while (Test-Path $candidate)
        Write-Host "Collision: writing to $candidate" -ForegroundColor Yellow
        Copy-Item -Path $sourcePath -Destination $candidate -Force
    } else {
        Copy-Item -Path $sourcePath -Destination $destPath -Force
    }
}

# Main
Write-Host "Starting consolidation to: $TargetRoot" -ForegroundColor Green
foreach ($sd in $SourceDirs) {
    try {
        if (-not (Test-Path $sd)) { Write-Host "Source not found: $sd" -ForegroundColor Red; continue }
        Get-ChildItem -Path $sd -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            $src = $_.FullName
            $ext = $_.Extension
            $category = Get-Category $ext
            $relPath = $_.FullName.Substring($sd.Length).TrimStart('\')
            $destDir = Join-Path -Path $TargetRoot -ChildPath $category
            $destPath = Join-Path -Path $destDir -ChildPath $relPath
            $destPath = [System.IO.Path]::GetFullPath($destPath)

            try {
                Safe-Copy -sourcePath $src -destPath $destPath
                if ($Verbose) { Write-Host "Copied: $src -> $destPath" }
            } catch {
                Write-Host "ERROR copying $src: $_" -ForegroundColor Red
            }
        }
    } catch {
        Write-Host "ERROR scanning $sd: $_" -ForegroundColor Red
    }
}
Write-Host "Consolidation complete." -ForegroundColor Green
