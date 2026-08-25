"""selenium-expect — Playwright-style expect() for Selenium Python."""

from __future__ import annotations

from selenium_expect._config import (
    ExpectConfig,
    get_config,
    set_debug_mode,
    set_default_polling_interval,
    set_default_polling_intervals,
    set_default_timeout,
    set_screenshot_on_failure,
)
from selenium_expect._expect import expect
from selenium_expect._matcher import extend
from selenium_expect._poll import poll
from selenium_expect._soft import SoftAssertionCollector, assert_all

__version__ = "0.1.0"

expect.poll = poll  # type: ignore[attr-defined]

__all__: list[str] = [
    "ExpectConfig",
    "SoftAssertionCollector",
    "assert_all",
    "expect",
    "extend",
    "get_config",
    "poll",
    "set_debug_mode",
    "set_default_polling_interval",
    "set_default_polling_intervals",
    "set_default_timeout",
    "set_screenshot_on_failure",
]
