"""Regression tests for bugs found during static review.

Each test class corresponds to a specific bug fix:

1. Vacuous truth in location/size comparison methods when all params are None
2. satisfy_all/any/none no longer accept unused timeout/polling params
3. None guarding in to_have_text_contains and to_have_text_matches
4. Index bounds checking for negative indices
5. to_have_text_not_empty None handling
6. Empty polling_intervals causing IndexError in retry loop
7. timeout=0 skipping first poll in retry loop
8. PollAssertion.to_contain breaking on falsy non-string values
9. PollAssertion not normalizing timeout (5000 → 5000s instead of 5s)
10. ExpectConfig rejecting empty polling_intervals
11. Per-assertion empty polling list validation
12. None guarding in list.py to_have_texts_contains / to_have_texts_containing
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from selenium.webdriver.remote.webelement import WebElement

from selenium_expect import expect
from selenium_expect._compose import satisfy_all, satisfy_any, satisfy_none
from selenium_expect._config import ExpectConfig
from selenium_expect._poll import PollAssertion
from selenium_expect._retry import retry_until

# --- Fix 1: Vacuous truth in location/size comparison methods ---


class TestLocationSizeVacuousTruth:
    """to_have_location/size_greater_than/less_than must reject all-None params."""

    def test_location_greater_than_no_params_raises(self, mock_element: Any) -> None:
        """to_have_location_greater_than() with no args raises ValueError."""
        with pytest.raises(ValueError, match="At least one of x or y"):
            expect(mock_element).to_have_location_greater_than()

    def test_location_less_than_no_params_raises(self, mock_element: Any) -> None:
        """to_have_location_less_than() with no args raises ValueError."""
        with pytest.raises(ValueError, match="At least one of x or y"):
            expect(mock_element).to_have_location_less_than()

    def test_size_greater_than_no_params_raises(self, mock_element: Any) -> None:
        """to_have_size_greater_than() with no args raises ValueError."""
        with pytest.raises(ValueError, match="At least one of width or height"):
            expect(mock_element).to_have_size_greater_than()

    def test_size_less_than_no_params_raises(self, mock_element: Any) -> None:
        """to_have_size_less_than() with no args raises ValueError."""
        with pytest.raises(ValueError, match="At least one of width or height"):
            expect(mock_element).to_have_size_less_than()

    def test_location_greater_than_with_x_passes(self, mock_element: Any) -> None:
        """to_have_location_greater_than(x=50) passes when loc x=100."""
        expect(mock_element).to_have_location_greater_than(x=50)

    def test_location_greater_than_with_y_passes(self, mock_element: Any) -> None:
        """to_have_location_greater_than(y=100) passes when loc y=200."""
        expect(mock_element).to_have_location_greater_than(y=100)


# --- Fix 2: satisfy_all/any/none removed unused timeout/polling ---


class TestComposeNoTimeoutPolling:
    """Composition functions no longer accept timeout/polling params."""

    def test_satisfy_all_no_timeout_param(self, mock_element: Any) -> None:
        """satisfy_all does not accept timeout kwarg."""
        with pytest.raises(TypeError):
            satisfy_all(mock_element, lambda t: None, timeout=5.0)  # type: ignore[call-overload]

    def test_satisfy_any_no_timeout_param(self, mock_element: Any) -> None:
        """satisfy_any does not accept timeout kwarg."""
        with pytest.raises(TypeError):
            satisfy_any(mock_element, lambda t: None, timeout=5.0)  # type: ignore[call-overload]

    def test_satisfy_none_no_polling_param(self, mock_element: Any) -> None:
        """satisfy_none does not accept polling kwarg."""
        with pytest.raises(TypeError):
            satisfy_none(mock_element, lambda t: None, polling=0.5)  # type: ignore[call-overload]

    def test_to_satisfy_all_no_timeout_param(self, mock_element: Any) -> None:
        """expect(el).to_satisfy_all does not accept timeout kwarg."""
        with pytest.raises(TypeError):
            expect(mock_element).to_satisfy_all(lambda t: None, timeout=5.0)  # type: ignore[call-overload]


# --- Fix 3: None guarding in to_have_text_contains and to_have_text_matches ---


class TestTextNoneGuarding:
    """Text methods should handle None text without raising TypeError."""

    @pytest.fixture()
    def element_none_text(self) -> Any:
        """WebElement whose .text returns None."""
        el = MagicMock(spec=WebElement)
        el.is_displayed.return_value = True
        el.is_enabled.return_value = True
        el.is_selected.return_value = False
        el.text = None
        return el

    def test_to_have_text_contains_none_text(self, element_none_text: Any) -> None:
        """to_have_text_contains on None text should not raise TypeError."""
        with pytest.raises(AssertionError, match="to have text containing"):
            expect(element_none_text).to_have_text_contains("something")

    def test_to_have_text_matches_none_text(self, element_none_text: Any) -> None:
        """to_have_text_matches on None text should not raise TypeError."""
        with pytest.raises(AssertionError, match="to have text matching"):
            expect(element_none_text).to_have_text_matches(r"\w+")


# --- Fix 4: Index bounds checking for negative indices ---


class TestNegativeIndexBounds:
    """Index-based assertions should reject out-of-range negative indices."""

    def test_to_have_text_at_negative_out_of_range(self, mock_elements: list[Any]) -> None:
        """to_have_text_at with negative index beyond range fails."""
        with pytest.raises(AssertionError, match="out of range"):
            expect(mock_elements).to_have_text_at(-10, "test")

    def test_to_have_value_at_negative_out_of_range(self, mock_elements: list[Any]) -> None:
        """to_have_value_at with negative index beyond range fails."""
        with pytest.raises(AssertionError, match="out of range"):
            expect(mock_elements).to_have_value_at(-10, "test")

    def test_to_have_attribute_at_negative_out_of_range(self, mock_elements: list[Any]) -> None:
        """to_have_attribute_at with negative index beyond range fails."""
        with pytest.raises(AssertionError, match="out of range"):
            expect(mock_elements).to_have_attribute_at(-10, "id", "test")

    def test_to_have_text_at_valid_negative_index(self, mock_elements: list[Any]) -> None:
        """to_have_text_at with valid negative index works."""
        expect(mock_elements).to_have_text_at(-1, "Cherry")


# --- Fix 5: to_have_text_not_empty None handling ---


class TestTextNotEmptyNone:
    """to_have_text_not_empty should fail when text is None, not pass."""

    def test_to_have_text_not_empty_with_none_text(self) -> None:
        """to_have_text_not_empty on None text should raise AssertionError."""
        el = MagicMock(spec=WebElement)
        el.is_displayed.return_value = True
        el.is_enabled.return_value = True
        el.is_selected.return_value = False
        el.text = None

        with pytest.raises(AssertionError, match="to have text not empty"):
            expect(el).to_have_text_not_empty()


# --- Fix 6: Empty polling_intervals causing IndexError ---


class TestEmptyPollingIntervals:
    """retry_until with empty polling_intervals list should not crash."""

    def test_retry_until_empty_polling_intervals(self) -> None:
        """retry_until with empty polling_intervals should fall back to polling_interval."""
        result = retry_until(
            condition=lambda: (True, "ok"),
            timeout=1.0,
            polling_interval=0.1,
            polling_intervals=[],
        )
        assert result.passed is True
        assert result.poll_count == 1

    def test_retry_until_empty_polling_intervals_failing(self) -> None:
        """retry_until with empty polling_intervals and failing condition should not crash."""
        result = retry_until(
            condition=lambda: (False, "nope"),
            timeout=0.1,
            polling_interval=0.05,
            polling_intervals=[],
        )
        assert result.passed is False
        assert result.poll_count >= 1


# --- Fix 7: timeout=0 skipping first poll ---


class TestTimeoutZeroFirstPoll:
    """retry_until with timeout=0 should still evaluate the condition at least once."""

    def test_timeout_zero_passes_if_condition_true(self) -> None:
        """timeout=0 with a passing condition should return passed=True."""
        result = retry_until(
            condition=lambda: (True, "ok"),
            timeout=0.0,
            polling_interval=0.1,
        )
        assert result.passed is True
        assert result.poll_count == 1

    def test_timeout_zero_fails_if_condition_false(self) -> None:
        """timeout=0 with a failing condition should return passed=False."""
        result = retry_until(
            condition=lambda: (False, "nope"),
            timeout=0.0,
            polling_interval=0.1,
        )
        assert result.passed is False
        assert result.poll_count == 1


# --- Fix 8: PollAssertion.to_contain breaking on falsy non-string values ---


class TestPollContainFalsyValues:
    """to_contain should handle falsy non-string values like 0, False, []."""

    def test_to_contain_integer_in_list(self) -> None:
        """to_contain should work with lists containing 0."""
        pa = PollAssertion(lambda: [0, 1, 2], timeout=0.1, polling=0.05)
        pa.to_contain(0)

    def test_to_contain_false_in_dict(self) -> None:
        """to_contain should work with dict containing False."""
        pa = PollAssertion(lambda: {"a": False, "b": True}, timeout=0.1, polling=0.05)
        pa.to_contain("a")

    def test_to_contain_none_returns_false(self) -> None:
        """to_contain on None function result should fail, not crash."""
        pa = PollAssertion(lambda: None, timeout=0.1, polling=0.05)
        with pytest.raises(AssertionError, match="to contain"):
            pa.to_contain("anything")


# --- Fix 9: PollAssertion timeout normalization ---


class TestPollTimeoutNormalization:
    """PollAssertion should normalize timeout=5000 as 5 seconds, not 5000 seconds."""

    def test_poll_timeout_ms_normalization(self) -> None:
        """PollAssertion with timeout=5000 should be treated as 5 seconds."""
        pa = PollAssertion(lambda: True, timeout=5000, polling=0.05)
        assert pa._timeout == 5.0

    def test_poll_timeout_seconds_unchanged(self) -> None:
        """PollAssertion with timeout=5 should remain 5 seconds."""
        pa = PollAssertion(lambda: True, timeout=5, polling=0.05)
        assert pa._timeout == 5.0


# --- Fix 10: ExpectConfig rejecting empty polling_intervals ---


class TestExpectConfigEmptyPollingIntervals:
    """ExpectConfig should reject empty polling_intervals list."""

    def test_empty_polling_intervals_raises(self) -> None:
        """ExpectConfig with empty polling_intervals should raise ValueError."""
        with pytest.raises(ValueError, match="polling_intervals must not be empty"):
            ExpectConfig(polling_intervals=[])

    def test_none_polling_intervals_ok(self) -> None:
        """ExpectConfig with None polling_intervals should be fine."""
        cfg = ExpectConfig(polling_intervals=None)
        assert cfg.polling_intervals is None


# --- Fix 11: Per-assertion empty polling list validation ---


class TestPerAssertionEmptyPollingList:
    """Passing polling=[] per-assertion should raise ValueError."""

    def test_run_assertion_empty_polling_list(self, mock_element: Any) -> None:
        """_run_assertion with polling=[] should raise ValueError."""
        with pytest.raises(ValueError, match="polling list must not be empty"):
            expect(mock_element).to_be_visible(polling=[])

    def test_poll_empty_polling_list(self) -> None:
        """PollAssertion with polling=[] should raise ValueError."""
        with pytest.raises(ValueError, match="polling list must not be empty"):
            PollAssertion(lambda: True, timeout=0.1, polling=[])


# --- Fix 12: None guarding in list.py to_have_texts_contains / to_have_texts_containing ---


class TestListTextsContainsNoneGuarding:
    """List text methods should handle None element.text without TypeError."""

    def test_to_have_texts_contains_with_none_text(self) -> None:
        """to_have_texts_contains should not crash when element.text is None."""
        el = MagicMock(spec=WebElement)
        el.text = None
        el.is_displayed.return_value = True
        el.is_enabled.return_value = True
        with pytest.raises(AssertionError, match="to have texts containing"):
            expect([el]).to_have_texts_contains(["something"])

    def test_to_have_texts_containing_with_none_text(self) -> None:
        """to_have_texts_containing should not crash when element.text is None."""
        el = MagicMock(spec=WebElement)
        el.text = None
        el.is_displayed.return_value = True
        el.is_enabled.return_value = True
        with pytest.raises(AssertionError, match="to have texts containing"):
            expect([el]).to_have_texts_containing("something")


# --- Fix 13: to_have_js_result_contains breaking on falsy non-string values ---


class TestJSResultContainsFalsy:
    """to_have_js_result_contains should handle falsy non-string values like 0, False, []."""

    def test_to_contain_zero_in_list(self, mock_driver_js: Any) -> None:
        """to_have_js_result_contains should work with lists containing 0."""
        from selenium_expect.assertions.js import ExpectJS

        mock_driver_js.execute_script.side_effect = lambda script, *args: [0, 1, 2]
        ExpectJS(mock_driver_js).to_have_js_result_contains("return [0,1,2];", 0)

    def test_to_contain_none_returns_false(self, mock_driver_js: Any) -> None:
        """to_have_js_result_contains on None should fail, not crash."""
        from selenium_expect.assertions.js import ExpectJS

        mock_driver_js.execute_script.side_effect = lambda script, *args: None
        with pytest.raises(AssertionError, match="to have JS result containing"):
            ExpectJS(mock_driver_js).to_have_js_result_contains("return null;", "anything")


# --- Fix 14: JS injection in localStorage/sessionStorage methods ---


class TestJSInjectionPrevention:
    """localStorage/sessionStorage methods should not be vulnerable to JS injection via key."""

    def test_local_storage_item_with_quote_in_key(self, mock_driver_js: Any) -> None:
        """Key with single quote should not break JS — uses arguments[0] not f-string."""
        from selenium_expect.assertions.js import ExpectJS

        ExpectJS(mock_driver_js).to_have_local_storage_item("token", "abc123")

    def test_local_storage_item_present_with_quote_in_key(self, mock_driver_js: Any) -> None:
        """Key with single quote should not break JS for presence check."""
        from selenium_expect.assertions.js import ExpectJS

        ExpectJS(mock_driver_js).to_have_local_storage_item_present("token")

    def test_session_storage_item_with_quote_in_key(self, mock_driver_js: Any) -> None:
        """Key with single quote should not break JS for sessionStorage."""
        from selenium_expect.assertions.js import ExpectJS

        ExpectJS(mock_driver_js).to_have_session_storage_item("key", "value123")

    def test_js_variable_uses_safe_access(self, mock_driver_js: Any) -> None:
        """to_have_js_variable should use window[arguments[0]] not f-string."""
        from selenium_expect.assertions.js import ExpectJS

        ExpectJS(mock_driver_js).to_have_js_variable("innerWidth", 1280)


# --- Fix 15: to_have_capability_contains falsy non-string values ---


class TestCapabilityContainsFalsy:
    """to_have_capability_contains should handle falsy non-string capability values."""

    def test_capability_contains_with_bool_true(self, mock_driver: Any) -> None:
        """to_have_capability_contains should work with boolean True capability."""
        mock_driver.capabilities = {"acceptInsecureCerts": True}
        expect(mock_driver).to_have_capability_contains("acceptInsecureCerts", "rue")

    def test_capability_contains_with_int_zero(self, mock_driver: Any) -> None:
        """to_have_capability_contains should work with integer 0 capability."""
        mock_driver.capabilities = {"timeout": 0}
        expect(mock_driver).to_have_capability_contains("timeout", "0")

    def test_capability_contains_with_none(self, mock_driver: Any) -> None:
        """to_have_capability_contains on None capability should fail, not crash."""
        mock_driver.capabilities = {"missing": None}
        with pytest.raises(AssertionError, match="capability"):
            expect(mock_driver).to_have_capability_contains("missing", "anything")


# --- Fix 16: to_have_property_contains falsy non-string values ---


class TestPropertyContainsFalsy:
    """to_have_property_contains should handle falsy non-string property values."""

    def test_property_contains_with_int_zero(self, mock_element: Any) -> None:
        """to_have_property_contains should work with integer 0 property."""
        mock_element.get_property.return_value = 0
        expect(mock_element).to_have_property_contains("value", "0")

    def test_property_contains_with_bool_false(self, mock_element: Any) -> None:
        """to_have_property_contains should work with boolean False property."""
        mock_element.get_property.return_value = False
        expect(mock_element).to_have_property_contains("checked", "alse")

    def test_property_contains_with_none(self, mock_element: Any) -> None:
        """to_have_property_contains on None property should fail, not crash."""
        mock_element.get_property.return_value = None
        with pytest.raises(AssertionError, match="property"):
            expect(mock_element).to_have_property_contains("value", "anything")
