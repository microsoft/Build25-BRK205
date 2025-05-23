function Get-DirectoryHash($directoryPath) {
    $hashes = Get-ChildItem -Path $directoryPath -Recurse -File |
        Sort-Object FullName |
        ForEach-Object {
            $fileHash = Get-FileHash $_.FullName -Algorithm SHA256
            "$($fileHash.Hash)`t$($_.FullName)"
        }

    $concatenated = ($hashes -join "`n")
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($concatenated)
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $finalHash = $sha256.ComputeHash($bytes)
    -join ($finalHash | ForEach-Object { $_.ToString("x2") })
}
