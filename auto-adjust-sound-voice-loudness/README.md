# auto-adjust-sound-voice-loudness

This script is a utility tool for managing audio consistency across languages in a Wwise project. It adjusts the Make-Up Gain of Sound Voice sources in non-reference languages to align their loudness with the reference language. The tool supports both momentary max and integrated loudness measurements and applies corrections automatically.

## Features

* Analyze and adjust loudness across all or specified languages in the Wwise project.
* Define custom paths for targeting specific Sound Voice objects.
* Choose between momentaryMax or integrated loudness measurements for adjustments.
* Automatically apply calculated Make-up Gain values to align loudness with the reference language.

## Overview
```
usage: . [-h] [--language [LANGUAGE]] [--path [PATH]]
         [--loudness {momentaryMax,integrated}]

Automatically adjust the loudness of Sound Voice sources in your Wwise project   
to align with the reference language, ensuring consistent audio levels across    
languages.

options:
  -h, --help            show this help message and exit
  --language [LANGUAGE]
                        Optional. Specify the language to validate (e.g., en,    
                        fr). If omitted, all languages will be validated
                        against the reference language.
  --path [PATH]         Optional. Specify the path to enumerate Sound Voice      
                        objects (e.g., "\Actor-Mixer
                        Hierarchy\Character\Voices"). If omitted, the entire     
                        project is scanned.
  --loudness {momentaryMax,integrated}
                        Optional. Specify the loudness measurement to use        
                        (momentaryMax or integrated). Default is momentaryMax.
```

## Requirements

 * Wwise 2023.1.0+
 * Python 3.6+
 * Python packages:

    `py -3 -m pip install waapi-client`
    
## Instructions

**Note**: Refer to installation instructions in [waapi-python-tools](../README.md).

1. Open a Wwise project.
2. Run the script.


## Examples

Adjust all languages using the default loudness type (momentaryMax):

```
python adjust_loudness.py
```

Adjust the French language only:

```
python adjust_loudness.py --language fr
```

Adjust languages within a specific path using integrated loudness:

```
python adjust_loudness.py --path "\Actor-Mixer Hierarchy\Characters" --loudness integrated
```