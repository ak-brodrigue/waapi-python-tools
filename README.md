# waapi-python-tools

This repository is a collection of tools to be used inside Audiokinetic Wwise. The tools use WAAPI (Wwise Authoring API) and Python to perform several automated tasks.

## Requirements
* Python 3.6+
* Running instance of Wwise.exe with the Wwise Authoring API enabled (Project > User Preferences... > Enable Wwise Authoring API)
* waapi-client python project installed

## Setup

We recommend to use the Python Launcher for Windows which is installed with Python 3 from python.org.

### Install Python 3.6

* Install Python 3.6 from: https://www.python.org/downloads/

### Install waapi-client

* **Windows**: `py -3 -m pip install waapi-client`
* **Other platforms**: `python3 -m pip install waapi-client`

Additional instructions can be found at:
https://pypi.org/project/waapi-client/

## Running the script

* **Windows**: `py -3 <tool-name>`
* **Other platforms**: `python3 <tool-name>`

Replace `<tool-name>` by the name of the folder you want to use.

## More information

To learn more about WAAPI:
https://www.audiokinetic.com/library/edge/?source=SDK&id=waapi.html


To learn more about using Python with WAAPI:
https://www.audiokinetic.com/library/edge/?source=SDK&id=waapi_client_python_rpc.html