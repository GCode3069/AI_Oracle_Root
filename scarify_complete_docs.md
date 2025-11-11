# AI_Oracle_Root Backup and Automation Documentation

## Overview

This document describes the automated backup and synchronization system for the `F:\AI_Oracle_Root` repository. The system ensures robust data protection through multiple layers: local Git commits, local mirrored backups, and cloud synchronization.

## Architecture

### Components

1. **Git Auto-Push Script** (`scripts/Automation/auto_git_push.ps1`)
   - Automatically commits and pushes changes every 30 minutes
   - Handles divergence detection and prevents conflicts
   - Excludes virtual environments, logs, and backup directories

2. **Nightly Backup Script** (`scripts/Automation/nightly_backup.ps1`)
   - Creates timestamped mirrored backups using robocopy
   - Implements 14-day retention policy
   - Excludes unnecessary files and directories

3. **Windows Task Scheduler Integration**
   - Auto-push runs every 30 minutes
   - Nightly backup runs daily at 2:00 AM

4. **GCP Cloud Sync** (Planned)
   - Dedicated bucket with versioning enabled
   - Automated rsync for additional redundancy

5. **MCP/Ops Integration** (Planned)
   - Central logging and alerting
   - Runbook documentation

## Setup Instructions

### Prerequisites

- Windows 10/11 with PowerShell 5.1+
- Git installed and configured
- Administrator access for Task Scheduler registration

### Initial Setup

1. **Register Scheduled Tasks** (Run as Administrator):
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File "F:\AI_Oracle_Root\Scripts\Automation\register_scheduled_tasks.ps1"
   ```

2. **Verify Tasks Registered**:
   ```powershell
   Get-ScheduledTask -TaskName "AI_Oracle_*"
   ```

3. **Test Scripts Manually**:
   ```powershell
   # Test auto-push (dry run)
   .\scripts\Automation\auto_git_push.ps1 -DryRun
   
   # Test backup
   .\scripts\Automation\nightly_backup.ps1
   ```

## Script Details

### auto_git_push.ps1

**Purpose**: Automatically commit and push repository changes.

**Features**:
- Fetches latest from origin before pushing
- Detects branch divergence (ahead/behind commits)
- Aborts if branch is behind remote (requires manual sync)
- Filters out excluded paths (venv, logs, backups)
- Comprehensive logging to `Logs/Automation/auto_git_push.log`

**Excluded Patterns**:
- `Logs/`, `Backups/`, `backup/`, `Archive/`, `archive_cleanup/`
- `tmp/`, `temp/`
- `.venv*`, `venv*`

**Parameters**:
- `-RepoPath`: Repository root path (default: `F:\AI_Oracle_Root`)
- `-LogFile`: Log file path (default: `F:\AI_Oracle_Root\Logs\Automation\auto_git_push.log`)
- `-DryRun`: Test mode without actual Git operations

### nightly_backup.ps1

**Purpose**: Create timestamped mirrored backups with retention.

**Features**:
- Uses robocopy for efficient mirroring
- Timestamped backup folders: `scarify_YYYYMMDD_HHmm`
- 14-day retention (configurable)
- Excludes Git, virtual environments, node_modules, temp files
- Logs to `Logs/Automation/nightly_backup.log`

**Parameters**:
- `-SourcePath`: Source directory (default: `F:\AI_Oracle_Root`)
- `-BackupRoot`: Backup destination root (default: `F:\Backups\scarify`)
- `-RetentionDays`: Days to keep backups (default: 14)
- `-ExcludeDirs`: Additional directories to exclude
- `-ExcludeFiles`: File patterns to exclude

## Logging

All automation scripts write logs to `F:\AI_Oracle_Root\Logs\Automation\`:
- `auto_git_push.log`: Git automation activity
- `nightly_backup.log`: Backup job execution

Logs include timestamps and detailed operation status.

## Backup Locations

- **Local Backups**: `F:\Backups\scarify\scarify_YYYYMMDD_HHmm\`
- **Manual Snapshots**: `F:\Backups\scarify\manual\snapshot_YYYYMMDD_HHmmss\`
- **Git Remote**: `https://github.com/GCode3069/AI_Oracle_Root.git`

## Recovery Procedures

### Restore from Local Backup

1. Navigate to backup folder: `F:\Backups\scarify\`
2. Identify desired timestamp folder
3. Copy contents back to `F:\AI_Oracle_Root` (or restore specific files)

### Restore from Git

1. Clone fresh copy:
   ```powershell
   git clone https://github.com/GCode3069/AI_Oracle_Root.git F:\AI_Oracle_Root_Restore
   ```

2. Checkout specific commit if needed:
   ```powershell
   git log --oneline
   git checkout <commit-hash>
   ```

### Manual Snapshot Creation

```powershell
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupFolder = "F:\Backups\scarify\manual\snapshot_$timestamp"
New-Item -ItemType Directory -Path $backupFolder -Force
git status -sb | Out-File "$backupFolder\git-status.txt"
git diff > "$backupFolder\git-diff.patch"
# Create zip if needed
```

## Troubleshooting

### Auto-Push Fails

1. Check log: `Logs\Automation\auto_git_push.log`
2. Verify Git credentials: `git config --list`
3. Check branch divergence: `git status`
4. If behind remote, manually sync: `git pull --rebase origin main`

### Backup Fails

1. Check log: `Logs\Automation\nightly_backup.log`
2. Verify disk space: `Get-PSDrive F`
3. Check robocopy exit codes (0-7 are success, 8+ indicate errors)

### Scheduled Tasks Not Running

1. Verify tasks exist: `Get-ScheduledTask -TaskName "AI_Oracle_*"`
2. Check task history: Task Scheduler → Task Scheduler Library → AI_Oracle_*
3. Verify execution policy: `Get-ExecutionPolicy`
4. Re-register tasks if needed (run register script as Administrator)

## Future Enhancements

### GCP Cloud Sync

- [ ] Create dedicated GCP bucket with versioning
- [ ] Set up service account credentials
- [ ] Implement `gsutil rsync` automation
- [ ] Schedule weekly cloud sync

### MCP/Ops Integration

- [ ] Forward logs to central monitoring system
- [ ] Set up alerting for automation failures
- [ ] Create runbook for common recovery scenarios
- [ ] Integrate with existing MCP infrastructure

## Maintenance

### Regular Checks

- Weekly: Review automation logs for errors
- Monthly: Verify backup retention is working
- Quarterly: Test recovery procedures

### Updates

When updating scripts:
1. Test changes in dry-run mode
2. Commit and push updates
3. Restart scheduled tasks if needed: `Restart-ScheduledTask -TaskName "AI_Oracle_*"`

## Contact

For issues or questions about the automation system, check logs first, then review this documentation.

---

**Last Updated**: 2025-11-11
**Version**: 1.0

