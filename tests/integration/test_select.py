"""Integration tests for Select assertions."""

from __future__ import annotations

from typing import Any

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationSelect:
    def test_value(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "select-single")
        select = Select(el)
        expect(select).to_have_value("banana")

    def test_selected_text(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "select-single")
        select = Select(el)
        expect(select).to_have_selected_text("Banana")

    def test_option_count(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "select-single")
        select = Select(el)
        expect(select).to_have_option_count(3)

    def test_multiple_selected_values(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "select-multiple")
        select = Select(el)
        expect(select).to_have_selected_values(["green", "blue"])

    def test_is_multiple(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "select-multiple")
        select = Select(el)
        expect(select).to_be_multiple()

    def test_is_single(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "select-single")
        select = Select(el)
        expect(select).not_.to_be_multiple()
