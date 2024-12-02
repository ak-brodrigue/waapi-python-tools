from waapi import WaapiClient, CannotConnectToWaapiException
from pprint import pprint
import argparse

# Define arguments for the script
parser = argparse.ArgumentParser(description="Validate Sound Voice objects against the reference language's playback duration and report missing sources or violations of duration thresholds.")
parser.add_argument('--language', const=1, default=None, type=str, nargs='?', help='Optional. Specify the language to validate (e.g., en, fr). If omitted, all languages will be validated against the reference language.')
parser.add_argument('--path', const=1, default=None, type=str, nargs='?', help='Optional. Specify the path to enumerate Sound Voice objects (e.g., "\Actor-Mixer Hierarchy\Character\Voices"). If omitted, the entire project is scanned.')
parser.add_argument('--min_threshold', const=1, default=60, type=float, nargs='?', help='Optional. Minimum accepted duration ratio as a percentage (default: 60).')
parser.add_argument('--max_threshold', const=1, default=140, type=float, nargs='?', help='Optional. Maximum accepted duration ratio as a percentage (default: 140).')

args = parser.parse_args()

# Convert percent to ratio
min_threshold = args.min_threshold / 100;
max_threshold = args.max_threshold / 100;

path = args.path

def get_language_name(id, languages):
    language = next((language for language in languages if language["id"] == id), None)
    return language["name"]

if path is None:
    path = F"\Actor-Mixer Hierarchy"

try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        projectInfo = client.call("ak.wwise.core.getProjectInfo")
        
        languages = []

        if args.language is not None:
            # Validate language is valid
            if not any(language["id"] == args.language for language in projectInfo["languages"]):
                raise ValueError("The language is invalid.")
            languages.append(args.language)
        else:
            # take all languages from the project
            languages = [language["id"] for language in projectInfo["languages"]]

        ref_language_name = get_language_name(projectInfo["referenceLanguageId"], projectInfo["languages"])

        # Query the voices of the reference language
        get_args = { "waql": F"$ \"{path}\" select descendants where nodeType = \"Sound Voice\""}
        get_options = {
            "return": ["name", "id", "path", "(activeSource != null) as hasSource", "duration.max as duration"],
            "language": projectInfo["referenceLanguageId"]}
        references_voices = client.call("ak.wwise.core.object.get", get_args, options=get_options)['return']

        voices_per_id = {voice["id"]: voice for voice in references_voices}

        print(F"Checking {ref_language_name}...")
        for ref_voice in references_voices:
            if ref_voice["hasSource"] == False:
                print(F"{ref_voice['path']}: Reference language '{ref_language_name}' does not have a source.")

        for language in languages:
            if language == projectInfo["referenceLanguageId"]:
                continue

            language_name = get_language_name(language, projectInfo["languages"])
            print(F"Processing {language_name}...")

            # Use WAQL to obtain all audio sources under the object
            get_options["language"] = language
            voices = client.call("ak.wwise.core.object.get", get_args, options=get_options)['return']

            for voice in voices:
                ref_voice = voices_per_id.get(voice["id"], None)
                if ref_voice is None:
                    raise KeyError("The language is invalid.")
                
                if ref_voice["hasSource"] == False:
                    continue
                
                if voice["hasSource"] == False:
                    print(F"{voice['path']}: Language '{language_name}' does not have a source.")
                    continue

                ratio = voice["duration"] / ref_voice["duration"]
                if ratio < min_threshold or ratio > max_threshold:
                    print(F"{voice['path']}: Voice duration of {voice['duration']} for language '{language_name}' exceeds threshold ratio from reference duration {ref_voice['duration']} with ratio {ratio * 100:.0f}%.")
                    continue
                    

except Exception as e:
    print(str(e))