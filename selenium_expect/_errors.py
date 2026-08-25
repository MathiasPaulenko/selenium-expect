"""Assertion error message formatting for selenium-expect."""

from __future__ import annotations

from typing import Any


class AssertionFormatter:
    """Builds descriptive multi-line error messages."""

    @staticmethod
    def format_error(
        entity: str,
        condition: str,
        expected: Any,
        actual: Any,
        elapsed_ms: int,
        poll_count: int,
        polling_interval: float,
        message: str | None = None,
        element_html: str | None = None,
        timeline: list[dict[str, Any]] | None = None,
    ) -> str:
        """Format a descriptive AssertionError message.

        Output format:
            Expected {entity} {condition}, but got {actual}
              Expected: {expected}
              Actual:   {actual}
              Element:  {truncated_html}     # if element_html provided
              Waited:   {elapsed_ms}ms ({poll_count} polls at {polling_interval}s interval)
              Message:  {custom_message}     # if message provided
              Timeline: [poll N: actual, ...] # last 5 polls if timeline provided
        """
        lines: list[str] = [
            f"Expected {entity} {condition}, but got {actual}",
            f"  Expected: {expected}",
            f"  Actual:   {actual}",
        ]

        if element_html is not None:
            truncated = element_html if len(element_html) <= 200 else element_html[:200] + "..."
            lines.append(f"  Element:  {truncated}")

        lines.append(
            f"  Waited:   {elapsed_ms}ms ({poll_count} polls at {polling_interval}s interval)"
        )

        if message is not None:
            lines.append(f"  Message:  {message}")

        if timeline:
            recent = timeline[-5:]
            entries = ", ".join(f"poll {e['poll']}: {e['actual']}" for e in recent)
            lines.append(f"  Timeline: [{entries}]")

        return "\n".join(lines)
