"""Integration tests for composition assertions."""

from __future__ import annotations

from typing import Any

import pytest
from selenium.webdriver.common.by import By

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationCompose:
    def test_satisfy_all(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "btn-enabled")

        def is_visible(target: Any) -> None:
            assert target.is_displayed()

        def is_enabled(target: Any) -> None:
            assert target.is_enabled()

        expect(el).to_satisfy_all(is_visible, is_enabled)

    def test_satisfy_any(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "btn-enabled")

        def is_selected(target: Any) -> None:
            assert target.is_selected()

        def is_enabled(target: Any) -> None:
            assert target.is_enabled()

        expect(el).to_satisfy_any(is_selected, is_enabled)

    def test_satisfy_none(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "btn-enabled")

        def is_selected(target: Any) -> None:
            assert target.is_selected()

        def is_disabled(target: Any) -> None:
            assert not target.is_enabled()

        expect(el).to_satisfy_none(is_selected, is_disabled)
