"""Unit tests for selenium_expect.assertions.select.ExpectSelect."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect
from selenium_expect.assertions.select import ExpectSelect


class TestExpectSelect:
    def test_to_have_value(self, mock_select: Any) -> None:
        """expect(select).to_have_value('opt1') passes."""
        expect(mock_select).to_have_value("opt1")

    def test_to_have_first_selected_value(self, mock_select: Any) -> None:
        """expect(select).to_have_first_selected_value('opt1') passes."""
        expect(mock_select).to_have_first_selected_value("opt1")

    def test_to_have_selected_text(self, mock_select: Any) -> None:
        """expect(select).to_have_selected_text('Option 1') passes."""
        expect(mock_select).to_have_selected_text("Option 1")

    def test_to_have_selected_values(self, mock_select_multiple: Any) -> None:
        """expect(select).to_have_selected_values(['opt1', 'opt2']) passes."""
        expect(mock_select_multiple).to_have_selected_values(["opt1", "opt2"])

    def test_to_have_selected_texts(self, mock_select_multiple: Any) -> None:
        """expect(select).to_have_selected_texts(['Option 1', 'Option 2']) passes."""
        expect(mock_select_multiple).to_have_selected_texts(["Option 1", "Option 2"])

    def test_to_have_selected_count(self, mock_select: Any) -> None:
        """expect(select).to_have_selected_count(1) passes."""
        expect(mock_select).to_have_selected_count(1)

    def test_to_have_option_count(self, mock_select: Any) -> None:
        """expect(select).to_have_option_count(3) passes."""
        expect(mock_select).to_have_option_count(3)

    def test_to_have_option_count_greater_than(self, mock_select: Any) -> None:
        """expect(select).to_have_option_count_greater_than(2) passes."""
        expect(mock_select).to_have_option_count_greater_than(2)

    def test_to_have_option_at_index(self, mock_select: Any) -> None:
        """expect(select).to_have_option_at_index(0, 'Option 1') passes."""
        expect(mock_select).to_have_option_at_index(0, "Option 1")

    def test_to_have_option(self, mock_select: Any) -> None:
        """expect(select).to_have_option('opt2') passes."""
        expect(mock_select).to_have_option("opt2")

    def test_to_have_option_text(self, mock_select: Any) -> None:
        """expect(select).to_have_option_text('Option 3') passes."""
        expect(mock_select).to_have_option_text("Option 3")

    def test_to_be_multiple(self, mock_select_multiple: Any) -> None:
        """expect(select).to_be_multiple() passes for multi-select."""
        expect(mock_select_multiple).to_be_multiple()

    def test_to_be_single_select(self, mock_select: Any) -> None:
        """expect(select).to_be_single_select() passes for single-select."""
        expect(mock_select).to_be_single_select()

    # --- Failure cases ---

    def test_to_have_value_fails(self, mock_select: Any) -> None:
        """expect(select).to_have_value('wrong') raises."""
        with pytest.raises(AssertionError, match="to have value"):
            expect(mock_select).to_have_value("wrong")

    def test_to_have_option_count_fails(self, mock_select: Any) -> None:
        """expect(select).to_have_option_count(99) raises."""
        with pytest.raises(AssertionError, match="option count"):
            expect(mock_select).to_have_option_count(99)

    def test_to_be_multiple_fails(self, mock_select: Any) -> None:
        """expect(select).to_be_multiple() raises for single-select."""
        with pytest.raises(AssertionError, match="to be multiple"):
            expect(mock_select).to_be_multiple()


class TestExpectSelectDispatch:
    def test_expect_dispatches_to_select(self, mock_select: Any) -> None:
        """expect(select) returns ExpectSelect instance."""
        result = expect(mock_select)
        assert isinstance(result, ExpectSelect)
