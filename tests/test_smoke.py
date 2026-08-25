"""Smoke test — verifies the package is importable and version is correct."""

import selenium_expect


def test_version() -> None:
    assert selenium_expect.__version__ == "0.1.0"


def test_all_empty() -> None:
    assert selenium_expect.__all__ == []
