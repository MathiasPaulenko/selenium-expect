"""Integration tests for WebElement assertions."""

from __future__ import annotations

from typing import Any

import pytest
from selenium.webdriver.common.by import By

from selenium_expect import expect

pytestmark = pytest.mark.integration


class TestIntegrationElementState:
    def test_visible_element(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "title")
        expect(el).to_be_visible()

    def test_hidden_element(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "hidden-div")
        expect(el).to_be_hidden()

    def test_enabled_element(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "btn-enabled")
        expect(el).to_be_enabled()

    def test_disabled_button(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "btn-disabled")
        expect(el).to_be_disabled()

    def test_checked_checkbox(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "checkbox-checked")
        expect(el).to_be_checked()

    def test_present_element(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_be_present()

    def test_clickable_element(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "btn-enabled")
        expect(el).to_be_clickable()


class TestIntegrationElementText:
    def test_text_exact(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "title")
        expect(el).to_have_text("Hello World")

    def test_text_contains(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "title")
        expect(el).to_have_text_contains("Hello")

    def test_text_empty(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "empty-input")
        expect(el).to_have_text("")

    def test_value(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "text-input")
        expect(el).to_have_value("test value")


class TestIntegrationElementAttributes:
    def test_attribute_id(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_attribute("id", "main")

    def test_attribute_class(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_attribute("class", "container active")

    def test_attribute_contains(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_attribute_contains("class", "container")

    def test_attribute_present(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_attribute_present("role")

    def test_attribute_absent(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "title")
        expect(el).not_.to_have_attribute_present("role")


class TestIntegrationElementCSS:
    def test_css_display(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_css_property("display", "block")

    def test_css_color(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_css_property_contains("color", "rgba(255")


class TestIntegrationElementIdentity:
    def test_tag_name(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "title")
        expect(el).to_have_tag("h1")

    def test_id(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_id("main")

    def test_class(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_class("active")


class TestIntegrationElementPosition:
    def test_location(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "box")
        expect(el).to_have_location(10, 20)

    def test_size(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "box")
        expect(el).to_have_size(100, 50)

    def test_rect(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "box")
        expect(el).to_have_rect(10, 20, 100, 50)


class TestIntegrationElementAccessibility:
    def test_aria_role(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_aria_role("main")

    def test_accessible_name(self, test_page: Any) -> None:
        el = test_page.find_element(By.ID, "main")
        expect(el).to_have_accessible_name("Main content")
