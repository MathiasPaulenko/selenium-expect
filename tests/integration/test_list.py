"""Integration tests for list assertions."""

from __future__ import annotations

from typing import Any

import pytest
from selenium.webdriver.common.by import By

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationList:
    def test_count(self, test_page: Any) -> None:
        items = test_page.find_elements(By.CSS_SELECTOR, "#item-list li")
        expect(items).to_have_count(3)

    def test_texts(self, test_page: Any) -> None:
        items = test_page.find_elements(By.CSS_SELECTOR, "#item-list li")
        expect(items).to_have_texts(["Item 1", "Item 2", "Item 3"])

    def test_text_at(self, test_page: Any) -> None:
        items = test_page.find_elements(By.CSS_SELECTOR, "#item-list li")
        expect(items).to_have_text_at(0, "Item 1")

    def test_all_visible(self, test_page: Any) -> None:
        items = test_page.find_elements(By.CSS_SELECTOR, "#item-list li")
        expect(items).to_have_all_visible()

    def test_any_visible(self, test_page: Any) -> None:
        items = test_page.find_elements(By.CSS_SELECTOR, "#item-list li")
        expect(items).to_have_any_visible()
