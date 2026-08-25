"""Integration tests for Cookie assertions."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect

pytestmark = pytest.mark.integration


@pytest.fixture()
def cookie_driver(test_page: Any) -> Any:
    """Navigate to a real HTTP origin so cookies can be set."""
    test_page.get("https://example.com")
    test_page.add_cookie({"name": "test-cookie", "value": "test-cookie-value"})
    return test_page


class TestIntegrationCookie:
    def test_cookie_exists(self, cookie_driver: Any) -> None:
        expect(cookie_driver).to_have_cookie("test-cookie")

    def test_cookie_value(self, cookie_driver: Any) -> None:
        expect(cookie_driver).to_have_cookie_value("test-cookie", "test-cookie-value")

    def test_cookie_count(self, cookie_driver: Any) -> None:
        expect(cookie_driver).to_have_cookie_count(1)
