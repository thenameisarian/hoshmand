# Register Hooshmand as a background Scheduled Task that runs at logon and
# survives closing any window, logging out, and reboots. Run this ONCE.
# Re-run to update. If it complains about access, run it in an *elevated*
# PowerShell (Run as Administrator).
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$py = Join-Path $PSScriptRoot "venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "venv not found. Run .\launch-windows.ps1 once first." -ForegroundColor Yellow
    exit 1
}

$action  = New-ScheduledTaskAction -Execute $py `
    -Argument "-m uvicorn app:app --host 127.0.0.1 --port 7000" `
    -WorkingDirectory $PSScriptRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries -StartWhenAvailable `
    -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit ([TimeSpan]::Zero)

Register-ScheduledTask -TaskName "Hooshmand" -Action $action -Trigger $trigger `
    -Settings $settings -Description "Hooshmand assistant (uvicorn) background server" -Force

Start-ScheduledTask -TaskName "Hooshmand"
Start-Sleep -Seconds 3
Write-Host "Registered and started scheduled task 'Hooshmand'." -ForegroundColor Green
Write-Host "Open: http://127.0.0.1:7000"
Write-Host ""
Write-Host "Manage it later with:"
Write-Host "  Start-ScheduledTask Hooshmand     # start"
Write-Host "  Stop-ScheduledTask  Hooshmand     # stop"
Write-Host "  Unregister-ScheduledTask Hooshmand -Confirm:`$false   # remove"
