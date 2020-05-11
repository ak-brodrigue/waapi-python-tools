# Text To Speech From Wwise

## Overview

This sample demonstrates how to generate WAV files using text-to-speech from Wwise directly.

Demonstrates:

- WAAPI [ak.wwise.core.object.get](https://www.audiokinetic.com/library/edge/?source=SDK&id=ak__wwise__core__object__get.html)
- WAAPI [ak.wwise.core.audio.import](https://www.audiokinetic.com/library/edge/?source=SDK&id=ak__wwise__core__audio__import.html)
- Text to Speech using Windows Powershell and SpeechSynthesizer
- Wwise [Command Add-ons](https://www.audiokinetic.com/fr/library/edge/?source=SDK&id=defining_custom_commands.html)

## Requirements

- Wwise 2019.2.x or more recent
- [Python 3.6 or more recent](https://www.python.org/downloads/)
- [waapi-client python library](https://pypi.org/project/waapi-client/)
- Windows 10 and Windows Powershell

## Setup

1. Install python 3.6 or more recent
2. Install python dependencies:

    `py -3 -m pip install waapi-client`
3. Create the `Add-ons` folder under `%APPDATA%\Audiokinetic\Wwise`
4. Unzip the git repository under: `%APPDATA%\Audiokinetic\Wwise\Add-ons`

   **Note**: ensure the `Commands` and `waapi-text-to-speech` folders are directly located under the `Add-ons` folder.

5. Restart Wwise or run the command **Command Add-ons/Reload**

## How to use

1. Create a **Sound SFX** or **Sound Voice** object in the project.
2. Type some text in the **Notes** field.
3. Right-click the object, and select **Generate Text-to-Speech**.

## How it works

The source code is located in [main.py](waapi-text-to-speech/main.py).

This script is using WAAPI and the Command Add-ons system. It will retrieve the selection from executed command and generate a WAV file for each selected Sound objects using Windows text to speech. The WAV files will be automatically imported in the project with WAAPI.

Refer to this [blog article](https://blog.audiokinetic.com/waapi-three-open-source-projects-for-wwise-authoring-api/) for more information.