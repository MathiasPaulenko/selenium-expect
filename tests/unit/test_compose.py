"""Unit tests for selenium_expect._compose composition assertions."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect
from selenium_expect._compose import satisfy_all, satisfy_any, satisfy_none


def _is_visible(target: Any) -> None:
    """Condition: target.is_displayed() must be True."""
    assert target.is_displayed(), "not visible"


def _is_enabled(target: Any) -> None:
    """Condition: target.is_enabled() must be True."""
    assert target.is_enabled(), "not enabled"


def _is_selected(target: Any) -> None:
    """Condition: target.is_selected() must be True."""
    assert target.is_selected(), "not selected"


def _always_fail(target: Any) -> None:
    """Condition that always fails."""
    raise AssertionError("always fails")


def _always_pass(target: Any) -> None:
    """Condition that always passes."""


class TestSatisfyAll:
    def test_all_pass(self, mock_element: Any) -> None:
        """satisfy_all passes when all conditions pass."""
        satisfy_all(mock_element, _is_visible, _is_enabled)

    def test_one_fails(self, mock_element: Any) -> None:
        """satisfy_all raises when one condition fails."""
        with pytest.raises(AssertionError, match="to_satisfy_all"):
            satisfy_all(mock_element, _is_visible, _is_selected)

    def test_all_fail(self, mock_element: Any) -> None:
        """satisfy_all raises when all conditions fail."""
        with pytest.raises(AssertionError, match="to_satisfy_all"):
            satisfy_all(mock_element, _always_fail, _always_fail)

    def test_empty_conditions(self, mock_element: Any) -> None:
        """satisfy_all with no conditions passes vacuously."""
        satisfy_all(mock_element)


class TestSatisfyAny:
    def test_one_passes(self, mock_element: Any) -> None:
        """satisfy_any passes when at least one condition passes."""
        satisfy_any(mock_element, _is_selected, _is_visible)

    def test_all_pass(self, mock_element: Any) -> None:
        """satisfy_any passes when all conditions pass."""
        satisfy_any(mock_element, _is_visible, _is_enabled)

    def test_all_fail(self, mock_element: Any) -> None:
        """satisfy_any raises when all conditions fail."""
        with pytest.raises(AssertionError, match="to_satisfy_any"):
            satisfy_any(mock_element, _always_fail, _always_fail)

    def test_empty_conditions(self, mock_element: Any) -> None:
        """satisfy_any with no conditions raises (none passed)."""
        with pytest.raises(AssertionError, match="to_satisfy_any"):
            satisfy_any(mock_element)


class TestSatisfyNone:
    def test_all_fail(self, mock_element: Any) -> None:
        """satisfy_none passes when no condition passes."""
        satisfy_none(mock_element, _always_fail, _always_fail)

    def test_one_passes(self, mock_element: Any) -> None:
        """satisfy_none raises when a condition passes."""
        with pytest.raises(AssertionError, match="to_satisfy_none"):
            satisfy_none(mock_element, _always_pass, _always_fail)

    def test_all_pass(self, mock_element: Any) -> None:
        """satisfy_none raises when all conditions pass."""
        with pytest.raises(AssertionError, match="to_satisfy_none"):
            satisfy_none(mock_element, _always_pass, _always_pass)

    def test_empty_conditions(self, mock_element: Any) -> None:
        """satisfy_none with no conditions passes vacuously."""
        satisfy_none(mock_element)


class TestAssertionMixinIntegration:
    def test_to_satisfy_all_on_expect(self, mock_element: Any) -> None:
        """expect(el).to_satisfy_all(cond1, cond2) passes."""
        expect(mock_element).to_satisfy_all(_is_visible, _is_enabled)

    def test_to_satisfy_all_fails(self, mock_element: Any) -> None:
        """expect(el).to_satisfy_all raises when a condition fails."""
        with pytest.raises(AssertionError, match="to_satisfy_all"):
            expect(mock_element).to_satisfy_all(_is_visible, _is_selected)

    def test_to_satisfy_any_on_expect(self, mock_element: Any) -> None:
        """expect(el).to_satisfy_any(cond1, cond2) passes if one passes."""
        expect(mock_element).to_satisfy_any(_is_selected, _is_visible)

    def test_to_satisfy_any_fails(self, mock_element: Any) -> None:
        """expect(el).to_satisfy_any raises when all fail."""
        with pytest.raises(AssertionError, match="to_satisfy_any"):
            expect(mock_element).to_satisfy_any(_always_fail, _always_fail)

    def test_to_satisfy_none_on_expect(self, mock_element: Any) -> None:
        """expect(el).to_satisfy_none(cond) passes when cond fails."""
        expect(mock_element).to_satisfy_none(_always_fail)

    def test_to_satisfy_none_fails(self, mock_element: Any) -> None:
        """expect(el).to_satisfy_none raises when cond passes."""
        with pytest.raises(AssertionError, match="to_satisfy_none"):
            expect(mock_element).to_satisfy_none(_always_pass)
