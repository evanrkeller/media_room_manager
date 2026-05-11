"""Media Room Manager — Home Assistant custom integration.

Sets up the integration's bundled profile registry on first config-entry
setup and registers the WebSocket command surface used by Story #45's
`media_room_manager/list_profiles` command.
"""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from custom_components.media_room_manager.const import DOMAIN
from custom_components.media_room_manager.profiles.registry import (
    ProfileRegistry,
    load_bundled_profiles,
)
from custom_components.media_room_manager.websocket import async_register_commands

_LOGGER = logging.getLogger(__name__)

_BUNDLED_PROFILES_DIR = Path(__file__).parent / "profiles" / "bundled"


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Media Room Manager from a config entry.

    Bundled profiles are static (read from package YAML), so they're loaded
    once for the HA process lifetime on the first entry setup. WebSocket
    commands are likewise registered once.
    """
    if DOMAIN not in hass.data:
        profiles = await hass.async_add_executor_job(load_bundled_profiles, _BUNDLED_PROFILES_DIR)
        hass.data[DOMAIN] = {"profile_registry": ProfileRegistry(profiles)}
        async_register_commands(hass)
        _LOGGER.info("Loaded %d bundled device profiles", len(profiles))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry.

    The bundled profile registry and WebSocket command registrations are
    process-global and intentionally outlive a single config entry —
    cleanup happens at HA shutdown.
    """
    return True
