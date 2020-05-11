from waapi import WaapiClient, CannotConnectToWaapiException
import argparse, os, subprocess

# Define arguments for the script
parser = argparse.ArgumentParser(description='Generate text to speech from Wwise object ID')
parser.add_argument('id', metavar='GUID', nargs='+', help='one or multiple guid of the form \{01234567-89ab-cdef-0123-4567890abcde\}')
parser.add_argument('--original', help='path to the original folder',required=True)

args = parser.parse_args()

try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        # Obtain more information for all objects being passed
        get_args = {
            "from": {"id": args.id},
        }
        options = {
            "return": ['name', 'notes','type', '@IsVoice', 'path']
        }
        get_result = client.call("ak.wwise.core.object.get", get_args, options=options)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        speak_script_path = os.path.join( script_dir, 'speak.ps1')

        imports = []

        for obj in get_result['return']:

            language_dir = "Voices/English(US)" if obj['@IsVoice'] else "SFX"
            wav_file = os.path.join(args.original, language_dir, obj['name']) + '.wav'
            
            print('Generating {0}...'.format(wav_file))

            # Execute the powershell script with the Speech Synthesizer from .NET
            subprocess.check_output(["powershell.exe",  '-executionpolicy', 'bypass', '-File', speak_script_path, wav_file, obj['notes']])

            imports.append({ 
                "audioFile": wav_file,
                "objectPath": obj['path'] + '\\<AudioFileSource>' + obj['name'],
                "importLanguage": "English(US)" if obj['@IsVoice'] else "SFX" 
                })

        # Import the generated wav files to Wwise
        import_args = {
            "importOperation": "useExisting",
            "default": {},
            "imports": imports
        }
        client.call("ak.wwise.core.audio.import",import_args)


except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")