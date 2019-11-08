# auto-rename-container

Automatically rename a container based on the name of its children.

## Usage

### Add the command to Wwise

Refer to [Defining custom commands](https://www.audiokinetic.com/library/edge/?source=SDK&id=defining__custom__commands.html) in the Wwise SDK documentation.

### Example command definition
```json
{
    "commands": [
        {
            "id": "ak.auto_rename_container",
            "displayName": "Auto Rename Container",
            "defaultShortcut": "Alt+R",
            "program": "pyw",
            "startMode": "SingleSelectionSingleProcess",
            "args": "C:\\waapi-python-tools\\auto-rename-container",
            "cwd": "",
            "contextMenu": {
                "basePath": "Add-ons"
            }
        }
    ]
}
```