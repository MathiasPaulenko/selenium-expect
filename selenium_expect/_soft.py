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

    The context variable holds an immutable tuple, so a child task that
    inherits its parent's context gets a snapshot: failures added inside
    the child (or the parent) never leak into the other context.
    """

    _failures: ClassVar[ContextVar[tuple[str, ...]]] = ContextVar(
        "soft_assertion_failures", default=()
    )

    @classmethod
    def _current(cls) -> tuple[str, ...]:
        """Return this context's failures (immutable snapshot)."""
        return cls._failures.get()

    @classmethod
    def add_failure(cls, message: str) -> None:
        """Record a soft assertion failure in the current context."""
        cls._failures.set((*cls._failures.get(), message))

    @classmethod
    def get_failures(cls) -> list[str]:
        """Return all collected failures in this context."""
        return list(cls._failures.get())

    @classmethod
    def reset(cls) -> None:
        """Clear all collected failures in this context."""
        cls._failures.set(())

    @classmethod
    def assert_all(cls) -> None:
        """Raise ``AssertionError`` if any failures were collected, then reset."""
        failures = cls._failures.get()
        if not failures:
            return
        cls.reset()
        combined = "\n---\n".join(failures)
        raise AssertionError(f"Soft assertion failures ({len(failures)}):\n{combined}")


def assert_all() -> None:
    """Raise ``AssertionError`` if any soft failures were collected, then reset.

    Convenience wrapper around ``SoftAssertionCollector.assert_all()``.
    """
    SoftAssertionCollector.assert_all()
