"""Unit tests for selenium_expect._errors."""

from __future__ import annotations

from selenium_expect._errors import AssertionFormatter


class TestAssertionFormatter:
    def test_basic_error_message(self) -> None:
        """format_error produces 'Expected {entity} {condition}, but got {actual}'."""
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to be visible",
            expected=True,
            actual=False,
            elapsed_ms=5000,
            poll_count=10,
            polling_interval=0.5,
        )
        first_line = msg.splitlines()[0]
        assert first_line == "Expected element to be visible, but got False"

    def test_error_with_expected_and_actual(self) -> None:
        """message includes 'Expected: X' and 'Actual: Y' lines."""
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to have text",
            expected="Hello",
            actual="World",
            elapsed_ms=1000,
            poll_count=2,
            polling_interval=0.5,
        )
        lines = msg.splitlines()
        assert "  Expected: Hello" in lines
        assert "  Actual:   World" in lines

    def test_error_with_element_html(self) -> None:
        """message includes 'Element: <truncated html>' when provided."""
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to be visible",
            expected=True,
            actual=False,
            elapsed_ms=1000,
            poll_count=2,
            polling_interval=0.5,
            element_html='<div id="test">Hello</div>',
        )
        lines = msg.splitlines()
        element_line = [line for line in lines if line.startswith("  Element:")]
        assert len(element_line) == 1
        assert '<div id="test">Hello</div>' in element_line[0]

    def test_error_with_wait_info(self) -> None:
        """message includes 'Waited: Xms (N polls at Ys interval)'."""
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to be visible",
            expected=True,
            actual=False,
            elapsed_ms=5000,
            poll_count=10,
            polling_interval=0.5,
        )
        lines = msg.splitlines()
        wait_line = [line for line in lines if line.startswith("  Waited:")]
        assert len(wait_line) == 1
        assert "5000ms" in wait_line[0]
        assert "10 polls" in wait_line[0]
        assert "0.5s interval" in wait_line[0]

    def test_error_with_custom_message(self) -> None:
        """message includes 'Message: {custom}' when provided."""
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to be visible",
            expected=True,
            actual=False,
            elapsed_ms=1000,
            poll_count=2,
            polling_interval=0.5,
            message="Custom error context",
        )
        lines = msg.splitlines()
        message_line = [line for line in lines if line.startswith("  Message:")]
        assert len(message_line) == 1
        assert "Custom error context" in message_line[0]

    def test_error_with_timeline(self) -> None:
        """message includes last 5 poll results when timeline provided."""
        timeline = [
            {"poll": 1, "passed": False, "actual": False},
            {"poll": 2, "passed": False, "actual": False},
            {"poll": 3, "passed": False, "actual": False},
        ]
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to be visible",
            expected=True,
            actual=False,
            elapsed_ms=1500,
            poll_count=3,
            polling_interval=0.5,
            timeline=timeline,
        )
        lines = msg.splitlines()
        timeline_line = [line for line in lines if line.startswith("  Timeline:")]
        assert len(timeline_line) == 1
        assert "poll 1: False" in timeline_line[0]
        assert "poll 2: False" in timeline_line[0]
        assert "poll 3: False" in timeline_line[0]

    def test_truncates_long_element_html(self) -> None:
        """element_html > 200 chars is truncated with '...'."""
        long_html = "<div>" + "x" * 250 + "</div>"
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to be visible",
            expected=True,
            actual=False,
            elapsed_ms=1000,
            poll_count=2,
            polling_interval=0.5,
            element_html=long_html,
        )
        lines = msg.splitlines()
        element_line = [line for line in lines if line.startswith("  Element:")]
        assert len(element_line) == 1
        assert element_line[0].endswith("...")
        # The element line should not contain the full 250+ char html
        assert len(element_line[0]) < len(long_html) + 20

    def test_handles_none_values(self) -> None:
        """expected=None or actual=None handled gracefully."""
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to have attribute",
            expected=None,
            actual=None,
            elapsed_ms=1000,
            poll_count=2,
            polling_interval=0.5,
        )
        lines = msg.splitlines()
        assert "  Expected: None" in lines
        assert "  Actual:   None" in lines
        assert "but got None" in lines[0]

    def test_timeline_truncated_to_last_5(self) -> None:
        """timeline with more than 5 entries only shows last 5."""
        timeline = [{"poll": i, "passed": False, "actual": f"val{i}"} for i in range(1, 11)]
        msg = AssertionFormatter.format_error(
            entity="element",
            condition="to be visible",
            expected=True,
            actual=False,
            elapsed_ms=5000,
            poll_count=10,
            polling_interval=0.5,
            timeline=timeline,
        )
        lines = msg.splitlines()
        timeline_line = [line for line in lines if line.startswith("  Timeline:")]
        assert len(timeline_line) == 1
        # Should contain poll 6 through 10 (last 5)
        assert "poll 6: val6" in timeline_line[0]
        assert "poll 10: val10" in timeline_line[0]
        # Should not contain poll 1-5
        assert "poll 1: val1" not in timeline_line[0]
        assert "poll 5: val5" not in timeline_line[0]
