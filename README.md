# Launchpad Duo Sync v2.0.0

Launchpad Duo Sync synchronizes the vertical Session navigation of two or more Novation Launchpads in Ableton Live while allowing each controller to keep its own horizontal track position.

Version 2.0 adds configurable model selection, support for mixed Launchpad combinations, multiple identical devices, and setups with more than two controllers.

## Main features

- Shared Up/Down Session navigation
- Configurable scene jump size
- Independent horizontal navigation
- Optional Horizontal Lock
- Mixed Launchpad models
- Multiple identical Launchpads using `instance_index`
- Two or more configured controllers
- Friendly model names in `config.py`
- Raw Ableton Control Surface names as a fallback for future models

##Demo
images/Demo.gif

## Installation

See [`docs/INSTALLATION.md`](docs/INSTALLATION.md) for the full installation and update guide.

The short version:

1. Close Ableton Live.
2. Copy the folder `LaunchpadDuoSync` into:

   ```text
   ~/Music/Ableton/User Library/Remote Scripts/
   ```

3. Edit `LaunchpadDuoSync/config.py` and enter your devices.
4. Restart Ableton Live.
5. Keep the official Novation Control Surface for each Launchpad enabled.
6. Add `LaunchpadDuoSync` as an additional Control Surface with **Input: None** and **Output: None**.

## Configuration examples

### Launchpad X + Launchpad Mini MK3

```python
DEVICES = [
    {
        "label": "Left Launchpad",
        "model": "Launchpad X",
        "instance_index": 0,
        "track_offset": 0,
    },
    {
        "label": "Right Launchpad",
        "model": "Launchpad Mini MK3",
        "instance_index": 0,
        "track_offset": 9,
    },
]
```

### Two identical Launchpad X devices

```python
DEVICES = [
    {
        "label": "Left Launchpad X",
        "model": "Launchpad X",
        "instance_index": 0,
        "track_offset": 0,
    },
    {
        "label": "Right Launchpad X",
        "model": "Launchpad X",
        "instance_index": 1,
        "track_offset": 8,
    },
]
```

`instance_index` refers to the order of matching official Control Surface rows in Ableton Live:

- `0` = first matching device
- `1` = second matching device
- `2` = third matching device

## Recognized friendly model names

- `Launchpad X`
- `Launchpad Mini MK3`
- `Launchpad Pro MK3`
- `Launchpad Pro`
- `Launchpad MK2`
- `Launchpad`

For an unlisted or future model, enter the raw Ableton Control Surface script name in `model`. Compatibility still depends on that official script exposing a compatible Session Ring.

## Important settings

```python
VERTICAL_STEP_SCENES = 9
LOCK_HORIZONTAL = False
INITIALIZE_HORIZONTAL_LAYOUT = True
SYNC_VERTICAL = True
```

- `VERTICAL_STEP_SCENES`: number of scenes moved per Up/Down press
- `LOCK_HORIZONTAL = False`: each Launchpad may move left/right independently
- `LOCK_HORIZONTAL = True`: each Launchpad remains at its configured `track_offset`
- `INITIALIZE_HORIZONTAL_LAYOUT`: applies configured track positions when connecting
- `SYNC_VERTICAL`: enables or disables shared vertical navigation

## Compatibility

Confirmed working with:

- Ableton Live 12.3.5
- macOS 26.5.2
- Launchpad X
- Launchpad Mini MK3

The architecture supports other official Launchpad Control Surfaces, but each model combination should be hardware-tested.

## License

MIT License — Copyright © 2026 Özer Cihan
