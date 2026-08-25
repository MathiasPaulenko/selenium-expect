"""Unit tests for selenium_expect.assertions.js.ExpectJS."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect.assertions.js import ExpectJS


class TestExpectJS:
    def test_to_have_js_result(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_js_result('return document.readyState;', 'complete') passes."""
        ExpectJS(mock_driver_js).to_have_js_result("return document.readyState;", "complete")

    def test_to_have_js_result_contains(self, mock_driver_js: Any) -> None:
        """to_have_js_result_contains with 'comp' substring passes."""
        ExpectJS(mock_driver_js).to_have_js_result_contains("return document.readyState;", "comp")

    def test_to_have_js_result_matches(self, mock_driver_js: Any) -> None:
        """to_have_js_result_matches with r'comp\\w+' pattern passes."""
        ExpectJS(mock_driver_js).to_have_js_result_matches(
            "return document.readyState;", r"comp\w+"
        )

    def test_to_have_async_js_result(self, mock_driver_js: Any) -> None:
        """to_have_async_js_result with 'complete' value passes."""
        ExpectJS(mock_driver_js).to_have_async_js_result("return document.readyState;", "complete")

    def test_to_have_local_storage_item(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_local_storage_item('token', 'abc123') passes."""
        ExpectJS(mock_driver_js).to_have_local_storage_item("token", "abc123")

    def test_to_have_local_storage_item_present(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_local_storage_item_present('token') passes."""
        ExpectJS(mock_driver_js).to_have_local_storage_item_present("token")

    def test_to_have_local_storage_item_absent(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_local_storage_item_absent('missing') passes."""
        ExpectJS(mock_driver_js).to_have_local_storage_item_absent("missing")

    def test_to_have_local_storage_length(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_local_storage_length(3) passes."""
        ExpectJS(mock_driver_js).to_have_local_storage_length(3)

    def test_to_have_session_storage_item(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_session_storage_item('key', 'value123') passes."""
        ExpectJS(mock_driver_js).to_have_session_storage_item("key", "value123")

    def test_to_have_session_storage_item_present(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_session_storage_item_present('key') passes."""
        ExpectJS(mock_driver_js).to_have_session_storage_item_present("key")

    def test_to_have_session_storage_item_absent(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_session_storage_item_absent('missing') passes."""
        ExpectJS(mock_driver_js).to_have_session_storage_item_absent("missing")

    def test_to_have_session_storage_length(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_session_storage_length(2) passes."""
        ExpectJS(mock_driver_js).to_have_session_storage_length(2)

    # --- Failure cases ---

    def test_to_have_js_result_fails(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_js_result('return document.readyState;', 'loading') raises."""
        with pytest.raises(AssertionError, match="to have JS result"):
            ExpectJS(mock_driver_js).to_have_js_result("return document.readyState;", "loading")

    def test_to_have_local_storage_item_fails(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_local_storage_item('token', 'wrong') raises."""
        with pytest.raises(AssertionError, match="localStorage"):
            ExpectJS(mock_driver_js).to_have_local_storage_item("token", "wrong")

    def test_to_have_local_storage_length_fails(self, mock_driver_js: Any) -> None:
        """ExpectJS(driver).to_have_local_storage_length(99) raises."""
        with pytest.raises(AssertionError, match="localStorage length"):
            ExpectJS(mock_driver_js).to_have_local_storage_length(99)
