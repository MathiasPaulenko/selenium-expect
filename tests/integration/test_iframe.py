"""Integration tests for iframe assertions."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationIframe:
    def test_frame_available(self, test_page: Any) -> None:
        expect(test_page).to_have_frame_available("test-iframe")

    def test_frame_count(self, test_page: Any) -> None:
        expect(test_page).to_have_frame_count(1)

    def test_frame_text(self, test_page: Any) -> None:
        expect(test_page).to_have_frame_text("test-iframe", "Iframe content")
