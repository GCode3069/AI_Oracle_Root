<#
.SYNOPSIS
SCARIFY Master Control - Primary System Orchestrator

.DESCRIPTION
Master control system for SCARIFY video production workflows.
Coordinates all subsystems and manages the complete pipeline.

.AUTHOR
GCode3069

.VERSION
1.0
#>

param(
    [string]$Operation = "status",
    [string]$Campaign = "awakening", 
    [string]$Mode = "full",
    [int]$Count = 1,
    [switch]$Force
)

$ErrorActionPreference = "Continue"

function Write-ScarifyMasterLog {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $color = switch($Level) {
        "SUCCESS" { "Green" }
        "ERROR" { "Red" }
        "WARNING" { "Yellow" }
        "MASTER" { "Magenta" }
        default { "Cyan" }
    }
    Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor $color
}

Write-ScarifyMasterLog "🎭 SCARIFY MASTER CONTROL SYSTEM v1.0" "MASTER"
Write-ScarifyMasterLog "🔧 Operation: $Operation | Campaign: $Campaign | Mode: $Mode" "INFO"

switch ($Operation.ToLower()) {
    "status" {
        Write-ScarifyMasterLog "📊 Checking system status..." "INFO"
        
        $components = @{
            "Video Production" = Test-Path "scarify_complete_video_production.ps1"
            "Master Launch" = Test-Path "MasterLaunch.ps1"
            "Desktop Launcher" = Test-Path "SCARIFY-Desktop-Launcher.ps1"
            "Output Directory" = Test-Path "Output"
        }
        
        foreach ($component in $components.Keys) {
            $status = if ($components[$component]) { "✅ ONLINE" } else { "❌ OFFLINE" }
            $level = if ($components[$component]) { "SUCCESS" } else { "ERROR" }
            Write-ScarifyMasterLog "$component`: $status" $level
        }
        
        $allOnline = ($components.Values | Where-Object { $_ -eq $false }).Count -eq 0
        if ($allOnline) {
            Write-ScarifyMasterLog "🚀 ALL SYSTEMS OPERATIONAL - READY FOR DEPLOYMENT" "SUCCESS"
        } else {
            Write-ScarifyMasterLog "⚠️ SOME SYSTEMS OFFLINE - CHECK FAILED COMPONENTS" "WARNING"
        }
    }
    
    "execute" {
        Write-ScarifyMasterLog "🚀 Executing full system deployment..." "MASTER"
        
        # Launch video production
        Write-ScarifyMasterLog "📺 Launching video production pipeline..." "INFO"
        $productionArgs = "-Campaign $Campaign -VideoType $Mode -Count $Count"
        if ($Force) { $productionArgs += " -FastMode" }
        
        try {
            $result = & ".\scarify_complete_video_production.ps1" -Campaign $Campaign -VideoType $Mode -Count $Count
            Write-ScarifyMasterLog "✅ Video production completed successfully" "SUCCESS"
        } catch {
            Write-ScarifyMasterLog "❌ Video production failed: $($_.Exception.Message)" "ERROR"
        }
        
        Write-ScarifyMasterLog "🎯 SCARIFY Master Control execution completed!" "MASTER"
    }
    
    "test" {
        Write-ScarifyMasterLog "🧪 Running system tests..." "INFO"
        
        # Test video production with minimal settings
        try {
            & ".\scarify_complete_video_production.ps1" -Campaign "test" -VideoType "shorts" -Count 1 -FastMode
            Write-ScarifyMasterLog "✅ Test execution successful" "SUCCESS"
        } catch {
            Write-ScarifyMasterLog "❌ Test execution failed: $($_.Exception.Message)" "ERROR"
        }
    }
    
    default {
        Write-ScarifyMasterLog "❌ Invalid operation: $Operation" "ERROR"
        Write-ScarifyMasterLog "Valid operations: status, execute, test" "INFO"
    }
}

Write-ScarifyMasterLog "🔚 SCARIFY Master Control session ended" "MASTER"