param(
  [int]$Count = 3,
  [int]$Duration = 45,
  [int]$DelayBetween = 5
)

if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
  Write-Host "Virtualenv not found. Create and activate .venv first." -ForegroundColor Red
  exit 1
}

Write-Host "Starting batch: Count=$Count, Duration=$Duration sec" -ForegroundColor Cyan

for ($i = 1; $i -le $Count; $i++) {
  $title = "SCARIFY Transmission Batch $i - $(Get-Date -Format yyyyMMdd_HHmmss)"
  Write-Host "`n=== Generating video $i/$Count: $title ===" -ForegroundColor Yellow

  python .\scarify_cli.py generate --duration $Duration --theme "batch_$i"
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Generation failed for item $i. Aborting batch." -ForegroundColor Red
    exit 1
  }

  $outdir = Join-Path (Get-Location) "scarify\Output\YouTubeReady"
  if (-not (Test-Path $outdir)) {
    Write-Host "Output dir not found: $outdir" -ForegroundColor Red
    exit 1
  }

  $video = Get-ChildItem $outdir -Filter "SCARIFY_*.mp4" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if (-not $video) {
    Write-Host "No generated video found after generation step." -ForegroundColor Red
    exit 1
  }

  Write-Host "Uploading: $($video.FullName) (if credentials are present)" -ForegroundColor Cyan

  # If credentials are not present this will fail; you can remove the upload line to only generate.
  python .\scarify_cli.py upload --title $title --auto-find

  if ($LASTEXITCODE -ne 0) {
    Write-Host "Upload failed for $($video.Name). Continuing to next item." -ForegroundColor Red
  } else {
    Write-Host "Uploaded: $title" -ForegroundColor Green
  }

  Start-Sleep -Seconds $DelayBetween
}

Write-Host "`nBatch complete." -ForegroundColor Green