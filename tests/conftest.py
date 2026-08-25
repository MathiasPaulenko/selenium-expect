"""Shared pytest fixtures for selenium-expect."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, PropertyMock

import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

import selenium_expect._config as cfg_module
from selenium_expect._config import ExpectConfig

# --- Config reset ---


@pytest.fixture(autouse=True)
def _reset_config() -> Any:
    """Reset global config between tests."""
    original = cfg_module._global_config
    cfg_module._global_config = ExpectConfig()
    yield
    cfg_module._global_config = original


# --- Mock WebDriver ---


@pytest.fixture()
def mock_driver() -> Any:
    """Mock WebDriver with common properties pre-configured."""
    driver = MagicMock(spec=WebDriver)
    driver.title = "Test Page"
    driver.current_url = "https://example.com/page"
    driver.current_window_handle = "CDwindow-01"
    driver.window_handles = ["CDwindow-01"]
    driver.name = "chrome"
    driver.orientation = "LANDSCAPE"
    driver.capabilities = {
        "browserName": "chrome",
        "browserVersion": "120.0",
        "platformName": "linux",
        "acceptInsecureCerts": True,
    }
    driver.page_source = "<html><body><h1>Hello</h1></body></html>"
    driver.get_window_position.return_value = {"x": 0, "y": 0}
    driver.get_window_size.return_value = {"width": 1280, "height": 720}
    driver.get_window_rect.return_value = {"x": 0, "y": 0, "width": 1280, "height": 720}

    active_el = MagicMock()
    active_el.tag_name = "input"
    active_el.get_attribute.return_value = "username"
    driver.switch_to.active_element = active_el

    return driver


@pytest.fixture()
def mock_alert() -> Any:
    """Mock Alert object with pre-configured text."""
    from selenium.webdriver.common.alert import Alert

    alert = MagicMock(spec=Alert)
    alert.text = "Are you sure?"
    return alert


@pytest.fixture()
def mock_driver_with_alert(mock_driver: Any) -> Any:
    """Mock WebDriver with alert support."""
    alert = MagicMock()
    alert.text = "Are you sure?"
    mock_driver.switch_to.alert = alert
    return mock_driver


@pytest.fixture()
def mock_driver_no_alert(mock_driver: Any) -> Any:
    """Mock WebDriver where switch_to.alert raises NoAlertPresentException."""
    from selenium.common.exceptions import NoAlertPresentException

    mock_driver.switch_to.alert.side_effect = NoAlertPresentException("No alert")
    return mock_driver


# --- Mock WebElement ---


@pytest.fixture()
def mock_element() -> Any:
    """Mock WebElement with common properties pre-configured."""
    el = MagicMock(spec=WebElement)
    el.is_displayed.return_value = True
    el.is_enabled.return_value = True
    el.is_selected.return_value = False
    el.text = "Hello World"
    el.tag_name = "div"
    el.location = {"x": 100, "y": 200}
    el.size = {"width": 300, "height": 50}
    el.rect = {"x": 100, "y": 200, "width": 300, "height": 50}
    el.location_once_scrolled_into_view = {"x": 100, "y": 200}

    def get_attribute(name: str) -> Any:
        attrs = {
            "outerHTML": '<div id="main-content" class="container active">Hello World</div>',
            "id": "main-content",
            "class": "container active",
            "value": "test_value",
            "data-testid": "submit-btn",
            "href": "https://example.com/link",
            "placeholder": "Enter text...",
            "checked": None,
        }
        return attrs.get(name)

    el.get_attribute.side_effect = get_attribute

    def value_of_css_property(name: str) -> str:
        css = {
            "color": "rgba(0, 0, 255, 1)",
            "display": "block",
            "visibility": "visible",
            "background-color": "rgb(255, 255, 255)",
        }
        return css.get(name, "")

    el.value_of_css_property.side_effect = value_of_css_property

    el.aria_role = "button"
    el.accessible_name = "Submit Form"
    el.shadow_root = None

    return el


@pytest.fixture()
def mock_element_hidden(mock_element: Any) -> Any:
    """Mock WebElement that is hidden."""
    mock_element.is_displayed.return_value = False
    return mock_element


@pytest.fixture()
def mock_element_disabled(mock_element: Any) -> Any:
    """Mock WebElement that is disabled."""
    mock_element.is_enabled.return_value = False
    return mock_element


@pytest.fixture()
def mock_element_checked(mock_element: Any) -> Any:
    """Mock WebElement that is checked/selected."""
    mock_element.is_selected.return_value = True
    return mock_element


@pytest.fixture()
def mock_element_stale(mock_element: Any) -> Any:
    """Mock WebElement that raises StaleElementReferenceException on any access."""
    from selenium.common.exceptions import StaleElementReferenceException

    stale_exc = StaleElementReferenceException("Element is stale")

    mock_element.is_displayed.side_effect = stale_exc
    mock_element.is_enabled.side_effect = stale_exc
    mock_element.is_selected.side_effect = stale_exc
    mock_element.get_attribute.side_effect = stale_exc
    # Properties on spec'd mocks need type-level patching
    type(mock_element).text = PropertyMock(side_effect=stale_exc)
    type(mock_element).tag_name = PropertyMock(side_effect=stale_exc)
    return mock_element


# --- Mock WebElement list ---


@pytest.fixture()
def mock_elements() -> list[Any]:
    """Mock list of WebElements."""
    elements: list[Any] = []
    texts = ["Apple", "Banana", "Cherry"]
    for text in texts:
        el = MagicMock(spec=WebElement)
        el.is_displayed.return_value = True
        el.is_enabled.return_value = True
        el.is_selected.return_value = False
        el.text = text
        el.get_attribute.return_value = text.lower()
        elements.append(el)
    return elements


@pytest.fixture()
def mock_elements_empty() -> list[Any]:
    """Mock empty list of WebElements."""
    return []


@pytest.fixture()
def mock_elements_mixed_visibility() -> list[Any]:
    """Mock list with mixed visibility."""
    elements: list[Any] = []
    for i, visible in enumerate([True, False, True]):
        el = MagicMock(spec=WebElement)
        el.is_displayed.return_value = visible
        el.is_enabled.return_value = True
        el.text = f"Item {i}"
        elements.append(el)
    return elements


# --- Mock Select ---


@pytest.fixture()
def mock_select() -> Any:
    """Mock Select wrapping a WebElement."""
    from selenium.webdriver.support.ui import Select

    select = MagicMock(spec=Select)

    opt1 = MagicMock()
    opt1.text = "Option 1"
    opt1.get_attribute.return_value = "opt1"
    opt1.is_selected.return_value = True

    opt2 = MagicMock()
    opt2.text = "Option 2"
    opt2.get_attribute.return_value = "opt2"
    opt2.is_selected.return_value = False

    opt3 = MagicMock()
    opt3.text = "Option 3"
    opt3.get_attribute.return_value = "opt3"
    opt3.is_selected.return_value = False

    select.options = [opt1, opt2, opt3]
    select.all_selected_options = [opt1]
    select.first_selected_option = opt1
    select.is_multiple = False

    return select


@pytest.fixture()
def mock_select_multiple(mock_select: Any) -> Any:
    """Mock multi-select."""
    mock_select.is_multiple = True
    opt2 = mock_select.options[1]
    opt2.is_selected.return_value = True
    mock_select.all_selected_options = [mock_select.options[0], opt2]
    return mock_select


# --- Mock ShadowRoot ---


@pytest.fixture()
def mock_shadow_root() -> Any:
    """Mock ShadowRoot with child elements."""
    from selenium.webdriver.remote.shadowroot import ShadowRoot

    shadow = MagicMock(spec=ShadowRoot)

    child = MagicMock()
    child.is_displayed.return_value = True
    child.text = "Shadow content"
    child.get_attribute.return_value = "shadow-item"

    shadow.find_element.return_value = child
    shadow.find_elements.return_value = [child]

    return shadow


# --- Mock Cookie ---


@pytest.fixture()
def mock_driver_with_cookies(mock_driver: Any) -> Any:
    """Mock WebDriver with cookies."""
    mock_driver.get_cookies.return_value = [
        {
            "name": "session",
            "value": "abc123",
            "domain": ".example.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,
            "sameSite": "Lax",
        },
        {
            "name": "theme",
            "value": "dark",
            "domain": ".example.com",
            "path": "/",
            "httpOnly": False,
            "secure": False,
            "sameSite": "Strict",
        },
    ]
    mock_driver.get_cookie.side_effect = lambda name: {
        "session": {
            "name": "session",
            "value": "abc123",
            "domain": ".example.com",
            "path": "/",
            "httpOnly": True,
            "secure": True,
            "sameSite": "Lax",
            "expiry": 1735689600,
        },
        "theme": {
            "name": "theme",
            "value": "dark",
            "domain": ".example.com",
            "path": "/",
            "httpOnly": False,
            "secure": False,
            "sameSite": "Strict",
        },
    }.get(name)
    return mock_driver


# --- Mock for JS execution ---


@pytest.fixture()
def mock_driver_js(mock_driver: Any) -> Any:
    """Mock WebDriver with execute_script/execute_async_script."""
    js_values: dict[str, Any] = {
        "return localStorage.getItem('token');": "abc123",
        "return localStorage.length;": 3,
        "return sessionStorage.getItem('key');": "value123",
        "return sessionStorage.length;": 2,
        "return document.readyState;": "complete",
        "return window.innerWidth;": 1280,
    }
    mock_driver.execute_script.side_effect = lambda script, *args: js_values.get(script)
    mock_driver.execute_async_script.side_effect = lambda script, *args: js_values.get(script)
    return mock_driver


# --- Mock for iframe ---


@pytest.fixture()
def mock_driver_iframe(mock_driver: Any) -> Any:
    """Mock WebDriver with iframe support."""
    iframe = MagicMock()
    iframe.text = "Frame content"

    mock_driver.find_elements.return_value = [iframe]
    mock_driver.page_source = "<html><body>Frame content</body></html>"
    mock_driver.switch_to.frame = MagicMock()
    mock_driver.switch_to.default_content = MagicMock()
    return mock_driver


# --- Mock for window ---


@pytest.fixture()
def mock_driver_window(mock_driver: Any) -> Any:
    """Mock WebDriver with window position/size/rect."""
    mock_driver.get_window_position.return_value = {"x": 100, "y": 200}
    mock_driver.get_window_size.return_value = {"width": 1280, "height": 720}
    mock_driver.get_window_rect.return_value = {
        "x": 100,
        "y": 200,
        "width": 1280,
        "height": 720,
    }
    return mock_driver
