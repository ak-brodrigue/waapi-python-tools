#!/usr/bin/env python3

from waapi import WaapiClient, CannotConnectToWaapiException
import sys, re, os, argparse

# Define arguments for the script
parser = argparse.ArgumentParser(description='Auto-rename container for the specified Wwise object ID.')
parser.add_argument('id', metavar='GUID', nargs='?', help='One guid of the form {01234567-89ab-cdef-0123-4567890abcde}. The script retrieves the current selected if no GUID specified.')

args = parser.parse_args()
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
            "return": ['name']
        }
        children = client.call("ak.wwise.core.object.get", get_args, options=options)['return']

        names = list(map(lambda object: object['name'], children))
        common = os.path.commonprefix(names)

        common = common.rstrip('_ -')

        if not common:
            raise Exception('No common prefix found')

        set_name_args = {
            "object": args.id,
            "value":common
        }
        client.call("ak.wwise.core.object.setName", set_name_args)


except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

except Exception as e:
    print(str(e))
