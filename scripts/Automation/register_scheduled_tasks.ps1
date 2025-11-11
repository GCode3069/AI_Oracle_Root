# Run this script as Administrator to register scheduled tasks
# Right-click PowerShell -> Run as Administrator, then execute this script

$ErrorActionPreference = 'Stop'

$autoPushScript = "F:\AI_Oracle_Root\scripts\Automation\auto_git_push.ps1"
$backupScript = "F:\AI_Oracle_Root\scripts\Automation\nightly_backup.ps1"

if (-not (Test-Path $autoPushScript)) {
    Write-Error "Auto push script not found: $autoPushScript"
    exit 1
}

if (-not (Test-Path $backupScript)) {
    Write-Error "Backup script not found: $backupScript"
    exit 1
}

# Register auto-git-push task (runs every 30 minutes)
$autoPushAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$autoPushScript`""
$autoPushTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30) -RepetitionDuration (New-TimeSpan -Days 365)
$autoPushPrincipal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest
$autoPushSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "AI_Oracle_AutoGitPush" -Action $autoPushAction -Trigger $autoPushTrigger -Principal $autoPushPrincipal -Settings $autoPushSettings -Description "Automatically commit and push changes to AI_Oracle_Root repository every 30 minutes" -Force

Write-Output "Registered task: AI_Oracle_AutoGitPush"

# Register nightly backup task (runs daily at 2 AM)
$backupAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$backupScript`""
$backupTrigger = New-ScheduledTaskTrigger -Daily -At "02:00"
$backupPrincipal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Highest
$backupSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "AI_Oracle_NightlyBackup" -Action $backupAction -Trigger $backupTrigger -Principal $backupPrincipal -Settings $backupSettings -Description "Nightly mirrored backup of AI_Oracle_Root repository" -Force

Write-Output "Registered task: AI_Oracle_NightlyBackup"
Write-Output "Scheduled tasks registered successfully!"

