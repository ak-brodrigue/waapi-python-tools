from waapi import WaapiClient, CannotConnectToWaapiException
from pprint import pprint
import argparse

# Define arguments for the script
parser = argparse.ArgumentParser(description="Automatically adjust the loudness of Sound Voice sources in your Wwise project to align with the reference language, ensuring consistent audio levels across languages.")
parser.add_argument('--language', const=1, default=None, type=str, nargs='?', help='Optional. Specify the language to validate (e.g., en, fr). If omitted, all languages will be validated against the reference language.')
parser.add_argument('--path', const=1, default=None, type=str, nargs='?', help='Optional. Specify the path to enumerate Sound Voice objects (e.g., "\Actor-Mixer Hierarchy\Character\Voices"). If omitted, the entire project is scanned.')
parser.add_argument('--loudness', type=str, default='momentaryMax', choices=['momentaryMax', 'integrated'], required=False, help='Optional. Specify the loudness measurement to use (momentaryMax or integrated). Default is momentaryMax.')
args = parser.parse_args()

path = args.path

def get_language_name(id, languages):
    language = next((language for language in languages if language["id"] == id), None)
    return language["name"]

def get_language_id(name, languages):
    language = next((language for language in languages if language["name"] == name), None)
    return language["id"]

if path is None:
    path = F"\Actor-Mixer Hierarchy"

try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        projectInfo = client.call("ak.wwise.core.getProjectInfo")
        
        languages = []

        if args.language is not None:
            # Validate language is valid
            if not any(language["name"] == args.language for language in projectInfo["languages"]):
                raise ValueError("The language is invalid.")
            languages.append(get_language_id(args.language, projectInfo["languages"]))
        else:
            # take all languages from the project
            languages = [language["id"] for language in projectInfo["languages"]]

        ref_language_name = get_language_name(projectInfo["referenceLanguageId"], projectInfo["languages"])

        # Query the voices of the reference language
        get_args = { "waql": F"$ \"{path}\" select descendants where nodeType = \"Sound Voice\" select activeSource"}
        get_options = {
            "return": ["name", "parent.id as parentId", "id", "path", "loudness.momentaryMax as momentaryMax", "loudness.integrated as integrated", "VolumeOffset"],
            "language": projectInfo["referenceLanguageId"]}
        references_voices = client.call("ak.wwise.core.object.get", get_args, options=get_options)['return']

        voices_per_id = {voice["parentId"]: voice for voice in references_voices}

        set_args = {
            "objects": [],
            "onNameConflict": "merge",
        }

        for language in languages:
            if language == projectInfo["referenceLanguageId"]:
                continue

            language_name = get_language_name(language, projectInfo["languages"])
            print(F"Processing {language_name}...")

            # Use WAQL to obtain all audio sources under the specified root
            get_options["language"] = language
            voices = client.call("ak.wwise.core.object.get", get_args, options=get_options)['return']

            for voice in voices:
                ref_voice = voices_per_id.get(voice["parentId"], None)
                if ref_voice is None:
                    raise KeyError("The language is invalid.")
                
                if args.loudness not in ref_voice or args.loudness not in voice:
                    continue

                offset = float(ref_voice[args.loudness]) - float(voice[args.loudness])
                if abs(offset) > 0.1:
                    print(F"{voice['path']}: '{ref_language_name}':{ref_voice[args.loudness]} '{language_name}':{voice[args.loudness]} Offset:{offset}")

                    # Set the VolumeOffset property which is labelled as Make-up Gain in Wwise
                    set_args["objects"].append({ 
                        "object":voice['id'],
                        "@VolumeOffset": offset
                        })

        client.call("ak.wwise.core.undo.beginGroup")
        client.call("ak.wwise.core.object.set", set_args)
        client.call("ak.wwise.core.undo.endGroup", { 'displayName': 'Auto Adjust Volume Offset'})

except Exception as e:
   print(str(e))