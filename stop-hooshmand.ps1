# Stop the background Hooshmand server started by start-hooshmand-bg.ps1.
Set-Location -Path $PSScriptRoot
$pidFile = Join-Path $PSScriptRoot "logs\server.pid"

if (Test-Path $pidFile) {
    $serverPid = Get-Content $pidFile
    try {
        Stop-Process -Id $serverPid -Force -ErrorAction Stop
        Write-Host ("Stopped Hooshmand (PID " + $serverPid + ").") -ForegroundColor Green
    } catch {
        Write-Host ("Process " + $serverPid + " was not running.")
    }
    Remove-Item $pidFile -ErrorAction SilentlyContinue
} else {
    Write-Host "No PID file found. Searching for a uvicorn app:app process..."
    Get-CimInstance Win32_Process |
        Where-Object { $_.CommandLine -like '*uvicorn*app:app*' } |
        ForEach-Object {
            Stop-Process -Id $_.ProcessId -Force
            Write-Host ("Stopped PID " + $_.ProcessId)
        }
}
