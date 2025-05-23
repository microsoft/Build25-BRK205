param (
    [string]$WorkspaceName
)

# 1. Load environment and utility functions
. "$PSScriptRoot\env.ps1"
. "$PSScriptRoot\utils.ps1"

# Check if workspace name parameter was provided
if ([string]::IsNullOrEmpty($WorkspaceName)) {
    Write-Host -NoNewline -ForegroundColor Red "Error: "
    Write-Host "Workspace name parameter is required." -ForegroundColor White
    Write-Host "Usage: .\import-changes.ps1 <WorkspaceName>" -ForegroundColor White
    exit 1
}

# Append .Workspace to the workspace name if it doesn't already end with it
if (-not $WorkspaceName.EndsWith(".Workspace")) {
    $WorkspaceName = "$WorkspaceName.Workspace"
    Write-Host -NoNewline -ForegroundColor Green "* "
}

# 2. Ensure previous hash file exists
if (!(Test-Path $hashFilePath)) {
    "" | Out-File $hashFilePath
}

# 3. Load previous hashes
$previousHashes = @{}
if (Test-Path $hashFilePath) {
    Get-Content $hashFilePath | ForEach-Object {
        $parts = $_ -split "="
        if ($parts.Length -eq 2) {
            $previousHashes[$parts[0]] = $parts[1]
        }
    }
}

# 4. Compute current hashes and compare
$currentHashes = @{}
$changedItems = @()

Get-ChildItem $itemsPath -Directory | ForEach-Object {
    $itemName = $_.Name
    $itemFullPath = $_.FullName
    $dirHash = Get-DirectoryHash $itemFullPath
    $currentHashes[$itemName] = $dirHash

    if (-not $previousHashes.ContainsKey($itemName) -or $previousHashes[$itemName] -ne $dirHash) {
        $changedItems += $itemName
    }
}

# 5. Check if any items have changed, and write a message accordingly.
if ($changedItems.Count -eq 0) {
    Write-Host "No items have changed. Exiting..."
    exit
} else {
    Write-Host "Changed items: $changedItems. Proceeding with fab import..."
}

## TIME TO USE THE FABRIC CLI -----------------------------------------------
# 6. Import only changed items - that have different hashes
foreach ($item in $changedItems) {
    Write-Host "Importing changed item: $item"
    fab import "$WorkspaceName/$item" -i "$itemsPath\$item" -f
}

# 7. Save updated hashes
$currentHashes.GetEnumerator() | ForEach-Object {
    "$($_.Key)=$($_.Value)"
} | Set-Content $hashFilePath
