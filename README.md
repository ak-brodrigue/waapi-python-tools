# waapi-python-tools

This repository is a collection of tools to be used inside Audiokinetic Wwise. The tools use WAAPI (Wwise Authoring API) and Python to perform several automated tasks.

Refer to **General Setup Instructions** below, then find the specific instructions README.md in the sub-folders.

## Requirements
* Python 3.6+
* Running instance of Wwise.exe with the Wwise Authoring API enabled (Project > User Preferences... > Enable Wwise Authoring API)
* **waapi-client** python project installed

## General Setup Instructions

We recommend to use the Python Launcher for Windows which is installed with Python 3 from python.org.

### Install Python 3.6

* Install Python 3.6 or greater from: https://www.python.org/downloads/

### Install waapi-client

* **Windows**: `py -3 -m pip install waapi-client`
* **Other platforms**: `python3 -m pip install waapi-client`

Additional instructions can be found at:
https://pypi.org/project/waapi-client/

### Installing the Command Add-ons (2019.2.x+)

1. Ensure the folder `%APPDATA%\Audiokinetic\Wwise\Add-ons` is present. Create `Add-ons` if not present.
2. Download this whole repository zip file from GitHub.
3. Unzip the content from `waapi-python-tools` folder inside `Add-ons`.
4. Restart Wwise or use the command **Reload Commands**

At the end, the following file structure should be present:  
`%APPDATA%\Audiokinetic\Wwise\Add-ons\Commands\waapi-python-tools.json`

### Installing for External Editors (2018.1.x)

1. Download this whole repository zip file from GitHub.
2. Unzip the content of zip file on your computer.
3. In Wwise, open **Project > User Preferences**.
4. Add `<tool-name>.cmd` in the **External Editors** list.

## Running the script

* **Windows**: `py -3 <tool-name>`
* **Other platforms**: `python3 <tool-name>`

Replace `<tool-name>` by the name of the folder you want to use.

## More information

To learn more about WAAPI:
https://www.audiokinetic.com/library/edge/?source=SDK&id=waapi.html

To learn more about using Python with WAAPI:
https://www.audiokinetic.com/library/edge/?source=SDK&id=waapi_client_python_rpc.html

To learn more about Command Add-ons:
https://www.audiokinetic.com/library/edge/?source=SDK&id=defining_custom_commands.html