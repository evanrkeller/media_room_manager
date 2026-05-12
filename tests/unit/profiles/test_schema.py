"""Tests for profile schema validation."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
import voluptuous as vol

from custom_components.media_room_manager.profiles.schema import (
    POWER_HANDLING_VALUES,
    Profile,
    validate_profile,
)


def _minimal_valid_profile_dict() -> dict[str, object]:
    return {
        "profile_id": "apple_tv_4k",
        "manufacturer": "Apple",
        "model": "TV 4K",
        "category": "streamer",
        "power_handling": "discrete_capable",
    }


def test_validate_accepts_minimal_valid_profile() -> None:
    profile = validate_profile(_minimal_valid_profile_dict())
    assert isinstance(profile, Profile)
    assert profile.profile_id == "apple_tv_4k"
    assert profile.manufacturer == "Apple"
    assert profile.model == "TV 4K"
    assert profile.category == "streamer"
    assert profile.power_handling == "discrete_capable"


def test_validate_supplies_default_power_on_delay() -> None:
    profile = validate_profile(_minimal_valid_profile_dict())
    assert profile.power_on_delay == 0


def test_validate_supplies_default_empty_structural_fields() -> None:
    """Optional structural fields default to empty tuples — not None or absent."""
    profile = validate_profile(_minimal_valid_profile_dict())
    assert profile.output_groups == ()
    assert profile.interfaces == ()
    assert profile.virtual_sources == ()


def test_validate_collects_structural_fields_when_present() -> None:
    data = _minimal_valid_profile_dict() | {
        "power_on_delay": 3,
        "output_groups": [{"id": "main"}],
        "interfaces": [{"id": "hdmi_1", "direction": "input", "type": "hdmi", "label": "HDMI 1"}],
        "virtual_sources": [{"id": "tuner", "label": "AM/FM"}],
    }
    profile = validate_profile(data)
    assert profile.power_on_delay == 3
    assert profile.output_groups == ({"id": "main"},)
    assert profile.interfaces[0]["id"] == "hdmi_1"
    assert profile.virtual_sources[0]["id"] == "tuner"


def test_validate_allows_extra_top_level_fields() -> None:
    """Schema is permissive: richer profiles can include fields the dataclass
    does not yet surface. Later stories extend the dataclass."""
    data = _minimal_valid_profile_dict() | {"future_field": "not in dataclass"}
    profile = validate_profile(data)
    assert profile.profile_id == "apple_tv_4k"


@pytest.mark.parametrize(
    "missing_field",
    ["profile_id", "manufacturer", "model", "category", "power_handling"],
)
def test_validate_rejects_missing_required_field(missing_field: str) -> None:
    data = _minimal_valid_profile_dict()
    del data[missing_field]
    with pytest.raises(vol.Invalid):
        validate_profile(data)


def test_validate_rejects_wrong_type_for_profile_id() -> None:
    data = _minimal_valid_profile_dict() | {"profile_id": 42}
    with pytest.raises(vol.Invalid):
        validate_profile(data)


def test_validate_rejects_invalid_power_handling() -> None:
    """Per CLAUDE.md, only the four documented values are allowed."""
    data = _minimal_valid_profile_dict() | {"power_handling": "banana"}
    with pytest.raises(vol.Invalid):
        validate_profile(data)


@pytest.mark.parametrize("value", POWER_HANDLING_VALUES)
def test_validate_accepts_each_documented_power_handling_value(value: str) -> None:
    data = _minimal_valid_profile_dict() | {"power_handling": value}
    profile = validate_profile(data)
    assert profile.power_handling == value


def test_validate_rejects_non_list_output_groups() -> None:
    data = _minimal_valid_profile_dict() | {"output_groups": "not a list"}
    with pytest.raises(vol.Invalid):
        validate_profile(data)


def test_validate_rejects_non_dict_in_interfaces_list() -> None:
    data = _minimal_valid_profile_dict() | {"interfaces": ["not a dict"]}
    with pytest.raises(vol.Invalid):
        validate_profile(data)


def test_profile_is_frozen() -> None:
    profile = Profile(
        profile_id="x",
        manufacturer="X",
        model="Y",
        category="streamer",
        power_handling="discrete_capable",
    )
    with pytest.raises(FrozenInstanceError):
        profile.profile_id = "changed"  # type: ignore[misc]
