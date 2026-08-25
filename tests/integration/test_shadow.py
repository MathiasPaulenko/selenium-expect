"""Integration tests for Shadow DOM assertions."""

from __future__ import annotations

from typing import Any

import pytest
from selenium.webdriver.common.by import By

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationShadow:
    def test_shadow_element(self, test_page: Any) -> None:
        host = test_page.find_element(By.ID, "shadow-host")
        shadow_root = host.shadow_root
        el = shadow_root.find_element(By.CSS_SELECTOR, "#shadow-text")
        expect(el).to_be_present()

    def test_shadow_element_text(self, test_page: Any) -> None:
        host = test_page.find_element(By.ID, "shadow-host")
        shadow_root = host.shadow_root
        el = shadow_root.find_element(By.CSS_SELECTOR, "#shadow-text")
        expect(el).to_have_text("Shadow content")

    def test_shadow_element_visible(self, test_page: Any) -> None:
        host = test_page.find_element(By.ID, "shadow-host")
        shadow_root = host.shadow_root
        el = shadow_root.find_element(By.CSS_SELECTOR, "#shadow-btn")
        expect(el).to_be_visible()
