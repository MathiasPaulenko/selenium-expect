"""Unit tests for medium priority features."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from selenium.common.exceptions import NoSuchFrameException

from selenium_expect import expect
from selenium_expect.assertions.iframe import ExpectIframe

# ============================================================
# Element — State
# ============================================================


class TestElementState:
    def test_to_be_unselected(self, mock_element: Any) -> None:
        expect(mock_element).to_be_unselected()

    def test_to_be_unselected_fails_when_selected(self, mock_element_checked: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element_checked).to_be_unselected()

    def test_not_to_be_unselected(self, mock_element_checked: Any) -> None:
        expect(mock_element_checked).not_.to_be_unselected()

    def test_to_be_unchecked(self, mock_element: Any) -> None:
        expect(mock_element).to_be_unchecked()

    def test_to_be_unchecked_fails_when_checked(self, mock_element_checked: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element_checked).to_be_unchecked()

    def test_not_to_be_unchecked(self, mock_element_checked: Any) -> None:
        expect(mock_element_checked).not_.to_be_unchecked()

    def test_to_be_focused(self, mock_element: Any, mock_driver: Any) -> None:
        mock_element.parent = mock_driver
        mock_driver.switch_to.active_element = mock_element
        expect(mock_element).to_be_focused()

    def test_to_be_focused_fails(self, mock_element: Any, mock_driver: Any) -> None:
        mock_element.parent = mock_driver
        other = MagicMock()
        mock_driver.switch_to.active_element = other
        with pytest.raises(AssertionError):
            expect(mock_element).to_be_focused()

    def test_not_to_be_focused(self, mock_element: Any, mock_driver: Any) -> None:
        mock_element.parent = mock_driver
        other = MagicMock()
        mock_driver.switch_to.active_element = other
        expect(mock_element).not_.to_be_focused()

    def test_to_be_focused_different_instance_same_id(
        self, mock_element: Any, mock_driver: Any
    ) -> None:
        """to_be_focused compares element IDs, not Python object identity.

        Regression: previously used `active == el` (identity comparison).
        In real Selenium, driver.switch_to.active_element returns a NEW
        WebElement instance each call, so `==` would always be False even
        when the element is actually focused. The fix compares `.id`
        (W3C WebDriver element references) instead.
        """
        mock_element.parent = mock_driver
        mock_element.id = "elem-123"
        active = MagicMock()
        active.id = "elem-123"
        mock_driver.switch_to.active_element = active
        expect(mock_element).to_be_focused()

    def test_to_be_focused_different_instance_different_id(
        self, mock_element: Any, mock_driver: Any
    ) -> None:
        """to_be_focused fails when active element has a different ID."""
        mock_element.parent = mock_driver
        mock_element.id = "elem-123"
        active = MagicMock()
        active.id = "elem-456"
        mock_driver.switch_to.active_element = active
        with pytest.raises(AssertionError):
            expect(mock_element).to_be_focused()

    def test_to_be_editable(self, mock_element: Any) -> None:
        mock_element.tag_name = "input"
        mock_element.get_attribute.side_effect = lambda name: None if name == "readonly" else "test"
        expect(mock_element).to_be_editable()

    def test_to_be_editable_fails_not_input(self, mock_element: Any) -> None:
        mock_element.tag_name = "div"
        with pytest.raises(AssertionError):
            expect(mock_element).to_be_editable()

    def test_to_be_editable_fails_readonly(self, mock_element: Any) -> None:
        mock_element.tag_name = "input"
        mock_element.get_attribute.side_effect = lambda name: "true" if name == "readonly" else None
        with pytest.raises(AssertionError):
            expect(mock_element).to_be_editable()

    def test_to_be_editable_fails_disabled(self, mock_element_disabled: Any) -> None:
        mock_element_disabled.tag_name = "input"
        mock_element_disabled.get_attribute.side_effect = lambda name: None
        with pytest.raises(AssertionError):
            expect(mock_element_disabled).to_be_editable()

    def test_not_to_be_editable(self, mock_element: Any) -> None:
        mock_element.tag_name = "div"
        expect(mock_element).not_.to_be_editable()

    def test_to_be_readonly(self, mock_element: Any) -> None:
        mock_element.get_attribute.side_effect = lambda name: "true" if name == "readonly" else None
        expect(mock_element).to_be_readonly()

    def test_to_be_readonly_fails(self, mock_element: Any) -> None:
        mock_element.get_attribute.side_effect = lambda name: None
        with pytest.raises(AssertionError):
            expect(mock_element).to_be_readonly()

    def test_not_to_be_readonly(self, mock_element: Any) -> None:
        mock_element.get_attribute.side_effect = lambda name: None
        expect(mock_element).not_.to_be_readonly()

    def test_to_be_empty(self, mock_element: Any) -> None:
        mock_element.text = ""
        expect(mock_element).to_be_empty()

    def test_to_be_empty_with_whitespace(self, mock_element: Any) -> None:
        mock_element.text = "   "
        expect(mock_element).to_be_empty()

    def test_to_be_empty_fails(self, mock_element: Any) -> None:
        mock_element.text = "Hello"
        with pytest.raises(AssertionError):
            expect(mock_element).to_be_empty()

    def test_not_to_be_empty(self, mock_element: Any) -> None:
        mock_element.text = "Hello"
        expect(mock_element).not_.to_be_empty()


# ============================================================
# Element — Text
# ============================================================


class TestElementText:
    def test_to_have_text_starting_with(self, mock_element: Any) -> None:
        expect(mock_element).to_have_text_starting_with("Hello")

    def test_to_have_text_starting_with_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_text_starting_with("World")

    def test_not_to_have_text_starting_with(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_text_starting_with("World")

    def test_to_have_text_ending_with(self, mock_element: Any) -> None:
        expect(mock_element).to_have_text_ending_with("World")

    def test_to_have_text_ending_with_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_text_ending_with("Hello")

    def test_not_to_have_text_ending_with(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_text_ending_with("Hello")

    def test_to_have_text_in_list(self, mock_element: Any) -> None:
        expect(mock_element).to_have_text_in_list("Hello World", "Other")

    def test_to_have_text_in_list_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_text_in_list("Other", "Different")

    def test_not_to_have_text_in_list(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_text_in_list("Other", "Different")

    def test_to_have_text_in_list_empty_raises(self, mock_element: Any) -> None:
        """to_have_text_in_list() with no args raises ValueError — fail fast."""
        with pytest.raises(ValueError, match="At least one text"):
            expect(mock_element).to_have_text_in_list()


# ============================================================
# Element — Attributes
# ============================================================


class TestElementAttributes:
    def test_to_have_attribute_in_list(self, mock_element: Any) -> None:
        expect(mock_element).to_have_attribute_in_list("id", ["main-content", "other"])

    def test_to_have_attribute_in_list_empty_raises(self, mock_element: Any) -> None:
        with pytest.raises(ValueError, match="values list must not be empty"):
            expect(mock_element).to_have_attribute_in_list("id", [])

    def test_to_have_attribute_in_list_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_attribute_in_list("id", ["wrong", "other"])

    def test_not_to_have_attribute_in_list(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_attribute_in_list("id", ["wrong", "other"])

    def test_to_have_dom_attribute(self, mock_element: Any) -> None:
        mock_element.get_dom_attribute.return_value = "container"
        expect(mock_element).to_have_dom_attribute("class", "container")

    def test_to_have_dom_attribute_fails(self, mock_element: Any) -> None:
        mock_element.get_dom_attribute.return_value = "container"
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_dom_attribute("class", "wrong")

    def test_not_to_have_dom_attribute(self, mock_element: Any) -> None:
        mock_element.get_dom_attribute.return_value = "container"
        expect(mock_element).not_.to_have_dom_attribute("class", "wrong")

    def test_to_have_dom_attribute_contains(self, mock_element: Any) -> None:
        mock_element.get_dom_attribute.return_value = "container active"
        expect(mock_element).to_have_dom_attribute_contains("class", "active")

    def test_to_have_dom_attribute_contains_fails(self, mock_element: Any) -> None:
        mock_element.get_dom_attribute.return_value = "container"
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_dom_attribute_contains("class", "active")

    def test_not_to_have_dom_attribute_contains(self, mock_element: Any) -> None:
        mock_element.get_dom_attribute.return_value = "container"
        expect(mock_element).not_.to_have_dom_attribute_contains("class", "active")

    def test_to_have_property(self, mock_element: Any) -> None:
        mock_element.get_property.return_value = True
        expect(mock_element).to_have_property("checked", True)

    def test_to_have_property_fails(self, mock_element: Any) -> None:
        mock_element.get_property.return_value = False
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_property("checked", True)

    def test_not_to_have_property(self, mock_element: Any) -> None:
        mock_element.get_property.return_value = False
        expect(mock_element).not_.to_have_property("checked", True)

    def test_to_have_property_contains(self, mock_element: Any) -> None:
        mock_element.get_property.return_value = "hello world"
        expect(mock_element).to_have_property_contains("title", "world")

    def test_to_have_property_contains_fails(self, mock_element: Any) -> None:
        mock_element.get_property.return_value = "hello"
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_property_contains("title", "world")

    def test_not_to_have_property_contains(self, mock_element: Any) -> None:
        mock_element.get_property.return_value = "hello"
        expect(mock_element).not_.to_have_property_contains("title", "world")


# ============================================================
# Element — CSS
# ============================================================


class TestElementCSS:
    def test_to_have_css_property_matches(self, mock_element: Any) -> None:
        expect(mock_element).to_have_css_property_matches("color", r"rgba\(0.*\)")

    def test_to_have_css_property_matches_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_css_property_matches("color", r"rgba\(255.*\)")

    def test_not_to_have_css_property_matches(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_css_property_matches("color", r"rgba\(255.*\)")


# ============================================================
# Element — Class
# ============================================================


class TestElementClass:
    def test_to_contain_class(self, mock_element: Any) -> None:
        expect(mock_element).to_contain_class("container")

    def test_to_contain_class_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_contain_class("nonexistent")

    def test_not_to_contain_class(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_contain_class("nonexistent")

    def test_to_have_class_matching(self, mock_element: Any) -> None:
        expect(mock_element).to_have_class_matching(r"cont.*")

    def test_to_have_class_matching_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_class_matching(r"nonexist.*")

    def test_not_to_have_class_matching(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_class_matching(r"nonexist.*")

    def test_to_have_all_classes(self, mock_element: Any) -> None:
        expect(mock_element).to_have_all_classes("container", "active")

    def test_to_have_all_classes_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_all_classes("container", "nonexistent")

    def test_not_to_have_all_classes(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_all_classes("container", "nonexistent")

    def test_to_have_class_in_list(self, mock_element: Any) -> None:
        expect(mock_element).to_have_class_in_list("container", "nonexistent")

    def test_to_have_class_in_list_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_class_in_list("nonexistent", "other")

    def test_not_to_have_class_in_list(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_class_in_list("nonexistent", "other")

    def test_to_have_all_classes_empty_raises(self, mock_element: Any) -> None:
        """to_have_all_classes() with no args raises ValueError — not vacuous pass.

        Regression: previously, set().issubset(elem_classes) was always True,
        so calling with zero classes would vacuously pass.
        """
        with pytest.raises(ValueError, match="At least one class"):
            expect(mock_element).to_have_all_classes()

    def test_to_have_class_in_list_empty_raises(self, mock_element: Any) -> None:
        """to_have_class_in_list() with no args raises ValueError — fail fast."""
        with pytest.raises(ValueError, match="At least one class"):
            expect(mock_element).to_have_class_in_list()

    def test_to_have_aria_role_in_list_empty_raises(self, mock_element: Any) -> None:
        """to_have_aria_role_in_list() with no args raises ValueError — fail fast."""
        with pytest.raises(ValueError, match="At least one role"):
            expect(mock_element).to_have_aria_role_in_list()


# ============================================================
# Element — Value
# ============================================================


class TestElementValue:
    def test_to_have_value_matches(self, mock_element: Any) -> None:
        expect(mock_element).to_have_value_matches(r"test_.*")

    def test_to_have_value_matches_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_value_matches(r"wrong_.*")

    def test_not_to_have_value_matches(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_value_matches(r"wrong_.*")

    def test_to_have_value_in_list(self, mock_element: Any) -> None:
        expect(mock_element).to_have_value_in_list(["test_value", "other"])

    def test_to_have_value_in_list_empty_raises(self, mock_element: Any) -> None:
        with pytest.raises(ValueError, match="values list must not be empty"):
            expect(mock_element).to_have_value_in_list([])

    def test_to_have_value_in_list_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_value_in_list(["wrong", "other"])

    def test_not_to_have_value_in_list(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_value_in_list(["wrong", "other"])


# ============================================================
# Element — Position / Dimensions
# ============================================================


class TestElementPosition:
    def test_to_have_location_greater_than(self, mock_element: Any) -> None:
        expect(mock_element).to_have_location_greater_than(x=50, y=100)

    def test_to_have_location_greater_than_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_location_greater_than(x=200, y=300)

    def test_not_to_have_location_greater_than(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_location_greater_than(x=200, y=300)

    def test_to_have_location_less_than(self, mock_element: Any) -> None:
        expect(mock_element).to_have_location_less_than(x=200, y=300)

    def test_to_have_location_less_than_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_location_less_than(x=50, y=100)

    def test_not_to_have_location_less_than(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_location_less_than(x=50, y=100)

    def test_to_have_size_greater_than(self, mock_element: Any) -> None:
        expect(mock_element).to_have_size_greater_than(width=200, height=40)

    def test_to_have_size_greater_than_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_size_greater_than(width=400, height=100)

    def test_not_to_have_size_greater_than(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_size_greater_than(width=400, height=100)

    def test_to_have_size_less_than(self, mock_element: Any) -> None:
        expect(mock_element).to_have_size_less_than(width=400, height=100)

    def test_to_have_size_less_than_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_size_less_than(width=200, height=40)

    def test_not_to_have_size_less_than(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_size_less_than(width=200, height=40)

    def test_to_have_location_once_scrolled_into_view(self, mock_element: Any) -> None:
        expect(mock_element).to_have_location_once_scrolled_into_view(100, 200)

    def test_to_have_location_once_scrolled_into_view_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_location_once_scrolled_into_view(0, 0)

    def test_not_to_have_location_once_scrolled_into_view(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_location_once_scrolled_into_view(0, 0)


# ============================================================
# Element — Accessibility
# ============================================================


class TestElementAccessibility:
    def test_to_have_aria_role_in_list(self, mock_element: Any) -> None:
        expect(mock_element).to_have_aria_role_in_list("button", "link")

    def test_to_have_aria_role_in_list_fails(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_aria_role_in_list("link", "textbox")

    def test_not_to_have_aria_role_in_list(self, mock_element: Any) -> None:
        expect(mock_element).not_.to_have_aria_role_in_list("link", "textbox")


# ============================================================
# Element — JS Property
# ============================================================


class TestElementJSProperty:
    def test_to_have_js_property(self, mock_element: Any, mock_driver: Any) -> None:
        mock_element.parent = mock_driver
        mock_driver.execute_script.return_value = True
        expect(mock_element).to_have_js_property("checked", True)

    def test_to_have_js_property_fails(self, mock_element: Any, mock_driver: Any) -> None:
        mock_element.parent = mock_driver
        mock_driver.execute_script.return_value = False
        with pytest.raises(AssertionError):
            expect(mock_element).to_have_js_property("checked", True)

    def test_not_to_have_js_property(self, mock_element: Any, mock_driver: Any) -> None:
        mock_element.parent = mock_driver
        mock_driver.execute_script.return_value = False
        expect(mock_element).not_.to_have_js_property("checked", True)


# ============================================================
# Driver — New Window
# ============================================================


class TestDriverNewWindow:
    def test_to_have_new_window_opened(self, mock_driver: Any) -> None:
        mock_driver.window_handles = ["CDwindow-01", "CDwindow-02"]
        expect(mock_driver).to_have_new_window_opened(["CDwindow-01"])

    def test_to_have_new_window_opened_fails(self, mock_driver: Any) -> None:
        mock_driver.window_handles = ["CDwindow-01"]
        with pytest.raises(AssertionError):
            expect(mock_driver).to_have_new_window_opened(["CDwindow-01"])

    def test_not_to_have_new_window_opened(self, mock_driver: Any) -> None:
        mock_driver.window_handles = ["CDwindow-01"]
        expect(mock_driver).not_.to_have_new_window_opened(["CDwindow-01"])


# ============================================================
# Cookies — Expiry
# ============================================================


class TestCookieExpiry:
    def test_to_have_cookie_expiry(self, mock_driver_with_cookies: Any) -> None:
        expect(mock_driver_with_cookies).to_have_cookie_expiry("session", 1735689600)

    def test_to_have_cookie_expiry_fails(self, mock_driver_with_cookies: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_driver_with_cookies).to_have_cookie_expiry("session", 9999999)

    def test_to_have_cookie_expiry_fails_no_cookie(self, mock_driver_with_cookies: Any) -> None:
        with pytest.raises(AssertionError):
            expect(mock_driver_with_cookies).to_have_cookie_expiry("nonexistent", 123)

    def test_not_to_have_cookie_expiry(self, mock_driver_with_cookies: Any) -> None:
        expect(mock_driver_with_cookies).not_.to_have_cookie_expiry("session", 9999999)


# ============================================================
# JavaScript — Variable
# ============================================================


class TestJSVariable:
    def test_to_have_js_variable(self, mock_driver_js: Any) -> None:
        mock_driver_js.execute_script.side_effect = lambda script, *args: (
            42
            if script == "return window[arguments[0]];" and args and args[0] == "counter"
            else None
        )
        expect(mock_driver_js).to_have_js_variable("counter", 42)

    def test_to_have_js_variable_fails(self, mock_driver_js: Any) -> None:
        mock_driver_js.execute_script.side_effect = lambda script, *args: (
            10
            if script == "return window[arguments[0]];" and args and args[0] == "counter"
            else None
        )
        with pytest.raises(AssertionError):
            expect(mock_driver_js).to_have_js_variable("counter", 42)

    def test_not_to_have_js_variable(self, mock_driver_js: Any) -> None:
        mock_driver_js.execute_script.side_effect = lambda script, *args: (
            10
            if script == "return window[arguments[0]];" and args and args[0] == "counter"
            else None
        )
        expect(mock_driver_js).not_.to_have_js_variable("counter", 42)


# ============================================================
# Iframe — In Frame / Default Content
# ============================================================


class TestIframeFrameContext:
    def test_to_be_in_frame(self, mock_driver_iframe: Any) -> None:
        iframe = ExpectIframe(mock_driver_iframe)
        iframe.to_be_in_frame("frame1")

    def test_to_be_in_frame_fails(self, mock_driver_iframe: Any) -> None:
        mock_driver_iframe.switch_to.frame.side_effect = NoSuchFrameException("No frame")
        iframe = ExpectIframe(mock_driver_iframe)
        with pytest.raises(AssertionError):
            iframe.to_be_in_frame("nonexistent")

    def test_not_to_be_in_frame(self, mock_driver_iframe: Any) -> None:
        mock_driver_iframe.switch_to.frame.side_effect = NoSuchFrameException("No frame")
        iframe = ExpectIframe(mock_driver_iframe)
        iframe.not_.to_be_in_frame("nonexistent")

    def test_to_be_in_default_content(self, mock_driver_iframe: Any) -> None:
        iframe = ExpectIframe(mock_driver_iframe)
        iframe.to_be_in_default_content()

    def test_to_be_in_default_content_fails(self, mock_driver_iframe: Any) -> None:
        mock_driver_iframe.switch_to.default_content.side_effect = Exception("Error")
        iframe = ExpectIframe(mock_driver_iframe)
        with pytest.raises(AssertionError):
            iframe.to_be_in_default_content()

    def test_not_to_be_in_default_content(self, mock_driver_iframe: Any) -> None:
        mock_driver_iframe.switch_to.default_content.side_effect = Exception("Error")
        iframe = ExpectIframe(mock_driver_iframe)
        iframe.not_.to_be_in_default_content()


# ============================================================
# Retry — New Exceptions
# ============================================================


class TestRetryNewExceptions:
    def test_element_not_interactable_is_retryable(self) -> None:
        from selenium.common.exceptions import ElementNotInteractableException

        from selenium_expect._retry import RETRYABLE_EXCEPTIONS

        assert ElementNotInteractableException in RETRYABLE_EXCEPTIONS

    def test_no_such_shadow_root_is_retryable(self) -> None:
        from selenium.common.exceptions import NoSuchShadowRootException

        from selenium_expect._retry import RETRYABLE_EXCEPTIONS

        assert NoSuchShadowRootException in RETRYABLE_EXCEPTIONS
