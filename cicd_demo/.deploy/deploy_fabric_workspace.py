"""Deploy workspace to Fabric leveraging fabric-cicd"""

import argparse
from pathlib import Path

from azure.identity import AzureCliCredential

from fabric_cicd import (
    FabricWorkspace,
    publish_all_items,
    unpublish_all_orphan_items,
    append_feature_flag,
)

# Establish parser for command line arguments
parser = argparse.ArgumentParser(description="Input Variables")
parser.add_argument("--workspace_name", type=str, required=True)
parser.add_argument("--item_type_in_scope", nargs="+", required=True)
parser.add_argument("--environment", type=str, required=True)
args = parser.parse_args()

# Enable shortcut publish
append_feature_flag("enable_shortcut_publish")

# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_name=args.workspace_name,
    environment=args.environment,
    repository_directory=str(Path(__file__).resolve().parent.parent / "workspace"),
    item_type_in_scope=args.item_type_in_scope,
    token_credential=AzureCliCredential(),
)

# Publish all items defined in item_type_in_scope
publish_all_items(target_workspace)

# Unpublish all items defined in item_type_in_scope not found in repository
unpublish_all_orphan_items(target_workspace)
