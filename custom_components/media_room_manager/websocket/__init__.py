"""WebSocket commands for Media Room Manager.

Per the project's CLAUDE.md boundary, every command's contract is
documented in `docs/websocket-api.md`. Schema changes ship in the
same commit as docs updates.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant
import voluptuous as vol

from custom_components.media_room_manager.const import DOMAIN
from custom_components.media_room_manager.profiles.schema import Profile


def _profile_summary_dict(profile: Profile) -> dict[str, str]:
    """Identity-only serialization — used by `list_profiles`."""
    return {
        "profile_id": profile.profile_id,
        "manufacturer": profile.manufacturer,
        "model": profile.model,
        "category": profile.category,
    }


def _profile_full_dict(profile: Profile) -> dict[str, Any]:
    """Full serialization — used by `get_profile`."""
    return {
        "profile_id": profile.profile_id,
        "manufacturer": profile.manufacturer,
        "model": profile.model,
        "category": profile.category,
        "power_handling": profile.power_handling,
        "power_on_delay": profile.power_on_delay,
        "output_groups": list(profile.output_groups),
        "interfaces": list(profile.interfaces),
        "virtual_sources": list(profile.virtual_sources),
    }


@websocket_api.websocket_command(
    {
        vol.Required("type"): "media_room_manager/list_profiles",
    }
)
@websocket_api.async_response
async def handle_list_profiles(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return all bundled device profiles, identity fields only.

    Returns an empty array if the integration is not yet set up or no
    profiles are bundled — Story #45 explicitly requires the empty case
    to be a successful empty result, not an error.
    """
    domain_data = hass.data.get(DOMAIN, {})
    registry = domain_data.get("profile_registry")
    if registry is None:
        connection.send_result(msg["id"], [])
        return
    profiles = [_profile_summary_dict(p) for p in registry.list_all()]
    connection.send_result(msg["id"], profiles)


@websocket_api.websocket_command(
    {
        vol.Required("type"): "media_room_manager/get_profile",
        vol.Required("profile_id"): str,
    }
)
@websocket_api.async_response
async def handle_get_profile(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    """Return the full profile for the requested `profile_id`.

    Per Story #46:
    - Unknown `profile_id` → `not_found` error naming the id.
    - Missing/wrong-type `profile_id` → handled by HA's WebSocket schema
      layer as an `invalid_format` validation error.
    """
    domain_data = hass.data.get(DOMAIN, {})
    registry = domain_data.get("profile_registry")
    profile_id = msg["profile_id"]
    if registry is None:
        connection.send_error(
            msg["id"],
            "not_loaded",
            "Media Room Manager profile registry is not loaded.",
        )
        return
    profile = registry.get(profile_id)
    if profile is None:
        connection.send_error(
            msg["id"],
            "not_found",
            f"No profile with profile_id={profile_id!r} is bundled or registered.",
        )
        return
    connection.send_result(msg["id"], _profile_full_dict(profile))


def async_register_commands(hass: HomeAssistant) -> None:
    """Register all Media Room Manager WebSocket commands with HA."""
    websocket_api.async_register_command(hass, handle_list_profiles)
    websocket_api.async_register_command(hass, handle_get_profile)
