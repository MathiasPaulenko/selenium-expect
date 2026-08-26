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

    def test_to_have_count_greater_than_or_equal(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count_greater_than_or_equal(3) passes (equal)."""
        expect(mock_elements).to_have_count_greater_than_or_equal(3)

    def test_to_have_count_greater_than_or_equal_more(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count_greater_than_or_equal(2) passes (greater)."""
        expect(mock_elements).to_have_count_greater_than_or_equal(2)

    def test_to_have_count_greater_than_or_equal_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count_greater_than_or_equal(5) raises."""
        with pytest.raises(AssertionError, match="to have count >="):
            expect(mock_elements).to_have_count_greater_than_or_equal(5)

    def test_not_to_have_count_greater_than_or_equal(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_count_greater_than_or_equal(5) passes."""
        expect(mock_elements).not_.to_have_count_greater_than_or_equal(5)

    def test_to_have_count_less_than_or_equal(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count_less_than_or_equal(3) passes (equal)."""
        expect(mock_elements).to_have_count_less_than_or_equal(3)

    def test_to_have_count_less_than_or_equal_less(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count_less_than_or_equal(5) passes (less)."""
        expect(mock_elements).to_have_count_less_than_or_equal(5)

    def test_to_have_count_less_than_or_equal_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_count_less_than_or_equal(2) raises."""
        with pytest.raises(AssertionError, match="to have count <="):
            expect(mock_elements).to_have_count_less_than_or_equal(2)

    def test_not_to_have_count_less_than_or_equal(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_count_less_than_or_equal(2) passes."""
        expect(mock_elements).not_.to_have_count_less_than_or_equal(2)

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

    def test_to_have_all_texts_contain_empty_list_fails(
        self, mock_elements_empty: list[Any]
    ) -> None:
        """expect([]).to_have_all_texts_contain('a') fails — empty list must not vacuously pass.

        Regression: previously, `all(text in (t or "") for t in [])` returned True
        vacuously, so the assertion passed on an empty list. This was inconsistent
        with other 'all' assertions (to_have_all_visible, to_have_all_enabled, etc.)
        which require len > 0.
        """
        with pytest.raises(AssertionError, match="to have all texts"):
            expect(mock_elements_empty).to_have_all_texts_contain("a")

    def test_to_have_any_text_contain(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_any_text_contain('App') passes."""
        expect(mock_elements).to_have_any_text_contain("App")

    def test_to_have_none_text_contain(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_none_text_contain('XYZ') passes."""
        expect(mock_elements).to_have_none_text_contain("XYZ")

    def test_to_have_none_text_contain_empty_list_fails(
        self, mock_elements_empty: list[Any]
    ) -> None:
        """expect([]).to_have_none_text_contain('XYZ') fails — empty list must not vacuously pass.

        Regression: previously, `not any(text in (t or "") for t in [])` returned True
        vacuously, so the assertion passed on an empty list. This was inconsistent
        with to_have_all_texts_contain which requires len > 0.
        """
        with pytest.raises(AssertionError, match="to have no text"):
            expect(mock_elements_empty).to_have_none_text_contain("XYZ")

    def test_to_have_texts_empty_list_raises(self, mock_elements: list[Any]) -> None:
        """to_have_texts([]) raises ValueError — not vacuous pass via [] == [].

        Regression: previously, an empty texts list with an empty element list
        would pass vacuously via [] == [] == True.
        """
        with pytest.raises(ValueError, match="texts list must not be empty"):
            expect(mock_elements).to_have_texts([])

    def test_to_have_texts_contains_empty_list_raises(self, mock_elements: list[Any]) -> None:
        """to_have_texts_contains([]) raises ValueError — not vacuous pass via all([]).

        Regression: previously, an empty texts list would pass vacuously via
        all([]) == True.
        """
        with pytest.raises(ValueError, match="texts list must not be empty"):
            expect(mock_elements).to_have_texts_contains([])

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

    def test_to_have_exact_texts(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_exact_texts('Apple', 'Banana', 'Cherry') passes."""
        expect(mock_elements).to_have_exact_texts("Apple", "Banana", "Cherry")

    def test_to_have_exact_texts_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_exact_texts('Wrong') raises."""
        with pytest.raises(AssertionError, match="to have exact texts"):
            expect(mock_elements).to_have_exact_texts("Wrong", "List", "Items")

    def test_not_to_have_exact_texts(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_exact_texts('Wrong') passes."""
        expect(mock_elements).not_.to_have_exact_texts("Wrong", "List", "Items")

    def test_to_have_texts_containing(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_texts_containing('App', 'Ban', 'Che') passes."""
        expect(mock_elements).to_have_texts_containing("App", "Ban", "Che")

    def test_to_have_texts_containing_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_texts_containing('XYZ') raises."""
        with pytest.raises(AssertionError, match="to have texts containing"):
            expect(mock_elements).to_have_texts_containing("XYZ", "Ban", "Che")

    def test_not_to_have_texts_containing(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_texts_containing('XYZ') passes."""
        expect(mock_elements).not_.to_have_texts_containing("XYZ", "Ban", "Che")

    def test_to_have_texts_in_any_order(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_texts_in_any_order('Cherry', 'Apple', 'Banana') passes."""
        expect(mock_elements).to_have_texts_in_any_order("Cherry", "Apple", "Banana")

    def test_to_have_texts_in_any_order_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_texts_in_any_order('Wrong') raises."""
        with pytest.raises(AssertionError, match="to have texts in any order"):
            expect(mock_elements).to_have_texts_in_any_order("Wrong", "Apple", "Banana")

    def test_not_to_have_texts_in_any_order(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_texts_in_any_order('Wrong') passes."""
        expect(mock_elements).not_.to_have_texts_in_any_order("Wrong", "Apple", "Banana")

    def test_to_have_exact_texts_empty_raises(self, mock_elements: list[Any]) -> None:
        """to_have_exact_texts() with no args raises ValueError — not vacuous pass.

        Regression: previously, zero texts with an empty element list would
        pass vacuously via [] == [] == True.
        """
        with pytest.raises(ValueError, match="At least one text"):
            expect(mock_elements).to_have_exact_texts()

    def test_to_have_texts_containing_empty_raises(self, mock_elements: list[Any]) -> None:
        """to_have_texts_containing() with no args raises ValueError — not vacuous pass.

        Regression: previously, zero texts with an empty element list would
        pass vacuously via all([]) == True.
        """
        with pytest.raises(ValueError, match="At least one text"):
            expect(mock_elements).to_have_texts_containing()

    def test_to_have_texts_in_any_order_empty_raises(self, mock_elements: list[Any]) -> None:
        """to_have_texts_in_any_order() with no args raises ValueError — not vacuous pass."""
        with pytest.raises(ValueError, match="At least one text"):
            expect(mock_elements).to_have_texts_in_any_order()

    def test_to_have_first_text(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_first_text('Apple') passes."""
        expect(mock_elements).to_have_first_text("Apple")

    def test_to_have_first_text_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_first_text('Wrong') raises."""
        with pytest.raises(AssertionError, match="to have first text"):
            expect(mock_elements).to_have_first_text("Wrong")

    def test_not_to_have_first_text(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_first_text('Wrong') passes."""
        expect(mock_elements).not_.to_have_first_text("Wrong")

    def test_to_have_last_text(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_last_text('Cherry') passes."""
        expect(mock_elements).to_have_last_text("Cherry")

    def test_to_have_last_text_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_last_text('Wrong') raises."""
        with pytest.raises(AssertionError, match="to have last text"):
            expect(mock_elements).to_have_last_text("Wrong")

    def test_not_to_have_last_text(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_last_text('Wrong') passes."""
        expect(mock_elements).not_.to_have_last_text("Wrong")

    def test_to_have_nth_text_contains(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_nth_text_contains(0, 'App') passes."""
        expect(mock_elements).to_have_nth_text_contains(0, "App")

    def test_to_have_nth_text_contains_negative_index(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_nth_text_contains(-1, 'Che') passes."""
        expect(mock_elements).to_have_nth_text_contains(-1, "Che")

    def test_to_have_nth_text_contains_fails(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_nth_text_contains(0, 'XYZ') raises."""
        with pytest.raises(AssertionError, match="to have text at"):
            expect(mock_elements).to_have_nth_text_contains(0, "XYZ")

    def test_not_to_have_nth_text_contains(self, mock_elements: list[Any]) -> None:
        """expect(elements).not_.to_have_nth_text_contains(0, 'XYZ') passes."""
        expect(mock_elements).not_.to_have_nth_text_contains(0, "XYZ")


class TestExpectListValues:
    def test_to_have_values(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_values(['apple', 'banana', 'cherry']) passes.

        mock_elements get_attribute returns text.lower() for any attribute.
        """
        expect(mock_elements).to_have_values(["apple", "banana", "cherry"])

    def test_to_have_value_at(self, mock_elements: list[Any]) -> None:
        """expect(elements).to_have_value_at(1, 'banana') passes."""
        expect(mock_elements).to_have_value_at(1, "banana")

    def test_to_have_values_empty_list_raises(self, mock_elements: list[Any]) -> None:
        """to_have_values([]) raises ValueError — not vacuous pass via [] == [].

        Regression: previously, an empty values list with an empty element list
        would pass vacuously via [] == [] == True.
        """
        with pytest.raises(ValueError, match="values list must not be empty"):
            expect(mock_elements).to_have_values([])

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

    def test_to_have_none_visible_empty_list_fails(self, mock_elements_empty: list[Any]) -> None:
        """expect([]).to_have_none_visible() fails — empty list must not vacuously pass.

        Regression: previously, `not any([])` returned True vacuously, so the
        assertion passed on an empty list. This was inconsistent with
        to_have_all_visible which requires len > 0.
        """
        with pytest.raises(AssertionError, match="to have none visible"):
            expect(mock_elements_empty).to_have_none_visible()

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
