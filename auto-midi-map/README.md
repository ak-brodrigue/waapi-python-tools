# auto-midi-map

**Work-in-progress** - The project may not work well yet

Automatically structure the children of Wwise container and set the MIDI properties based on a naming convention.

## Overview

It is possible to implement a sample-based MIDI instrument in Wwise directly in the Actor-Mixer hierarchy. 
However, it can be a tedious task. This tool aims to ease the setup of such complex structures by setting up
automatically the structure for you after you imported the sounds.

## Instructions

1. Create a Blend container.
2. Import sample sounds in the container. The sounds must contain a note name (C,D,E,F,G,A,B, then # or b, then the octave).
3. Select the Blend Container.
4. Run the script.

Note: If multiple sounds have the same note, a random container will be created
