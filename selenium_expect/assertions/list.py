"""ExpectList — assertions for lists of WebElements."""

from __future__ import annotations

import re
from typing import Any, Self

from selenium.webdriver.remote.webelement import WebElement

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions import register
from selenium_expect.assertions._base import AssertionMixin


class ExpectList(AssertionMixin):
    """Assertions for lists of WebElements."""

    def __init__(
        self,
        target: list[WebElement],
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    # --- Count ---

    def to_have_count(
        self,
        count: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert len(elements) == count."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(elements)
            return (actual == count, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have count {count}",
            expected=count,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_count_greater_than(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert len(elements) > n."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(elements)
            return (actual > n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have count > {n}",
            expected=f">{n}",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_count_less_than(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert len(elements) < n."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(elements)
            return (actual < n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have count < {n}",
            expected=f"<{n}",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_count_greater_than_or_equal(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert len(elements) >= n."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(elements)
            return (actual >= n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have count >= {n}",
            expected=f">={n}",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_count_less_than_or_equal(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert len(elements) <= n."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(elements)
            return (actual <= n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have count <= {n}",
            expected=f"<={n}",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_be_empty(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert len(elements) == 0."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(elements)
            return (actual == 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to be empty",
            expected=0,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_be_not_empty(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert len(elements) > 0."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(elements)
            return (actual > 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to be not empty",
            expected=">0",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    # --- Text ---

    def to_have_texts(
        self,
        texts: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert [el.text for el in elements] == texts (exact, ordered)."""
        if not texts:
            raise ValueError("texts list must not be empty")
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            return (actual == texts, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have texts {texts!r}",
            expected=texts,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_texts_contains(
        self,
        texts: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert each text in texts is in corresponding element.text."""
        if not texts:
            raise ValueError("texts list must not be empty")
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            if len(actual) != len(texts):
                return (False, actual)
            return (all(t in (a or "") for a, t in zip(actual, texts, strict=False)), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have texts containing {texts!r}",
            expected=texts,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_texts_match(
        self,
        patterns: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert each element's text matches the corresponding regex pattern."""
        if not patterns:
            raise ValueError("patterns list must not be empty")
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            if len(actual) != len(patterns):
                return (False, actual)
            return (
                all(
                    re.search(p, a or "") is not None
                    for a, p in zip(actual, patterns, strict=False)
                ),
                actual,
            )

        self._run_assertion(
            condition=condition,
            condition_name=f"to have texts matching {patterns!r}",
            expected=patterns,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_text_at(
        self,
        index: int,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert elements[index].text == text."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            if index >= len(elements) or index < -len(elements):
                return (False, f"index {index} out of range")
            actual = elements[index].text
            return (actual == text, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text at [{index}]={text!r}",
            expected=text,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_any_text(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert any element has text == text."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            return (text in actual, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have any text {text!r}",
            expected=text,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_all_texts_contain(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert all elements contain text."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            return (all(text in (t or "") for t in actual) and len(actual) > 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have all texts containing {text!r}",
            expected=text,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_any_text_contain(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert any element contains text."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            return (any(text in (t or "") for t in actual), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have any text containing {text!r}",
            expected=text,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_none_text_contain(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert no element contains text."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            return (not any(text in (t or "") for t in actual) and len(actual) > 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have no text containing {text!r}",
            expected=f"none containing {text!r}",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_exact_texts(
        self,
        *texts: str,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert [el.text for el in elements] == list(texts) (exact, ordered, varargs)."""
        if not texts:
            raise ValueError("At least one text must be provided")
        elements = self._target
        expected = list(texts)

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            return (actual == expected, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have exact texts {expected!r}",
            expected=expected,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_texts_containing(
        self,
        *texts: str,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert each element.text contains the corresponding text (varargs)."""
        if not texts:
            raise ValueError("At least one text must be provided")
        elements = self._target
        expected = list(texts)

        def condition() -> tuple[bool, Any]:
            actual = [el.text for el in elements]
            if len(actual) != len(expected):
                return (False, actual)
            return (all(t in (a or "") for a, t in zip(actual, expected, strict=False)), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have texts containing {expected!r}",
            expected=expected,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_texts_in_any_order(
        self,
        *texts: str,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert element texts match texts in any order (varargs)."""
        if not texts:
            raise ValueError("At least one text must be provided")
        elements = self._target
        expected = sorted(texts)

        def condition() -> tuple[bool, Any]:
            actual = sorted(el.text for el in elements)
            return (actual == expected, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have texts in any order {list(texts)!r}",
            expected=list(texts),
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_first_text(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert elements[0].text == text."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            if not elements:
                return (False, "empty list")
            actual = elements[0].text
            return (actual == text, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have first text {text!r}",
            expected=text,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_last_text(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert elements[-1].text == text."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            if not elements:
                return (False, "empty list")
            actual = elements[-1].text
            return (actual == text, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have last text {text!r}",
            expected=text,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_nth_text_contains(
        self,
        index: int,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert text in elements[index].text."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            if index >= len(elements) or index < -len(elements):
                return (False, f"index {index} out of range")
            actual = elements[index].text
            return (text in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text at [{index}] containing {text!r}",
            expected=text,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    # --- Values ---

    def to_have_values(
        self,
        values: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert [el.get_attribute('value') for el in elements] == values."""
        if not values:
            raise ValueError("values list must not be empty")
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.get_attribute("value") for el in elements]
            return (actual == values, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have values {values!r}",
            expected=values,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_values_contains(
        self,
        values: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert each value is a substring of the corresponding element's value."""
        if not values:
            raise ValueError("values list must not be empty")
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.get_attribute("value") for el in elements]
            if len(actual) != len(values):
                return (False, actual)
            return (all(v in (a or "") for a, v in zip(actual, values, strict=False)), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have values containing {values!r}",
            expected=values,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_value_at(
        self,
        index: int,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert elements[index].get_attribute('value') == value."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            if index >= len(elements) or index < -len(elements):
                return (False, f"index {index} out of range")
            actual = elements[index].get_attribute("value")
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have value at [{index}]={value!r}",
            expected=value,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    # --- State (aggregate) ---

    def to_have_all_visible(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert all elements are visible."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.is_displayed() for el in elements]
            return (all(actual) and len(actual) > 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have all visible",
            expected="all visible",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_any_visible(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert at least one element is visible."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.is_displayed() for el in elements]
            return (any(actual), actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have any visible",
            expected="any visible",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_none_visible(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert no element is visible."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.is_displayed() for el in elements]
            return (not any(actual) and len(actual) > 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have none visible",
            expected="none visible",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_all_enabled(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert all elements are enabled."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.is_enabled() for el in elements]
            return (all(actual) and len(actual) > 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have all enabled",
            expected="all enabled",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_all_selected(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert all elements are selected."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.is_selected() for el in elements]
            return (all(actual) and len(actual) > 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have all selected",
            expected="all selected",
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    # --- Attributes ---

    def to_have_attribute_at(
        self,
        index: int,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert elements[index].get_attribute(name) == value."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            if index >= len(elements) or index < -len(elements):
                return (False, f"index {index} out of range")
            actual = elements[index].get_attribute(name)
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r}={value!r} at [{index}]",
            expected=value,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_all_attribute(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert all elements have attribute == value."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.get_attribute(name) for el in elements]
            return (all(a == value for a in actual) and len(actual) > 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have all attribute {name!r}={value!r}",
            expected=value,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    def to_have_any_attribute(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> Self:
        """Assert any element has attribute == value."""
        elements = self._target

        def condition() -> tuple[bool, Any]:
            actual = [el.get_attribute(name) for el in elements]
            return (any(a == value for a in actual), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have any attribute {name!r}={value!r}",
            expected=value,
            entity="list",
            timeout=timeout,
            polling=polling,
        )

        return self

    # --- Overrides ---

    def _entity_description(self) -> str:
        return f"list[{len(self._target)}]"

    def _get_element_html(self) -> str | None:
        return None


register("list", ExpectList)
