"""Unit tests for selenium_expect.assertions.iframe.ExpectIframe."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect.assertions.iframe import ExpectIframe


class TestExpectIframe:
    def test_to_have_frame_available(self, mock_driver_iframe: Any) -> None:
        """ExpectIframe(driver).to_have_frame_available('frame1') passes."""
        ExpectIframe(mock_driver_iframe).to_have_frame_available("frame1")

    def test_to_have_frame_count(self, mock_driver_iframe: Any) -> None:
        """ExpectIframe(driver).to_have_frame_count(1) passes."""
        ExpectIframe(mock_driver_iframe).to_have_frame_count(1)

    def test_to_have_frame_count_greater_than(self, mock_driver_iframe: Any) -> None:
        """ExpectIframe(driver).to_have_frame_count_greater_than(0) passes."""
        ExpectIframe(mock_driver_iframe).to_have_frame_count_greater_than(0)

    def test_to_have_frame_text(self, mock_driver_iframe: Any) -> None:
        """ExpectIframe(driver).to_have_frame_text('frame1', 'Frame content') passes."""
        ExpectIframe(mock_driver_iframe).to_have_frame_text("frame1", "Frame content")

    # --- Failure cases ---

    def test_to_have_frame_count_fails(self, mock_driver_iframe: Any) -> None:
        """ExpectIframe(driver).to_have_frame_count(99) raises."""
        with pytest.raises(AssertionError, match="frame count"):
            ExpectIframe(mock_driver_iframe).to_have_frame_count(99)

    def test_to_have_frame_text_fails(self, mock_driver_iframe: Any) -> None:
        """ExpectIframe(driver).to_have_frame_text('frame1', 'Missing') raises."""
        with pytest.raises(AssertionError, match="frame"):
            ExpectIframe(mock_driver_iframe).to_have_frame_text("frame1", "Missing text")

    def test_to_have_frame_text_switches_back_on_success(self, mock_driver_iframe: Any) -> None:
        """to_have_frame_text calls default_content after reading page_source."""
        ExpectIframe(mock_driver_iframe).to_have_frame_text("frame1", "Frame content")
        mock_driver_iframe.switch_to.default_content.assert_called()

    def test_to_have_frame_text_switches_back_on_exception(self, mock_driver_iframe: Any) -> None:
        """to_have_frame_text calls default_content even if page_source raises.

        Regression: previously, if page_source raised a non-NoSuchFrameException,
        default_content was never called, leaving the driver stuck in the frame.
        """
        from unittest.mock import PropertyMock

        from selenium.common.exceptions import WebDriverException

        type(mock_driver_iframe).page_source = PropertyMock(
            side_effect=WebDriverException("navigation interrupted")
        )
        with pytest.raises(WebDriverException):
            ExpectIframe(mock_driver_iframe).to_have_frame_text("frame1", "Frame content")
        mock_driver_iframe.switch_to.default_content.assert_called()
