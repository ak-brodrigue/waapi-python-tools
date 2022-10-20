# auto-trim-sources

Automatically trim sources based on the specified decibel threshold. Optionally add a fade in or fade out.

## Overview
```
usage: . [-h] [--threshold_begin [THRESHOLD_BEGIN]] [--threshold_end [THRESHOLD_END]] [--trim_begin [TRIM_BEGIN]] [--trim_end [TRIM_END]] [--fade_begin [FADE_BEGIN]] [--fade_end [FADE_END]] [GUID ...]

Automatically trim the sources for specified objects (ID).

positional arguments:
  GUID             One or many guid of the form:
                   "{01234567-89ab-cdef-0123-4567890abcde}". 
                   The script retrieves the current selected if no GUID specified.
optional arguments:
  -h, --help            show this help message and exit

  --threshold_begin [THRESHOLD_BEGIN]
    Threshold in decibels under which the begin is trimmed. (Default:-40)

  --threshold_end [THRESHOLD_END]
    Threshold in decibels under which the end is trimmed. (Default:-30)

  --trim_begin [TRIM_BEGIN]
    Trim the begin of the sources (Default:True)

  --trim_end [TRIM_END]
    Trim the end of the sources (Default:True)

  --fade_begin [FADE_BEGIN]
    Fade duration when trimming begin (Default:0)

  --fade_end [FADE_END]
    Fade duration when trimming end (Default:0.02)
```
## Requirements

* Wwise 2022.1.x+

## Instructions

**Note**: Refer to installation instructions in [waapi-python-tools](../README.md).

1. Select objects from the Actor-Mixer Hierarchy.
2. Right click and select **Auto Trim Sources**.


