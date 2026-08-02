# Launchpad Duo Sync

Synchronizes the **vertical Session Ring navigation** of a Novation Launchpad X and Launchpad Mini MK3 in Ableton Live, while allowing independent horizontal navigation.


## Demo

![Launchpad Duo Sync Demo](images/Demo.gif)




## Validated setup

- Ableton Live 12.3.5
- macOS 26.5.2
- Novation Launchpad X
- Novation Launchpad Mini MK3

## Default behavior

- Launchpad X starts at tracks **1–8**.
- Launchpad Mini MK3 starts at tracks **10–17**.
- Pressing **Up** or **Down** on either Launchpad moves both Session Rings by **9 scenes**.
- Horizontal lock is disabled by default, so left/right navigation remains independent.
- Scene offsets are clamped at zero.
- The official Novation scripts continue handling LEDs, clip launching, mixer modes, and device modes.

## Installation

1. Quit Ableton Live.
2. Copy the `LaunchpadDuoSync` folder to:

   ```text
   ~/Music/Ableton/User Library/Remote Scripts/
   ```

3. Start Ableton Live.
4. Open **Settings → Link, Tempo & MIDI**.
5. Keep the official rows for:
   - Launchpad X with its DAW input and output
   - Launchpad Mini MK3 with its DAW input and output
6. Add another Control Surface row:
   - Control Surface: `LaunchpadDuoSync`
   - Input: `None`
   - Output: `None`

See [docs/INSTALL.md](docs/INSTALL.md) for detailed setup and troubleshooting.

## Configuration

Edit `LaunchpadDuoSync/config.py` while Live is closed.

```python
VERTICAL_STEP_SCENES = 9
LOCK_HORIZONTAL = False
LAUNCHPAD_X_TRACK_OFFSET = 0
LAUNCHPAD_MINI_TRACK_OFFSET = 9
```

Track offsets are zero-based.

## Compatibility note

This script accesses Ableton Live's internal Control Surface objects. Ableton does not publish these APIs as a stable third-party SDK, so future Live updates may require changes.

## License

MIT. See [LICENSE](LICENSE).
