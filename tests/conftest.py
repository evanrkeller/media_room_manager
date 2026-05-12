"""Pytest configuration for Media Room Manager tests.

Enables the HA test harness fixtures (`hass`, `hass_ws_client`, etc.)
and turns on `enable_custom_integrations` for every test so HA can
discover our `custom_components/media_room_manager` package.
"""

from __future__ import annotations

from collections.abc import Generator

import pytest

pytest_plugins = ["pytest_homeassistant_custom_component"]


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(
    enable_custom_integrations: None,
) -> Generator[None]:
    """Automatically enable our custom integration for every test."""
    yield
