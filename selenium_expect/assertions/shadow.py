"""ExpectShadow — assertions for ShadowRoot elements."""

from __future__ import annotations

from typing import Any

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.shadowroot import ShadowRoot

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions import register
from selenium_expect.assertions._base import AssertionMixin


class ExpectShadow(AssertionMixin):
    """Assertions for ShadowRoot elements."""

    def __init__(
        self,
        target: ShadowRoot,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    def to_have_element(
        self,
        by: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert shadow_root.find_element(by, value) doesn't raise."""
        shadow = self._target

        def condition() -> tuple[bool, Any]:
            try:
                el = shadow.find_element(by, value)
                return (True, el)
            except NoSuchElementException:
                return (False, "not found")

        self._run_assertion(
            condition=condition,
            condition_name=f"to have element ({by}={value!r})",
            expected="present",
            entity="shadow",
            timeout=timeout,
            polling=polling,
        )

    def to_have_element_count(
        self,
        by: str,
        value: str,
        count: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(shadow_root.find_elements(by, value)) == count."""
        shadow = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(shadow.find_elements(by, value))
            return (actual == count, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have element count {count} ({by}={value!r})",
            expected=count,
            entity="shadow",
            timeout=timeout,
            polling=polling,
        )

    def to_have_element_text(
        self,
        by: str,
        value: str,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert shadow_root.find_element(by, value).text == text."""
        shadow = self._target

        def condition() -> tuple[bool, Any]:
            try:
                el = shadow.find_element(by, value)
                actual = el.text
                return (actual == text, actual)
            except NoSuchElementException:
                return (False, "not found")

        self._run_assertion(
            condition=condition,
            condition_name=f"to have element text {text!r} ({by}={value!r})",
            expected=text,
            entity="shadow",
            timeout=timeout,
            polling=polling,
        )

    def to_have_element_attribute(
        self,
        by: str,
        value: str,
        attr: str,
        attr_value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert shadow_root.find_element(by, value).get_attribute(attr) == attr_value."""
        shadow = self._target

        def condition() -> tuple[bool, Any]:
            try:
                el = shadow.find_element(by, value)
                actual = el.get_attribute(attr)
                return (actual == attr_value, actual)
            except NoSuchElementException:
                return (False, "not found")

        self._run_assertion(
            condition=condition,
            condition_name=f"to have element attribute {attr!r}={attr_value!r} ({by}={value!r})",
            expected=attr_value,
            entity="shadow",
            timeout=timeout,
            polling=polling,
        )

    def to_have_element_visible(
        self,
        by: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert shadow_root.find_element(by, value).is_displayed() == True."""
        shadow = self._target

        def condition() -> tuple[bool, Any]:
            try:
                el = shadow.find_element(by, value)
                actual = el.is_displayed()
                return (actual is True, actual)
            except NoSuchElementException:
                return (False, "not found")

        self._run_assertion(
            condition=condition,
            condition_name=f"to have element visible ({by}={value!r})",
            expected=True,
            entity="shadow",
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        return "ShadowRoot"

    def _get_element_html(self) -> str | None:
        return None


register("ShadowRoot", ExpectShadow)
