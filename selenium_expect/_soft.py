"""Soft assertion collector for selenium-expect.

Accumulates assertion failures when ``soft_mode=True`` instead of raising
immediately. ``assert_all()`` raises a combined ``AssertionError`` if any
failures were collected.

The failure list is isolated per thread/async context via ``ContextVar``,
so parallel tests do not leak failures into each other.
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import ClassVar


class SoftAssertionCollector:
    """Collects soft assertion failures for deferred raising.

    Failures are stored per execution context (``ContextVar``): each
    thread and each async task has its own list.
    """

    _failures: ClassVar[ContextVar[list[str] | None]] = ContextVar(
        "soft_assertion_failures", default=None
    )

    @classmethod
    def _current(cls) -> list[str]:
        """Return this context's failure list, creating it on first use."""
        failures = cls._failures.get()
        if failures is None:
            failures = []
            cls._failures.set(failures)
        return failures

    @classmethod
    def add_failure(cls, message: str) -> None:
        """Record a soft assertion failure."""
        cls._current().append(message)

    @classmethod
    def get_failures(cls) -> list[str]:
        """Return all collected failures in this context."""
        return list(cls._current())

    @classmethod
    def reset(cls) -> None:
        """Clear all collected failures in this context."""
        cls._failures.set([])

    @classmethod
    def assert_all(cls) -> None:
        """Raise ``AssertionError`` if any failures were collected, then reset."""
        failures = cls._current()
        if not failures:
            return
        messages = list(failures)
        cls.reset()
        combined = "\n---\n".join(messages)
        raise AssertionError(f"Soft assertion failures ({len(messages)}):\n{combined}")


def assert_all() -> None:
    """Raise ``AssertionError`` if any soft failures were collected, then reset.

    Convenience wrapper around ``SoftAssertionCollector.assert_all()``.
    """
    SoftAssertionCollector.assert_all()
