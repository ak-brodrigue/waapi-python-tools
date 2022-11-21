# auto-create-events

Automatically create play events on the selected objects and replicate the same work unit hierarchy on the event hierarchy. This is useful in the context of multiple users to avoid modifying the Default Work Unit.

## Overview
```
usage: [-h] [GUID ...]

Automatically create new event from the selection and replicate the work unit hierarchy.

positional arguments:
  GUID      One or many guid of the form {01234567-89ab-cdef-0123-4567890abcde}. 
            The script retrieves the current selected if no GUID specified.
```

## Requirements

 * Wwise 2022.1.x+
 * Python 3.6+
 * Python packages:

    `py -3 -m pip install waapi-client`
    
  

## Instructions

**Note**: Refer to installation instructions in [waapi-python-tools](../README.md).

1. Select objects from the Actor-Mixer Hierarchy.
2. Right click and select **Auto Create Event(s) with Work Units**.


