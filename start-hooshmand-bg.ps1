# Start Hooshmand in the BACKGROUND so it keeps running after you close this
# window. Requires that launch-windows.ps1 has been run once (to create venv).
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$py = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "venv not found. Run .\launch-windows.ps1 once first, then use this." -ForegroundColor Yellow
    exit 1
}

New-Item -ItemType Directory -Force -Path "logs" | Out-Null

# Already running?
$pidFile = Join-Path $PSScriptRoot "logs\server.pid"
if (Test-Path $pidFile) {
    $existing = Get-Content $pidFile
    if (Get-Process -Id $existing -ErrorAction SilentlyContinue) {
        Write-Host ("Hooshmand already running (PID " + $existing + ") at http://127.0.0.1:7000")
        exit 0
    }
}

$proc = Start-Process -FilePath $py `
    -ArgumentList "-m","uvicorn","app:app","--host","127.0.0.1","--port","7000" `
    -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput "logs\server.out.log" `
    -RedirectStandardError  "logs\server.err.log"

$proc.Id | Out-File -Encoding ascii $pidFile
Start-Sleep -Seconds 2
Write-Host ("Hooshmand started in background (PID " + $proc.Id + ").") -ForegroundColor Green
Write-Host "Open:  http://127.0.0.1:7000"
Write-Host "Logs:  logs\server.out.log  /  logs\server.err.log"
Write-Host "Stop:  .\stop-hooshmand.ps1"
