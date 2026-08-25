"""Integration tests for JS / browser state assertions."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationJS:
    def test_js_result(self, test_page: Any) -> None:
        expect(test_page).to_have_js_result("return 1 + 1", 2)

    def test_local_storage_item(self, test_page: Any) -> None:
        expect(test_page).to_have_local_storage_item("test-key", "test-value")

    def test_local_storage_length(self, test_page: Any) -> None:
        expect(test_page).to_have_local_storage_length(2)

    def test_session_storage_item(self, test_page: Any) -> None:
        expect(test_page).to_have_session_storage_item("session-key", "session-value")
