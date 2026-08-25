"""Unit tests for selenium_expect.assertions.window.ExpectWindow."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect.assertions.window import ExpectWindow


class TestExpectWindow:
    def test_to_have_position(self, mock_driver_window: Any) -> None:
        """ExpectWindow(driver).to_have_position(100, 200) passes."""
        ExpectWindow(mock_driver_window).to_have_position(100, 200)

    def test_to_have_size(self, mock_driver_window: Any) -> None:
        """ExpectWindow(driver).to_have_size(1280, 720) passes."""
        ExpectWindow(mock_driver_window).to_have_size(1280, 720)

    def test_to_have_rect(self, mock_driver_window: Any) -> None:
        """ExpectWindow(driver).to_have_rect(100, 200, 1280, 720) passes."""
        ExpectWindow(mock_driver_window).to_have_rect(100, 200, 1280, 720)

    # --- Failure cases ---

    def test_to_have_position_fails(self, mock_driver_window: Any) -> None:
        """ExpectWindow(driver).to_have_position(0, 0) raises."""
        with pytest.raises(AssertionError, match="window position"):
            ExpectWindow(mock_driver_window).to_have_position(0, 0)

    def test_to_have_size_fails(self, mock_driver_window: Any) -> None:
        """ExpectWindow(driver).to_have_size(800, 600) raises."""
        with pytest.raises(AssertionError, match="window size"):
            ExpectWindow(mock_driver_window).to_have_size(800, 600)
