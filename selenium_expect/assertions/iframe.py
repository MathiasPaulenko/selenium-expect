"""ExpectIframe — assertions for iframe/frame context."""

from __future__ import annotations

from typing import Any

from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions._base import AssertionMixin


class ExpectIframe(AssertionMixin):
    """Assertions for iframe/frame context.

    Not dispatched via ``expect()`` (which maps ``WebDriver`` to
    ``ExpectDriver``); instantiate directly with a driver.
    """

    def __init__(
        self,
        target: WebDriver,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    def to_have_frame_available(
        self,
        frame_id: str | int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.switch_to.frame(frame_id) doesn't raise."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            try:
                driver.switch_to.frame(frame_id)
                driver.switch_to.default_content()
                return (True, "available")
            except NoSuchFrameException:
                return (False, "not available")

        self._run_assertion(
            condition=condition,
            condition_name=f"to have frame {frame_id!r} available",
            expected="available",
            entity="iframe",
            timeout=timeout,
            polling=polling,
        )

    def to_have_frame_count(
        self,
        count: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(driver.find_elements(By.TAG_NAME, 'iframe')) == count."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(driver.find_elements(By.TAG_NAME, "iframe"))
            return (actual == count, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have frame count {count}",
            expected=count,
            entity="iframe",
            timeout=timeout,
            polling=polling,
        )

    def to_have_frame_count_greater_than(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert iframe count > n."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(driver.find_elements(By.TAG_NAME, "iframe"))
            return (actual > n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have frame count > {n}",
            expected=f">{n}",
            entity="iframe",
            timeout=timeout,
            polling=polling,
        )

    def to_have_frame_text(
        self,
        frame_id: str | int,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Switch to frame, assert driver.page_source contains text, switch back."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            try:
                driver.switch_to.frame(frame_id)
                source = driver.page_source
                return (text in (source or ""), len(source) if source else 0)
            except NoSuchFrameException:
                return (False, "frame not available")
            finally:
                driver.switch_to.default_content()

        self._run_assertion(
            condition=condition,
            condition_name=f"to have frame {frame_id!r} text containing {text!r}",
            expected=text,
            entity="iframe",
            timeout=timeout,
            polling=polling,
        )

    def to_be_in_frame(
        self,
        frame_id: str | int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver is currently in the given frame (switch_to.frame succeeds)."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            try:
                driver.switch_to.frame(frame_id)
                return (True, "in frame")
            except NoSuchFrameException:
                return (False, "not in frame")

        self._run_assertion(
            condition=condition,
            condition_name=f"to be in frame {frame_id!r}",
            expected="in frame",
            entity="iframe",
            timeout=timeout,
            polling=polling,
        )

    def to_be_in_default_content(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver is in default content (not in any frame)."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            try:
                driver.switch_to.default_content()
                return (True, "in default content")
            except Exception as exc:
                return (False, str(exc))

        self._run_assertion(
            condition=condition,
            condition_name="to be in default content",
            expected="in default content",
            entity="iframe",
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        return "iframe"

    def _get_element_html(self) -> str | None:
        return None
