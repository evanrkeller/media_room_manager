"""Profile YAML schema and Profile dataclass.

Narrowed to fields Story #45 (list_profiles) and Story #46 (get_profile)
require. Additional fields are accepted (extra=ALLOW_EXTRA) so richer
bundled profiles can include data the dataclass doesn't surface yet —
later stories extend the dataclass to expose those fields without
breaking existing YAMLs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import voluptuous as vol


@dataclass(frozen=True)
class Profile:
    """A device profile from the bundled or community library."""

    profile_id: str
    manufacturer: str
    model: str
    category: str


PROFILE_SCHEMA = vol.Schema(
    {
        vol.Required("profile_id"): str,
        vol.Required("manufacturer"): str,
        vol.Required("model"): str,
        vol.Required("category"): str,
    },
    extra=vol.ALLOW_EXTRA,
)


def validate_profile(data: dict[str, Any]) -> Profile:
    """Validate a profile dict and return a typed `Profile`.

    Raises `voluptuous.Invalid` if required fields are missing or
    have the wrong type.
    """
    validated = PROFILE_SCHEMA(data)
    return Profile(
        profile_id=validated["profile_id"],
        manufacturer=validated["manufacturer"],
        model=validated["model"],
        category=validated["category"],
    )
