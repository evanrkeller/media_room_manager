"""Config flow for Media Room Manager.

Single-entry, no user input. Per `README.md`, configuration happens in
the integration's panel rather than via the config flow; the flow exists
solely to install the integration.
"""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from custom_components.media_room_manager.const import DOMAIN


class MediaRoomManagerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the install-only config flow for Media Room Manager."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial install step. Single-instance only."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        return self.async_create_entry(title="Media Room Manager", data={})
