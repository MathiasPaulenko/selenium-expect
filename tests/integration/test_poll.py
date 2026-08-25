"""Integration tests for poll() assertions."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect, poll

pytestmark = pytest.mark.integration


class TestIntegrationPoll:
    def test_poll_js_result(self, test_page: Any) -> None:
        poll(lambda: test_page.execute_script("return 1 + 1"), timeout=2.0).to_equal(2)

    def test_poll_local_storage(self, test_page: Any) -> None:
        poll(
            lambda: test_page.execute_script("return localStorage.getItem('test-key')"),
            timeout=2.0,
        ).to_equal("test-value")

    def test_expect_poll(self, test_page: Any) -> None:
        expect.poll(
            lambda: test_page.execute_script("return document.title"),
            timeout=2.0,
        ).to_equal("Test Page")
