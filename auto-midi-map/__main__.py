#!/usr/bin/env python3

from waapi import WaapiClient, CannotConnectToWaapiException
from pprint import pprint
from collections import defaultdict
import sys, re, math, os, argparse

# Define arguments for the script
parser = argparse.ArgumentParser(description='Generate text to speech for the specified Wwise object ID.')
parser.add_argument('id', metavar='GUID', nargs='?', help='One guid of the form {01234567-89ab-cdef-0123-4567890abcde}. The script retrieves the current selected if no GUID specified.')

args = parser.parse_args()

notes = {
    'c': 0,
    'c#': 1,
    'db': 1,
    'd': 2,
    'd#': 3,
    'eb': 3,
    'e': 4,
    'f': 5,
    'f#': 6,
    'gb': 6,
    'g': 7,
    'g#': 8,
    'ab': 8,
    'a': 9,
    'a#': 10,
    'bb': 10,
    'b': 11
    }

def note_name_to_number(name):
    note = 60
    match = re.search('(?P<letter>[cdefgabCDEFGAB][#b]?)(?P<octave>[0-9]+)', name)
    if match is not None:
        letter = match.group('letter').lower()
        octave = int(match.group('octave'))

        # Find the note number
        note = notes[letter]
        note = note + (octave + 2) * 12
        
    return note

try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        if args.id is None:
            selected  = client.call("ak.wwise.ui.getSelectedObjects")['objects']
            if len(selected) != 1:
                raise Exception('Only works with a single selection')
            args.id = selected[0]['id']

        # Obtain more information for all objects being passed
        get_args = {
            "from": {"id": [args.id]},
            "transform": [
                {"select": ['children']}
            ]
        }
        options = {
            "return": ['id', 'name','type']
        }
        sounds = client.call("ak.wwise.core.object.get", get_args, options=options)['return']

        # Parse the sound names and find the MIDI notes
        groups = defaultdict(list)
        errors = []
        for child in sounds:
            name = child['name']

            match = re.search('(?P<note>[cdefgabCDEFGAB][#b]?[0-9]+)', name)
            if match is None:
                errors.append('Could not find a note in ' + name)
            else:
                note_number = note_name_to_number(match.group('note'))
                child['note'] = note_number
                groups[note_number].append(child)

        if len(errors) > 0:
            raise Exception('\n'.join(errors))

        # Start the work
        client.call("ak.wwise.core.undo.beginGroup")

        children = []

        # For each group, create a container and move it in
        for note, elements in groups.items():

            if len(elements) == 1:
                children.append(elements[0])
            else:
                # Find common name for parent
                names = list(map(lambda object: object['name'], elements))
                common = os.path.commonprefix(names)
                common = common.rstrip('_ -')

                if not common:
                    common = str(note)

                create_args = {
                    "parent": selected[0]['id'], 
                    "type": 'RandomSequenceContainer', 
                    "name": common, 
                    "onNameConflict": "rename"
                }

                container = client.call("ak.wwise.core.object.create", create_args)
                container['note'] = note

                # Move sounds to the new container
                for element in elements:
                    move_args = {
                        'object': element['id'],
                        'parent': container['id']
                    }
                    client.call("ak.wwise.core.object.move", move_args)

                children.append(container)

        # Try to fill whole between notes & prepare midi settings
        children.sort(key=lambda object: object['note'])
        
        i = 0
        for child in children:
            min = 0
            max = 127
            if i != 0:
                min = children[i - 1]['@MidiKeyFilterMax'] + 1
            if i != len(children) - 1:
                max = child['note'] + math.floor((children[i + 1]['note'] - children[i]['note']) / 2)

            child['@MidiKeyFilterMin'] = min
            child['@MidiKeyFilterMax'] = max
            child['@EnableMidiNoteTracking'] = 1
            child['@MidiTrackingRootNote'] = child['note']
            child['@OverrideMidiNoteTracking'] = 1
            max = 127

            i += 1

        # Set properties
        for child in children:
            for key, value in child.items():
                if key.startswith('@'):
                    set_property_args = {
                        'object': child['id'],
                        'property': key[1:],
                        'value': value
                    }
                    client.call("ak.wwise.core.object.setProperty", set_property_args)
        
        client.call("ak.wwise.core.undo.endGroup", { 'displayName': 'Auto MIDI map'})


except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

except Exception as e:
    print(str(e))
