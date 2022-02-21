# OBS JSON Generator

Tool to help build OBS scene collections from parts. 

Requires the (excellent) [`click`](https://click.palletsprojects.com/en/8.0.x/) package.

## JSON File Format

The JSON file format appears to be undocumented(?). As such, it's likely intended to be an internal representation and not accessible from the outside. However, it's also a really convenient way to programmatically generate a scene collection. #yolo

The file seems to look like this:

```json
{
    "AuxAudioDevice1":      { ... },
    "DesktopAudioDevice1":  { ... },
    "modules": {
        "auto-scene-switcher": { ... },
        "captions": { ... },
        "decklink_captions": { ... },
        "output-timer": { ... },
        "scripts-tool": []
    },
    "quick_transitions": [ ... ],
    "transitions": [],

    // There are a bunch of key-value pairs here that can be set, but it's not clear which
    // ones are actually important. These are the ones that were set in my file.
    "preview_locked": false,
    "scaling_enabled": false,
    "scaling_level": 0,
    "scaling_off_x": 0.0,
    "scaling_off_y": 0.0,
    "transition_duration": 500,

    // This one is important, for sure!
    "name": "My Scene Collection Name",

    // These are the parts we're focus on filling in with our generator program.
    "groups": [ ... ],
    "sources": [ ... ],
    "scene_order": [ ... ],

    // These will vary based on what's in your scene list, 
    // but they need to be here for things to be happy
    "current_program_scene": "Outro",
    "current_scene": "Outro",
    "current_transition": "Fade",

}
```

The most variable things are the `sources` list and the `scene_order` list. In OBS, pretty much everything is a `source`, including scenes, input devices, etc. I expect that any source type is valid here, with names that match the tags in the `obs_source_info` structs buried in each source struct. You can use the `extract_source.py` script in this directory to extract a particular source from an existing exported scene collection.

> Editorial note: using the type punning / struct inheritance mechanism is really nice for making portable code that can be compiled with really old toolchains, but it makes documenting the code really hard, and difficult for people extending the codebase to find all of the types that use the base type. If you're going to build out a type system and rely on it, why not just use C++99 or something? Maybe I'm insufficiently 10x to get it, but it seems like a maintenance nightmare.

### Audio Devices

There's a fixed block of settings that seem to be the default input and output channels. I expect that it might be different based on the operating system that you are using OBS on (Windows vs. Mac vs. Linux), and there may be some diffences based on the type of installation you did. I'd recommend getting a basic setup working in OBS, exporting the thing that basically works, and then copying the audio devices into the `fixed.json` file.