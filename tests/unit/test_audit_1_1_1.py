"""Regression tests for bugs found in the 1.1.1 audit cycle.

Covers:
1. to_be_absent / to_be_stale false positives on non-stale driver errors
2. to_have_frame_text popping frame context when switch_to.frame fails
3. SoftAssertionCollector context leaks between asyncio tasks
4. expect(driver, locator=...) accepting malformed locator values
5. Misleading fixed-interval message when a backoff schedule is used
6. Screenshot dir failures masking the real AssertionError
7. expect.configure(soft=True) dropping soft mode for .poll()
8. extend() crashing on callables without __dict__ (builtins)
"""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import MagicMock, PropertyMock

import pytest
from selenium.common.exceptions import NoSuchFrameException, WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from selenium_expect import expect
from selenium_expect._config import set_screenshot_on_failure
from selenium_expect._matcher import CustomMatcherRegistry, extend
from selenium_expect._poll import PollAssertion
from selenium_expect._soft import SoftAssertionCollector, assert_all


class TestAbsentStaleNoFalsePositive:
    """to_be_absent / to_be_stale must not pass on unexpected driver errors."""

    def _element_raising(self, exc: Exception) -> Any:
        el = MagicMock(spec=WebElement)
        type(el).tag_name = PropertyMock(side_effect=exc)
        return el

    def test_to_be_absent_propagates_driver_error(self) -> None:
        el = self._element_raising(WebDriverException("browser crashed"))
        with pytest.raises(WebDriverException):
            expect(el).to_be_absent()

    def test_to_be_stale_propagates_driver_error(self) -> None:
        el = self._element_raising(WebDriverException("browser crashed"))
        with pytest.raises(WebDriverException):
            expect(el).to_be_stale()

    def test_to_be_absent_still_passes_on_stale(self, mock_element_stale: Any) -> None:
        expect(mock_element_stale).to_be_absent()

    def test_to_be_stale_still_passes_on_stale(self, mock_element_stale: Any) -> None:
        expect(mock_element_stale).to_be_stale()


class TestFrameTextContextIntegrity:
    """to_have_frame_text must not leave the frame context when switch fails."""

    def test_parent_frame_not_called_when_switch_fails(self) -> None:
        driver = MagicMock(spec=WebDriver)
        driver.switch_to.frame.side_effect = NoSuchFrameException("no frame")
        parent_frame = MagicMock()
        driver.switch_to.parent_frame = parent_frame

        with pytest.raises(AssertionError):
            expect(driver).to_have_frame_text("missing", "hello", timeout=0.1, polling=0.05)

        assert parent_frame.call_count == 0

    def test_parent_frame_called_after_successful_switch(self) -> None:
        driver = MagicMock(spec=WebDriver)
        driver.page_source = "<html>hello</html>"
        parent_frame = MagicMock()
        driver.switch_to.parent_frame = parent_frame

        expect(driver).to_have_frame_text("f", "hello", timeout=0.1)

        assert parent_frame.call_count == 1


class TestSoftCollectorContextIsolation:
    """Async child tasks must not share the parent's failure list."""

    def test_child_failures_do_not_leak_to_parent(self) -> None:
        async def main() -> None:
            SoftAssertionCollector.reset()
            SoftAssertionCollector.add_failure("parent")

            async def child() -> None:
                SoftAssertionCollector.add_failure("child")

            await asyncio.create_task(child())
            assert SoftAssertionCollector.get_failures() == ["parent"]

        asyncio.run(main())

    def test_parent_failures_visible_as_snapshot_in_child(self) -> None:
        async def main() -> None:
            SoftAssertionCollector.reset()
            SoftAssertionCollector.add_failure("parent")
            seen: list[str] = []

            async def child() -> None:
                # Child inherits a snapshot; adding locally is isolated.
                SoftAssertionCollector.add_failure("child")
                seen.extend(SoftAssertionCollector.get_failures())

            await asyncio.create_task(child())
            assert seen == ["parent", "child"]
            assert SoftAssertionCollector.get_failures() == ["parent"]

        asyncio.run(main())


class TestLocatorValidation:
    """expect(driver, locator=...) rejects malformed locator values."""

    def test_locator_string_rejected(self, mock_driver: Any) -> None:
        with pytest.raises(TypeError, match="locator"):
            expect(mock_driver, locator="ab")  # type: ignore[arg-type]

    def test_locator_wrong_arity_rejected(self, mock_driver: Any) -> None:
        with pytest.raises(TypeError, match="locator"):
            expect(mock_driver, locator=("id",))  # type: ignore[arg-type]

    def test_locator_non_sequence_rejected(self, mock_driver: Any) -> None:
        with pytest.raises(TypeError, match="locator"):
            expect(mock_driver, locator=123)  # type: ignore[arg-type]

    def test_non_str_by_rejected(self, mock_driver: Any) -> None:
        with pytest.raises(TypeError, match="must be str"):
            expect(mock_driver, by=123, value="foo")  # type: ignore[arg-type]

    def test_non_str_value_rejected(self, mock_driver: Any) -> None:
        with pytest.raises(TypeError, match="must be str"):
            expect(mock_driver, by="id", value=123)  # type: ignore[arg-type]

    def test_valid_locator_still_works(self, mock_driver: Any) -> None:
        from selenium_expect._locator import LocatorExpect

        result = expect(mock_driver, locator=("id", "foo"))
        assert isinstance(result, LocatorExpect)


class TestBackoffScheduleErrorMessage:
    """Error messages must describe the real schedule, not a phantom 0.5s."""

    def test_poll_message_shows_schedule(self) -> None:
        pa = PollAssertion(lambda: "nope", timeout=0.2, polling=[0.05, 0.1])
        with pytest.raises(AssertionError) as exc_info:
            pa.to_equal("yes")
        assert "backoff schedule [0.05, 0.1]" in str(exc_info.value)

    def test_element_message_shows_schedule(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError) as exc_info:
            expect(mock_element).to_have_text("nope", timeout=0.2, polling=[0.05, 0.1])
        assert "backoff schedule" in str(exc_info.value)

    def test_fixed_interval_message_unchanged(self, mock_element: Any) -> None:
        with pytest.raises(AssertionError) as exc_info:
            expect(mock_element).to_have_text("nope", timeout=0.2, polling=0.05)
        assert "at 0.05s interval" in str(exc_info.value)


class TestScreenshotFailureDoesNotMaskAssertion:
    """A broken screenshot path must not hide the real assertion failure."""

    def test_unwritable_screenshot_path_still_raises_assertion(
        self, mock_element_hidden: Any, tmp_path: Any
    ) -> None:
        blocker = tmp_path / "blocker"
        blocker.write_text("x")  # path exists as a file, not a directory

        set_screenshot_on_failure(True, str(blocker))
        with pytest.raises(AssertionError, match="to be visible"):
            expect(mock_element_hidden).to_be_visible(timeout=0.1, polling=0.05)


class TestPollSoftMode:
    """poll() must honor soft mode like every other assertion."""

    def teardown_method(self) -> None:
        SoftAssertionCollector.reset()

    def test_poll_soft_kwarg_collects(self) -> None:
        PollAssertion(lambda: "nope", timeout=0.1, polling=0.05, soft=True).to_equal("yes")
        assert len(SoftAssertionCollector.get_failures()) == 1
        with pytest.raises(AssertionError):
            assert_all()

    def test_expect_poll_soft_kwarg_collects(self) -> None:
        expect.poll(lambda: "nope", timeout=0.1, polling=0.05, soft=True).to_equal("yes")
        assert len(SoftAssertionCollector.get_failures()) == 1
        with pytest.raises(AssertionError):
            assert_all()

    def test_configure_soft_applies_to_poll(self) -> None:
        fast = expect.configure(soft=True, timeout=0.1, polling=0.05)
        fast.poll(lambda: "nope").to_equal("yes")
        assert len(SoftAssertionCollector.get_failures()) == 1
        with pytest.raises(AssertionError):
            assert_all()

    def test_poll_without_soft_still_raises(self) -> None:
        with pytest.raises(AssertionError):
            PollAssertion(lambda: "nope", timeout=0.1, polling=0.05).to_equal("yes")


class TestExtendOnBuiltin:
    """extend() must not crash on callables that reject attribute assignment."""

    def teardown_method(self) -> None:
        CustomMatcherRegistry.reset()

    def test_extend_builtin_function(self) -> None:
        matcher = extend("to_be_builtin")(len)
        assert matcher is len
        assert CustomMatcherRegistry.get("to_be_builtin") is len
