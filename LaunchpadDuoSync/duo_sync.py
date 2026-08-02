import builtins
import traceback

from ableton.v2.control_surface import ControlSurface

from .config import (
    LAUNCHPAD_X_TRACK_OFFSET,
    LAUNCHPAD_MINI_TRACK_OFFSET,
    INITIALIZE_HORIZONTAL_LAYOUT,
    STARTUP_DELAY_TICKS,
    POLL_TICKS,
    SYNC_VERTICAL,
    VERTICAL_STEP_SCENES,
    LOCK_HORIZONTAL,
    VERBOSE_SYNC_LOGGING,
)

PREFIX = "[DuoSync]"
VERSION = "1.0"


class LaunchpadDuoSync(ControlSurface):
    """Links vertical Session Ring navigation for Launchpad X and Mini MK3."""

    def __init__(self, c_instance):
        self._duo_c_instance = c_instance
        self._x_ring = None
        self._mini_ring = None
        self._last_x_scene = None
        self._last_mini_scene = None
        self._shared_scene = 0
        self._running = True
        super().__init__(c_instance=c_instance)
        self.name = "Launchpad Duo Sync"
        self._log("Loaded v{}".format(VERSION))
        self.schedule_message(STARTUP_DELAY_TICKS, self._connect)

    def disconnect(self):
        self._running = False
        self._x_ring = None
        self._mini_ring = None
        super().disconnect()

    def _log(self, message):
        line = "{} {}".format(PREFIX, message)
        try:
            self._duo_c_instance.log_message(line)
            return
        except Exception:
            pass
        try:
            print(line)
        except Exception:
            pass

    @staticmethod
    def _matching_surfaces(module_prefix):
        return [
            surface
            for surface in list(getattr(builtins, "control_surfaces", []))
            if surface.__class__.__module__.startswith(module_prefix)
        ]

    def _connect(self):
        if not self._running:
            return
        try:
            x_surfaces = self._matching_surfaces("Launchpad_X.")
            mini_surfaces = self._matching_surfaces("Launchpad_Mini_MK3.")

            if len(x_surfaces) > 1:
                self._log(
                    "WARNING: {} Launchpad X surfaces found; using the first. "
                    "Disable duplicate rows in Live Settings.".format(len(x_surfaces))
                )
            if len(mini_surfaces) > 1:
                self._log(
                    "WARNING: {} Launchpad Mini MK3 surfaces found; using the first. "
                    "Disable duplicate rows in Live Settings.".format(len(mini_surfaces))
                )

            if not x_surfaces or not mini_surfaces:
                self._log(
                    "WAITING: Launchpad X found={} Mini MK3 found={}".format(
                        len(x_surfaces), len(mini_surfaces)
                    )
                )
                self.schedule_message(25, self._connect)
                return

            self._x_ring = self._find_session_ring(x_surfaces[0])
            self._mini_ring = self._find_session_ring(mini_surfaces[0])

            if self._x_ring is None or self._mini_ring is None:
                self._log(
                    "WAITING: Session rings available X={} Mini={}".format(
                        self._x_ring is not None, self._mini_ring is not None
                    )
                )
                self.schedule_message(25, self._connect)
                return

            initial_scene = max(0, int(self._x_ring.scene_offset))
            self._shared_scene = initial_scene

            if INITIALIZE_HORIZONTAL_LAYOUT:
                self._set_ring(self._x_ring, LAUNCHPAD_X_TRACK_OFFSET, initial_scene)
                self._set_ring(self._mini_ring, LAUNCHPAD_MINI_TRACK_OFFSET, initial_scene)
            else:
                self._set_scene_only(self._x_ring, initial_scene)
                self._set_scene_only(self._mini_ring, initial_scene)

            self._last_x_scene = int(self._x_ring.scene_offset)
            self._last_mini_scene = int(self._mini_ring.scene_offset)

            self._log(
                "CONNECTED v{} X(track={}, scene={}) Mini(track={}, scene={}) "
                "vertical_step={} horizontal_lock={}".format(
                    VERSION,
                    self._x_ring.track_offset,
                    self._x_ring.scene_offset,
                    self._mini_ring.track_offset,
                    self._mini_ring.scene_offset,
                    VERTICAL_STEP_SCENES,
                    LOCK_HORIZONTAL,
                )
            )
            self.schedule_message(POLL_TICKS, self._poll)
        except Exception as error:
            self._log_exception("CONNECT", error)
            self.schedule_message(25, self._connect)

    @staticmethod
    def _components_for(surface):
        components = []
        for attribute_name in ("components", "_components"):
            try:
                value = getattr(surface, attribute_name, None)
                if value:
                    components.extend(list(value))
            except Exception:
                pass

        unique = []
        seen = set()
        for component in components:
            identity = id(component)
            if identity not in seen:
                seen.add(identity)
                unique.append(component)
        return unique

    def _find_session_ring(self, surface):
        for component in self._components_for(surface):
            try:
                if (
                    component.__class__.__name__ == "SessionRingComponent"
                    and getattr(component, "name", "") == "Session_Ring"
                    and hasattr(component, "set_offsets")
                ):
                    return component
            except Exception:
                pass
        return None

    @staticmethod
    def _set_ring(ring, track_offset, scene_offset):
        ring.set_offsets(int(track_offset), max(0, int(scene_offset)))

    def _set_scene_only(self, ring, scene_offset):
        self._set_ring(ring, int(ring.track_offset), scene_offset)

    def _apply_vertical_scene(self, scene_offset):
        scene_offset = max(0, int(scene_offset))
        if LOCK_HORIZONTAL:
            self._set_ring(self._x_ring, LAUNCHPAD_X_TRACK_OFFSET, scene_offset)
            self._set_ring(self._mini_ring, LAUNCHPAD_MINI_TRACK_OFFSET, scene_offset)
        else:
            self._set_scene_only(self._x_ring, scene_offset)
            self._set_scene_only(self._mini_ring, scene_offset)
        self._shared_scene = scene_offset

    @staticmethod
    def _direction(current, previous):
        if current > previous:
            return 1
        if current < previous:
            return -1
        return 0

    def _poll(self):
        if not self._running:
            return
        try:
            if self._x_ring is None or self._mini_ring is None:
                self.schedule_message(10, self._connect)
                return

            x_scene = int(self._x_ring.scene_offset)
            mini_scene = int(self._mini_ring.scene_offset)
            x_changed = x_scene != self._last_x_scene
            mini_changed = mini_scene != self._last_mini_scene

            direction = 0
            source = None

            if SYNC_VERTICAL:
                if x_changed and not mini_changed:
                    direction = self._direction(x_scene, self._last_x_scene)
                    source = "X"
                elif mini_changed and not x_changed:
                    direction = self._direction(mini_scene, self._last_mini_scene)
                    source = "Mini"
                elif x_changed and mini_changed:
                    x_direction = self._direction(x_scene, self._last_x_scene)
                    mini_direction = self._direction(mini_scene, self._last_mini_scene)
                    direction = x_direction if x_direction != 0 else mini_direction
                    source = "both"
                elif x_scene != mini_scene:
                    # Repair unexpected drift without adding another nine-scene jump.
                    self._apply_vertical_scene(self._shared_scene)
                    source = "drift repair"

            if direction != 0:
                target_scene = max(
                    0,
                    int(self._shared_scene) + direction * max(1, int(VERTICAL_STEP_SCENES)),
                )
                self._apply_vertical_scene(target_scene)
                if VERBOSE_SYNC_LOGGING:
                    self._log(
                        "SYNC source={} direction={} scene={}".format(
                            source, direction, target_scene
                        )
                    )
            elif LOCK_HORIZONTAL:
                if int(self._x_ring.track_offset) != LAUNCHPAD_X_TRACK_OFFSET:
                    self._set_ring(
                        self._x_ring,
                        LAUNCHPAD_X_TRACK_OFFSET,
                        int(self._x_ring.scene_offset),
                    )
                if int(self._mini_ring.track_offset) != LAUNCHPAD_MINI_TRACK_OFFSET:
                    self._set_ring(
                        self._mini_ring,
                        LAUNCHPAD_MINI_TRACK_OFFSET,
                        int(self._mini_ring.scene_offset),
                    )

            self._last_x_scene = int(self._x_ring.scene_offset)
            self._last_mini_scene = int(self._mini_ring.scene_offset)
        except Exception as error:
            self._log_exception("POLL", error)

        self.schedule_message(POLL_TICKS, self._poll)

    def _log_exception(self, stage, error):
        self._log("{} ERROR {!r}".format(stage, error))
        for line in traceback.format_exc().splitlines():
            self._log("TRACE {}".format(line))
