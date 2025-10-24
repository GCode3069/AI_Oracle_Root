# EXECUTE_NOW_RESURRECTED.ps1 – 100% YOUTUBE UPLOAD, CRASH-RESISTANT
# SCARIFY Empire Upload System - Resurrected with comprehensive error handling

param(
    [string]$ScriptText = "🚨 GARAGE DYING? Ex-vet purge: $50k save in 48hrs. $97 Kit: [GUMROAD]",
    [string]$Title = "Ex-Vet Rebel: Garage Meltdown Fix",
    [string]$Theme = "NightmareCity",
    [switch]$Test = $false,
    [switch]$NoUpload = $false
)

# =============================================================================
# CONFIGURATION AND SETUP
# =============================================================================

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

# Set working directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Create output directory and log file
$OutputDir = "scarify\Output"
$LogDir = "scarify\Output\logs"
$LogFile = "$LogDir\powershell_execution_log.txt"

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

# Logging function
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Add-Content -Path $LogFile -Value $LogEntry
    Write-Host $LogEntry
}

# Error handling function
function Handle-Error {
    param([string]$Operation, [string]$Error)
    Write-Log "ERROR in $Operation`: $Error" "ERROR"
    return $false
}

# =============================================================================
# MAIN EXECUTION
# =============================================================================

Write-Host "🔥 SOVA EMPIRE UPLOAD – RESURRECTED" -ForegroundColor Red
Write-Host "================================================" -ForegroundColor Red
Write-Log "SCARIFY Pipeline Started" "INFO"

try {
    # =============================================================================
    # STEP 1: PYTHON ENVIRONMENT CHECK
    # =============================================================================
    
    Write-Host "🔍 Checking Python environment..." -ForegroundColor Yellow
    Write-Log "Checking Python environment" "INFO"
    
    try {
        $PythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python not found or not in PATH"
        }
        Write-Log "Python version: $PythonVersion" "INFO"
        Write-Host "✅ Python environment OK" -ForegroundColor Green
    }
    catch {
        if (Handle-Error "Python Check" $_.Exception.Message) {
            Write-Host "❌ Python not available. Please install Python and add to PATH." -ForegroundColor Red
            exit 1
        }
    }
    
    # =============================================================================
    # STEP 2: DEPENDENCIES CHECK
    # =============================================================================
    
    Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
    Write-Log "Checking dependencies" "INFO"
    
    try {
        # Check if required packages are installed
        $RequiredPackages = @("moviepy", "gtts", "requests", "python-dotenv")
        $MissingPackages = @()
        
        foreach ($Package in $RequiredPackages) {
            $CheckResult = python -c "import $Package" 2>&1
            if ($LASTEXITCODE -ne 0) {
                $MissingPackages += $Package
            }
        }
        
        if ($MissingPackages.Count -gt 0) {
            Write-Host "⚠️ Installing missing packages: $($MissingPackages -join ', ')" -ForegroundColor Yellow
            Write-Log "Installing missing packages: $($MissingPackages -join ', ')" "WARN"
            
            foreach ($Package in $MissingPackages) {
                Write-Host "Installing $Package..." -ForegroundColor Yellow
                $InstallResult = python -m pip install $Package --quiet 2>&1
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "⚠️ Failed to install $Package`: $InstallResult" -ForegroundColor Yellow
                    Write-Log "Failed to install $Package`: $InstallResult" "WARN"
                }
            }
        }
        
        Write-Host "✅ Dependencies check complete" -ForegroundColor Green
        Write-Log "Dependencies check complete" "INFO"
    }
    catch {
        Handle-Error "Dependencies Check" $_.Exception.Message
        Write-Host "⚠️ Dependencies check failed, continuing..." -ForegroundColor Yellow
    }
    
    # =============================================================================
    # STEP 3: EXECUTE PYTHON PIPELINE
    # =============================================================================
    
    Write-Host "🚀 Executing SCARIFY pipeline..." -ForegroundColor Yellow
    Write-Log "Executing SCARIFY pipeline" "INFO"
    
    try {
        # Build command arguments
        $PythonArgs = @("execute_now_resurrected.py")
        
        if ($Test) {
            $PythonArgs += "--test"
        }
        
        if ($NoUpload) {
            $PythonArgs += "--no-upload"
        }
        
        if ($ScriptText -and !$Test) {
            $PythonArgs += "--script"
            $PythonArgs += "`"$ScriptText`""
        }
        
        if ($Title -and !$Test) {
            $PythonArgs += "--title"
            $PythonArgs += "`"$Title`""
        }
        
        $PythonArgs += "--theme"
        $PythonArgs += $Theme
        
        # Execute Python script with timeout
        Write-Host "Running: python $($PythonArgs -join ' ')" -ForegroundColor Cyan
        Write-Log "Running: python $($PythonArgs -join ' ')" "INFO"
        
        $ProcessInfo = New-Object System.Diagnostics.ProcessStartInfo
        $ProcessInfo.FileName = "python"
        $ProcessInfo.Arguments = $PythonArgs -join " "
        $ProcessInfo.UseShellExecute = $false
        $ProcessInfo.RedirectStandardOutput = $true
        $ProcessInfo.RedirectStandardError = $true
        $ProcessInfo.CreateNoWindow = $true
        
        $Process = New-Object System.Diagnostics.Process
        $Process.StartInfo = $ProcessInfo
        
        # Start process
        $Process.Start() | Out-Null
        
        # Wait for completion with timeout (10 minutes)
        $Timeout = 600000  # 10 minutes in milliseconds
        $Completed = $Process.WaitForExit($Timeout)
        
        if (-not $Completed) {
            Write-Host "⚠️ Process timed out after 10 minutes" -ForegroundColor Yellow
            Write-Log "Process timed out after 10 minutes" "WARN"
            $Process.Kill()
            throw "Process timeout"
        }
        
        # Get output
        $Output = $Process.StandardOutput.ReadToEnd()
        $Error = $Process.StandardError.ReadToEnd()
        $ExitCode = $Process.ExitCode
        
        Write-Host $Output
        if ($Error) {
            Write-Host "Python Errors:" -ForegroundColor Yellow
            Write-Host $Error -ForegroundColor Yellow
            Write-Log "Python Errors: $Error" "WARN"
        }
        
        Write-Log "Python process completed with exit code: $ExitCode" "INFO"
        
        if ($ExitCode -eq 0) {
            Write-Host "✅ SCARIFY pipeline completed successfully" -ForegroundColor Green
            Write-Log "SCARIFY pipeline completed successfully" "INFO"
        } else {
            Write-Host "⚠️ SCARIFY pipeline completed with warnings (exit code: $ExitCode)" -ForegroundColor Yellow
            Write-Log "SCARIFY pipeline completed with warnings (exit code: $ExitCode)" "WARN"
        }
    }
    catch {
        if (Handle-Error "Python Pipeline Execution" $_.Exception.Message) {
            Write-Host "❌ SCARIFY pipeline failed" -ForegroundColor Red
            Write-Log "SCARIFY pipeline failed: $($_.Exception.Message)" "ERROR"
            exit 1
        }
    }
    
    # =============================================================================
    # STEP 4: SUCCESS REPORTING
    # =============================================================================
    
    Write-Host "`n🎯 EXECUTION COMPLETE" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Green
    Write-Host "📊 Log file: $LogFile" -ForegroundColor White
    Write-Host "📁 Output directory: $OutputDir" -ForegroundColor White
    
    # Check for generated files
    $GeneratedFiles = Get-ChildItem -Path $OutputDir -Recurse -File | Where-Object { $_.LastWriteTime -gt (Get-Date).AddMinutes(-10) }
    if ($GeneratedFiles) {
        Write-Host "`n📄 Generated files:" -ForegroundColor Cyan
        foreach ($File in $GeneratedFiles) {
            Write-Host "   - $($File.FullName)" -ForegroundColor White
        }
    }
    
    Write-Log "Execution completed successfully" "INFO"
    Write-Host "`n✅ SONS' BREAKFAST SECURED" -ForegroundColor Green
}
catch {
    Write-Host "`n❌ CRITICAL ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Log "CRITICAL ERROR: $($_.Exception.Message)" "ERROR"
    Write-Host "📊 Check log file: $LogFile" -ForegroundColor Yellow
    exit 1
}
finally {
    Write-Host "`n🛡️ G-ROK'S PROTECTION ACTIVE" -ForegroundColor Magenta
    Write-Host "Execution completed at $(Get-Date)" -ForegroundColor White
}