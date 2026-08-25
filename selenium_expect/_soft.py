"""Soft assertion collector for selenium-expect.

Accumulates assertion failures when ``soft_mode=True`` instead of raising
immediately. ``assert_all()`` raises a combined ``AssertionError`` if any
failures were collected.
"""

from __future__ import annotations

from typing import ClassVar


class SoftAssertionCollector:
    """Collects soft assertion failures for deferred raising."""

    _failures: ClassVar[list[str]] = []

    @classmethod
    def add_failure(cls, message: str) -> None:
        """Record a soft assertion failure."""
        cls._failures.append(message)

    @classmethod
    def get_failures(cls) -> list[str]:
        """Return all collected failures."""
        return list(cls._failures)

    @classmethod
    def reset(cls) -> None:
        """Clear all collected failures."""
        cls._failures.clear()

    @classmethod
    def assert_all(cls) -> None:
        """Raise ``AssertionError`` if any failures were collected, then reset."""
        if not cls._failures:
            return
        messages = list(cls._failures)
        cls.reset()
        combined = "\n---\n".join(messages)
        raise AssertionError(f"Soft assertion failures ({len(messages)}):\n{combined}")


def assert_all() -> None:
    """Raise ``AssertionError`` if any soft failures were collected, then reset.

    Convenience wrapper around ``SoftAssertionCollector.assert_all()``.
    """
    SoftAssertionCollector.assert_all()
