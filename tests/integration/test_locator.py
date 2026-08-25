"""Integration tests for LocatorExpect."""

from __future__ import annotations

from typing import Any

import pytest
from selenium.webdriver.common.by import By

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationLocator:
    def test_locator_finds_element(self, test_page: Any) -> None:
        expect(test_page, by=By.ID, value="title", timeout=2.0).to_be_visible()

    def test_locator_retries_when_not_found(self, test_page: Any) -> None:
        with pytest.raises(AssertionError):
            expect(test_page, by=By.ID, value="nonexistent", timeout=0.5).to_be_visible()

    def test_locator_to_have_text(self, test_page: Any) -> None:
        expect(test_page, by=By.ID, value="title", timeout=2.0).to_have_text("Hello World")
