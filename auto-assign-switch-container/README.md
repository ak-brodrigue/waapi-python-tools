# auto-assign-switch-container

Automatically assign the unassigned children of a Switch Container to the Switch or State whose name best matches theirs.

The best match is found by splitting both names into words and scoring them with a Levenshtein distance, so `Footstep_Grass_01` is assigned to the `Grass` Switch without the names having to match exactly.

**Attention**: Every unassigned child is assigned to its best match, even when that match is poor. There is no minimum score, so review the results before saving. All assignments are made in a single undo group.

## Requirements

* Wwise 2019.2.x+ for using with the **Command Add-ons** (custom menus).
* The Switch Container must have a Switch Group or State Group assigned.

## Instructions

**Note**: Refer to installation instructions in [waapi-python-tools](../README.md).

1. Create a Switch Container and assign a Switch Group or State Group to it.
2. Add children to the Switch Container, naming them after the Switches or States.
3. Select the Switch Container.
4. Right click and select **Auto Assign Switch Container** or run the script manually.

The script prints each assignment it makes, with the score of the match:

```
Assigning 'Footstep_Grass_01' -> 'Grass' (Score: 1.00)
Assigning 'Footstep_Gravel_01' -> 'Gravel' (Score: 1.00)
```

Multiple Switch Containers can be selected at once. Each one is processed in its own undo group.

## Notes

* Children that are already assigned to a Switch or State are left untouched. Only unassigned children are considered, so the script can be run again after adding new children.
* Words are split on spaces, underscores, and camelCase transitions. Other separators, such as `-`, are not split on and are treated as part of the word.
* For a State Group, the `None` State is a child of the group like any other, so it is a possible assignment target.
