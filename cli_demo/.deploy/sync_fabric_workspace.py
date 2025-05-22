"""Sync workspace to Fabric leveraging updateFromGit API"""

import argparse
import os

from azure.identity import AzureCliCredential

from fabric_cicd import FabricWorkspace

# Establish parser for command line arguments
parser = argparse.ArgumentParser(description="Input Variables")
parser.add_argument("--workspace_name", type=str, required=True)
args = parser.parse_args()

# Initialize the FabricWorkspace object with the required parameters
# fabric-cicd is being used to simplify authentication to the APIs
target_workspace = FabricWorkspace(
    workspace_name=args.workspace_name,
    repository_directory=".",  # required, but not applicable
    item_type_in_scope=["Notebook"], # required, but not applicable
    token_credential=AzureCliCredential(),
)

# Update Git credentials in Fabric
# https://learn.microsoft.com/en-us/rest/api/fabric/core/git/update-my-git-credentials
git_credential_url = f"{target_workspace.base_api_url}/git/myGitCredentials"
git_credential_body = {
    "source": "ConfiguredConnection",
    "connectionId": "47d1f273-7091-47c4-b45d-df8f1231ea74",
}
target_workspace.endpoint.invoke(method="PATCH", url=git_credential_url, body=git_credential_body)

# Get commit heads from workspace and remote branch
# https://learn.microsoft.com/en-us/rest/api/fabric/core/git/get-status
git_status_url = f"{target_workspace.base_api_url}/git/status"
git_status = target_workspace.endpoint.invoke(method="GET", url=git_status_url)
workspace_head = git_status["body"]["workspaceHead"]
remote_head = os.getenv("BUILD_SOURCEVERSION")

# Force update to sync workspace with remote branch
# https://learn.microsoft.com/en-us/rest/api/fabric/core/git/update-from-git
git_update_url = f"{target_workspace.base_api_url}/git/updateFromGit"
git_update_body = {
    "workspaceHead": f"{workspace_head}",
    "remoteCommitHash": f"{remote_head}",
    "conflictResolution": {
        "conflictResolutionType": "Workspace",
        "conflictResolutionPolicy": "PreferRemote",
    },
    "options": {"allowOverrideItems": True},
}
target_workspace.endpoint.invoke(method="POST", url=git_update_url, body=git_update_body, max_retries=10)
