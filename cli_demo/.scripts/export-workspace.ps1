param (
    [string]$WorkspaceName
)

# 1. Load environment and utility functions
. "$PSScriptRoot\env.ps1"
. "$PSScriptRoot\utils.ps1"

# Check if workspace name parameter was provided, if so override the default from env.ps1
if ([string]::IsNullOrEmpty($WorkspaceName)) {
    Write-Host -NoNewline -ForegroundColor Red "Error: "
    Write-Host "Workspace name parameter is required." -ForegroundColor White
    Write-Host "Usage: .\export-workspace.ps1 <WorkspaceName>" -ForegroundColor White
    exit 1
}

# Append .Workspace to the workspace name if it doesn't already end with it
if (-not $WorkspaceName.EndsWith(".Workspace")) {
    $WorkspaceName = "$WorkspaceName.Workspace"
    Write-Host -NoNewline -ForegroundColor Green "* "
    Write-Host " Appended .Workspace to the name: $WorkspaceName" -ForegroundColor White
}

# 2. Check if the items path exists, if not, create it
if (!(Test-Path $itemsPath)) {
    Write-Host -NoNewline -ForegroundColor Green "* "
    Write-Host " Creating items path at $itemsPath..." -ForegroundColor White
    New-Item -ItemType Directory -Path $itemsPath -Force | Out-Null
}

## TIME TO USE THE FABRIC CLI -----------------------------------------------
# 3. Export the workspace to the current directory
Write-Host -NoNewline -ForegroundColor Green "* "
Write-Host " Exporting workspace $WorkspaceName to $itemsPath..." -ForegroundColor White
fab export $WorkspaceName -o $itemsPath -f -a

# 4. Compute hashes and write to hash file
Write-Host -NoNewline -ForegroundColor Green "* "
Write-Host " Export complete. Hashes will be initialized." -ForegroundColor White
$hashEntries = Get-ChildItem $itemsPath -Directory | ForEach-Object {
    $itemName = $_.Name
    $itemHash = Get-DirectoryHash $_.FullName
    "$itemName=$itemHash"
}

# 5. Save hashes to file
Write-Host -NoNewline -ForegroundColor Green "* "
Write-Host " Saving hashes to $hashFilePath..." -ForegroundColor White
$hashEntries | Set-Content $hashFilePath

# 6. Write a message indicating completion
Write-Host -NoNewline -ForegroundColor Green "* "
Write-Host " Export complete. Hashes initialized at $hashFilePath." -ForegroundColor White