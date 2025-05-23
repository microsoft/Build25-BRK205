. "$PSScriptRoot\env.ps1"
. "$PSScriptRoot\utils.ps1"

# Check if $itemsPath exists and delete it
if (Test-Path $itemsPath) {
    Write-Host "*  Deleting items path at $itemsPath..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force -Path $itemsPath
}

# Check if $hashFilePath exists and delete it
if (Test-Path $hashFilePath) {
    Write-Host "*  Deleting hash file at $hashFilePath..." -ForegroundColor Yellow
    Remove-Item -Force -Path $hashFilePath
}

Write-Host "*  Local environment cleaned successfully." -ForegroundColor Green

