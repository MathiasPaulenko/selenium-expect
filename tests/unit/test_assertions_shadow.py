"""Unit tests for selenium_expect.assertions.shadow.ExpectShadow."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect
from selenium_expect.assertions.shadow import ExpectShadow


class TestExpectShadow:
    def test_to_have_element(self, mock_shadow_root: Any) -> None:
        """expect(shadow).to_have_element('css selector', 'div') passes."""
        expect(mock_shadow_root).to_have_element("css selector", "div")

    def test_to_have_element_count(self, mock_shadow_root: Any) -> None:
        """expect(shadow).to_have_element_count('css selector', 'div', 1) passes."""
        expect(mock_shadow_root).to_have_element_count("css selector", "div", 1)

    def test_to_have_element_text(self, mock_shadow_root: Any) -> None:
        """expect(shadow).to_have_element_text('css selector', 'div', 'Shadow content') passes."""
        expect(mock_shadow_root).to_have_element_text("css selector", "div", "Shadow content")

    def test_to_have_element_attribute(self, mock_shadow_root: Any) -> None:
        """to_have_element_attribute with id='shadow-item' passes."""
        expect(mock_shadow_root).to_have_element_attribute(
            "css selector", "div", "id", "shadow-item"
        )

    def test_to_have_element_visible(self, mock_shadow_root: Any) -> None:
        """expect(shadow).to_have_element_visible('css selector', 'div') passes."""
        expect(mock_shadow_root).to_have_element_visible("css selector", "div")

    # --- Failure cases ---

    def test_to_have_element_count_fails(self, mock_shadow_root: Any) -> None:
        """expect(shadow).to_have_element_count('css selector', 'div', 5) raises."""
        with pytest.raises(AssertionError, match="element count"):
            expect(mock_shadow_root).to_have_element_count("css selector", "div", 5)

    def test_to_have_element_text_fails(self, mock_shadow_root: Any) -> None:
        """expect(shadow).to_have_element_text('css selector', 'div', 'Wrong') raises."""
        with pytest.raises(AssertionError, match="element text"):
            expect(mock_shadow_root).to_have_element_text("css selector", "div", "Wrong text")


class TestExpectShadowDispatch:
    def test_expect_dispatches_to_shadow(self, mock_shadow_root: Any) -> None:
        """expect(shadow_root) returns ExpectShadow instance."""
        result = expect(mock_shadow_root)
        assert isinstance(result, ExpectShadow)
