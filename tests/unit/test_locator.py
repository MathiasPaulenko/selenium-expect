"""Unit tests for selenium_expect._locator.LocatorExpect."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_expect import expect
from selenium_expect._locator import LocatorExpect


@pytest.fixture()
def mock_driver() -> Any:
    """Mock WebDriver with find_element support."""
    driver = MagicMock(spec=WebDriver)
    return driver


@pytest.fixture()
def mock_element_for_locator() -> Any:
    """Mock WebElement for locator tests."""
    from selenium.webdriver.remote.webelement import WebElement

    el = MagicMock(spec=WebElement)
    el.is_displayed.return_value = True
    el.is_enabled.return_value = True
    el.is_selected.return_value = False
    el.text = "Hello World"
    el.tag_name = "div"
    el.get_attribute.side_effect = lambda name: {
        "outerHTML": '<div id="main">Hello</div>',
        "id": "main",
        "class": "active",
    }.get(name)
    return el


class TestLocatorExpectCreation:
    def test_returns_locator_expect(self, mock_driver: Any) -> None:
        """expect(driver, by=..., value=...) returns LocatorExpect."""
        result = expect(mock_driver, by=By.ID, value="foo")
        assert isinstance(result, LocatorExpect)

    def test_raises_for_non_driver_target(self, mock_element_for_locator: Any) -> None:
        """expect(element, by=..., value=...) raises TypeError."""
        with pytest.raises(TypeError, match="WebDriver"):
            expect(mock_element_for_locator, by=By.ID, value="foo")


class TestLocatorExpectAssertions:
    def test_to_be_visible_passes(self, mock_driver: Any, mock_element_for_locator: Any) -> None:
        """Locator-based to_be_visible passes when element is visible."""
        mock_driver.find_element.return_value = mock_element_for_locator
        expect(mock_driver, by=By.ID, value="foo", timeout=1.0).to_be_visible()

    def test_to_be_visible_fails_when_not_found(self, mock_driver: Any) -> None:
        """Locator-based to_be_visible raises when element not found."""
        from selenium.common.exceptions import NoSuchElementException

        mock_driver.find_element.side_effect = NoSuchElementException()
        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_driver, by=By.ID, value="missing", timeout=0.5).to_be_visible()

    def test_to_have_text_passes(self, mock_driver: Any, mock_element_for_locator: Any) -> None:
        """Locator-based to_have_text passes with correct text."""
        mock_driver.find_element.return_value = mock_element_for_locator
        expect(mock_driver, by=By.ID, value="foo", timeout=1.0).to_have_text("Hello World")

    def test_to_have_text_fails(self, mock_driver: Any, mock_element_for_locator: Any) -> None:
        """Locator-based to_have_text raises with wrong text."""
        mock_driver.find_element.return_value = mock_element_for_locator
        with pytest.raises(AssertionError, match="to have text"):
            expect(mock_driver, by=By.ID, value="foo", timeout=0.5).to_have_text("Wrong Text")

    def test_to_be_enabled_passes(self, mock_driver: Any, mock_element_for_locator: Any) -> None:
        """Locator-based to_be_enabled passes when element is enabled."""
        mock_driver.find_element.return_value = mock_element_for_locator
        expect(mock_driver, by=By.ID, value="foo", timeout=1.0).to_be_enabled()


class TestLocatorExpectReFind:
    def test_refinds_on_each_poll(self, mock_driver: Any) -> None:
        """LocatorExpect re-finds the element on each poll cycle."""
        from selenium.webdriver.remote.webelement import WebElement

        # First few calls: element not visible, then becomes visible
        hidden_el = MagicMock(spec=WebElement)
        hidden_el.is_displayed.return_value = False

        visible_el = MagicMock(spec=WebElement)
        visible_el.is_displayed.return_value = True

        mock_driver.find_element.side_effect = [hidden_el, hidden_el, visible_el]
        expect(mock_driver, by=By.ID, value="foo", timeout=5, polling=0.01).to_be_visible()
        assert mock_driver.find_element.call_count >= 2

    def test_stale_element_refinds(self, mock_driver: Any, mock_element_for_locator: Any) -> None:
        """If element goes stale, LocatorExpect re-finds on next poll."""
        from selenium.common.exceptions import StaleElementReferenceException
        from selenium.webdriver.remote.webelement import WebElement

        stale_el = MagicMock(spec=WebElement)
        stale_el.is_displayed.side_effect = StaleElementReferenceException()

        fresh_el = MagicMock(spec=WebElement)
        fresh_el.is_displayed.return_value = True

        mock_driver.find_element.side_effect = [stale_el, fresh_el]
        expect(mock_driver, by=By.ID, value="foo", timeout=5, polling=0.01).to_be_visible()


class TestLocatorExpectNegation:
    def test_not_to_be_visible(self, mock_driver: Any, mock_element_for_locator: Any) -> None:
        """Locator-based not_.to_be_visible passes when element is not visible."""
        mock_element_for_locator.is_displayed.return_value = False
        mock_driver.find_element.return_value = mock_element_for_locator
        expect(mock_driver, by=By.ID, value="foo", timeout=1.0).not_.to_be_visible()


class TestLocatorExpectEntityDescription:
    def test_entity_description(self, mock_driver: Any) -> None:
        """LocatorExpect entity description includes by and value."""
        locator = LocatorExpect(mock_driver, By.ID, "foo")
        desc = locator._entity_description()
        assert "id" in desc
        assert "foo" in desc
