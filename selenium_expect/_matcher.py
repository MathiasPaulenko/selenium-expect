"""Custom matcher registry for selenium-expect.

Allows users to register custom assertion methods that integrate with
the retry loop and negation via ``__getattr__`` on ``AssertionMixin``.
"""

from __future__ import annotations

from collections.abc import Callable
from types import ModuleType
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

    @classmethod
    def merge_from(cls, *modules: ModuleType) -> list[str]:
        """Merge matchers from the given modules into this registry.

        Each module is expected to have used ``@extend`` to register
        matchers at import time. This method imports (if passed as a
        string) or processes each module and returns the names of
        newly registered matchers.
        """
        added: list[str] = []
        for mod in modules:
            for name in dir(mod):
                fn = getattr(mod, name, None)
                if callable(fn) and hasattr(fn, "_selenium_expect_matcher"):
                    matcher_name: str = fn._selenium_expect_matcher
                    if matcher_name not in cls._matchers:
                        cls._matchers[matcher_name] = fn
                        added.append(matcher_name)
        return added


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
        fn._selenium_expect_matcher = name  # type: ignore[attr-defined]
        return fn

    return decorator


def merge_expects(*modules: ModuleType | str) -> list[str]:
    """Combine custom matchers from multiple modules into the registry.

    Each module should have used ``@extend`` to register matchers.
    Pass modules as objects or importable strings.

    Usage::

        import my_matchers
        merge_expects(my_matchers)

        # or by import path:
        merge_expects("my_project.matchers")

    Returns the list of newly registered matcher names.
    """
    import importlib

    resolved: list[ModuleType] = []
    for mod in modules:
        if isinstance(mod, str):
            resolved.append(importlib.import_module(mod))
        else:
            resolved.append(mod)
    return CustomMatcherRegistry.merge_from(*resolved)
