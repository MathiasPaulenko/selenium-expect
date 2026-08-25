"""Integration tests for Alert assertions."""

from __future__ import annotations

from typing import Any

import pytest
from selenium.webdriver.common.by import By

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationAlert:
    def test_alert_present(self, test_page: Any) -> None:
        test_page.find_element(By.ID, "alert-btn").click()
        alert = test_page.switch_to.alert
        expect(alert).to_be_present(timeout=3.0)
        alert.accept()

    def test_alert_text(self, test_page: Any) -> None:
        test_page.find_element(By.ID, "alert-btn").click()
        alert = test_page.switch_to.alert
        expect(alert).to_have_text("Test Alert", timeout=3.0)
        alert.accept()
