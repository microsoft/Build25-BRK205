#!/usr/bin/env python3
"""
A script to connect a Git repository to a Microsoft Fabric workspace.
"""
import sys
import json
import subprocess
import os

def connect_git(workspace_id):
    """Connect Git repository to the specified workspace."""
    print("")
    print(f"Connecting Git repository to workspace {workspace_id}...")
    print("")
    
    # The JSON payload
    payload = {
        "gitProviderDetails": {
            "organizationName": "fabricmsit02262025ali",
            "projectName": "ProjectTest",
            "gitProviderType": "AzureDevOps",
            "repositoryName": "ProjectTest",
            "branchName": "Customers/CustomerB",
            "directoryName": ""
        }
    }
    
    # Convert the payload to JSON string
    payload_str = json.dumps(payload)
    
    # Print the command being executed
    print("Command: fab api workspaces/{}/git/connect -X post -i <json_payload>".format(workspace_id))
    
    # Execute the fab command
    try:
        cmd = ["fab", "api", f"workspaces/{workspace_id}/git/connect", "-X", "post", "-i", payload_str]
        subprocess.run(cmd, check=True)
        print("\nGit repository successfully connected!")
    except subprocess.CalledProcessError as e:
        print(f"\nError connecting Git repository: {e}", file=sys.stderr)
        return 1
    
    return 0

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print("Error: Workspace ID is required", file=sys.stderr)
        print(f"Usage: {os.path.basename(sys.argv[0])} <workspace_id>", file=sys.stderr)
        return 1
    
    workspace_id = sys.argv[1]
    return connect_git(workspace_id)

if __name__ == "__main__":
    sys.exit(main())
