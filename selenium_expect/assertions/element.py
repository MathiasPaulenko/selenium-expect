"""ExpectElement — assertions for WebElement state, text, and more."""

from __future__ import annotations

import re
from typing import Any

from selenium.webdriver.remote.webelement import WebElement

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions import register
from selenium_expect.assertions._base import AssertionMixin


class ExpectElement(AssertionMixin):
    """Assertions for WebElement state, text, attributes, CSS, identity, position."""

    def __init__(
        self,
        target: WebElement,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    # --- State ---

    def to_be_visible(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_displayed() == True."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            return (el.is_displayed(), el.is_displayed())

        self._run_assertion(
            condition=condition,
            condition_name="to be visible",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_hidden(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_displayed() == False."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            displayed = el.is_displayed()
            return (not displayed, displayed)

        self._run_assertion(
            condition=condition,
            condition_name="to be hidden",
            expected=False,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_enabled(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_enabled() == True."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            return (el.is_enabled(), el.is_enabled())

        self._run_assertion(
            condition=condition,
            condition_name="to be enabled",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_disabled(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_enabled() == False."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            enabled = el.is_enabled()
            return (not enabled, enabled)

        self._run_assertion(
            condition=condition,
            condition_name="to be disabled",
            expected=False,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_checked(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_selected() == True (checkbox/radio)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            return (el.is_selected(), el.is_selected())

        self._run_assertion(
            condition=condition,
            condition_name="to be checked",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_selected(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_selected() == True (option/checkbox/radio)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            return (el.is_selected(), el.is_selected())

        self._run_assertion(
            condition=condition,
            condition_name="to be selected",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_present(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element exists in DOM (element.tag_name doesn't raise)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            try:
                tag = el.tag_name
                return (True, tag)
            except Exception as exc:
                return (False, str(exc))

        self._run_assertion(
            condition=condition,
            condition_name="to be present",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_absent(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element doesn't exist (raises StaleElementReferenceException
        or NoSuchElementException)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            try:
                el.tag_name  # noqa: B018
                return (False, "present")
            except Exception:
                return (True, "absent")

        self._run_assertion(
            condition=condition,
            condition_name="to be absent",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_clickable(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_displayed() and element.is_enabled()."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            displayed = el.is_displayed()
            enabled = el.is_enabled()
            clickable = displayed and enabled
            return (clickable, {"displayed": displayed, "enabled": enabled})

        self._run_assertion(
            condition=condition,
            condition_name="to be clickable",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_stale(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element is stale (any access raises StaleElementReferenceException)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            try:
                el.tag_name  # noqa: B018
                return (False, "not stale")
            except Exception:
                return (True, "stale")

        self._run_assertion(
            condition=condition,
            condition_name="to be stale",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_unselected(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_selected() == False (semantic alias for not_.to_be_selected())."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            selected = el.is_selected()
            return (not selected, selected)

        self._run_assertion(
            condition=condition,
            condition_name="to be unselected",
            expected=False,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_unchecked(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_selected() == False (semantic alias for not_.to_be_checked())."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            selected = el.is_selected()
            return (not selected, selected)

        self._run_assertion(
            condition=condition,
            condition_name="to be unchecked",
            expected=False,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_focused(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element is the active element (driver.switch_to.active_element == element)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            driver = getattr(el, "parent", None)
            if driver is None:
                return (False, "no driver")
            active = driver.switch_to.active_element
            return (active.id == el.id, active)

        self._run_assertion(
            condition=condition,
            condition_name="to be focused",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_editable(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element is editable (input/textarea, not readonly, not disabled)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            tag = el.tag_name
            if tag not in ("input", "textarea"):
                return (False, f"tag={tag!r}")
            if not el.is_enabled():
                return (False, "disabled")
            readonly = el.get_attribute("readonly")
            if readonly is not None:
                return (False, "readonly")
            return (True, "editable")

        self._run_assertion(
            condition=condition,
            condition_name="to be editable",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_readonly(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element is readonly (get_attribute('readonly') is not None)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("readonly")
            return (actual is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to be readonly",
            expected="not None",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_empty(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text.strip() == '' (no visible text)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return ((actual or "").strip() == "", actual)

        self._run_assertion(
            condition=condition,
            condition_name="to be empty",
            expected="",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Text ---

    def to_have_text(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text == text."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (actual == text, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text {text!r}",
            expected=text,
            entity=self._entity_description(),
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
        """Assert text in element.text."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (text in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text containing {text!r}",
            expected=text,
            entity=self._entity_description(),
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
        """Assert re.search(pattern, element.text)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (re.search(pattern, actual or "") is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text matching {pattern!r}",
            expected=pattern,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_empty(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text == ''."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (actual == "", actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have text empty",
            expected="",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_not_empty(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text != ''."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (bool(actual), actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have text not empty",
            expected="non-empty",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_starting_with(
        self,
        prefix: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text.startswith(prefix)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return ((actual or "").startswith(prefix), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text starting with {prefix!r}",
            expected=prefix,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_ending_with(
        self,
        suffix: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text.endswith(suffix)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return ((actual or "").endswith(suffix), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text ending with {suffix!r}",
            expected=suffix,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_in_list(
        self,
        *texts: str,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text is one of *texts."""
        if not texts:
            raise ValueError("At least one text must be provided")
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (actual in texts, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text in {list(texts)!r}",
            expected=list(texts),
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_value(
        self,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute('value') == value."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("value")
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have value {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_value_contains(
        self,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in element.get_attribute('value')."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("value")
            return (value in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have value containing {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_value_matches(
        self,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, element.get_attribute('value'))."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("value")
            return (re.search(pattern, actual or "") is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have value matching {pattern!r}",
            expected=pattern,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_value_in_list(
        self,
        values: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute('value') in values."""
        if not values:
            raise ValueError("values list must not be empty")
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("value")
            return (actual in values, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have value in {values!r}",
            expected=values,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Attributes ---

    def to_have_attribute(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) == value."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r}={value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_contains(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in element.get_attribute(name)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (value in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} containing {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_matches(
        self,
        name: str,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, element.get_attribute(name))."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (re.search(pattern, actual or "") is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} matching {pattern!r}",
            expected=pattern,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_empty(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) == '' or None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual is None or actual == "", actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} empty",
            expected="empty or None",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_present(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) is not None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} present",
            expected="present",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_absent(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) is None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual is None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} absent",
            expected="absent",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_in_list(
        self,
        name: str,
        values: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) in values."""
        if not values:
            raise ValueError("values list must not be empty")
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual in values, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} in {values!r}",
            expected=values,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_dom_attribute(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_dom_attribute(name) == value."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_dom_attribute(name)
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have DOM attribute {name!r}={value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_dom_attribute_contains(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in element.get_dom_attribute(name)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_dom_attribute(name)
            return (value in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have DOM attribute {name!r} containing {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_property(
        self,
        name: str,
        value: Any,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_property(name) == value."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_property(name)
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have property {name!r}={value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_property_contains(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in str(element.get_property(name))."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_property(name)
            if actual is None:
                return (False, actual)
            return (value in str(actual), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have property {name!r} containing {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- CSS properties ---

    def to_have_css_property(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.value_of_css_property(name) == value."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.value_of_css_property(name)
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have CSS {name!r}={value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_css_property_contains(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in element.value_of_css_property(name)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.value_of_css_property(name)
            return (value in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have CSS {name!r} containing {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_css_property_matches(
        self,
        name: str,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, element.value_of_css_property(name))."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.value_of_css_property(name)
            return (re.search(pattern, actual or "") is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have CSS {name!r} matching {pattern!r}",
            expected=pattern,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Identity / DOM ---

    def to_have_tag(
        self,
        tag: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.tag_name == tag."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.tag_name
            return (actual == tag, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have tag {tag!r}",
            expected=tag,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_id(
        self,
        id: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute('id') == id."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("id")
            return (actual == id, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have id {id!r}",
            expected=id,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_class(
        self,
        class_name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert class_name in element.get_attribute('class').split()."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("class")
            classes = (actual or "").split()
            return (class_name in classes, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have class {class_name!r}",
            expected=class_name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_class_contains(
        self,
        class_name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert class_name in element.get_attribute('class') (substring)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("class")
            return (class_name in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have class containing {class_name!r}",
            expected=class_name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_contain_class(
        self,
        class_name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert class_name in element.get_attribute('class').split() (alias of to_have_class)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("class")
            classes = (actual or "").split()
            return (class_name in classes, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to contain class {class_name!r}",
            expected=class_name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_class_matching(
        self,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert any class in element.get_attribute('class').split() matches pattern."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("class")
            classes = (actual or "").split()
            return (any(re.search(pattern, c) for c in classes), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have class matching {pattern!r}",
            expected=pattern,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_all_classes(
        self,
        *classes: str,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element has all specified classes."""
        if not classes:
            raise ValueError("At least one class must be provided")
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("class")
            elem_classes = set((actual or "").split())
            return (set(classes).issubset(elem_classes), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have all classes {list(classes)!r}",
            expected=list(classes),
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_class_in_list(
        self,
        *classes: str,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element has at least one of the specified classes."""
        if not classes:
            raise ValueError("At least one class must be provided")
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("class")
            elem_classes = set((actual or "").split())
            return (bool(elem_classes & set(classes)), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have class in {list(classes)!r}",
            expected=list(classes),
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Position / dimensions ---

    def to_have_location(
        self,
        x: int,
        y: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location == {'x': x, 'y': y}."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            loc = el.location
            actual = {"x": loc["x"], "y": loc["y"]}
            return (actual == {"x": x, "y": y}, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location ({x}, {y})",
            expected={"x": x, "y": y},
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_location_x(
        self,
        x: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location['x'] == x."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.location["x"]
            return (actual == x, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location x={x}",
            expected=x,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_location_y(
        self,
        y: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location['y'] == y."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.location["y"]
            return (actual == y, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location y={y}",
            expected=y,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_size(
        self,
        width: int,
        height: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.size == {'width': width, 'height': height}."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            sz = el.size
            actual = {"width": sz["width"], "height": sz["height"]}
            return (actual == {"width": width, "height": height}, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have size ({width}x{height})",
            expected={"width": width, "height": height},
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_size_width(
        self,
        width: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.size['width'] == width."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.size["width"]
            return (actual == width, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have size width={width}",
            expected=width,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_size_height(
        self,
        height: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.size['height'] == height."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.size["height"]
            return (actual == height, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have size height={height}",
            expected=height,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.rect matches all four values."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            rect = el.rect
            actual = {
                "x": rect["x"],
                "y": rect["y"],
                "width": rect["width"],
                "height": rect["height"],
            }
            expected = {"x": x, "y": y, "width": width, "height": height}
            return (actual == expected, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have rect ({x}, {y}, {width}x{height})",
            expected={"x": x, "y": y, "width": width, "height": height},
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_location_greater_than(
        self,
        x: int | None = None,
        y: int | None = None,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location x and/or y are greater than given values."""
        if x is None and y is None:
            raise ValueError("At least one of x or y must be provided")
        el = self._target

        def condition() -> tuple[bool, Any]:
            loc = el.location
            actual = {"x": loc["x"], "y": loc["y"]}
            checks = []
            if x is not None:
                checks.append(loc["x"] > x)
            if y is not None:
                checks.append(loc["y"] > y)
            return (all(checks), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location > ({x}, {y})",
            expected=f"x>{x}, y>{y}",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_location_less_than(
        self,
        x: int | None = None,
        y: int | None = None,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location x and/or y are less than given values."""
        if x is None and y is None:
            raise ValueError("At least one of x or y must be provided")
        el = self._target

        def condition() -> tuple[bool, Any]:
            loc = el.location
            actual = {"x": loc["x"], "y": loc["y"]}
            checks = []
            if x is not None:
                checks.append(loc["x"] < x)
            if y is not None:
                checks.append(loc["y"] < y)
            return (all(checks), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location < ({x}, {y})",
            expected=f"x<{x}, y<{y}",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_size_greater_than(
        self,
        width: int | None = None,
        height: int | None = None,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.size width and/or height are greater than given values."""
        if width is None and height is None:
            raise ValueError("At least one of width or height must be provided")
        el = self._target

        def condition() -> tuple[bool, Any]:
            sz = el.size
            actual = {"width": sz["width"], "height": sz["height"]}
            checks = []
            if width is not None:
                checks.append(sz["width"] > width)
            if height is not None:
                checks.append(sz["height"] > height)
            return (all(checks), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have size > ({width}, {height})",
            expected=f"w>{width}, h>{height}",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_size_less_than(
        self,
        width: int | None = None,
        height: int | None = None,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.size width and/or height are less than given values."""
        if width is None and height is None:
            raise ValueError("At least one of width or height must be provided")
        el = self._target

        def condition() -> tuple[bool, Any]:
            sz = el.size
            actual = {"width": sz["width"], "height": sz["height"]}
            checks = []
            if width is not None:
                checks.append(sz["width"] < width)
            if height is not None:
                checks.append(sz["height"] < height)
            return (all(checks), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have size < ({width}, {height})",
            expected=f"w<{width}, h<{height}",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_location_once_scrolled_into_view(
        self,
        x: int,
        y: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location_once_scrolled_into_view == {'x': x, 'y': y}."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            loc = el.location_once_scrolled_into_view
            actual = {"x": loc["x"], "y": loc["y"]}
            return (actual == {"x": x, "y": y}, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location once scrolled into view ({x}, {y})",
            expected={"x": x, "y": y},
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Accessibility (Selenium 4+) ---

    def to_have_aria_role(
        self,
        role: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.aria_role == role."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.aria_role
            return (actual == role, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have aria role {role!r}",
            expected=role,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_aria_role_contains(
        self,
        role: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert role in element.aria_role."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.aria_role
            return (role in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have aria role containing {role!r}",
            expected=role,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_aria_role_in_list(
        self,
        *roles: str,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.aria_role is one of *roles."""
        if not roles:
            raise ValueError("At least one role must be provided")
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.aria_role
            return (actual in roles, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have aria role in {list(roles)!r}",
            expected=list(roles),
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_accessible_name(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.accessible_name == name."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.accessible_name
            return (actual == name, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have accessible name {name!r}",
            expected=name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_accessible_name_contains(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert name in element.accessible_name."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.accessible_name
            return (name in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have accessible name containing {name!r}",
            expected=name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Shadow DOM ---

    def to_have_js_property(
        self,
        name: str,
        value: Any,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element JS property == value via execute_script."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            driver = getattr(el, "parent", None)
            if driver is None:
                return (False, "no driver")
            actual = driver.execute_script("return arguments[0][arguments[1]];", el, name)
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have JS property {name!r}={value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_shadow_root(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.shadow_root is not None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.shadow_root
            return (actual is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have shadow root",
            expected="not None",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_shadow_root_absent(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.shadow_root is None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.shadow_root
            return (actual is None, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have shadow root absent",
            expected="None",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        el = self._target
        try:
            tag = el.tag_name
            elem_id = el.get_attribute("id")
            if elem_id:
                return f"<{tag} id={elem_id!r}>"
            return f"<{tag}>"
        except Exception:
            return repr(el)

    def _get_element_html(self) -> str | None:
        el = self._target
        try:
            html = el.get_attribute("outerHTML")
            return html if html else None
        except Exception:
            return None


register("WebElement", ExpectElement)
