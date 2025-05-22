# CICD Demo Directory

This directory contains resources and scripts for building and deploying Microsoft Fabric workspaces as part of the Build demo.

## Structure

- `.deploy/` – Deployment automation scripts (Python) for workspace sync and publish.
- `.pipelines/` – Azure DevOps pipeline YAML for CI/CD.
- `workspace/` – Sample workspace files, including notebooks, pipelines, variable libraries, and lakehouse metadata.

## Important Notes

- **Sample Files:** The `workspace` subdirectory contains sample items for demonstration purposes. These files may reference connection IDs and resources that are not present in your own tenant.
- **Connection IDs:** You may need to update connection IDs in the sample files to match connections available in your environment.
- **git_credential_body:** The connection id in the git credential body is defined within your tenant, and is a new ADO connection that needs to be configured.  Docs will publish once this goes live.
- **Service Principal (SPN) Support:** SPN authentication is not fully supported in all regions. The demo scripts and automation may not work until SPN support is rolled out to your region.

## Usage

1. Review and update connection IDs in the workspace files as needed.
2. Use the deployment scripts and pipeline definitions to automate workspace deployment.
3. If you encounter authentication issues, verify SPN support in your region.