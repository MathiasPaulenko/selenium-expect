"""Unit tests for ExpectElement state and text assertions."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from selenium_expect import expect
from selenium_expect.assertions.element import ExpectElement


class TestExpectElementState:
    def test_to_be_visible(self, mock_element: Any) -> None:
        """expect(el).to_be_visible() passes when is_displayed() == True."""
        expect(mock_element).to_be_visible()

    def test_to_be_hidden(self, mock_element_hidden: Any) -> None:
        """expect(el).to_be_hidden() passes when is_displayed() == False."""
        expect(mock_element_hidden).to_be_hidden()

    def test_to_be_enabled(self, mock_element: Any) -> None:
        """expect(el).to_be_enabled() passes when is_enabled() == True."""
        expect(mock_element).to_be_enabled()

    def test_to_be_disabled(self, mock_element_disabled: Any) -> None:
        """expect(el).to_be_disabled() passes when is_enabled() == False."""
        expect(mock_element_disabled).to_be_disabled()

    def test_to_be_checked(self, mock_element_checked: Any) -> None:
        """expect(el).to_be_checked() passes when is_selected() == True."""
        expect(mock_element_checked).to_be_checked()

    def test_to_be_selected(self, mock_element_checked: Any) -> None:
        """expect(el).to_be_selected() passes when is_selected() == True."""
        expect(mock_element_checked).to_be_selected()

    def test_to_be_present(self, mock_element: Any) -> None:
        """expect(el).to_be_present() passes when element exists in DOM."""
        expect(mock_element).to_be_present()

    def test_to_be_clickable(self, mock_element: Any) -> None:
        """expect(el).to_be_clickable() passes when displayed and enabled."""
        expect(mock_element).to_be_clickable()

    def test_to_be_stale(self, mock_element_stale: Any) -> None:
        """expect(el).to_be_stale() passes when element is stale."""
        expect(mock_element_stale).to_be_stale()

    def test_not_to_be_visible(self, mock_element_hidden: Any) -> None:
        """expect(hidden_el).not_.to_be_visible() passes (negation)."""
        expect(mock_element_hidden).not_.to_be_visible()

    def test_not_to_be_enabled(self, mock_element_disabled: Any) -> None:
        """expect(disabled_el).not_.to_be_enabled() passes (negation)."""
        expect(mock_element_disabled).not_.to_be_enabled()

    def test_to_be_visible_fails(self, mock_element_hidden: Any) -> None:
        """expect(hidden_el).to_be_visible() raises AssertionError."""
        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_element_hidden).to_be_visible()

    def test_to_be_hidden_fails(self, mock_element: Any) -> None:
        """expect(visible_el).to_be_hidden() raises AssertionError."""
        with pytest.raises(AssertionError, match="to be hidden"):
            expect(mock_element).to_be_hidden()

    def test_to_be_enabled_fails(self, mock_element_disabled: Any) -> None:
        """expect(disabled_el).to_be_enabled() raises AssertionError."""
        with pytest.raises(AssertionError, match="to be enabled"):
            expect(mock_element_disabled).to_be_enabled()

    def test_to_be_disabled_fails(self, mock_element: Any) -> None:
        """expect(enabled_el).to_be_disabled() raises AssertionError."""
        with pytest.raises(AssertionError, match="to be disabled"):
            expect(mock_element).to_be_disabled()


class TestExpectElementText:
    def test_to_have_text_exact(self, mock_element: Any) -> None:
        """expect(el).to_have_text('Hello World') passes."""
        expect(mock_element).to_have_text("Hello World")

    def test_to_have_text_contains(self, mock_element: Any) -> None:
        """expect(el).to_have_text_contains('Hello') passes."""
        expect(mock_element).to_have_text_contains("Hello")

    def test_to_have_text_matches(self, mock_element: Any) -> None:
        """expect(el).to_have_text_matches(r'Hello') passes."""
        expect(mock_element).to_have_text_matches(r"Hello")

    def test_to_have_text_empty(self, mock_element: Any) -> None:
        """expect(el).to_have_text_empty() — mock_element has text, so fails."""
        with pytest.raises(AssertionError, match="text empty"):
            expect(mock_element).to_have_text_empty()

    def test_to_have_text_empty_passes(self) -> None:
        """expect(el).to_have_text_empty() passes when text is empty string."""
        from selenium.webdriver.remote.webelement import WebElement

        el = MagicMock(spec=WebElement)
        el.text = ""
        el.tag_name = "div"
        el.get_attribute.return_value = None
        expect(el).to_have_text_empty()

    def test_to_have_text_not_empty(self, mock_element: Any) -> None:
        """expect(el).to_have_text_not_empty() passes when text is non-empty."""
        expect(mock_element).to_have_text_not_empty()

    def test_to_have_value(self, mock_element: Any) -> None:
        """expect(el).to_have_value('test_value') passes."""
        expect(mock_element).to_have_value("test_value")

    def test_to_have_value_contains(self, mock_element: Any) -> None:
        """expect(el).to_have_value_contains('test') passes."""
        expect(mock_element).to_have_value_contains("test")

    def test_not_to_have_text(self, mock_element: Any) -> None:
        """expect(el).not_.to_have_text('Goodbye') passes (negation)."""
        expect(mock_element).not_.to_have_text("Goodbye")

    def test_to_have_text_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_text('Wrong') raises AssertionError."""
        with pytest.raises(AssertionError, match="to have text"):
            expect(mock_element).to_have_text("Wrong text")

    def test_to_have_text_contains_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_text_contains('NonExistent') raises."""
        with pytest.raises(AssertionError, match="text containing"):
            expect(mock_element).to_have_text_contains("NonExistentText")

    def test_to_have_value_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_value('wrong') raises AssertionError."""
        with pytest.raises(AssertionError, match="to have value"):
            expect(mock_element).to_have_value("wrong_value")


class TestExpectElementNegation:
    def test_not_property_returns_new_instance(self, mock_element: Any) -> None:
        """expect(el).not_ returns a new ExpectElement instance."""
        original = expect(mock_element)
        negated = original.not_
        assert negated is not original
        assert isinstance(negated, ExpectElement)

    def test_not_does_not_mutate_original(self, mock_element: Any) -> None:
        """not_ does not change the original instance's _negate flag."""
        original = expect(mock_element)
        _ = original.not_
        assert original._negate is False

    def test_chained_not_not_cancels_out(self, mock_element: Any) -> None:
        """expect(el).not_.not_.to_be_visible() passes (double negation)."""
        expect(mock_element).not_.not_.to_be_visible()


class TestExpectElementAttributes:
    def test_to_have_attribute(self, mock_element: Any) -> None:
        """expect(el).to_have_attribute('id', 'main-content') passes."""
        expect(mock_element).to_have_attribute("id", "main-content")

    def test_to_have_attribute_contains(self, mock_element: Any) -> None:
        """expect(el).to_have_attribute_contains('class', 'container') passes."""
        expect(mock_element).to_have_attribute_contains("class", "container")

    def test_to_have_attribute_matches(self, mock_element: Any) -> None:
        """expect(el).to_have_attribute_matches('href', r'example.com') passes."""
        expect(mock_element).to_have_attribute_matches("href", r"example\.com")

    def test_to_have_attribute_empty(self, mock_element: Any) -> None:
        """expect(el).to_have_attribute_empty('checked') passes (None attr)."""
        expect(mock_element).to_have_attribute_empty("checked")

    def test_to_have_attribute_present(self, mock_element: Any) -> None:
        """expect(el).to_have_attribute_present('id') passes."""
        expect(mock_element).to_have_attribute_present("id")

    def test_to_have_attribute_absent(self, mock_element: Any) -> None:
        """expect(el).to_have_attribute_absent('nonexistent') passes."""
        expect(mock_element).to_have_attribute_absent("nonexistent")

    def test_to_have_attribute_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_attribute('id', 'wrong') raises."""
        with pytest.raises(AssertionError, match="to have attribute"):
            expect(mock_element).to_have_attribute("id", "wrong-id")


class TestExpectElementCSS:
    def test_to_have_css_property(self, mock_element: Any) -> None:
        """expect(el).to_have_css_property('display', 'block') passes."""
        expect(mock_element).to_have_css_property("display", "block")

    def test_to_have_css_property_contains(self, mock_element: Any) -> None:
        """expect(el).to_have_css_property_contains('color', '0, 0, 255') passes."""
        expect(mock_element).to_have_css_property_contains("color", "0, 0, 255")

    def test_to_have_css_property_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_css_property('display', 'none') raises."""
        with pytest.raises(AssertionError, match="to have CSS"):
            expect(mock_element).to_have_css_property("display", "none")


class TestExpectElementIdentity:
    def test_to_have_tag(self, mock_element: Any) -> None:
        """expect(el).to_have_tag('div') passes."""
        expect(mock_element).to_have_tag("div")

    def test_to_have_id(self, mock_element: Any) -> None:
        """expect(el).to_have_id('main-content') passes."""
        expect(mock_element).to_have_id("main-content")

    def test_to_have_class(self, mock_element: Any) -> None:
        """expect(el).to_have_class('container') passes (exact class match)."""
        expect(mock_element).to_have_class("container")

    def test_to_have_class_contains(self, mock_element: Any) -> None:
        """expect(el).to_have_class_contains('container') passes (substring)."""
        expect(mock_element).to_have_class_contains("container")

    def test_to_have_tag_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_tag('span') raises."""
        with pytest.raises(AssertionError, match="to have tag"):
            expect(mock_element).to_have_tag("span")

    def test_to_have_id_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_id('wrong') raises."""
        with pytest.raises(AssertionError, match="to have id"):
            expect(mock_element).to_have_id("wrong-id")

    def test_to_have_class_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_class('nonexistent') raises."""
        with pytest.raises(AssertionError, match="to have class"):
            expect(mock_element).to_have_class("nonexistent")


class TestExpectElementPosition:
    def test_to_have_location(self, mock_element: Any) -> None:
        """expect(el).to_have_location(100, 200) passes."""
        expect(mock_element).to_have_location(100, 200)

    def test_to_have_location_x(self, mock_element: Any) -> None:
        """expect(el).to_have_location_x(100) passes."""
        expect(mock_element).to_have_location_x(100)

    def test_to_have_location_y(self, mock_element: Any) -> None:
        """expect(el).to_have_location_y(200) passes."""
        expect(mock_element).to_have_location_y(200)

    def test_to_have_size(self, mock_element: Any) -> None:
        """expect(el).to_have_size(300, 50) passes."""
        expect(mock_element).to_have_size(300, 50)

    def test_to_have_size_width(self, mock_element: Any) -> None:
        """expect(el).to_have_size_width(300) passes."""
        expect(mock_element).to_have_size_width(300)

    def test_to_have_size_height(self, mock_element: Any) -> None:
        """expect(el).to_have_size_height(50) passes."""
        expect(mock_element).to_have_size_height(50)

    def test_to_have_rect(self, mock_element: Any) -> None:
        """expect(el).to_have_rect(100, 200, 300, 50) passes."""
        expect(mock_element).to_have_rect(100, 200, 300, 50)

    def test_to_have_location_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_location(0, 0) raises."""
        with pytest.raises(AssertionError, match="to have location"):
            expect(mock_element).to_have_location(0, 0)

    def test_to_have_size_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_size(0, 0) raises."""
        with pytest.raises(AssertionError, match="to have size"):
            expect(mock_element).to_have_size(0, 0)


class TestExpectElementAccessibility:
    def test_to_have_aria_role(self, mock_element: Any) -> None:
        """expect(el).to_have_aria_role('button') passes."""
        expect(mock_element).to_have_aria_role("button")

    def test_to_have_aria_role_contains(self, mock_element: Any) -> None:
        """expect(el).to_have_aria_role_contains('but') passes."""
        expect(mock_element).to_have_aria_role_contains("but")

    def test_to_have_accessible_name(self, mock_element: Any) -> None:
        """expect(el).to_have_accessible_name('Submit Form') passes."""
        expect(mock_element).to_have_accessible_name("Submit Form")

    def test_to_have_accessible_name_contains(self, mock_element: Any) -> None:
        """expect(el).to_have_accessible_name_contains('Submit') passes."""
        expect(mock_element).to_have_accessible_name_contains("Submit")

    def test_to_have_aria_role_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_aria_role('link') raises."""
        with pytest.raises(AssertionError, match="aria role"):
            expect(mock_element).to_have_aria_role("link")


class TestExpectElementShadow:
    def test_to_have_shadow_root(self, mock_element: Any) -> None:
        """expect(el).to_have_shadow_root() — mock has shadow_root=None, so fails."""
        with pytest.raises(AssertionError, match="shadow root"):
            expect(mock_element).to_have_shadow_root()

    def test_to_have_shadow_root_absent(self, mock_element: Any) -> None:
        """expect(el).to_have_shadow_root_absent() passes (shadow_root is None)."""
        expect(mock_element).to_have_shadow_root_absent()

    def test_to_have_shadow_root_passes(self) -> None:
        """expect(el).to_have_shadow_root() passes when shadow_root is not None."""
        from selenium.webdriver.remote.webelement import WebElement

        el = MagicMock(spec=WebElement)
        el.shadow_root = MagicMock()
        el.tag_name = "div"
        el.get_attribute.return_value = None
        expect(el).to_have_shadow_root()
