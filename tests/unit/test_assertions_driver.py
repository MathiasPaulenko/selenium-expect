"""Unit tests for selenium_expect.assertions.driver.ExpectDriver."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect
from selenium_expect.assertions.driver import ExpectDriver


class TestExpectDriverTitle:
    def test_to_have_title_exact(self, mock_driver: Any) -> None:
        """expect(driver).to_have_title('Test Page') passes."""
        expect(mock_driver).to_have_title("Test Page")

    def test_to_have_title_contains(self, mock_driver: Any) -> None:
        """expect(driver).to_have_title_contains('Test') passes."""
        expect(mock_driver).to_have_title_contains("Test")

    def test_to_have_title_matches(self, mock_driver: Any) -> None:
        """expect(driver).to_have_title_matches(r'Test \\w+') passes."""
        expect(mock_driver).to_have_title_matches(r"Test \w+")

    def test_to_have_title_negation(self, mock_driver: Any) -> None:
        """expect(driver).not_.to_have_title('Wrong') passes."""
        expect(mock_driver).not_.to_have_title("Wrong Title")

    def test_to_have_title_fails_with_descriptive_error(self, mock_driver: Any) -> None:
        """expect(driver).to_have_title('Wrong') raises AssertionError."""
        with pytest.raises(AssertionError, match="to have title"):
            expect(mock_driver).to_have_title("Wrong Title")


class TestExpectDriverUrl:
    def test_to_have_url_exact(self, mock_driver: Any) -> None:
        """expect(driver).to_have_url('https://example.com/page') passes."""
        expect(mock_driver).to_have_url("https://example.com/page")

    def test_to_have_url_contains(self, mock_driver: Any) -> None:
        """expect(driver).to_have_url_contains('example.com') passes."""
        expect(mock_driver).to_have_url_contains("example.com")

    def test_to_have_url_matches(self, mock_driver: Any) -> None:
        """expect(driver).to_have_url_matches(r'example\\.com') passes."""
        expect(mock_driver).to_have_url_matches(r"example\.com")

    def test_to_have_url_negation(self, mock_driver: Any) -> None:
        """expect(driver).not_.to_have_url('wrong') passes."""
        expect(mock_driver).not_.to_have_url("https://wrong.com")

    def test_to_have_url_fails(self, mock_driver: Any) -> None:
        """expect(driver).to_have_url('wrong') raises."""
        with pytest.raises(AssertionError, match="to have URL"):
            expect(mock_driver).to_have_url("https://wrong.com")


class TestExpectDriverUrlChanges:
    def test_to_have_url_changes_passes(self, mock_driver: Any) -> None:
        """expect(driver).to_have_url_changes('https://old.com') passes when URL differs."""
        expect(mock_driver).to_have_url_changes("https://old.com")

    def test_to_have_url_changes_fails(self, mock_driver: Any) -> None:
        """expect(driver).to_have_url_changes(current_url) raises."""
        with pytest.raises(AssertionError, match="URL changed"):
            expect(mock_driver).to_have_url_changes("https://example.com/page")

    def test_to_have_url_changes_negation(self, mock_driver: Any) -> None:
        """expect(driver).not_.to_have_url_changes(current_url) passes."""
        expect(mock_driver).not_.to_have_url_changes("https://example.com/page")


class TestExpectDriverReadyState:
    def test_to_have_ready_state_complete(self, mock_driver_js: Any) -> None:
        """expect(driver).to_have_ready_state('complete') passes."""
        expect(mock_driver_js).to_have_ready_state("complete")

    def test_to_have_ready_state_fails(self, mock_driver_js: Any) -> None:
        """expect(driver).to_have_ready_state('loading') raises."""
        with pytest.raises(AssertionError, match="ready state"):
            expect(mock_driver_js).to_have_ready_state("loading")

    def test_to_have_ready_state_negation(self, mock_driver_js: Any) -> None:
        """expect(driver).not_.to_have_ready_state('loading') passes."""
        expect(mock_driver_js).not_.to_have_ready_state("loading")


class TestExpectDriverWindows:
    def test_to_have_window_count(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_count(1) passes."""
        expect(mock_driver).to_have_window_count(1)

    def test_to_have_window_count_greater_than(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_count_greater_than(0) passes."""
        expect(mock_driver).to_have_window_count_greater_than(0)

    def test_to_have_window_count_less_than(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_count_less_than(2) passes."""
        expect(mock_driver).to_have_window_count_less_than(2)

    def test_to_have_window_handle(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_handle('CDwindow-01') passes."""
        expect(mock_driver).to_have_window_handle("CDwindow-01")

    def test_to_have_window_count_fails(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_count(5) raises."""
        with pytest.raises(AssertionError, match="window count"):
            expect(mock_driver).to_have_window_count(5)


class TestExpectDriverBrowser:
    def test_to_have_browser_name(self, mock_driver: Any) -> None:
        """expect(driver).to_have_browser_name('chrome') passes."""
        expect(mock_driver).to_have_browser_name("chrome")

    def test_to_have_orientation(self, mock_driver: Any) -> None:
        """expect(driver).to_have_orientation('LANDSCAPE') passes."""
        expect(mock_driver).to_have_orientation("LANDSCAPE")

    def test_to_have_capability(self, mock_driver: Any) -> None:
        """expect(driver).to_have_capability('browserName', 'chrome') passes."""
        expect(mock_driver).to_have_capability("browserName", "chrome")

    def test_to_have_capability_contains(self, mock_driver: Any) -> None:
        """expect(driver).to_have_capability_contains('browserVersion', '120') passes."""
        expect(mock_driver).to_have_capability_contains("browserVersion", "120")

    def test_to_have_browser_name_fails(self, mock_driver: Any) -> None:
        """expect(driver).to_have_browser_name('firefox') raises."""
        with pytest.raises(AssertionError, match="browser name"):
            expect(mock_driver).to_have_browser_name("firefox")


class TestExpectDriverPageSource:
    def test_to_have_page_source_contains(self, mock_driver: Any) -> None:
        """expect(driver).to_have_page_source_contains('Hello') passes."""
        expect(mock_driver).to_have_page_source_contains("Hello")

    def test_to_have_page_source_matches(self, mock_driver: Any) -> None:
        """expect(driver).to_have_page_source_matches(r'<h1>.*</h1>') passes."""
        expect(mock_driver).to_have_page_source_matches(r"<h1>.*</h1>")

    def test_to_have_page_source_not_contains(self, mock_driver: Any) -> None:
        """expect(driver).to_have_page_source_not_contains('Goodbye') passes."""
        expect(mock_driver).to_have_page_source_not_contains("Goodbye")

    def test_to_have_page_source_contains_fails(self, mock_driver: Any) -> None:
        """expect(driver).to_have_page_source_contains('Missing') raises."""
        with pytest.raises(AssertionError, match="page source"):
            expect(mock_driver).to_have_page_source_contains("Missing Text")


class TestExpectDriverWindow:
    def test_to_have_window_position(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_position(0, 0) passes."""
        expect(mock_driver).to_have_window_position(0, 0)

    def test_to_have_window_size(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_size(1280, 720) passes."""
        expect(mock_driver).to_have_window_size(1280, 720)

    def test_to_have_window_rect(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_rect(0, 0, 1280, 720) passes."""
        expect(mock_driver).to_have_window_rect(0, 0, 1280, 720)

    def test_to_have_window_position_fails(self, mock_driver: Any) -> None:
        """expect(driver).to_have_window_position(100, 100) raises."""
        with pytest.raises(AssertionError, match="window position"):
            expect(mock_driver).to_have_window_position(100, 100)


class TestExpectDriverActiveElement:
    def test_to_have_active_element_tag(self, mock_driver: Any) -> None:
        """expect(driver).to_have_active_element_tag('input') passes."""
        expect(mock_driver).to_have_active_element_tag("input")

    def test_to_have_active_element_id(self, mock_driver: Any) -> None:
        """expect(driver).to_have_active_element_id('username') passes."""
        expect(mock_driver).to_have_active_element_id("username")

    def test_to_have_active_element_tag_fails(self, mock_driver: Any) -> None:
        """expect(driver).to_have_active_element_tag('div') raises."""
        with pytest.raises(AssertionError, match="active element tag"):
            expect(mock_driver).to_have_active_element_tag("div")

    def test_to_have_active_element_class(self, mock_driver: Any) -> None:
        """expect(driver).to_have_active_element_class passes when class is present."""
        mock_driver.switch_to.active_element.get_attribute.return_value = "btn primary"
        expect(mock_driver).to_have_active_element_class("btn")

    def test_to_have_active_element_class_fails(self, mock_driver: Any) -> None:
        """expect(driver).to_have_active_element_class raises when class is absent."""
        mock_driver.switch_to.active_element.get_attribute.return_value = "btn primary"
        with pytest.raises(AssertionError, match="active element class"):
            expect(mock_driver).to_have_active_element_class("secondary")

    def test_to_have_active_element_class_uses_split_not_substring(self, mock_driver: Any) -> None:
        """Regression: to_have_active_element_class must use .split() matching,
        not substring matching. 'btn' must NOT match class 'btn-primary'."""
        mock_driver.switch_to.active_element.get_attribute.return_value = "btn-primary"
        with pytest.raises(AssertionError):
            expect(mock_driver).to_have_active_element_class("btn")

    def test_to_have_active_element_class_none(self, mock_driver: Any) -> None:
        """to_have_active_element_class handles None class attribute gracefully."""
        mock_driver.switch_to.active_element.get_attribute.return_value = None
        with pytest.raises(AssertionError):
            expect(mock_driver).to_have_active_element_class("btn")


class TestExpectDriverDispatch:
    def test_expect_dispatches_to_driver(self, mock_driver: Any) -> None:
        """expect(driver) returns ExpectDriver instance."""
        result = expect(mock_driver)
        assert isinstance(result, ExpectDriver)
