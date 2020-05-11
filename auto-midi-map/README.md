# auto-midi-map

Automatically structure the children of Wwise Blend Container and set the MIDI properties based on a naming convention.

**Attention**: The project works well with a specific file name convention. Please feel
free to modify in order to support other conventions.

## Overview

It is possible to implement a sample-based MIDI instrument in Wwise directly in the Actor-Mixer hierarchy.  However, it can be a tedious task. This tool aims to ease the setup of such complex structures by setting up automatically the structure for you after you imported the sounds.

## Requirements

* Wwise 2019.2.x+ for using with the **Command Add-ons** (custom menus).
* Wwise 2018.1.11+ for using auto-midi-map.cmd with **External Editors**.

## Instructions

**Note**: Refer to installation instructions in [waapi-python-tools](../README.md).

1. Create a **Blend container**.
2. Import sample sounds in the container. The sounds must contain a note name (C,D,E,F,G,A,B, then # or b, then the octave).
3. Select the **Blend Container**.
4. Right click and select **Auto MIDI map** or use `auto-midi-map.cmd` as an **External Editor**.

**Note**: If multiple sounds have the same note, a random container will be created.

Example of file names:

```(sh)
Flute_a#3.wav
Flute_a#4.wav
Flute_c3.wav
Flute_c4.wav
Flute_e3.wav
Flute_e4.wav
Flute_g3.wav
Flute_g4.wav
```
