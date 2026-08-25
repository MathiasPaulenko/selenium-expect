"""Custom matcher registry for selenium-expect.

Allows users to register custom assertion methods that integrate with
the retry loop and negation via ``__getattr__`` on ``AssertionMixin``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, ClassVar


class CustomMatcherRegistry:
    """Registry of user-defined custom matchers."""

    _matchers: ClassVar[dict[str, Callable[..., tuple[bool, Any]]]] = {}

    @classmethod
    def register(cls, name: str, matcher_fn: Callable[..., tuple[bool, Any]]) -> None:
        """Register a custom matcher function under *name*."""
        cls._matchers[name] = matcher_fn

    @classmethod
    def get(cls, name: str) -> Callable[..., tuple[bool, Any]] | None:
        """Return the matcher registered under *name*, or ``None``."""
        return cls._matchers.get(name)

    @classmethod
    def names(cls) -> list[str]:
        """Return all registered matcher names."""
        return list(cls._matchers)

    @classmethod
    def reset(cls) -> None:
        """Clear all registered matchers (for testing)."""
        cls._matchers.clear()


_MatcherFn = Callable[..., tuple[bool, Any]]


def extend(name: str) -> Callable[[_MatcherFn], _MatcherFn]:
    """Decorator to register a custom matcher under *name*.

    Usage::

        @extend("to_be_in_viewport")
        def check_in_viewport(element: Any) -> tuple[bool, Any]:
            ...
            return (passed, actual_value)

    The matcher function receives the assertion's ``_target`` as its
    first argument and must return a ``(bool, Any)`` tuple where the
    bool indicates pass/fail and the Any is the actual value for
    error reporting.
    """

    def decorator(fn: Callable[..., tuple[bool, Any]]) -> Callable[..., tuple[bool, Any]]:
        CustomMatcherRegistry.register(name, fn)
        return fn

    return decorator
