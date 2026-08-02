# Launchpad Duo Sync configuration
# Track offsets are zero-based: 0 = track 1, 9 = track 10.

LAUNCHPAD_X_TRACK_OFFSET = 0
LAUNCHPAD_MINI_TRACK_OFFSET = 9

# Place the controllers at the configured track offsets once when the script connects.
INITIALIZE_HORIZONTAL_LAYOUT = True

# True: keep both controllers permanently at the configured track ranges.
# False: left/right navigation remains available independently on each Launchpad.
LOCK_HORIZONTAL = False

# Keep the two vertical scene positions linked.
SYNC_VERTICAL = True

# Number of scenes moved for each single up/down button step.
VERTICAL_STEP_SCENES = 9

# Number of Ableton scheduler ticks before connecting.
STARTUP_DELAY_TICKS = 50

# Poll once per scheduler tick for responsive navigation.
POLL_TICKS = 1

# Write a line to Ableton's Log.txt for every synchronized scene change.
VERBOSE_SYNC_LOGGING = False
