# CLI Demo

CLI Demo has three parts:
1. CLI commands: available in the video itself.
1. Incremental deployment: code is inside the .scripts folder
1. Connect to Git: both python and powershell scripts available.

# Incremental deployment
To try this, first make sure you run the scripts from the cli_demo folder.

First, clean your envirenment using:

```
powershell ./.scripts/clean-local-env.ps1
```

Second, export workspace by name:

```
powershell ./.scripts/export-workspace.ps1 <workspace name>
```

Thirds, make a real change in one of the items, a notebook for example;

Fourth, run the Import-Changes command, provide a workspace name.

```
powershell ./.scripts/import-changes.ps1 <workspace name>
```

# Connect to git scripts

These scripts use the **fab api** command to call Fabric API of Connect-Workspace-To-Git.
