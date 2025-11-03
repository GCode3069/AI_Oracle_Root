# =========================================
# ??  SCARIFY: Resume PowerShell Session
# =========================================
$sessionDir = "F:\AI_Oracle_Root\scarify\session_state"

if (Test-Path "$sessionDir\last_dir.txt") {
    Set-Location (Get-Content "$sessionDir\last_dir.txt")
}

if (Test-Path "$sessionDir\command_history.xml") {
    Import-Clixml "$sessionDir\command_history.xml" | Add-History
}

if (Test-Path "$sessionDir\variables.xml") {
    $vars = Import-Clixml "$sessionDir\variables.xml"
    foreach ($var in $vars) {
        try {
            Set-Variable -Name $var.Name -Value $var.Value -Scope Global -Force
        } catch {}
    }
}

Write-Host "`n?? SCARIFY session restored — you’re back where you left off." -ForegroundColor Cyan
