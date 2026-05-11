"""End-to-end test of the `media_room_manager/list_profiles` WebSocket command.

Exercises the full path: install integration via config entry → load
bundled profiles → register WebSocket command → call command via the
WebSocket harness → verify response shape and content.

This is the AC test for Story #45.
"""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry
from pytest_homeassistant_custom_component.typing import (
    WebSocketGenerator,
)

from custom_components.media_room_manager.const import DOMAIN


async def test_list_profiles_returns_bundled_profiles(
    hass: HomeAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """AC: list_profiles returns >=2 profiles, each with required fields,
    spanning >=2 distinct categories."""
    entry = MockConfigEntry(domain=DOMAIN, title="Media Room Manager")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    client = await hass_ws_client(hass)
    await client.send_json_auto_id({"type": "media_room_manager/list_profiles"})
    response = await client.receive_json()

    assert response["success"], response
    profiles = response["result"]

    assert isinstance(profiles, list)
    assert len(profiles) >= 2, "Bundled starter set should include at least two profiles"

    required_fields = {"profile_id", "manufacturer", "model", "category"}
    for profile in profiles:
        missing = required_fields - profile.keys()
        assert not missing, f"Profile {profile} missing fields: {missing}"

    categories = {p["category"] for p in profiles}
    assert len(categories) >= 2, (
        f"Bundled profiles should cover at least two categories; got {categories}"
    )


async def test_list_profiles_includes_known_starter_profiles(
    hass: HomeAssistant, hass_ws_client: WebSocketGenerator
) -> None:
    """The bundled starter set ships an Apple TV and a Marantz SR8015 — both
    should be discoverable via list_profiles."""
    entry = MockConfigEntry(domain=DOMAIN, title="Media Room Manager")
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    client = await hass_ws_client(hass)
    await client.send_json_auto_id({"type": "media_room_manager/list_profiles"})
    response = await client.receive_json()

    assert response["success"], response
    ids = {p["profile_id"] for p in response["result"]}
    assert "apple_tv_4k" in ids
    assert "marantz_sr8015" in ids
