# Installation and troubleshooting

## Install

1. Close Ableton Live completely.
2. In Finder choose **Go → Go to Folder…**.
3. Enter:

   ```text
   ~/Music/Ableton/User Library/Remote Scripts/
   ```

4. Delete any older `LaunchpadDuoSync` folder.
5. Copy the new `LaunchpadDuoSync` folder into `Remote Scripts`.
6. Start Live and open **Settings → Link, Tempo & MIDI**.
7. Configure exactly one row for each official Novation script and one row for `LaunchpadDuoSync`.

The Duo Sync row must use `None` for input and output.

## Expected startup layout

- Launchpad X: tracks 1–8
- Launchpad Mini MK3: tracks 10–17

## Log file

```text
~/Library/Preferences/Ableton/Live 12.3.5/Log.txt
```

Search for:

```text
[DuoSync]
```

A successful startup includes:

```text
CONNECTED v1.0
```

## Duplicate surfaces

If the log reports multiple Launchpad X or Launchpad Mini MK3 surfaces, remove duplicate Control Surface rows in Live.

## Uninstall

1. Quit Live.
2. Delete `~/Music/Ableton/User Library/Remote Scripts/LaunchpadDuoSync`.
3. Restart Live and remove the `LaunchpadDuoSync` Control Surface row.
