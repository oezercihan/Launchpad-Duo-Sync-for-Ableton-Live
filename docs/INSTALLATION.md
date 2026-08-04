# Installation and Update Guide — Launchpad Duo Sync v2.0.0

## 1. Download and extract

Download `LaunchpadDuoSync-v2.0.0.zip` and extract it. The archive contains the installable folder:

```text
LaunchpadDuoSync/
```

Do not rename this folder.

## 2. Close Ableton Live

Quit Ableton Live completely before replacing or editing a Remote Script.

## 3. Open the Remote Scripts folder

In Finder, select **Go → Go to Folder…** and enter:

```text
~/Music/Ableton/User Library/Remote Scripts/
```

Create the `Remote Scripts` folder if it does not already exist.

## 4. Install or update

### New installation

Copy the complete `LaunchpadDuoSync` folder into `Remote Scripts`:

```text
~/Music/Ableton/User Library/Remote Scripts/LaunchpadDuoSync/
```

The final structure must look like this:

```text
Remote Scripts/
└── LaunchpadDuoSync/
    ├── __init__.py
    ├── config.py
    ├── models.py
    └── multi_sync.py
```

Avoid creating an extra nested folder such as:

```text
Remote Scripts/LaunchpadDuoSync/LaunchpadDuoSync/
```

### Updating from v1.x or a beta

1. Back up your existing `LaunchpadDuoSync/config.py` if it contains custom settings.
2. Remove the old `LaunchpadDuoSync` folder.
3. Copy the new v2.0.0 folder into `Remote Scripts`.
4. Re-enter your device configuration in the new `config.py` rather than blindly copying an old file, because the v2 format includes `model` and `instance_index`.

## 5. Configure your Launchpads

Open:

```text
LaunchpadDuoSync/config.py
```

Normally this is the only file you need to edit.

### Mixed models

```python
DEVICES = [
    {
        "label": "Left",
        "model": "Launchpad Pro MK3",
        "instance_index": 0,
        "track_offset": 0,
    },
    {
        "label": "Right",
        "model": "Launchpad X",
        "instance_index": 0,
        "track_offset": 8,
    },
]
```

### Two identical models

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

For identical models, `instance_index` follows the order of matching official Launchpad rows in Live's Control Surface list.

`track_offset` is zero-based:

- `0` = Track 1
- `8` = Track 9
- `9` = Track 10
- `16` = Track 17

## 6. Configure Ableton Live

Start Ableton Live and open:

```text
Live → Settings → Link, Tempo & MIDI
```

Keep one official Novation Control Surface row for every physical Launchpad, with the correct DAW Input and DAW Output ports assigned.

Add one additional row:

```text
Control Surface: LaunchpadDuoSync
Input: None
Output: None
```

Do not assign either Launchpad's MIDI ports directly to the `LaunchpadDuoSync` row.

## 7. Test

1. Open Session View.
2. Confirm that every Launchpad shows its configured horizontal track area.
3. Press Up or Down on either configured Launchpad.
4. All configured Session Rings should move vertically together.
5. When `LOCK_HORIZONTAL = False`, verify that each controller can still move left/right independently.

## Troubleshooting

### LaunchpadDuoSync does not appear in Live

- Confirm the folder name is exactly `LaunchpadDuoSync`.
- Confirm `__init__.py` is directly inside that folder.
- Restart Live after copying the script.
- Check for an accidental extra folder level.

### A device is not detected

- Verify that its official Control Surface row is enabled in Live.
- Confirm the friendly `model` name in `config.py`.
- For an unlisted model, use its raw Ableton Control Surface script name.
- Check Live's `Log.txt` for lines beginning with `[DuoSync]`.

### Identical devices are reversed

Swap their `instance_index` values or change the order/port assignment of their official Control Surface rows in Live.

### Horizontal movement keeps resetting

Set:

```python
LOCK_HORIZONTAL = False
```

### Log file location on macOS

```text
~/Library/Preferences/Ableton/Live 12.3.5/Log.txt
```
