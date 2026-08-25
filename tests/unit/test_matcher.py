"""Unit tests for selenium_expect._matcher.CustomMatcherRegistry and extend()."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect, extend
from selenium_expect._matcher import CustomMatcherRegistry


@pytest.fixture(autouse=True)
def _reset_matchers() -> Any:
    """Reset the matcher registry before and after each test."""
    CustomMatcherRegistry.reset()
    yield
    CustomMatcherRegistry.reset()


class TestCustomMatcherRegistry:
    def test_register_and_get(self) -> None:
        """register() stores a matcher, get() retrieves it."""

        def my_matcher(target: Any) -> tuple[bool, Any]:
            return (True, "ok")

        CustomMatcherRegistry.register("my_matcher", my_matcher)
        assert CustomMatcherRegistry.get("my_matcher") is my_matcher

    def test_get_unknown_returns_none(self) -> None:
        """get() returns None for unregistered names."""
        assert CustomMatcherRegistry.get("nonexistent") is None

    def test_names(self) -> None:
        """names() returns all registered matcher names."""
        CustomMatcherRegistry.register("matcher_a", lambda t: (True, None))
        CustomMatcherRegistry.register("matcher_b", lambda t: (True, None))
        names = CustomMatcherRegistry.names()
        assert "matcher_a" in names
        assert "matcher_b" in names

    def test_reset(self) -> None:
        """reset() clears all matchers."""
        CustomMatcherRegistry.register("my_matcher", lambda t: (True, None))
        CustomMatcherRegistry.reset()
        assert CustomMatcherRegistry.names() == []


class TestExtendDecorator:
    def test_extend_registers_matcher(self) -> None:
        """@extend('name') registers the function."""

        @extend("to_be_awesome")
        def check_awesome(target: Any) -> tuple[bool, Any]:
            return (True, "awesome")

        assert CustomMatcherRegistry.get("to_be_awesome") is check_awesome

    def test_extend_returns_function(self) -> None:
        """@extend returns the original function unchanged."""

        @extend("to_be_cool")
        def check_cool(target: Any) -> tuple[bool, Any]:
            return (True, "cool")

        assert callable(check_cool)


class TestCustomMatcherIntegration:
    def test_custom_matcher_passes(self, mock_element: Any) -> None:
        """expect(el).to_have_custom_attr('value') passes when matcher returns True."""

        @extend("to_have_custom_attr")
        def check_attr(element: Any, attr: str) -> tuple[bool, Any]:
            actual = element.get_attribute(attr)
            return (actual == "test_value", actual)

        # mock_element.get_attribute('value') returns 'test_value'
        expect(mock_element).to_have_custom_attr("value")

    def test_custom_matcher_fails(self, mock_element: Any) -> None:
        """expect(el).to_have_custom_attr('value') raises when matcher returns False."""

        @extend("to_have_custom_attr_fail")
        def check_attr(element: Any, attr: str) -> tuple[bool, Any]:
            return (False, "wrong")

        with pytest.raises(AssertionError, match="to_have_custom_attr_fail"):
            expect(mock_element).to_have_custom_attr_fail("value")

    def test_custom_matcher_negation(self, mock_element: Any) -> None:
        """expect(el).not_.to_have_custom_attr() negates the matcher result."""

        @extend("to_be_failing")
        def always_fail(element: Any) -> tuple[bool, Any]:
            return (False, "fail")

        # Negation: not False = True, so it passes
        expect(mock_element).not_.to_be_failing()

    def test_custom_matcher_negation_fails(self, mock_element: Any) -> None:
        """expect(el).not_.to_be_passing() raises when matcher passes."""

        @extend("to_be_passing")
        def always_pass(element: Any) -> tuple[bool, Any]:
            return (True, "pass")

        with pytest.raises(AssertionError, match="to_be_passing"):
            expect(mock_element).not_.to_be_passing()

    def test_custom_matcher_with_timeout(self, mock_element: Any) -> None:
        """Custom matcher accepts timeout kwarg."""

        @extend("to_have_quick_check")
        def quick_check(element: Any) -> tuple[bool, Any]:
            return (True, "ok")

        expect(mock_element).to_have_quick_check(timeout=1.0)

    def test_unknown_attribute_raises(self, mock_element: Any) -> None:
        """Accessing an unregistered matcher name raises AttributeError."""
        with pytest.raises(AttributeError, match="to_have_nonexistent"):
            expect(mock_element).to_have_nonexistent  # noqa: B018
