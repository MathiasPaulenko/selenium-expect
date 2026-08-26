"""Unit tests for selenium_expect._matcher.CustomMatcherRegistry and extend()."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect import expect, extend, merge_expects
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


class TestMergeExpects:
    def test_merge_from_module(self) -> None:
        """merge_expects registers matchers from a module object."""
        import types

        mod = types.ModuleType("test_matchers_mod")

        @extend("to_be_merged_1")
        def matcher_1(target: Any) -> tuple[bool, Any]:
            return (True, "ok")

        mod.to_be_merged_1 = matcher_1

        @extend("to_be_merged_2")
        def matcher_2(target: Any) -> tuple[bool, Any]:
            return (False, "fail")

        mod.to_be_merged_2 = matcher_2

        CustomMatcherRegistry.reset()
        added = merge_expects(mod)

        assert "to_be_merged_1" in added
        assert "to_be_merged_2" in added
        assert CustomMatcherRegistry.get("to_be_merged_1") is matcher_1
        assert CustomMatcherRegistry.get("to_be_merged_2") is matcher_2

    def test_merge_skips_already_registered(self) -> None:
        """merge_expects does not re-register already present matchers."""
        import types

        @extend("to_be_merged_existing")
        def matcher_existing(target: Any) -> tuple[bool, Any]:
            return (True, "ok")

        mod = types.ModuleType("test_matchers_mod_2")
        mod.to_be_merged_existing = matcher_existing

        added = merge_expects(mod)
        assert added == []

    def test_merge_multiple_modules(self) -> None:
        """merge_expects combines matchers from multiple modules."""
        import types

        mod_a = types.ModuleType("mod_a")
        mod_b = types.ModuleType("mod_b")

        @extend("to_be_from_a")
        def matcher_a(target: Any) -> tuple[bool, Any]:
            return (True, "a")

        @extend("to_be_from_b")
        def matcher_b(target: Any) -> tuple[bool, Any]:
            return (True, "b")

        mod_a.to_be_from_a = matcher_a
        mod_b.to_be_from_b = matcher_b

        CustomMatcherRegistry.reset()
        added = merge_expects(mod_a, mod_b)

        assert "to_be_from_a" in added
        assert "to_be_from_b" in added

    def test_merge_empty_modules(self) -> None:
        """merge_expects with no matchers returns empty list."""
        import types

        mod = types.ModuleType("empty_mod")
        CustomMatcherRegistry.reset()
        added = merge_expects(mod)
        assert added == []

    def test_merge_integration_with_expect(self, mock_element: Any) -> None:
        """merge_expects matchers work with expect()."""
        import types

        mod = types.ModuleType("integration_mod")

        @extend("to_be_custom_merged")
        def custom_check(element: Any) -> tuple[bool, Any]:
            return (element.is_displayed(), True)

        mod.to_be_custom_merged = custom_check

        CustomMatcherRegistry.reset()
        merge_expects(mod)

        expect(mock_element).to_be_custom_merged()

    def test_merge_no_modules(self) -> None:
        """merge_expects with no args returns empty list."""
        CustomMatcherRegistry.reset()
        assert merge_expects() == []
