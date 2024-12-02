from waapi import WaapiClient
from pprint import pprint
from pathlib import Path
import argparse, traceback

# Define arguments for the script
parser = argparse.ArgumentParser(description='Automatically create new play events from the selection and replicate the work unit hierarchy.')
parser.add_argument('ids', metavar='GUID', nargs='*', help='One or many guid of the form {01234567-89ab-cdef-0123-4567890abcde}. The script retrieves the current selected if no GUID specified.')

args = parser.parse_args()

def create_event(name, target):
    # Create an Event withe specified name and target
    return {
        "type":"Event",
        "name":name,
        "children":[
            {
                "type":"Action",
                "name": "",
                "@Target": target
            }
        ]
    }

def create_workunit(name):
    # Create a Work Unit with the specified name
    return {
        "type":"WorkUnit",
        "name": name
    }

def create_virtual_folder(name):
    # Create a Virtual Folder with the specified name
    return {
        "type":"Folder",
        "name": name
    }

def create_event_and_workunits(path, target):
    # Create an event and the parent work units

    # Create the event first
    current_hierarchy = create_event(str(path.stem), target)

    # Then create the parents in a loop
    current_path = path.parent
    while len(current_path.parents) > 1:

        new_parent = None
        if len(current_path.parents) == 2:
            new_parent = create_workunit(current_path.stem)
        else :
            new_parent = create_virtual_folder(current_path.stem)
        
        new_parent["children"] = [current_hierarchy]

        current_path = current_path.parent
        current_hierarchy = new_parent

    return current_hierarchy


try:

    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        selected = []
        
        options = { "return" : ["path", "id", "isPlayable"] }

        # if no ID is passed as argument, use the selected object from the project
        if args.ids is None or len(args.ids) == 0:
            selected  = client.call("ak.wwise.ui.getSelectedObjects", {}, options=options)['objects']
        else:
            ids_list = ', '.join(f'"{item}"' for item in args.ids)
            selected  = client.call("ak.wwise.core.object.get", { "waql":f"$ {ids_list}" }, options=options)['return']

        set_args = {
            "objects": []
        }

        for obj in selected:

            # Skip non playable objects
            if not obj["isPlayable"]:
                continue

            selection_path = Path(obj["path"])
            print(str(selection_path))

            # Choose the new event path
            parts = list(selection_path.parts)
            parts[1] = "Events"
            object_name = parts.pop()
            parts.append("Play_" + object_name)

            hierarchy = create_event_and_workunits(Path(*parts), obj["id"])

            set_args["objects"].append(
                {
                    "object":"\\Events",
                    "children": [ hierarchy ]
                });

        client.call("ak.wwise.core.object.set", set_args)


except Exception as e:
    traceback.print_exc()
    print(str(e))