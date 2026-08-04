import builtins
import traceback

from ableton.v2.control_surface import ControlSurface

from .config import (
    DEVICES,
    ALLOW_PARTIAL_SURFACE_MATCH,
    INITIALIZE_HORIZONTAL_LAYOUT,
    LOCK_HORIZONTAL,
    SYNC_VERTICAL,
    VERTICAL_STEP_SCENES,
    STARTUP_DELAY_TICKS,
    POLL_TICKS,
    RECONNECT_TICKS,
    VERBOSE_SYNC_LOGGING,
)
from .models import resolve_surface_match

PREFIX = "[DuoSync]"
VERSION = "2.0.0"


class LaunchpadDuoSync(ControlSurface):
    """Synchronizes vertical Session Rings for two or more configured surfaces."""

    def __init__(self, c_instance):
        self._duo_c_instance = c_instance
        self._devices = []
        self._shared_scene = 0
        self._running = True
        super().__init__(c_instance=c_instance)
        self.name = "Launchpad Duo Sync"
        self._log("Loaded v{}".format(VERSION))
        self.schedule_message(STARTUP_DELAY_TICKS, self._connect)

    def disconnect(self):
        self._running = False
        self._devices = []
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
    def _normalize(value):
        return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")

    @staticmethod
    def _all_surfaces():
        return list(getattr(builtins, "control_surfaces", []))

    def _surface_identifiers(self, surface):
        module = str(getattr(surface.__class__, "__module__", ""))
        module_root = module.split(".")[0] if module else ""
        class_name = str(getattr(surface.__class__, "__name__", ""))
        surface_name = str(getattr(surface, "name", ""))
        return {
            self._normalize(module_root),
            self._normalize(module),
            self._normalize(class_name),
            self._normalize(surface_name),
        }

    def _matching_surfaces(self, configured_match):
        target = self._normalize(configured_match)
        exact = []
        partial = []
        for surface in self._all_surfaces():
            if surface is self:
                continue
            identifiers = self._surface_identifiers(surface)
            if target in identifiers:
                exact.append(surface)
            elif ALLOW_PARTIAL_SURFACE_MATCH and any(
                target and target in identifier for identifier in identifiers
            ):
                partial.append(surface)
        return exact if exact else partial

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
        preferred = []
        fallback = []
        for component in self._components_for(surface):
            try:
                is_ring = (
                    component.__class__.__name__ == "SessionRingComponent"
                    and hasattr(component, "set_offsets")
                    and hasattr(component, "track_offset")
                    and hasattr(component, "scene_offset")
                )
                if not is_ring:
                    continue
                if getattr(component, "name", "") == "Session_Ring":
                    preferred.append(component)
                else:
                    fallback.append(component)
            except Exception:
                pass
        candidates = preferred or fallback
        return candidates[0] if candidates else None

    def _validate_config(self):
        if not isinstance(DEVICES, (list, tuple)) or len(DEVICES) < 2:
            raise ValueError("DEVICES must contain at least two device definitions")
        for index, config in enumerate(DEVICES):
            if not isinstance(config, dict):
                raise ValueError("DEVICES[{}] must be a dictionary".format(index))
            if not str(config.get("model", config.get("surface_match", ""))).strip():
                raise ValueError("DEVICES[{}] has no model".format(index))
            int(config.get("track_offset", 0))
            instance_index = int(config.get("instance_index", 0))
            if instance_index < 0:
                raise ValueError(
                    "DEVICES[{}] instance_index must be zero or greater".format(index)
                )

    def _connect(self):
        if not self._running:
            return
        try:
            self._validate_config()
            discovered = []
            unavailable = []

            for index, config in enumerate(DEVICES):
                label = str(config.get("label") or "Device {}".format(index + 1))
                configured_model = config.get("model", config.get("surface_match"))
                match = resolve_surface_match(configured_model)
                surfaces = self._matching_surfaces(match)
                instance_index = max(0, int(config.get("instance_index", 0)))

                if not surfaces:
                    unavailable.append("{}={!r}".format(label, match))
                    continue

                if instance_index >= len(surfaces):
                    unavailable.append(
                        "{}={!r} instance_index={} (only {} found)".format(
                            label, match, instance_index, len(surfaces)
                        )
                    )
                    continue

                selected_surface = surfaces[instance_index]
                if any(device["surface"] is selected_surface for device in discovered):
                    unavailable.append(
                        "{}={!r} instance_index={} (already assigned)".format(
                            label, match, instance_index
                        )
                    )
                    continue

                ring = self._find_session_ring(selected_surface)
                if ring is None:
                    unavailable.append(
                        "{}={!r} instance_index={} (no Session Ring)".format(
                            label, match, instance_index
                        )
                    )
                    continue

                discovered.append(
                    {
                        "label": label,
                        "model": str(configured_model),
                        "surface_match": match,
                        "instance_index": instance_index,
                        "surface": selected_surface,
                        "ring": ring,
                        "track_offset": max(0, int(config.get("track_offset", 0))),
                        "last_scene": int(ring.scene_offset),
                    }
                )

            if unavailable:
                self._log("WAITING: {}".format(", ".join(unavailable)))
                self.schedule_message(RECONNECT_TICKS, self._connect)
                return

            self._devices = discovered
            self._shared_scene = max(0, int(self._devices[0]["ring"].scene_offset))

            for device in self._devices:
                if INITIALIZE_HORIZONTAL_LAYOUT:
                    self._set_ring(
                        device["ring"], device["track_offset"], self._shared_scene
                    )
                else:
                    self._set_scene_only(device["ring"], self._shared_scene)
                device["last_scene"] = int(device["ring"].scene_offset)

            layout = "; ".join(
                "{}:{} track={} scene={}".format(
                    device["label"],
                    "{} -> {}[{}]".format(device["model"], device["surface_match"], device["instance_index"]),
                    device["ring"].track_offset,
                    device["ring"].scene_offset,
                )
                for device in self._devices
            )
            self._log(
                "CONNECTED v{} devices={} step={} horizontal_lock={} | {}".format(
                    VERSION,
                    len(self._devices),
                    VERTICAL_STEP_SCENES,
                    LOCK_HORIZONTAL,
                    layout,
                )
            )
            self.schedule_message(POLL_TICKS, self._poll)
        except Exception as error:
            self._log_exception("CONNECT", error)
            self.schedule_message(RECONNECT_TICKS, self._connect)

    @staticmethod
    def _set_ring(ring, track_offset, scene_offset):
        ring.set_offsets(max(0, int(track_offset)), max(0, int(scene_offset)))

    def _set_scene_only(self, ring, scene_offset):
        self._set_ring(ring, int(ring.track_offset), scene_offset)

    def _apply_vertical_scene(self, scene_offset):
        scene_offset = max(0, int(scene_offset))
        for device in self._devices:
            if LOCK_HORIZONTAL:
                self._set_ring(device["ring"], device["track_offset"], scene_offset)
            else:
                self._set_scene_only(device["ring"], scene_offset)
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
            if not self._devices:
                self.schedule_message(RECONNECT_TICKS, self._connect)
                return

            changed = []
            for device in self._devices:
                current = int(device["ring"].scene_offset)
                previous = int(device["last_scene"])
                if current != previous:
                    changed.append((device, self._direction(current, previous)))

            direction = 0
            source = None
            if SYNC_VERTICAL and changed:
                non_zero = [(device, value) for device, value in changed if value != 0]
                if non_zero:
                    direction = non_zero[0][1]
                    source = ",".join(device["label"] for device, _ in non_zero)
                    conflicting = any(value != direction for _, value in non_zero)
                    if conflicting:
                        self._log(
                            "WARNING: conflicting navigation directions detected; "
                            "using {} from {}".format(direction, source)
                        )
            elif SYNC_VERTICAL:
                scenes = [int(device["ring"].scene_offset) for device in self._devices]
                if any(scene != self._shared_scene for scene in scenes):
                    self._apply_vertical_scene(self._shared_scene)
                    source = "drift repair"

            if direction:
                target_scene = max(
                    0,
                    int(self._shared_scene)
                    + direction * max(1, int(VERTICAL_STEP_SCENES)),
                )
                self._apply_vertical_scene(target_scene)
                if VERBOSE_SYNC_LOGGING:
                    self._log(
                        "SYNC source={} direction={} scene={}".format(
                            source, direction, target_scene
                        )
                    )
            elif LOCK_HORIZONTAL:
                for device in self._devices:
                    ring = device["ring"]
                    if int(ring.track_offset) != int(device["track_offset"]):
                        self._set_ring(
                            ring, device["track_offset"], int(ring.scene_offset)
                        )

            for device in self._devices:
                device["last_scene"] = int(device["ring"].scene_offset)
        except Exception as error:
            self._log_exception("POLL", error)

        self.schedule_message(POLL_TICKS, self._poll)

    def _log_exception(self, stage, error):
        self._log("{} ERROR {!r}".format(stage, error))
        for line in traceback.format_exc().splitlines():
            self._log("TRACE {}".format(line))
