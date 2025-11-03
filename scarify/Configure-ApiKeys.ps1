$credentialDir = Join-Path $PSScriptRoot "..\credentials"
if (-not (Test-Path $credentialDir)) {
    New-Item -Path $credentialDir -ItemType Directory -Force | Out-Null
}

$apiKey = Read-Host "Enter ElevenLabs API key"
$env:ELEVEN_LABS_API_KEY = $apiKey
$keyPath = Join-Path $credentialDir "ElevenLabs.key"
Set-Content -Path $keyPath -Value $apiKey -Encoding UTF8
Write-Host "ElevenLabs API key configured:" -ForegroundColor Green
Write-Host "Current session: $apiKey" -ForegroundColor Gray
Write-Host "API key saved to $keyPath" -ForegroundColor Gray
Write-Host "" -ForegroundColor Gray
Write-Host "Now you can run:" -ForegroundColor Cyan
Write-Host "cd $PSScriptRoot" -ForegroundColor Cyan
Write-Host "python elevenlabs_config.py list" -ForegroundColor Cyan
