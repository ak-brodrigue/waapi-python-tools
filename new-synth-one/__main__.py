from waapi import WaapiClient, CannotConnectToWaapiException
from pprint import pprint
from random import uniform, randrange, choice
import argparse, traceback

# Define arguments for the script
parser = argparse.ArgumentParser(description='Automatically trim the sources for specified objects (ID).')
parser.add_argument('id', metavar='GUID', nargs='?', help='One guid of the form {01234567-89ab-cdef-0123-4567890abcde}. The script retrieves the current selected if no GUID specified.')
parser.add_argument('--count', const=1, default=10, type=int, nargs='?', help='Number of instances to generate.')

args = parser.parse_args()

effect = []

def RandomEffect():
    # return the id of one of the ShareSet effect from the project
    return choice(effects)['id']

def ADSR(property, a,d,s,r, y_min, y_max, stop):
    # Create a RTPC entry with custom ADSR envelope object
    return {
        "type": "RTPC",
        "name": "",
        "@Curve": {
            "type": "Curve",
            "points": [
                {
                    "x": 0,
                    "y": y_min,
                    "shape": "Linear"
                },
                {
                    "x": 1,
                    "y": y_max,
                    "shape": "Linear"
                }
            ]
        },
        "@PropertyName": property,
        "@ControlInput": {
            # Envelope properties
            "type":"ModulatorEnvelope",
            "name":"ENV",
            "@EnvelopeAttackTime": a,
            "@EnvelopeAutoRelease": True,
            "@EnvelopeStopPlayback": stop,
            "@EnvelopeDecayTime": d,
            "@EnvelopeReleaseTime": r,
            "@EnvelopeSustainTime": s
        }
    }

def LFO(property, freq, y_min, y_max):
    # Create a RTPC entry with a custom LFO modulator
    return {
        "type": "RTPC",
        "name": "",
        "@Curve": {
            "type": "Curve",
            # "@Flags": 3,
            "points": [
                {
                    "x": 0,
                    "y": y_min,
                    "shape": "Linear"
                },
                {
                    "x": 1,
                    "y": y_max,
                    "shape": "Linear"
                }
            ]
        },
        "@PropertyName": property,
        "@ControlInput": {
            # LFO properties
            "type":"ModulatorLfo",
            "name":"LFO",
            "@LfoAttack": 0,
            "@LfoDepth": uniform(0,100),
            "@LfoFrequency": freq,
            "@LfoWaveform": randrange(0,6),
            "@LfoPWM": uniform(10,90)
        }
    }

def Random(property, y_min, y_max):
    # Create a RTPC entry with a custom Random LFO modulator
    return {
        "type": "RTPC",
        "name": "",
        "@Curve": {
            "type": "Curve",
            "points": [
                {
                    "x": 0,
                    "y": y_min,
                    "shape": "Linear"
                },
                {
                    "x": 1,
                    "y": y_max,
                    "shape": "Linear"
                }
            ]
        },
        "@PropertyName": property,
        "@ControlInput": {
            "type":"ModulatorLfo",
            "name":"RAND",
            "@LfoWaveform": 5,
            "@LfoFrequency":0.01
        }
    }

def RandomPoints(x_min, x_max, y_min, y_max, count):
    # Return an array of random points
    points = [
        {
            "x": x_min,
            "y": uniform(y_min, y_max),
            "shape": "Linear"
        },
        {
            "x": x_max,
            "y": uniform(y_min, y_max),
            "shape": "Linear"
        }
    ]
    for x in range(0,count-2):
        points.insert(1+x,
            {
                "x": uniform(x_min, x_max),
                "y": uniform(y_min, y_max),
                "shape": "Linear"
            })

    points.sort(key=lambda p:p["x"])
    return points

def RandomTimeCurve(property, duration, y_min, y_max, count):
    # Return a RTPC entry with random time curve
    return {
        "type": "RTPC",
        "name": "",
        "@Curve": {
            "type": "Curve",
            "points": RandomPoints(0, duration, y_min, y_max, count)
        },
        "@PropertyName": property,
        "@ControlInput": {
            # Time modulator properties
            "type":"ModulatorTime",
            "name":"TimeMod",
            "@TimeModDuration": max(0.1, duration),
            "@EnvelopeStopPlayback": False
        }
    }

def Modulation(property, duration, y_min, y_max):
    # Create a random modulation RTPC entry
    
    pick = randrange(0,4)
    start_ratio = uniform(0,1)
    range = (y_max-y_min)
    y_min = y_min + range*start_ratio
    y_max = y_max - range*(1-start_ratio)*uniform(0,1)

    if pick == 0:
        return RandomTimeCurve(property, duration, y_min, y_max, randrange(2,9))
    elif pick == 1:
        return Random(property, y_min, y_max)
    elif pick == 2:
        return LFO(property, uniform(0.01, 30), y_min, y_max)
    elif pick == 3:
        attack = duration - uniform(0,duration)
        release = duration - attack
        return ADSR(property, attack, 0, 0, release, y_min, y_max, False)

def Sound(i, average_duration):
    # Return a Sound SFX object with a Synth One source

    attack = uniform(0.01, average_duration/4)
    decay = uniform(0.01, average_duration/4)
    release = uniform(0.01, average_duration/4)
    sustain = average_duration/4
    duration = attack + decay + average_duration/4 + release

    return {
        "type":"Sound",
        "name":"FX" + str(i),
        "children":[
            {
                "type":"SourcePlugin",
                "name":"WSFX",
                "classId": 9699330, # synth one: https://www.audiokinetic.com/library/edge/?source=SDK&id=wwiseobject_source_wwise_synth_one.html
                "@BaseFrequency": uniform(100, 1000),
                "@Osc1Waveform": randrange(0,4),
                "@Osc2Waveform": randrange(0,4),
                "@NoiseShape": randrange(0,4),
                "@NoiseLevel": uniform(-12, 0),
                "@RTPC":[
                    Modulation("Osc1Transpose", duration, -1200, 1200),
                    Modulation("Osc2Transpose", duration, -1200, 1200),
                    Modulation("NoiseLevel", duration, -96, 6),
                    Modulation("Osc1Pwm", duration, 1, 99),
                    Modulation("Osc2Pwm", duration, 1, 99),
                    Modulation("FmAmount", duration, 0, 100),
                ],
            }
        ],
        "@Effect0": RandomEffect(),
        "@RTPC":[
            ADSR("Volume", attack, decay, sustain, release, -96, 0, True),
            Modulation("Lowpass", duration, 0, 20),
            Modulation("Highpass", duration, 0, 20),
        ],
    }

def Generate(location, num_sounds, start_index):
    # Create the sounds using ak.wwise.core.object.set
    
    set_args = {
        "objects": [
            {
                "object": location,
                "children": list(map( lambda i : Sound(i, uniform(0.4, 1.5)), range(start_index,start_index+num_sounds)))
            },

        ],
        "onNameConflict": "rename",
        "listMode":"replaceAll"
    }

    # Call WAAPI to create the objects
    client.call("ak.wwise.core.undo.beginGroup")
    client.call("ak.wwise.core.object.set", set_args)
    client.call("ak.wwise.core.undo.endGroup", { 'displayName': 'Auto Trim Sources'})

try:

    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        # Obtain all effects from the project
        effects = client.call("ak.wwise.core.object.get", {"waql": '$ from type effect where parent != null and pluginname != "mastering suite"'})["return"]

        selected = []

        # if no ID is passed as argument, use the selected object from the project
        if args.id is None or len(args.id) == 0:
            selected  = map(lambda s: s["id"], client.call("ak.wwise.ui.getSelectedObjects")['objects'])
        else:
            selected = [args.id]

        location = "\\Actor-Mixer Hierarchy\\Default Work Unit"

        # Try to find the best location to create new sounds
        if len(selected) > 0:
            ancestors = client.call("ak.wwise.core.object.get", {"waql": f'$ "{selected[0]}" select this, ancestors where type : "container" or type : "folder" or type : "workunit" and category = "actor-mixer hierarchy"'})["return"]

            if len(ancestors) > 0:
                location = ancestors[0]['id']
        
        # Count how many FX we already have at the location
        siblings = client.call("ak.wwise.core.object.get", {"waql": f'$ "{location}" select children where name = /^FX\\d+/'})["return"]

        Generate(location, args.count, len(siblings))



except Exception as e:
    traceback.print_exc()
    print(str(e))