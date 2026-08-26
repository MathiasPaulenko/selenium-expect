"""Smoke test — verifies the package is importable and version is correct."""

import selenium_expect


def test_version() -> None:
    assert selenium_expect.__version__ == "0.1.0"


def test_all_exports() -> None:
    expected = {
        "ExpectConfig",
        "SoftAssertionCollector",
        "assert_all",
        "expect",
        "extend",
        "get_config",
        "merge_expects",
        "poll",
        "set_debug_mode",
        "set_default_polling_interval",
        "set_default_polling_intervals",
        "set_default_timeout",
        "set_screenshot_on_failure",
    }
    assert set(selenium_expect.__all__) == expected
