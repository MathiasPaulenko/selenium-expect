"""Unit tests for _base.py features: dual timeout and screenshot on failure."""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import MagicMock

import pytest

from selenium_expect import expect
from selenium_expect._config import set_screenshot_on_failure
from selenium_expect.assertions._base import _normalize_timeout


class TestNormalizeTimeout:
    def test_int_below_1000_treated_as_seconds(self) -> None:
        assert _normalize_timeout(5) == 5.0

    def test_int_above_1000_treated_as_milliseconds(self) -> None:
        assert _normalize_timeout(5000) == 5.0

    def test_int_1000_treated_as_milliseconds(self) -> None:
        assert _normalize_timeout(1000) == 1.0

    def test_int_999_treated_as_seconds(self) -> None:
        assert _normalize_timeout(999) == 999.0

    def test_float_treated_as_seconds(self) -> None:
        assert _normalize_timeout(0.5) == 0.5

    def test_float_above_1000_treated_as_seconds(self) -> None:
        """Floats are always seconds — only ints >= 1000 are milliseconds."""
        assert _normalize_timeout(5000.0) == 5000.0

    def test_zero(self) -> None:
        assert _normalize_timeout(0) == 0.0


class TestDualTimeout:
    def test_timeout_in_seconds(self, mock_element_hidden: Any) -> None:
        """timeout=1 (second) is treated as 1 second."""
        # With timeout=0, the assertion fails immediately without retry
        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_element_hidden).to_be_visible(timeout=0)

    def test_timeout_in_milliseconds(self, mock_element_hidden: Any) -> None:
        """timeout=1000 (milliseconds) is treated as 1 second."""
        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_element_hidden).to_be_visible(timeout=1000)

    def test_timeout_5000_ms_works(self, mock_element_hidden: Any) -> None:
        """timeout=5000 is treated as 5 seconds (not 5000 seconds)."""
        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_element_hidden).to_be_visible(timeout=5000)


class TestScreenshotOnFailure:
    def test_screenshot_saved_on_failure(self, mock_driver: Any, tmp_path: str) -> None:
        """Screenshot is saved when screenshot_on_failure is enabled."""
        set_screenshot_on_failure(True, str(tmp_path))

        mock_driver.title = "Test Page"

        with pytest.raises(AssertionError, match="to have title"):
            expect(mock_driver).to_have_title("Wrong Title")

        mock_driver.save_screenshot.assert_called_once()
        call_arg = mock_driver.save_screenshot.call_args[0][0]
        assert call_arg.startswith(str(tmp_path))
        assert call_arg.endswith(".png")
        assert "screenshot_" in os.path.basename(call_arg)

    def test_no_screenshot_when_disabled(self, mock_driver: Any) -> None:
        """No screenshot is saved when screenshot_on_failure is disabled."""
        mock_driver.title = "Test Page"

        with pytest.raises(AssertionError, match="to have title"):
            expect(mock_driver).to_have_title("Wrong Title")

        mock_driver.save_screenshot.assert_not_called()

    def test_screenshot_with_element_target(self, mock_element_hidden: Any, tmp_path: str) -> None:
        """Screenshot works when target is a WebElement (uses element.parent)."""
        set_screenshot_on_failure(True, str(tmp_path))

        mock_driver = mock_element_hidden.parent
        mock_driver.save_screenshot = MagicMock()

        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_element_hidden).to_be_visible()

        mock_driver.save_screenshot.assert_called_once()

    def test_screenshot_failure_does_not_raise(self, mock_driver: Any, tmp_path: str) -> None:
        """If save_screenshot raises, the assertion error still propagates."""
        set_screenshot_on_failure(True, str(tmp_path))

        mock_driver.save_screenshot.side_effect = RuntimeError("Cannot save")
        mock_driver.title = "Test Page"

        with pytest.raises(AssertionError, match="to have title"):
            expect(mock_driver).to_have_title("Wrong Title")

    def test_screenshot_filename_sanitizes_invalid_chars(
        self, mock_driver: Any, tmp_path: str
    ) -> None:
        """Screenshot filename must not contain Windows-invalid chars (<, >, :, etc.).

        Regression: previously, condition_name like "to have window count > 5"
        was only stripped of spaces and quotes, leaving '>' in the filename.
        On Windows this causes silent screenshot save failures.
        """
        set_screenshot_on_failure(True, str(tmp_path))

        mock_driver.window_handles = []

        with pytest.raises(AssertionError, match="to have window count"):
            expect(mock_driver).to_have_window_count_greater_than(5)

        mock_driver.save_screenshot.assert_called_once()
        filename = os.path.basename(mock_driver.save_screenshot.call_args[0][0])
        # No Windows-invalid characters in the filename
        invalid_chars = set('<>:"|?*')
        assert not (invalid_chars & set(filename)), (
            f"Filename {filename!r} contains invalid characters"
        )


class TestNegativeTimeoutPollingValidation:
    """Regression: negative timeout/polling passed directly to assertion methods
    must raise ValueError with a clear message, not an opaque
    'sleep length must be non-negative' from time.sleep().
    """

    def test_negative_timeout_raises_valueerror(self, mock_element: Any) -> None:
        with pytest.raises(ValueError, match="timeout must be >= 0"):
            expect(mock_element).to_be_visible(timeout=-1)

    def test_negative_timeout_float_raises_valueerror(self, mock_element: Any) -> None:
        with pytest.raises(ValueError, match="timeout must be >= 0"):
            expect(mock_element).to_be_visible(timeout=-0.5)

    def test_negative_polling_raises_valueerror(self, mock_element: Any) -> None:
        with pytest.raises(ValueError, match="polling interval must be >= 0"):
            expect(mock_element).to_be_visible(polling=-0.5)

    def test_negative_polling_in_list_raises_valueerror(self, mock_element: Any) -> None:
        with pytest.raises(ValueError, match="polling_intervals"):
            expect(mock_element).to_be_visible(polling=[0.1, -0.5, 1.0])

    def test_zero_timeout_allowed(self, mock_element_hidden: Any) -> None:
        """timeout=0 is valid — single poll, no retry."""
        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_element_hidden).to_be_visible(timeout=0)

    def test_zero_polling_allowed(self, mock_element_hidden: Any) -> None:
        """polling=0 is valid — busy-spin retry."""
        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_element_hidden).to_be_visible(timeout=0, polling=0)
