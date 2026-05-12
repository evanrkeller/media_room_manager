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


def _profile_to_dict(profile: Profile) -> dict[str, str]:
    """Serialize a `Profile` for WebSocket responses."""
    return {
        "profile_id": profile.profile_id,
        "manufacturer": profile.manufacturer,
        "model": profile.model,
        "category": profile.category,
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
    """Return all bundled device profiles as JSON-serializable dicts.

    Returns an empty array if the integration is not yet set up or
    no profiles are bundled — the AC for Story #45 explicitly requires
    the empty case to be a successful empty result, not an error.
    """
    domain_data = hass.data.get(DOMAIN, {})
    registry = domain_data.get("profile_registry")
    if registry is None:
        connection.send_result(msg["id"], [])
        return
    profiles = [_profile_to_dict(p) for p in registry.list_all()]
    connection.send_result(msg["id"], profiles)


def async_register_commands(hass: HomeAssistant) -> None:
    """Register all Media Room Manager WebSocket commands with HA."""
    websocket_api.async_register_command(hass, handle_list_profiles)
