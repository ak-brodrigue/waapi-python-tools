# New Synth One

## Overview

WAAPI SFX is a python script that generate Wwise Sound SFX objects in batch. Each Sound SFX is using a Synth One source plug-in, and the objects that are generated make great use of RTPCs and random modulation.

The script is a demonstration of the [ak.wwise.core.object.set](
https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_set.html) function in WAAPI.

## Prerequisites

* Wwise 2022.1.0 or more recent
- [Python 3.6 or more recent](https://www.python.org/downloads/)
- [waapi-client python library](https://pypi.org/project/waapi-client/)

## How to use

* Download or clone the repository
* Start Wwise and open a project
* Run the script:
 `py -3 waapi-sfx.py`
* Play the new sounds in the `\Actor-Mixer Hierarchy\Default Work Unit`

## Learn More

- [WAAPI Reference](https://www.audiokinetic.com/library/edge/?source=SDK&id=waapi_functions_index.html) - Learn the details of each WAAPI functions.
- [ak.wwise.core.object.set](
https://www.audiokinetic.com/library/edge/?source=SDK&id=ak_wwise_core_object_set.html) - Learn more about ak.wwise.core.object.set.
- [Importing Audio Files and Creating Structures](https://www.audiokinetic.com/library/edge/?source=SDK&id=waapi_import.html) - Learn how to create Wwise structures.
- [Synth One Reference](https://www.audiokinetic.com/library/edge/?source=SDK&id=wwiseobject_source_wwise_synth_one.html) - Learn about Synth One properties.
- [Wwise Object Reference](https://www.audiokinetic.com/library/edge/?source=SDK&id=wobjects_index.html) - Learn about Wwise objects and their properties.