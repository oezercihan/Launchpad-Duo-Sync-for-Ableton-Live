"""Friendly device model names mapped to Ableton Control Surface identifiers."""

SUPPORTED_MODELS = {
    "Launchpad X": "Launchpad_X",
    "Launchpad Mini MK3": "Launchpad_Mini_MK3",
    "Launchpad Pro MK3": "Launchpad_Pro_MK3",
    "Launchpad Pro": "Launchpad_Pro",
    "Launchpad MK2": "Launchpad_MK2",
    "Launchpad": "Launchpad",
}


def normalize_model_name(value):
    return str(value or "").strip().lower().replace("-", " ").replace("_", " ")


def resolve_surface_match(model):
    """Resolve a friendly name, alias, or raw Ableton script name.

    A raw value such as ``Launchpad_X`` remains valid, which makes the script
    forward-compatible with models not yet listed in SUPPORTED_MODELS.
    """
    raw = str(model or "").strip()
    if not raw:
        raise ValueError("device model is empty")

    wanted = normalize_model_name(raw)
    for friendly_name, script_name in SUPPORTED_MODELS.items():
        if wanted in (
            normalize_model_name(friendly_name),
            normalize_model_name(script_name),
        ):
            return script_name

    # Advanced/future-model fallback: accept the exact Ableton script name.
    return raw
