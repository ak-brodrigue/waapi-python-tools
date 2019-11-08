#!/usr/bin/env python3

from waapi import WaapiClient, CannotConnectToWaapiException
import sys, re, os

try:
    # Connecting to Waapi using default URL
    with WaapiClient() as client:

        # Simple RPC
        selected  = client.call("ak.wwise.ui.getSelectedObjects")['objects']

        if len(selected) != 1:
            raise Exception('Please select an object')

        # RPC with options
        # return an array of all children objects in the default actor-mixer work-unit
        args = {
            "from": {"id": [selected[0]['id']]},
            "transform": [
                {"select": ['children']}
            ]
        }
        options = {
            "return": ['name']
        }
        children = client.call("ak.wwise.core.object.get", args, options=options)['return']

        names = list(map(lambda object: object['name'], children))
        common = os.path.commonprefix(names)

        common = common.rstrip('_ -')

        if not common:
            raise Exception('No common prefix found')

        setNameArgs = {
            "object": selected[0]['id'],
            "value":common
        }
        client.call("ak.wwise.core.object.setName", setNameArgs)


except CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")

except Exception as e:
    print(str(e))
    input("Press key to continue...")