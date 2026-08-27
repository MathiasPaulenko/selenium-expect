# API reference

This page provides a complete reference for all public APIs in `selenium-expect`.

## Quick navigation

- [**`expect()`**](#expecttarget) — Entry point for all assertions
- [**`poll()`**](#pollfn) — Poll-based assertions on arbitrary functions
- [**`extend()`**](#extendname) — Register custom matchers
- [**`merge_expects()`**](#merge_expectsmodules) — Combine matchers from modules
- [**`SoftAssertionCollector`**](#softassertioncollector) — Soft assertion management
- [**`assert_all()`**](#assert_all) — Raise collected soft failures
- [**`ExpectConfig`**](#expectconfig) — Configuration dataclass
- [**Configuration setters**](#configuration-setters) — Global defaults
- [**Assertion classes**](#assertion-classes) — All assertion class references

## `expect(target, ...)`

Create an assertion for the given target. Dispatches to the appropriate assertion class based on the target's type.

### Supported targets

| Target type | Assertion class | Example |
|---|---|---|
| `WebElement` | `ExpectElement` | `expect(element).to_be_visible()` |
| `WebDriver` | `ExpectDriver` | `expect(driver).to_have_title("Page")` |
| `list[WebElement]` | `ExpectList` | `expect(elements).to_have_count(5)` |
| `Alert` | `ExpectAlert` | `expect(alert).to_have_text("Confirm?")` |
| `Select` | `ExpectSelect` | `expect(select).to_have_value("opt1")` |
| `ShadowRoot` | `ExpectShadow` | `expect(shadow).to_have_element(By.ID, "x")` |
| `WebDriver` + `by`/`value` | `LocatorExpect` | `expect(driver, by=By.ID, value="x").to_be_visible()` |

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `target` | `Any` | — | The object to assert on |
| `by` | `str` | `None` | Locator strategy (for locator-based expect) |
| `value` | `str` | `None` | Locator value (for locator-based expect) |
| `locator` | `tuple[str, str]` | `None` | `(by, value)` tuple shorthand |
| `message` | `str` | `None` | Custom message for error output |
| `soft` | `bool` | `False` | Enable soft assertion mode |
| `timeout` | `float` | `None` | Override default timeout |
| `polling` | `float \| list[float]` | `None` | Override default polling |

::: selenium_expect._expect.Expect

## `ExpectConfig`

Immutable configuration dataclass for all assertions.

### Fields

| Field | Type | Default | Description |
|---|---|---|---|
| `timeout` | `float` | `5.0` | Default timeout in seconds |
| `polling_interval` | `float` | `0.5` | Fixed polling interval |
| `polling_intervals` | `list[float] \| None` | `None` | Backoff schedule |
| `screenshot_on_failure` | `bool` | `False` | Capture screenshot on failure |
| `screenshot_path` | `str \| None` | `None` | Screenshot directory |
| `debug_mode` | `bool` | `False` | Debug logging |
| `soft_mode` | `bool` | `False` | Soft assertion mode |

### Usage

```python
from selenium_expect import ExpectConfig, expect

# Create a custom config
config = ExpectConfig(timeout=10, polling_interval=0.25, debug_mode=True)

# Use with expect.configure()
debug_expect = expect.configure(timeout=10, polling=0.25, debug_mode=True)
```

::: selenium_expect._config.ExpectConfig

## `poll(fn, ...)`

Create a `PollAssertion` for retry-based assertions on an arbitrary function.

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `fn` | `Callable[[], Any]` | — | Zero-argument callable to poll |
| `timeout` | `float` | `None` | Override default timeout |
| `polling` | `float \| list[float]` | `None` | Override default polling |

### Example

```python
from selenium_expect import expect, poll

# Using expect.poll
expect.poll(lambda: driver.execute_script("return document.readyState")).to_equal("complete")

# Using standalone poll
poll(lambda: driver.current_url, timeout=10).to_match(r"https://.*\.example\.com")
```

::: selenium_expect._poll.poll

## `PollAssertion`

Assertion over an arbitrary function with retry loop.

### Methods

| Method | Description |
|---|---|
| `to_equal(expected)` | Assert `fn() == expected` |
| `to_be_truthy()` | Assert `bool(fn())` is `True` |
| `to_be_falsy()` | Assert `bool(fn())` is `False` |
| `to_be_none()` | Assert `fn()` is `None` |
| `to_contain(expected)` | Assert `expected in fn()` |
| `to_match(pattern)` | Assert `re.search(pattern, str(fn()))` matches |
| `to_be_greater_than(expected)` | Assert `fn() > expected` |
| `to_be_less_than(expected)` | Assert `fn() < expected` |
| `to_be_in_list(expected)` | Assert `fn() in expected` |
| `to_have_length(expected)` | Assert `len(fn()) == expected` |

::: selenium_expect._poll.PollAssertion

## `extend(name)`

Decorator to register a custom matcher under `name`.

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | Method name to register (e.g. `"to_be_in_viewport"`) |

### Matcher signature

```python
def my_matcher(target: Any, *args, **kwargs) -> tuple[bool, Any]:
    ...
    return (passed, actual_value)
```

### Example

```python
from selenium_expect import extend

@extend("to_have_trimmed_text")
def check_trimmed_text(element, expected: str):
    actual = element.text.strip()
    return (actual == expected, actual)

# Usage
expect(element).to_have_trimmed_text("Hello!")
expect(element).not_.to_have_trimmed_text("  Hello!  ")
```

::: selenium_expect._matcher.extend

## `merge_expects(*modules)`

Combine custom matchers from multiple modules into the registry.

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `*modules` | `ModuleType \| str` | Modules or importable module paths |

### Example

```python
from selenium_expect import merge_expects

# Pass module objects
import my_project.matchers
import my_project.custom_assertions
merge_expects(my_project.matchers, my_project.custom_assertions)

# Or pass importable strings
merge_expects("my_project.matchers", "my_project.custom_assertions")
```

::: selenium_expect._matcher.merge_expects

## `SoftAssertionCollector`

Collects soft assertion failures for deferred raising.

### Methods

| Method | Description |
|---|---|
| `reset()` | Clear all collected failures |
| `get_failures()` | Return list of failure messages |
| `assert_all()` | Raise `AssertionError` if any failures, then reset |

### Example

```python
from selenium_expect import expect, SoftAssertionCollector, assert_all

SoftAssertionCollector.reset()

expect(element).to_be_visible(soft=True)
expect(element).to_have_text("Hello", soft=True)

failures = SoftAssertionCollector.get_failures()
if failures:
    print(f"{len(failures)} failures collected")

assert_all()  # raises if any failures
```

::: selenium_expect._soft.SoftAssertionCollector

## `assert_all()`

Raise `AssertionError` if any soft failures were collected, then reset.

### Example

```python
from selenium_expect import expect, assert_all

expect(element).to_be_visible(soft=True)
expect(element).to_have_text("Hello", soft=True)

assert_all()  # raises AssertionError with combined message if any failed
```

::: selenium_expect._soft.assert_all

## Configuration setters

### `set_default_timeout(seconds)`

Set the global default timeout for all assertions.

```python
from selenium_expect import set_default_timeout

set_default_timeout(10)     # 10 seconds
set_default_timeout(5000)   # interpreted as 5000ms = 5 seconds (int >= 1000)
```

::: selenium_expect._config.set_default_timeout

### `set_default_polling_interval(seconds)`

Set the global default polling interval (fixed).

```python
from selenium_expect import set_default_polling_interval

set_default_polling_interval(0.25)
```

::: selenium_expect._config.set_default_polling_interval

### `set_default_polling_intervals(intervals)`

Set a backoff schedule for polling. The list is cycled through during the retry loop.

```python
from selenium_expect import set_default_polling_intervals

set_default_polling_intervals([0.1, 0.2, 0.5, 1.0])
```

::: selenium_expect._config.set_default_polling_intervals

### `set_screenshot_on_failure(enabled, path=None)`

Enable automatic screenshot capture on assertion failure.

```python
from selenium_expect import set_screenshot_on_failure

set_screenshot_on_failure(True, path="./screenshots/")
```

::: selenium_expect._config.set_screenshot_on_failure

### `set_debug_mode(enabled)`

Enable debug logging for retry loops. Prints poll count, elapsed time, and actual values.

```python
from selenium_expect import set_debug_mode

set_debug_mode(True)
```

::: selenium_expect._config.set_debug_mode

### `get_config()`

Return the current global `ExpectConfig` instance.

```python
from selenium_expect import get_config

config = get_config()
print(f"Timeout: {config.timeout}s, Polling: {config.polling_interval}s")
```

::: selenium_expect._config.get_config

## Assertion classes

### `ExpectElement`

Assertions for `WebElement` objects. Provides methods for visibility, state, text, attributes, CSS, identity, position, accessibility, shadow DOM, and JavaScript properties.

**Key method categories**:

- **State**: `to_be_visible`, `to_be_hidden`, `to_be_present`, `to_be_enabled`, `to_be_disabled`, `to_be_selected`, `to_be_checked`, `to_be_clickable`, `to_be_stale`
- **Text**: `to_have_text`, `to_have_text_contains`, `to_have_text_matches`, `to_have_trimmed_text`
- **Attributes**: `to_have_attribute`, `to_have_attribute_present`, `to_have_attribute_absent`, `to_have_class`, `to_have_class_contain`, `to_have_id`, `to_have_value`
- **CSS**: `to_have_css_property`, `to_have_css_value_contains`
- **Identity**: `to_have_tag`, `to_have_role`, `to_have_aria_label`, `to_have_aria_describedby`
- **Position**: `to_have_position`, `to_have_size`, `to_have_rect`
- **Composition**: `to_satisfy_all`, `to_satisfy_any`, `to_satisfy_none`

::: selenium_expect.assertions.element.ExpectElement

### `ExpectDriver`

Assertions for `WebDriver` and page-level state.

**Key method categories**:

- **Title**: `to_have_title`, `to_have_title_contains`, `to_have_title_matches`
- **URL**: `to_have_url`, `to_have_url_contains`, `to_have_url_matches`
- **State**: `to_have_ready_state`
- **Windows**: `to_have_window_count`, `to_have_window_count_greater_than`, `to_have_window_handles`
- **Browser**: `to_have_browser_name`, `to_have_capability`
- **Page source**: `to_have_page_source_contains`
- **Window geometry**: `to_have_position`, `to_have_size`, `to_have_rect`
- **Active element**: `to_have_active_element_tag`, `to_have_active_element_attribute`, `to_have_active_element_text`, `to_have_active_element_visible`, `to_have_active_element_enabled`

::: selenium_expect.assertions.driver.ExpectDriver

### `ExpectList`

Assertions for lists of `WebElement` objects.

**Key method categories**:

- **Count**: `to_have_count`, `to_have_count_greater_than`, `to_have_count_less_than`, `to_have_count_greater_than_or_equal`, `to_have_count_less_than_or_equal`, `to_be_empty`, `to_be_not_empty`
- **Text**: `to_have_texts`, `to_have_texts_contains`, `to_have_text_at`, `to_have_any_text`, `to_have_all_texts_contain`, `to_have_any_text_contain`, `to_have_none_text_contain`, `to_have_exact_texts`, `to_have_texts_containing`, `to_have_texts_in_any_order`, `to_have_first_text`, `to_have_last_text`, `to_have_nth_text_contains`
- **Values**: `to_have_values`, `to_have_value_at`
- **State**: `to_have_all_visible`, `to_have_any_visible`, `to_have_none_visible`, `to_have_all_enabled`, `to_have_all_selected`
- **Attributes**: `to_have_attribute_at`, `to_have_all_attribute`, `to_have_any_attribute`

::: selenium_expect.assertions.list.ExpectList

### `ExpectAlert`

Assertions for JavaScript `Alert` objects.

**Methods**: `to_be_present`, `to_have_text`, `to_have_text_contains`, `to_have_text_matches`

::: selenium_expect.assertions.alert.ExpectAlert

### `ExpectCookie`

Assertions for browser cookies.

**Key method categories**:

- **Presence**: `to_have_cookie`, `to_have_no_cookies`, `to_have_cookie_count`, `to_have_cookie_count_greater_than`
- **Value**: `to_have_cookie_value`, `to_have_cookie_domain`, `to_have_cookie_path`, `to_have_cookie_expiry`
- **Security**: `to_have_cookie_secure`, `to_have_cookie_http_only`, `to_have_cookie_same_site`

::: selenium_expect.assertions.cookie.ExpectCookie

### `ExpectSelect`

Assertions for HTML `<select>` elements.

**Key method categories**:

- **Selection**: `to_have_value`, `to_have_first_selected_value`, `to_have_selected_text`, `to_have_selected_index`, `to_have_selected_values`, `to_have_selected_texts`, `to_have_selected_count`, `to_have_no_selection`
- **Options**: `to_have_option_count`, `to_have_option_count_greater_than`, `to_have_option`, `to_have_option_text`, `to_have_option_at_index`
- **Type**: `to_be_multiple`, `to_be_single_select`

::: selenium_expect.assertions.select.ExpectSelect

### `ExpectShadow`

Assertions for `ShadowRoot` elements.

**Methods**: `to_have_element`, `to_have_element_count`, `to_have_element_text`, `to_have_element_attribute`, `to_have_element_visible`

::: selenium_expect.assertions.shadow.ExpectShadow

### `ExpectJS`

Assertions for JavaScript and browser state.

**Key method categories**:

- **JS execution**: `to_have_js_result`, `to_have_js_result_contains`, `to_have_async_js_result`, `to_have_js_variable`
- **localStorage**: `to_have_local_storage_item`, `to_have_local_storage_item_present`, `to_have_local_storage_item_absent`, `to_have_local_storage_length`
- **sessionStorage**: `to_have_session_storage_item`, `to_have_session_storage_item_present`, `to_have_session_storage_item_absent`, `to_have_session_storage_length`

::: selenium_expect.assertions.js.ExpectJS

### `ExpectIframe`

Assertions for iframes.

**Methods**: `to_have_frame_available`, `to_have_frame_count`, `to_have_frame_count_greater_than`, `to_have_frame_text`, `to_be_in_frame`, `to_be_in_default_content`

::: selenium_expect.assertions.iframe.ExpectIframe

### `ExpectWindow`

Assertions for browser window position, size, and rect.

**Methods**: `to_have_position`, `to_have_size`, `to_have_rect`

::: selenium_expect.assertions.window.ExpectWindow

### `LocatorExpect`

Locator-based expect that re-finds the element on each poll. All `ExpectElement` methods are available via delegation.

```python
from selenium.webdriver.common.by import By
from selenium_expect import expect

# Re-finds element on each poll — avoids StaleElementReferenceException
expect(driver, by=By.ID, value="dynamic-element").to_be_visible(timeout=10)
expect(driver, locator=(By.CSS_SELECTOR, ".btn")).to_have_text("Submit")
```

::: selenium_expect._locator.LocatorExpect
