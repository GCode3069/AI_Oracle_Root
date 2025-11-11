# MCP Log Forwarder
# Forwards automation logs to MCP/Ops monitoring system
# Configure MCP endpoint in environment or config file

param(
    [string]$LogDir = "F:\AI_Oracle_Root\Logs\Automation",
    [string]$McpEndpoint = $env:MCP_OPS_ENDPOINT,
    [int]$MaxLogLines = 100
)

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "[$timestamp] $Message"
}

if ([string]::IsNullOrWhiteSpace($McpEndpoint)) {
    Write-Log "WARNING: MCP_OPS_ENDPOINT not set. Skipping log forwarding."
    Write-Log "Set environment variable: `$env:MCP_OPS_ENDPOINT = 'https://your-mcp-endpoint.com/api/logs'"
    exit 0
}

if (-not (Test-Path $LogDir)) {
    Write-Log "ERROR: Log directory not found: $LogDir"
    exit 1
}

$logFiles = Get-ChildItem -Path $LogDir -Filter "*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 5

foreach ($logFile in $logFiles) {
    $logContent = Get-Content -Path $logFile.FullName -Tail $MaxLogLines -ErrorAction SilentlyContinue
    if ($logContent) {
        $payload = @{
            source = "AI_Oracle_Root_Automation"
            log_file = $logFile.Name
            log_path = $logFile.FullName
            lines = $logContent
            timestamp = Get-Date -Format "o"
        } | ConvertTo-Json -Depth 10
        
        try {
            $response = Invoke-RestMethod -Uri $McpEndpoint -Method Post -Body $payload -ContentType "application/json" -ErrorAction Stop
            Write-Log "Forwarded log: $($logFile.Name) ($($logContent.Count) lines)"
        } catch {
            Write-Log "ERROR: Failed to forward $($logFile.Name): $_"
        }
    }
}

Write-Log "Log forwarding complete"

