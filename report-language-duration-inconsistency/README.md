# report-language-duration-inconsistency

This script is a validation tool designed to work with the currently opened Wwise project. It analyzes Sound Voice objects in the project to determine if their playback durations fall within an acceptable ratio range compared to the reference language. The script is particularly useful for validating multi-language audio projects, ensuring consistency in playback durations across different languages.

## Features
* Validate Sound Voice objects against a reference language's playback duration.
* Specify a custom path within the project for validation or scan the entire project.
* Define minimum and maximum acceptable duration ratio thresholds.
* Validate a specific language or all languages in the project.
* Report missing sources or violations of duration thresholds.

## Overview
```
usage: . [-h] [--language [LANGUAGE]] [--path [PATH]] [--min_threshold [MIN_THRESHOLD]] [--max_threshold [MAX_THRESHOLD]]

Validate Sound Voice objects against the reference language's playback duration and report missing sources or violations of duration thresholds.

options:
  -h, --help            show this help message and exit
  --language [LANGUAGE] 
                        Optional. Specify the language to validate (e.g., en, fr). 
                        If omitted, all languages will be validated against the reference language.
  --path [PATH]         Optional. Specify the path to enumerate Sound Voice objects 
                        If omitted, the entire project is scanned.
  --min_threshold [MIN_THRESHOLD]
                        Optional. Minimum accepted duration ratio as a percentage (default: 60).
  --max_threshold [MAX_THRESHOLD]
                        Optional. Maximum accepted duration ratio as a percentage (default: 140).
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

Validate all languages in the project against the reference language:
```
python validate_audio_duration.py
```

Validate the French language:
```
python validate_audio_duration.py --language fr
```

Validate languages under a specific path:

```
python validate_audio_duration.py --path "\Actor-Mixer Hierarchy\Characters"
```

Use custom thresholds for duration ratios:
```
python validate_audio_duration.py --min_threshold 80 --max_threshold 120
```
