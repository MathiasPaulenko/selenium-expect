"""Unit tests for selenium_expect.assertions.list.ExpectList."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect
from selenium_expect.assertions.list import ExpectList


class TestExpectListCount:
    def test_to_have_count(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count(3) passes."""
        expect(mock_elements).to_have_count(3)

    def test_to_have_count_greater_than(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count_greater_than(2) passes."""
        expect(mock_elements).to_have_count_greater_than(2)

    def test_to_have_count_less_than(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count_less_than(5) passes."""
        expect(mock_elements).to_have_count_less_than(5)

    def test_to_be_empty(self, mock_elements_empty: list[Any]) -> None:
        """expect([]).to_be_empty() passes."""
        expect(mock_elements_empty).to_be_empty()

    def test_to_be_not_empty(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_be_not_empty() passes."""
        expect(mock_elements).to_be_not_empty()

    def test_to_have_count_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count(5) raises."""
        with pytest.raises(AssertionError, match="to have count"):
            expect(mock_elements).to_have_count(5)

    def test_to_be_empty_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_be_empty() raises."""
        with pytest.raises(AssertionError, match="to be empty"):
            expect(mock_elements).to_be_empty()


class TestExpectListText:
    def test_to_have_texts(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_texts(['Apple', 'Banana', 'Cherry']) passes."""
        expect(mock_elements).to_have_texts(["Apple", "Banana", "Cherry"])

    def test_to_have_texts_contains(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_texts_contains(['App', 'Ban', 'Cher']) passes."""
        expect(mock_elements).to_have_texts_contains(["App", "Ban", "Cher"])

    def test_to_have_text_at(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_text_at(0, 'Apple') passes."""
        expect(mock_elements).to_have_text_at(0, "Apple")

    def test_to_have_any_text(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_any_text('Banana') passes."""
        expect(mock_elements).to_have_any_text("Banana")

    def test_to_have_all_texts_contain(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_all_texts_contain('a') fails — 'Cherry' lacks 'a'."""
        with pytest.raises(AssertionError, match="to have all texts"):
            expect(mock_elements).to_have_all_texts_contain("a")

    def test_to_have_any_text_contain(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_any_text_contain('App') passes."""
        expect(mock_elements).to_have_any_text_contain("App")

    def test_to_have_none_text_contain(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_none_text_contain('XYZ') passes."""
        expect(mock_elements).to_have_none_text_contain("XYZ")

    def test_to_have_texts_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_texts(['Wrong']) raises."""
        with pytest.raises(AssertionError, match="to have texts"):
            expect(mock_elements).to_have_texts(["Wrong", "List", "Items"])

    def test_to_have_text_at_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_text_at(0, 'Wrong') raises."""
        with pytest.raises(AssertionError, match="to have text at"):
            expect(mock_elements).to_have_text_at(0, "Wrong")

    def test_to_have_any_text_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_any_text('Missing') raises."""
        with pytest.raises(AssertionError, match="to have any text"):
            expect(mock_elements).to_have_any_text("Missing")


class TestExpectListValues:
    def test_to_have_values(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_values(['apple', 'banana', 'cherry']) passes.

        mock_elements get_attribute returns text.lower() for any attribute.
        """
        expect(mock_elements).to_have_values(["apple", "banana", "cherry"])

    def test_to_have_value_at(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_value_at(1, 'banana') passes."""
        expect(mock_elements).to_have_value_at(1, "banana")

    def test_to_have_values_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_values(['wrong']) raises."""
        with pytest.raises(AssertionError, match="to have values"):
            expect(mock_elements).to_have_values(["wrong", "vals", "here"])

    def test_to_have_value_at_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_value_at(0, 'wrong') raises."""
        with pytest.raises(AssertionError, match="to have value at"):
            expect(mock_elements).to_have_value_at(0, "wrong")


class TestExpectListState:
    def test_to_have_all_visible(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_all_visible() passes (all visible)."""
        expect(mock_elements).to_have_all_visible()

    def test_to_have_any_visible(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_any_visible() passes."""
        expect(mock_elements).to_have_any_visible()

    def test_to_have_none_visible(self, mock_elements_mixed_visibility: list[Any]) -> None:
        """expect(mixed).to_have_none_visible() fails (has visible ones)."""
        with pytest.raises(AssertionError, match="to have none visible"):
            expect(mock_elements_mixed_visibility).to_have_none_visible()

    def test_to_have_any_visible_mixed(self, mock_elements_mixed_visibility: list[Any]) -> None:
        """expect(mixed).to_have_any_visible() passes (some visible)."""
        expect(mock_elements_mixed_visibility).to_have_any_visible()

    def test_to_have_all_visible_mixed_fails(
        self, mock_elements_mixed_visibility: list[Any]
    ) -> None:
        """expect(mixed).to_have_all_visible() fails (one is hidden)."""
        with pytest.raises(AssertionError, match="to have all visible"):
            expect(mock_elements_mixed_visibility).to_have_all_visible()

    def test_to_have_all_enabled(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_all_enabled() passes."""
        expect(mock_elements).to_have_all_enabled()

    def test_to_have_all_selected_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_all_selected() fails (none selected)."""
        with pytest.raises(AssertionError, match="to have all selected"):
            expect(mock_elements).to_have_all_selected()


class TestExpectListAttributes:
    def test_to_have_attribute_at(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_attribute_at(0, 'value', 'apple') passes.

        mock_elements get_attribute returns text.lower() for any name.
        """
        expect(mock_elements).to_have_attribute_at(0, "value", "apple")

    def test_to_have_all_attribute(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_all_attribute('value', 'apple') fails (not all 'apple')."""
        with pytest.raises(AssertionError, match="to have all attribute"):
            expect(mock_elements).to_have_all_attribute("value", "apple")

    def test_to_have_any_attribute(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_any_attribute('value', 'apple') passes."""
        expect(mock_elements).to_have_any_attribute("value", "apple")

    def test_to_have_attribute_at_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_attribute_at(0, 'value', 'wrong') raises."""
        with pytest.raises(AssertionError, match="to have attribute"):
            expect(mock_elements).to_have_attribute_at(0, "value", "wrong")


class TestExpectListNegation:
    def test_not_to_have_count(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_count(5) passes."""
        expect(mock_elements).not_.to_have_count(5)

    def test_not_to_have_texts(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_texts(['Wrong']) passes."""
        expect(mock_elements).not_.to_have_texts(["Wrong", "List", "Items"])

    def test_not_to_be_empty(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_be_empty() passes."""
        expect(mock_elements).not_.to_be_empty()


class TestExpectListDispatch:
    def test_expect_dispatches_to_list(self, mock_elements: list[Any]) -> None:
        """expect(elements) returns ExpectList instance."""
        result = expect(mock_elements)
        assert isinstance(result, ExpectList)
