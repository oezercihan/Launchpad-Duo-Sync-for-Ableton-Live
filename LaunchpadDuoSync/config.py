"""Launchpad Duo Sync v2.0 configuration.

For normal use, edit only DEVICES and the options at the bottom.

Friendly model names are accepted, for example:
    Launchpad X
    Launchpad Mini MK3
    Launchpad Pro MK3
    Launchpad Pro
    Launchpad MK2
    Launchpad

Multiple identical devices use instance_index:
    0 = first matching Control Surface row in Ableton Live
    1 = second matching row
    2 = third matching row

track_offset is zero-based:
    0 = track 1
    8 = track 9
    9 = track 10
"""

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

# Shared vertical movement in scenes per Up/Down press.
VERTICAL_STEP_SCENES = 9

# False: each Launchpad can move horizontally on its own.
# True: every Launchpad is kept at its configured track_offset.
LOCK_HORIZONTAL = False

# Apply each configured track_offset when the script connects.
INITIALIZE_HORIZONTAL_LAYOUT = True

# Enable shared vertical navigation.
SYNC_VERTICAL = True

# Advanced settings. Most users should leave these unchanged.
ALLOW_PARTIAL_SURFACE_MATCH = False
STARTUP_DELAY_TICKS = 50
POLL_TICKS = 1
RECONNECT_TICKS = 25
VERBOSE_SYNC_LOGGING = False
