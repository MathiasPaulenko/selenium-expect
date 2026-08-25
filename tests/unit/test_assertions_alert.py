"""Unit tests for selenium_expect.assertions.alert.ExpectAlert."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect
from selenium_expect.assertions.alert import ExpectAlert


class TestExpectAlert:
    def test_to_be_present(self, mock_alert: Any) -> None:
        """expect(alert).to_be_present() passes."""
        expect(mock_alert).to_be_present()

    def test_to_have_text(self, mock_alert: Any) -> None:
        """expect(alert).to_have_text('Are you sure?') passes."""
        expect(mock_alert).to_have_text("Are you sure?")

    def test_to_have_text_contains(self, mock_alert: Any) -> None:
        """expect(alert).to_have_text_contains('you sure') passes."""
        expect(mock_alert).to_have_text_contains("you sure")

    def test_to_have_text_matches(self, mock_alert: Any) -> None:
        """expect(alert).to_have_text_matches(r'Are you sure\\?') passes."""
        expect(mock_alert).to_have_text_matches(r"Are you sure\?")

    def test_not_to_have_text(self, mock_alert: Any) -> None:
        """expect(alert).not_.to_have_text('Wrong') passes."""
        expect(mock_alert).not_.to_have_text("Wrong text")

    def test_to_have_text_fails(self, mock_alert: Any) -> None:
        """expect(alert).to_have_text('Wrong') raises."""
        with pytest.raises(AssertionError, match="to have text"):
            expect(mock_alert).to_have_text("Wrong text")

    def test_to_have_text_contains_fails(self, mock_alert: Any) -> None:
        """expect(alert).to_have_text_contains('Missing') raises."""
        with pytest.raises(AssertionError, match="to have text containing"):
            expect(mock_alert).to_have_text_contains("Missing")


class TestExpectAlertDispatch:
    def test_expect_dispatches_to_alert(self, mock_alert: Any) -> None:
        """expect(alert) returns ExpectAlert instance."""
        result = expect(mock_alert)
        assert isinstance(result, ExpectAlert)
