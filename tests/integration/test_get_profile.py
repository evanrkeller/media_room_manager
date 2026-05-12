"""End-to-end test of the `media_room_manager/get_profile` WebSocket command.

Exercises the full path: install integration via config entry → load bundled
profiles → register WebSocket command → call command via the WebSocket harness
→ verify response shape, content, and error cases.

This is the AC test for Story #46.
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.typing import WebSocketGenerator

from custom_components.media_room_manager.const import DOMAIN


async def _setup(hass: HomeAssistant) -> None:
    entry = MockConfigEntry(domain=DOMAIN, title="Media Room Manager")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_get_profile_returns_full_profile_for_known_id(
    hass: HomeAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """AC: get_profile returns identity + structural fields for a valid id."""
    await _setup(hass)
    client = await hass_ws_client(hass)
    await client.send_json_auto_id(
        {"type": "media_room_manager/get_profile", "profile_id": "apple_tv_4k"}
    )
    response = await client.receive_json()

    assert response["success"], response
    profile = response["result"]

    # Identity fields
    assert profile["profile_id"] == "apple_tv_4k"
    assert profile["manufacturer"] == "Apple"
    assert profile["model"] == "TV 4K"
    assert profile["category"] == "streamer"

    # Structural fields (presence, not deep shape — schema loose for now)
    assert profile["power_handling"] in {
        "discrete_capable",
        "toggle",
        "always_on",
        "disabled",
    }
    assert isinstance(profile["power_on_delay"], int)
    assert isinstance(profile["output_groups"], list)
    assert isinstance(profile["interfaces"], list)
    assert isinstance(profile["virtual_sources"], list)


async def test_get_profile_unknown_id_returns_error(
    hass: HomeAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """AC: unknown profile_id returns a clear error naming the id."""
    await _setup(hass)
    client = await hass_ws_client(hass)
    await client.send_json_auto_id(
        {
            "type": "media_room_manager/get_profile",
            "profile_id": "no_such_profile",
        }
    )
    response = await client.receive_json()

    assert response["success"] is False
    assert response["error"]["code"] == "not_found"
    assert "no_such_profile" in response["error"]["message"]


async def test_get_profile_missing_id_returns_validation_error(
    hass: HomeAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """AC: missing profile_id parameter returns a validation error."""
    await _setup(hass)
    client = await hass_ws_client(hass)
    await client.send_json_auto_id({"type": "media_room_manager/get_profile"})
    response = await client.receive_json()

    assert response["success"] is False
    assert response["error"]["code"] == "invalid_format"


async def test_get_profile_wrong_type_id_returns_validation_error(
    hass: HomeAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """AC: wrong-type profile_id (not a string) returns a validation error."""
    await _setup(hass)
    client = await hass_ws_client(hass)
    await client.send_json_auto_id({"type": "media_room_manager/get_profile", "profile_id": 42})
    response = await client.receive_json()

    assert response["success"] is False
    assert response["error"]["code"] == "invalid_format"


async def test_get_profile_returns_marantz_with_virtual_sources(
    hass: HomeAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """The Marantz starter profile carries an AM/FM tuner virtual source —
    confirms structural fields are surfaced through the command."""
    await _setup(hass)
    client = await hass_ws_client(hass)
    await client.send_json_auto_id(
        {
            "type": "media_room_manager/get_profile",
            "profile_id": "marantz_sr8015",
        }
    )
    response = await client.receive_json()

    assert response["success"], response
    profile = response["result"]
    assert profile["profile_id"] == "marantz_sr8015"
    assert len(profile["virtual_sources"]) >= 1
    assert any(vs.get("id") == "tuner" for vs in profile["virtual_sources"])
