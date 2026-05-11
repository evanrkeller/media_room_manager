"""Profile registry — in-memory store of loaded device profiles."""

from __future__ import annotations

from pathlib import Path

import yaml

from custom_components.media_room_manager.profiles.schema import (
    Profile,
    validate_profile,
)


def load_bundled_profiles(bundled_dir: Path) -> dict[str, Profile]:
    """Load every YAML profile in `bundled_dir`.

    Synchronous — call from an executor in async contexts so the event
    loop is not blocked on file I/O. Returns an empty dict if the
    directory does not exist or contains no YAML files (the empty case
    is the AC for Story #45).
    """
    profiles: dict[str, Profile] = {}
    if not bundled_dir.exists():
        return profiles
    for yaml_path in sorted(bundled_dir.glob("*.yaml")):
        with yaml_path.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        profile = validate_profile(data)
        profiles[profile.profile_id] = profile
    return profiles


class ProfileRegistry:
    """In-memory registry of loaded profiles, keyed by `profile_id`."""

    def __init__(self, profiles: dict[str, Profile]) -> None:
        """Construct from a pre-loaded mapping of profile_id -> Profile."""
        self._profiles: dict[str, Profile] = dict(profiles)

    def list_all(self) -> list[Profile]:
        """Return all loaded profiles, sorted by `profile_id` for stable output."""
        return sorted(self._profiles.values(), key=lambda p: p.profile_id)

    def get(self, profile_id: str) -> Profile | None:
        """Return the profile with the given id, or `None` if not found."""
        return self._profiles.get(profile_id)
