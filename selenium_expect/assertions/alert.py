"""ExpectAlert — assertions for JavaScript alerts/confirms/prompts."""

from __future__ import annotations

import re
from typing import Any

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.alert import Alert

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions import register
from selenium_expect.assertions._base import AssertionMixin


class ExpectAlert(AssertionMixin):
    """Assertions for JavaScript alerts/confirms/prompts."""

    def __init__(
        self,
        target: Alert,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    def to_be_present(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert alert is present (accessing .text doesn't raise)."""
        alert = self._target

        def condition() -> tuple[bool, Any]:
            try:
                _ = alert.text
                return (True, "present")
            except NoAlertPresentException:
                return (False, "not present")

        self._run_assertion(
            condition=condition,
            condition_name="to be present",
            expected="present",
            entity="alert",
            timeout=timeout,
            polling=polling,
        )

    def to_have_text(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert alert.text == text."""
        alert = self._target

        def condition() -> tuple[bool, Any]:
            actual = alert.text
            return (actual == text, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text {text!r}",
            expected=text,
            entity="alert",
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_contains(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert text in alert.text."""
        alert = self._target

        def condition() -> tuple[bool, Any]:
            actual = alert.text
            return (text in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text containing {text!r}",
            expected=text,
            entity="alert",
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_matches(
        self,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, alert.text)."""
        alert = self._target

        def condition() -> tuple[bool, Any]:
            actual = alert.text
            return (re.search(pattern, actual or "") is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text matching {pattern!r}",
            expected=pattern,
            entity="alert",
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        return "Alert"

    def _get_element_html(self) -> str | None:
        return None


register("Alert", ExpectAlert)
