"""Tests for profile schema validation."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
import voluptuous as vol

from custom_components.media_room_manager.profiles.schema import (
    Profile,
    validate_profile,
)


def test_validate_accepts_minimal_valid_profile() -> None:
    data = {
        "profile_id": "apple_tv_4k",
        "manufacturer": "Apple",
        "model": "TV 4K",
        "category": "streamer",
    }
    profile = validate_profile(data)
    assert isinstance(profile, Profile)
    assert profile.profile_id == "apple_tv_4k"
    assert profile.manufacturer == "Apple"
    assert profile.model == "TV 4K"
    assert profile.category == "streamer"


def test_validate_allows_extra_fields() -> None:
    """Schema is permissive: richer profiles can include fields the dataclass
    does not yet surface. Story #46 will read those richer fields."""
    data = {
        "profile_id": "x",
        "manufacturer": "X",
        "model": "Y",
        "category": "streamer",
        "future_field": "not in dataclass",
    }
    profile = validate_profile(data)
    assert profile.profile_id == "x"


def test_validate_rejects_missing_required_field() -> None:
    with pytest.raises(vol.Invalid):
        validate_profile({"profile_id": "x", "manufacturer": "X", "model": "Y"})


def test_validate_rejects_wrong_type() -> None:
    with pytest.raises(vol.Invalid):
        validate_profile(
            {
                "profile_id": 42,
                "manufacturer": "X",
                "model": "Y",
                "category": "streamer",
            }
        )


def test_profile_is_frozen() -> None:
    profile = Profile(profile_id="x", manufacturer="X", model="Y", category="streamer")
    with pytest.raises(FrozenInstanceError):
        profile.profile_id = "changed"  # type: ignore[misc]
