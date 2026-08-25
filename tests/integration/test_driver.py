"""Integration tests for driver-level assertions."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationDriver:
    def test_title_exact(self, test_page: Any) -> None:
        expect(test_page).to_have_title("Test Page")

    def test_title_contains(self, test_page: Any) -> None:
        expect(test_page).to_have_title_contains("Test")

    def test_title_matches(self, test_page: Any) -> None:
        expect(test_page).to_have_title_matches(r"Test \w+")

    def test_url_contains(self, test_page: Any) -> None:
        expect(test_page).to_have_url_contains("test_page")

    def test_url_matches(self, test_page: Any) -> None:
        expect(test_page).to_have_url_matches(r"test_page\.html")

    def test_window_count(self, test_page: Any) -> None:
        expect(test_page).to_have_window_count(1)

    def test_page_source_contains(self, test_page: Any) -> None:
        expect(test_page).to_have_page_source_contains("Hello World")

    def test_browser_name(self, test_page: Any) -> None:
        expect(test_page).to_have_browser_name("chrome")

    def test_capability(self, test_page: Any) -> None:
        expect(test_page).to_have_capability("browserName", "chrome")
