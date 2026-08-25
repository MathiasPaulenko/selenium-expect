"""ExpectSelect — assertions for Select/dropdown elements."""

from __future__ import annotations

from typing import Any

from selenium.webdriver.support.ui import Select

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions import register
from selenium_expect.assertions._base import AssertionMixin


class ExpectSelect(AssertionMixin):
    """Assertions for Select/dropdown elements."""

    def __init__(
        self,
        target: Select,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    def to_have_value(
        self,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert select.first_selected_option.get_attribute('value') == value."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = select.first_selected_option.get_attribute("value")
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have value {value!r}",
            expected=value,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_first_selected_value(
        self,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert select.first_selected_option.get_attribute('value') == value (alias)."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = select.first_selected_option.get_attribute("value")
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have first selected value {value!r}",
            expected=value,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_selected_text(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert select.first_selected_option.text == text."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = select.first_selected_option.text
            return (actual == text, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have selected text {text!r}",
            expected=text,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_selected_values(
        self,
        values: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert [opt.get_attribute('value') for opt in all_selected_options] == values."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = [opt.get_attribute("value") for opt in select.all_selected_options]
            return (actual == values, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have selected values {values!r}",
            expected=values,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_selected_texts(
        self,
        texts: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert [opt.text for opt in all_selected_options] == texts."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = [opt.text for opt in select.all_selected_options]
            return (actual == texts, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have selected texts {texts!r}",
            expected=texts,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_selected_count(
        self,
        count: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(select.all_selected_options) == count."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(select.all_selected_options)
            return (actual == count, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have selected count {count}",
            expected=count,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_option_count(
        self,
        count: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(select.options) == count."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(select.options)
            return (actual == count, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have option count {count}",
            expected=count,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_option_count_greater_than(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(select.options) > n."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(select.options)
            return (actual > n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have option count > {n}",
            expected=f">{n}",
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_option_at_index(
        self,
        index: int,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert select.options[index].text == text."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            if index >= len(select.options):
                return (False, f"index {index} out of range")
            actual = select.options[index].text
            return (actual == text, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have option at [{index}]={text!r}",
            expected=text,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_option(
        self,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value exists in select options (by value attribute)."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = [opt.get_attribute("value") for opt in select.options]
            return (value in actual, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have option with value {value!r}",
            expected=value,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_have_option_text(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert text exists in select options (by visible text)."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = [opt.text for opt in select.options]
            return (text in actual, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have option with text {text!r}",
            expected=text,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_be_multiple(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert select.is_multiple == True."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = select.is_multiple
            return (actual is True, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to be multiple",
            expected=True,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    def to_be_single_select(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert select.is_multiple == False."""
        select = self._target

        def condition() -> tuple[bool, Any]:
            actual = select.is_multiple
            return (actual is False, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to be single select",
            expected=False,
            entity="select",
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        return "Select"

    def _get_element_html(self) -> str | None:
        return None


register("Select", ExpectSelect)
