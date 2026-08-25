"""Integration tests for soft assertions."""

from __future__ import annotations

from typing import Any

import pytest
from selenium.webdriver.common.by import By

from selenium_expect import assert_all, expect

pytestmark = pytest.mark.integration


class TestIntegrationSoft:
    def test_soft_accumulates(self, test_page: Any) -> None:
        """Soft assertions accumulate failures without raising."""
        el = test_page.find_element(By.ID, "title")
        expect(el, soft=True).to_have_text("Wrong Text")
        expect(el, soft=True).to_have_tag("wrong")
        # Should not raise here

    def test_assert_all_raises(self, test_page: Any) -> None:
        """assert_all() raises after soft failures."""
        el = test_page.find_element(By.ID, "title")
        expect(el, soft=True).to_have_text("Wrong Text")
        with pytest.raises(AssertionError):
            assert_all()
