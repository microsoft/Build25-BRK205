param (
    [Parameter(Mandatory=$true)]
    [Alias("wid")]
    [string]$WorkspaceId
)

Write-Host
Write-Host "Connecting Git repository to workspace $WorkspaceId..." -ForegroundColor Green
Write-Host

$json = @"
{
  "gitProviderDetails": {
    "organizationName": "fabricmsit02262025ali",
    "projectName": "ProjectTest",
    "gitProviderType": "AzureDevOps",
    "repositoryName": "ProjectTest",
    "branchName": "Customers/CustomerB",
    "directoryName": ""
  }
}
"@

Write-Host "Command: fab api workspaces/$WorkspaceId/git/connect -X post -i <json_payload>" -ForegroundColor Blue

fab api "workspaces/$WorkspaceId/git/connect" -X post -i @"
{
  "gitProviderDetails": {
    "organizationName": "fabricmsit02262025ali",
    "projectName": "ProjectTest",
    "gitProviderType": "AzureDevOps",
    "repositoryName": "ProjectTest",
    "branchName": "Customers/CustomerB",
    "directoryName": ""
  }
}
"@
