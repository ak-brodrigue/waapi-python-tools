import re
from waapi import WaapiClient, CannotConnectToWaapiException


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculates the Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def split_words(name: str) -> list:
    """Splits a string into words based on spaces, underscores, and camelCase."""
    # Split by spaces, underscores, and camelCase transitions
    tokens = re.sub(r"([a-z])([A-Z])", r"\1 \2", name).replace("_", " ").split()
    return [t.lower() for t in tokens]


def get_score(tokens1: list, tokens2: list) -> float:
    """Calculates a similarity score between two sets of tokens."""
    if not tokens1:
        return 0.0

    score = 0.0
    for t1 in tokens1:
        best_distance = float("inf")
        for t2 in tokens2:
            best_distance = min(best_distance, levenshtein_distance(t1, t2))

        # Normalize similarity to a score (higher is better)
        similarity = 1.0 - (float(best_distance) / max(len(t1), 1))
        score += similarity

    return score / len(tokens1)


def call_return(client: WaapiClient, uri: str, args: dict, options: dict = None) -> list:
    """Calls a WAAPI function and returns its 'return' array, or [] if the call failed."""
    # client.call returns None when the remote procedure call fails
    result = client.call(uri, args, options=options) if options else client.call(uri, args)
    return result.get("return", []) if result else []


def log_warning(client: WaapiClient, message: str):
    """Prints a warning and adds it to the Wwise Logs view, on the general channel."""
    print(f"Warning: {message}")
    client.call(
        "ak.wwise.core.log.addItem",
        {"message": message, "severity": "Warning", "channel": "general"},
    )


def auto_assign(client: WaapiClient, switch_container_id: str):
    """Automatically assigns unassigned children to the best matching Switch/State."""

    # 1. Get the Switch Container and its referenced Switch/State Group
    container_args = {"from": {"id": [switch_container_id]}}
    container_opts = {"return": ["id", "name", "type", "@SwitchGroupOrStateGroup"]}

    containers = call_return(
        client, "ak.wwise.core.object.get", container_args, container_opts
    )
    if not containers:
        print("Error: Could not retrieve object.")
        return

    container = containers[0]
    if container["type"] != "SwitchContainer":
        print(
            f"Error: Selected object '{container['name']}' is not a Switch Container."
        )
        return

    group_ref = container.get("@SwitchGroupOrStateGroup")
    if not group_ref or group_ref["id"] == "{00000000-0000-0000-0000-000000000000}":
        print(
            f"Error: Switch Container '{container['name']}' has no Switch or State Group assigned."
        )
        return

    # 2. Get children of the Switch Container
    child_args = {
        "from": {"id": [switch_container_id]},
        "transform": [{"select": ["children"]}],
    }
    child_opts = {"return": ["id", "name"]}
    children = call_return(client, "ak.wwise.core.object.get", child_args, child_opts)

    # 3. Get the Switches/States from the assigned Group
    switch_args = {
        "from": {"id": [group_ref["id"]]},
        "transform": [{"select": ["children"]}],
    }
    switch_opts = {"return": ["id", "name"]}
    switches = call_return(client, "ak.wwise.core.object.get", switch_args, switch_opts)

    if not switches:
        print("No Switches or States found in the assigned group.")
        return

    # Prepare switch tokens
    switch_tokens = [split_words(switch["name"]) for switch in switches]

    # 4. Get current assignments to find out which children are already in use
    # Note: distinguish a failed call from an empty result, otherwise a failure here
    # looks like "nothing is assigned" and every child gets assigned a second time.
    assignments_res = client.call(
        "ak.wwise.core.switchContainer.getAssignments", {"id": switch_container_id}
    )
    if assignments_res is None:
        log_warning(
            client,
            f"Could not retrieve the existing assignments of Switch Container "
            f"'{container['name']}'. Children that are already assigned may be "
            f"assigned a second time.",
        )

    assigned_children = {
        assoc["child"] for assoc in (assignments_res or {}).get("return", [])
    }

    # 5. Open Undo Group
    client.call("ak.wwise.core.undo.beginGroup")

    try:
        # 6. Iterate and score unassigned children
        for child in children:
            if child["id"] in assigned_children:
                continue

            child_tokens = split_words(child["name"])

            best_score = -1.0
            best_switch_index = -1

            for i, s_tokens in enumerate(switch_tokens):
                score = get_score(s_tokens, child_tokens)
                if score > best_score:
                    best_score = score
                    best_switch_index = i

            # Assign if a valid match was found
            if best_score != -1.0 and best_switch_index < len(switches):
                target_switch = switches[best_switch_index]

                print(
                    f"Assigning '{child['name']}' -> '{target_switch['name']}' (Score: {best_score:.2f})"
                )

                client.call(
                    "ak.wwise.core.switchContainer.addAssignment",
                    {"child": child["id"], "stateOrSwitch": target_switch["id"]},
                )
    finally:
        client.call(
            "ak.wwise.core.undo.endGroup",
            {"displayName": "Auto Assign Switch Container"},
        )


def main():
    try:
        with WaapiClient() as client:
            # Technique: Retrieve the object to apply via currently selected objects
            selected_res = client.call("ak.wwise.ui.getSelectedObjects")
            selected_objects = selected_res.get("objects", [])

            if not selected_objects:
                print("No objects selected in Wwise. Please select a Switch Container.")
                return

            for obj in selected_objects:
                auto_assign(client, obj["id"])

    except CannotConnectToWaapiException:
        print(
            "Could not connect to Wwise Authoring API. Make sure Wwise is running and WAAPI is enabled."
        )


if __name__ == "__main__":
    main()
