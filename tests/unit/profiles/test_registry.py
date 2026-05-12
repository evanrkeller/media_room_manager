"""Tests for ProfileRegistry and bundled-profile loading."""

from __future__ import annotations

from pathlib import Path

from custom_components.media_room_manager.profiles.registry import (
    ProfileRegistry,
    load_bundled_profiles,
)
from custom_components.media_room_manager.profiles.schema import Profile


def _write_profile(tmp_path: Path, profile_id: str, category: str = "streamer") -> None:
    (tmp_path / f"{profile_id}.yaml").write_text(
        f"profile_id: {profile_id}\n"
        f"manufacturer: TestMfr\n"
        f"model: TestModel\n"
        f"category: {category}\n"
        f"power_handling: discrete_capable\n",
        encoding="utf-8",
    )


def test_load_empty_directory_returns_empty_dict(tmp_path: Path) -> None:
    """AC: empty bundled directory must not raise."""
    assert load_bundled_profiles(tmp_path) == {}


def test_load_nonexistent_directory_returns_empty_dict(tmp_path: Path) -> None:
    """A missing bundled/ directory should not raise — graceful empty result."""
    assert load_bundled_profiles(tmp_path / "does_not_exist") == {}


def test_load_one_profile(tmp_path: Path) -> None:
    _write_profile(tmp_path, "apple_tv_4k", "streamer")
    profiles = load_bundled_profiles(tmp_path)
    assert "apple_tv_4k" in profiles
    assert profiles["apple_tv_4k"].manufacturer == "TestMfr"
    assert profiles["apple_tv_4k"].category == "streamer"


def test_load_multiple_profiles_keyed_by_id(tmp_path: Path) -> None:
    _write_profile(tmp_path, "apple_tv_4k", "streamer")
    _write_profile(tmp_path, "marantz_sr8015", "avr")
    profiles = load_bundled_profiles(tmp_path)
    assert set(profiles.keys()) == {"apple_tv_4k", "marantz_sr8015"}


def test_load_ignores_non_yaml_files(tmp_path: Path) -> None:
    """Stray files in bundled/ should not break loading."""
    _write_profile(tmp_path, "apple_tv_4k", "streamer")
    (tmp_path / "README.md").write_text("not a profile", encoding="utf-8")
    profiles = load_bundled_profiles(tmp_path)
    assert set(profiles.keys()) == {"apple_tv_4k"}


def test_registry_list_all_returns_sorted_profiles() -> None:
    """Sort ordering is documented in `ProfileRegistry.list_all`'s docstring."""
    profiles = {
        "z_profile": Profile("z_profile", "Z", "z", "streamer", "discrete_capable"),
        "a_profile": Profile("a_profile", "A", "a", "avr", "discrete_capable"),
    }
    registry = ProfileRegistry(profiles)
    ids = [p.profile_id for p in registry.list_all()]
    assert ids == ["a_profile", "z_profile"]


def test_registry_get_known_profile_returns_it() -> None:
    profile = Profile("apple_tv_4k", "Apple", "TV 4K", "streamer", "discrete_capable")
    registry = ProfileRegistry({"apple_tv_4k": profile})
    assert registry.get("apple_tv_4k") is profile


def test_registry_get_unknown_returns_none() -> None:
    registry = ProfileRegistry({})
    assert registry.get("nonexistent") is None


def test_empty_registry_list_all_returns_empty_list() -> None:
    """AC for Story #45: empty bundled set returns [], not an error."""
    registry = ProfileRegistry({})
    assert registry.list_all() == []
