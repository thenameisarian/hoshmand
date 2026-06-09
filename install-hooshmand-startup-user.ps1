# No-admin persistence: add Hooshmand to your personal Startup folder so it
# launches in the background at every login (and start it now). Run ONCE.
# Remove later by deleting the shortcut it reports, or run with -Remove.
param([switch]$Remove)
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

$startup = [Environment]::GetFolderPath('Startup')
$lnkPath = Join-Path $startup "Hooshmand.lnk"

if ($Remove) {
    if (Test-Path $lnkPath) { Remove-Item $lnkPath -Force; Write-Host "Removed startup shortcut." }
    else { Write-Host "No startup shortcut found." }
    return
}

$bg = Join-Path $PSScriptRoot "start-hooshmand-bg.ps1"
if (-not (Test-Path $bg)) { Write-Host "start-hooshmand-bg.ps1 missing." -ForegroundColor Yellow; exit 1 }

$ws = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut($lnkPath)
$lnk.TargetPath = "powershell.exe"
$lnk.Arguments  = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$bg`""
$lnk.WorkingDirectory = $PSScriptRoot
$lnk.WindowStyle = 7   # minimized
$lnk.Description = "Start Hooshmand server in background at login"
$lnk.Save()
Write-Host "Created startup shortcut: $lnkPath" -ForegroundColor Green

# start it now too
powershell -ExecutionPolicy Bypass -File $bg
Write-Host ""
Write-Host "Hooshmand will now auto-start at every login."
Write-Host "To undo:  powershell -ExecutionPolicy Bypass -File .\install-hooshmand-startup-user.ps1 -Remove"
