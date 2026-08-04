# Configuration Reference — v2.0.0

For normal use, edit only `LaunchpadDuoSync/config.py`.

## Device fields

Each entry in `DEVICES` supports:

- `label`: readable name used in Live's log
- `model`: friendly model name or raw Ableton Control Surface script name
- `instance_index`: occurrence of that model in Live's Control Surface list, starting at `0`
- `track_offset`: zero-based horizontal starting or lock position

## Three-controller example

```python
DEVICES = [
    {"label": "Left", "model": "Launchpad Pro MK3", "instance_index": 0, "track_offset": 0},
    {"label": "Center", "model": "Launchpad X", "instance_index": 0, "track_offset": 8},
    {"label": "Right", "model": "Launchpad Mini MK3", "instance_index": 0, "track_offset": 16},
]
```

## Navigation options

```python
VERTICAL_STEP_SCENES = 9
LOCK_HORIZONTAL = False
INITIALIZE_HORIZONTAL_LAYOUT = True
SYNC_VERTICAL = True
```

## Advanced options

```python
ALLOW_PARTIAL_SURFACE_MATCH = False
STARTUP_DELAY_TICKS = 50
POLL_TICKS = 1
RECONNECT_TICKS = 25
VERBOSE_SYNC_LOGGING = False
```

Most users should leave the advanced options unchanged.
