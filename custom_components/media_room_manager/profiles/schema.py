"""Profile YAML schema and Profile dataclass.

Narrowed to fields stories #45 (list_profiles) and #46 (get_profile)
require — identity fields plus a loose representation of structural
fields (output groups, interfaces, virtual sources, power handling).

Inner structural shapes are intentionally loose at this stage. Tighter
validation lands when later stories (e.g., path resolution) need to
reason about those structures programmatically.

Additional top-level fields are accepted (`extra=ALLOW_EXTRA`) so
richer bundled profiles can include data the dataclass doesn't surface
yet — later stories extend the dataclass without breaking existing
YAMLs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import voluptuous as vol

# Per CLAUDE.md, the four allowed values for `power_handling`. The set is
# fixed at the spec level and intentionally not extensible.
POWER_HANDLING_VALUES = ("discrete_capable", "toggle", "always_on", "disabled")


@dataclass(frozen=True)
class Profile:
    """A device profile from the bundled or community library.

    Top-level container is frozen (`frozen=True`); the dicts inside the
    structural-field tuples are conventionally treated as read-only after
    validation. Mutating them is unsupported.
    """

    profile_id: str
    manufacturer: str
    model: str
    category: str
    power_handling: str
    power_on_delay: int = 0
    output_groups: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    interfaces: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    virtual_sources: tuple[dict[str, Any], ...] = field(default_factory=tuple)


PROFILE_SCHEMA = vol.Schema(
    {
        vol.Required("profile_id"): str,
        vol.Required("manufacturer"): str,
        vol.Required("model"): str,
        vol.Required("category"): str,
        vol.Required("power_handling"): vol.In(POWER_HANDLING_VALUES),
        vol.Optional("power_on_delay", default=0): int,
        vol.Optional("output_groups", default=list): [dict],
        vol.Optional("interfaces", default=list): [dict],
        vol.Optional("virtual_sources", default=list): [dict],
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
        power_handling=validated["power_handling"],
        power_on_delay=validated["power_on_delay"],
        output_groups=tuple(validated["output_groups"]),
        interfaces=tuple(validated["interfaces"]),
        virtual_sources=tuple(validated["virtual_sources"]),
    )
