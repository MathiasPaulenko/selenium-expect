# selenium-expect

Playwright-style `expect()` assertions with auto-retry for Selenium Python. Standalone, no framework required.

[![CI](https://github.com/MathiasPaulenko/selenium-expect/actions/workflows/ci.yml/badge.svg)](https://github.com/MathiasPaulenko/selenium-expect/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/selenium-expect.svg)](https://pypi.org/project/selenium-expect/)
[![Python](https://img.shields.io/pypi/pyversions/selenium-expect.svg)](https://pypi.org/project/selenium-expect/)
[![License](https://img.shields.io/github/license/MathiasPaulenko/selenium-expect.svg)](https://github.com/MathiasPaulenko/selenium-expect/blob/main/LICENSE)
[![Coverage](https://codecov.io/gh/MathiasPaulenko/selenium-expect/branch/main/graph/badge.svg)](https://codecov.io/gh/MathiasPaulenko/selenium-expect)

---

## Why?

Selenium's `WebDriverWait` + `expected_conditions` is verbose and inconsistent. Playwright's `expect()` is ergonomic and auto-retries. **selenium-expect** brings that experience to Selenium Python:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_expect import expect

driver = webdriver.Chrome()

# Auto-retry — no explicit WebDriverWait needed
expect(driver).to_have_title("Dashboard")
expect(driver).to_have_url_contains("/dashboard")

button = driver.find_element(By.ID, "submit")
expect(button).to_be_visible()
expect(button).to_be_enabled()
expect(button).to_have_text("Submit")

# Negation
expect(button).not_.to_be_disabled()

# Lists
items = driver.find_elements(By.CSS_SELECTOR, ".item")
expect(items).to_have_count(5)
expect(items).to_have_texts(["Apple", "Banana", "Cherry", "Date", "Elderberry"])

# Locator-based (re-finds on each poll — no StaleElementReferenceException)
expect(driver, by=By.ID, value="dynamic-content").to_have_text("Loaded!")
```

---

## Installation

```bash
pip install selenium-expect
```

Requires:

- Python >= 3.11
- selenium >= 4.10

---

## Quickstart

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_expect import expect, set_default_timeout

# Optional: configure global defaults
set_default_timeout(10)  # 10s timeout for all assertions

driver = webdriver.Chrome()
driver.get("https://example.com")

# Page-level assertions
expect(driver).to_have_title("Example Domain")
expect(driver).to_have_url("https://example.com/")
expect(driver).to_have_page_source_contains("This domain is for use in illustrative examples")

# Element assertions
heading = driver.find_element(By.TAG_NAME, "h1")
expect(heading).to_have_text("Example Domain")
expect(heading).to_have_tag("h1")
expect(heading).to_be_visible()

# Attribute assertions
link = driver.find_element(By.TAG_NAME, "a")
expect(link).to_have_attribute("href", "https://www.iana.org/domains/example")
expect(link).to_have_attribute_contains("href", "iana.org")

# CSS property assertions
expect(heading).to_have_css_property("color", "rgba(0, 0, 0, 1)")

# Negation
expect(link).not_.to_have_text("Click here")

driver.quit()
```

---

## Configuration

### Global defaults

```python
from selenium_expect import (
    set_default_timeout,
    set_default_polling_interval,
    set_default_polling_intervals,
    set_screenshot_on_failure,
    set_debug_mode,
)

set_default_timeout(10)  # 10s timeout (default: 5s)
set_default_polling_interval(0.2)  # 200ms between polls (default: 500ms)
set_default_polling_intervals([0.1, 0.2, 0.5, 1.0])  # Backoff schedule
set_screenshot_on_failure(True, "/tmp/screenshots")
set_debug_mode(True)  # Log each poll attempt
```

### Per-assertion override

```python
# Override timeout for a single assertion
expect(element).to_be_visible(timeout=15)

# Override polling interval
expect(element).to_have_text("Ready", polling=0.1)

# Backoff schedule
expect(element).to_be_clickable(polling=[0.05, 0.1, 0.5, 1.0])

# Custom error message
expect(element).to_have_text("Hello", message="Greeting should say Hello")

# Soft assertion (accumulate failures, check later)
expect(element, soft=True).to_be_visible()
expect(element, soft=True).to_have_text("Hello")
assert_all()  # Raises if any soft assertions failed
```

### Pre-configured expect

```python
from selenium_expect import expect

# Create a variant with pre-applied config
slow_expect = expect.configure(timeout=30, polling=1.0)
slow_expect(driver).to_have_title("Slow Page")
```

---

## Assertions reference

### Driver / Page

| Assertion | Selenium API |
|---|---|
| `to_have_title(text)` | `driver.title` |
| `to_have_title_contains(text)` | `text in driver.title` |
| `to_have_title_matches(pattern)` | `re.search(pattern, driver.title)` |
| `to_have_url(url)` | `driver.current_url` |
| `to_have_url_contains(url)` | `url in driver.current_url` |
| `to_have_url_matches(pattern)` | `re.search(pattern, driver.current_url)` |
| `to_have_window_count(n)` | `len(driver.window_handles)` |
| `to_have_window_count_greater_than(n)` | `len(driver.window_handles) > n` |
| `to_have_window_count_less_than(n)` | `len(driver.window_handles) < n` |
| `to_have_window_handle(handle)` | `driver.current_window_handle` |
| `to_have_browser_name(name)` | `driver.name` |
| `to_have_orientation(orientation)` | `driver.orientation` |
| `to_have_capability(key, value)` | `driver.capabilities[key]` |
| `to_have_page_source_contains(text)` | `text in driver.page_source` |
| `to_have_page_source_matches(pattern)` | `re.search(pattern, driver.page_source)` |
| `to_have_window_position(x, y)` | `driver.get_window_position()` |
| `to_have_window_size(w, h)` | `driver.get_window_size()` |
| `to_have_window_rect(x, y, w, h)` | `driver.get_window_rect()` |
| `to_have_active_element_tag(tag)` | `driver.switch_to.active_element.tag_name` |
| `to_have_active_element_id(id)` | `driver.switch_to.active_element.get_attribute('id')` |

### Element — State

| Assertion | Selenium API |
|---|---|
| `to_be_visible()` | `element.is_displayed()` |
| `to_be_hidden()` | `not element.is_displayed()` |
| `to_be_enabled()` | `element.is_enabled()` |
| `to_be_disabled()` | `not element.is_enabled()` |
| `to_be_checked()` | `element.is_selected()` |
| `to_be_selected()` | `element.is_selected()` |
| `to_be_present()` | `element.tag_name` (no exception) |
| `to_be_absent()` | `StaleElementReferenceException` / `NoSuchElementException` |
| `to_be_clickable()` | `is_displayed() and is_enabled()` |
| `to_be_stale()` | `StaleElementReferenceException` on access |

### Element — Text

| Assertion | Selenium API |
|---|---|
| `to_have_text(text)` | `element.text` |
| `to_have_text_contains(text)` | `text in element.text` |
| `to_have_text_matches(pattern)` | `re.search(pattern, element.text)` |
| `to_have_text_empty()` | `element.text == ''` |
| `to_have_text_not_empty()` | `element.text != ''` |
| `to_have_value(value)` | `element.get_attribute('value')` |
| `to_have_value_contains(value)` | `value in element.get_attribute('value')` |

### Element — Attributes

| Assertion | Selenium API |
|---|---|
| `to_have_attribute(name, value)` | `element.get_attribute(name)` |
| `to_have_attribute_contains(name, value)` | `value in element.get_attribute(name)` |
| `to_have_attribute_matches(name, pattern)` | `re.search(pattern, element.get_attribute(name))` |
| `to_have_attribute_empty(name)` | `element.get_attribute(name) in ('', None)` |
| `to_have_attribute_present(name)` | `element.get_attribute(name) is not None` |
| `to_have_attribute_absent(name)` | `element.get_attribute(name) is None` |

### Element — CSS

| Assertion | Selenium API |
|---|---|
| `to_have_css_property(name, value)` | `element.value_of_css_property(name)` |
| `to_have_css_property_contains(name, value)` | `value in element.value_of_css_property(name)` |

### Element — Identity

| Assertion | Selenium API |
|---|---|
| `to_have_tag(tag)` | `element.tag_name` |
| `to_have_id(id)` | `element.get_attribute('id')` |
| `to_have_class(class_name)` | `class_name in element.get_attribute('class').split()` |
| `to_have_class_contains(class_name)` | `class_name in element.get_attribute('class')` |

### Element — Position / Dimensions

| Assertion | Selenium API |
|---|---|
| `to_have_location(x, y)` | `element.location` |
| `to_have_location_x(x)` | `element.location['x']` |
| `to_have_location_y(y)` | `element.location['y']` |
| `to_have_size(width, height)` | `element.size` |
| `to_have_size_width(width)` | `element.size['width']` |
| `to_have_size_height(height)` | `element.size['height']` |
| `to_have_rect(x, y, w, h)` | `element.rect` |

### Element — Accessibility (Selenium 4+)

| Assertion | Selenium API |
|---|---|
| `to_have_aria_role(role)` | `element.aria_role` |
| `to_have_aria_role_contains(role)` | `role in element.aria_role` |
| `to_have_accessible_name(name)` | `element.accessible_name` |
| `to_have_accessible_name_contains(name)` | `name in element.accessible_name` |

### List

| Assertion | Selenium API |
|---|---|
| `to_have_count(n)` | `len(elements)` |
| `to_have_count_greater_than(n)` | `len(elements) > n` |
| `to_have_count_less_than(n)` | `len(elements) < n` |
| `to_be_empty()` | `len(elements) == 0` |
| `to_be_not_empty()` | `len(elements) > 0` |
| `to_have_texts(texts)` | `[el.text for el in elements]` |
| `to_have_texts_contains(texts)` | substring per element |
| `to_have_text_at(index, text)` | `elements[index].text` |
| `to_have_any_text(text)` | any element has text |
| `to_have_all_texts_contain(text)` | all elements contain text |
| `to_have_any_text_contain(text)` | any element contains text |
| `to_have_none_text_contain(text)` | no element contains text |
| `to_have_values(values)` | `[el.get_attribute('value') for el in elements]` |
| `to_have_all_visible()` | all `is_displayed()` |
| `to_have_any_visible()` | any `is_displayed()` |
| `to_have_none_visible()` | none `is_displayed()` |
| `to_have_all_enabled()` | all `is_enabled()` |
| `to_have_all_selected()` | all `is_selected()` |
| `to_have_attribute_at(index, name, value)` | `elements[index].get_attribute(name)` |
| `to_have_all_attribute(name, value)` | all elements have attribute |
| `to_have_any_attribute(name, value)` | any element has attribute |

### Alert

| Assertion | Selenium API |
|---|---|
| `to_be_present()` | `driver.switch_to.alert` (no exception) |
| `to_have_text(text)` | `alert.text` |
| `to_have_text_contains(text)` | `text in alert.text` |
| `to_have_text_matches(pattern)` | `re.search(pattern, alert.text)` |

### Cookie

| Assertion | Selenium API |
|---|---|
| `to_have_cookie(name)` | `driver.get_cookie(name) is not None` |
| `to_have_cookie_value(name, value)` | `driver.get_cookie(name)['value']` |
| `to_have_cookie_value_contains(name, value)` | `value in driver.get_cookie(name)['value']` |
| `to_have_cookie_domain(name, domain)` | `driver.get_cookie(name)['domain']` |
| `to_have_cookie_path(name, path)` | `driver.get_cookie(name)['path']` |
| `to_have_cookie_http_only(name)` | `driver.get_cookie(name)['httpOnly']` |
| `to_have_cookie_secure(name)` | `driver.get_cookie(name)['secure']` |
| `to_have_cookie_same_site(name, same_site)` | `driver.get_cookie(name)['sameSite']` |
| `to_have_cookie_count(n)` | `len(driver.get_cookies())` |
| `to_have_no_cookies()` | `len(driver.get_cookies()) == 0` |

### JavaScript / Browser state

| Assertion | Selenium API |
|---|---|
| `to_have_js_result(script, expected)` | `driver.execute_script(script)` |
| `to_have_js_result_contains(script, expected)` | `expected in driver.execute_script(script)` |
| `to_have_async_js_result(script, expected)` | `driver.execute_async_script(script)` |
| `to_have_local_storage_item(key, value)` | `localStorage.getItem(key)` via JS |
| `to_have_local_storage_item_present(key)` | `localStorage.getItem(key) is not None` |
| `to_have_local_storage_item_absent(key)` | `localStorage.getItem(key) is None` |
| `to_have_local_storage_length(n)` | `localStorage.length` via JS |
| `to_have_session_storage_item(key, value)` | `sessionStorage.getItem(key)` via JS |
| `to_have_session_storage_length(n)` | `sessionStorage.length` via JS |

### Shadow DOM

| Assertion | Selenium API |
|---|---|
| `to_have_element(by, value)` | `shadow_root.find_element(by, value)` |
| `to_have_element_count(by, value, n)` | `len(shadow_root.find_elements(by, value))` |
| `to_have_element_text(by, value, text)` | `shadow_root.find_element(by, value).text` |
| `to_have_element_attribute(by, value, attr, value)` | `.find_element().get_attribute(attr)` |
| `to_have_element_visible(by, value)` | `shadow_root.find_element(by, value).is_displayed()` |

### Select / Dropdown

| Assertion | Selenium API |
|---|---|
| `to_have_value(value)` | `select.first_selected_option.get_attribute('value')` |
| `to_have_selected_text(text)` | `select.first_selected_option.text` |
| `to_have_selected_values(values)` | `[opt.get_attribute('value') for opt in select.all_selected_options]` |
| `to_have_selected_texts(texts)` | `[opt.text for opt in select.all_selected_options]` |
| `to_have_selected_count(n)` | `len(select.all_selected_options)` |
| `to_have_option_count(n)` | `len(select.options)` |
| `to_have_option_at_index(index, text)` | `select.options[index].text` |
| `to_have_option(value)` | value exists in options |
| `to_have_option_text(text)` | text exists in options |
| `to_be_multiple()` | `select.is_multiple` |
| `to_be_single_select()` | `not select.is_multiple` |

### Iframe

| Assertion | Selenium API |
|---|---|
| `to_have_frame_available(frame_id)` | `driver.switch_to.frame(frame_id)` |
| `to_have_frame_count(n)` | `len(driver.find_elements(By.TAG_NAME, 'iframe'))` |
| `to_have_frame_text(frame_id, text)` | switch to frame, check page_source |

### Window

| Assertion | Selenium API |
|---|---|
| `to_have_position(x, y)` | `driver.get_window_position()` |
| `to_have_size(w, h)` | `driver.get_window_size()` |
| `to_have_rect(x, y, w, h)` | `driver.get_window_rect()` |

---

## Advanced features

### Soft assertions

Accumulate failures and check them all at once:

```python
from selenium_expect import expect, assert_all

form = driver.find_element(By.ID, "form")

# These won't raise immediately
expect(form, soft=True).to_be_visible()
expect(form, soft=True).to_have_attribute("method", "POST")
expect(form, soft=True).to_have_attribute("action", "/submit")

# Raises AssertionError with all failures if any failed
assert_all()
```

### Custom matchers

Extend `expect()` with your own assertions:

```python
from selenium_expect import expect, extend


@extend("to_be_in_viewport")
def check_in_viewport(element):
    script = """
        var r = arguments[0].getBoundingClientRect();
        return r.top >= 0 && r.left >= 0 &&
               r.bottom <= window.innerHeight &&
               r.right <= window.innerWidth;
    """
    result = element.parent.execute_script(script, element)
    return result, result


# Use it like any built-in assertion
expect(element).to_be_in_viewport()
expect(element).not_.to_be_in_viewport()
```

### Locator-based expect

Re-finds the element on each poll cycle — eliminates `StaleElementReferenceException`:

```python
# Instead of:
# element = driver.find_element(By.ID, "dynamic")
# expect(element).to_have_text("Loaded")  # element might go stale

# Use locator-based:
expect(driver, by=By.ID, value="dynamic").to_have_text("Loaded!")
```

### `expect.poll()`

Retry arbitrary functions:

```python
from selenium_expect import expect, poll

# Poll a JavaScript result
expect.poll(lambda: driver.execute_script("return localStorage.getItem('token')")).to_equal(
    "abc123"
)

# Poll with timeout
expect.poll(
    lambda: driver.execute_script("return document.readyState"),
    timeout=30,
).to_equal("complete")
```

### Composition

Combine multiple assertions:

```python
from selenium_expect import expect

# All must pass (AND)
expect(element).to_satisfy_all(
    lambda e: expect(e).to_be_visible(),
    lambda e: expect(e).to_be_enabled(),
    lambda e: expect(e).to_have_text("Submit"),
)

# At least one must pass (OR)
expect(element).to_satisfy_any(
    lambda e: expect(e).to_have_text("Save"),
    lambda e: expect(e).to_have_text("Submit"),
)

# None must pass (NOT)
expect(element).to_satisfy_none(
    lambda e: expect(e).to_be_disabled(),
    lambda e: expect(e).to_be_hidden(),
)
```

---

## Comparison

| Feature | selenium-expect | WebDriverWait + EC | Playwright expect | Selenium IDE |
|---|---|---|---|---|
| Auto-retry | Yes | Yes (explicit) | Yes | No |
| Fluent API | Yes | No | Yes | No |
| Negation | Yes (`.not_`) | Manual | Yes (`.not_`) | No |
| Soft assertions | Yes | No | No | No |
| Custom matchers | Yes | No | Yes | No |
| Locator re-find | Yes | Manual | Built-in | No |
| Lists | Yes | Manual | Yes | No |
| Cookies | Yes | No | No | No |
| JS state | Yes | No | No | No |
| Shadow DOM | Yes | No | Yes | No |
| Select/dropdown | Yes | No | Yes | No |
| Alerts | Yes | Yes | Yes | No |
| Configurable polling | Yes (fixed + backoff) | Fixed | Fixed | No |
| Descriptive errors | Yes (timeline + HTML) | Basic | Good | Basic |
| Framework dependency | None | Selenium | Playwright | IDE |
| Python support | >= 3.11 | All | N/A | N/A |

---

## Error messages

selenium-expect produces descriptive, multi-line error messages:

```text
AssertionError: Expected element to have text "Loaded!", but got "Loading..."
  Expected: Loaded!
  Actual:   Loading...
  Element:  <div id="status" class="loading">Loading...</div>
  Waited:   5001ms (10 polls at 0.5s interval)
  Message:  Status should show Loaded! after AJAX completes
  Timeline: [poll 1: Loading..., poll 2: Loading..., ..., poll 10: Loading...]
```

---

## License

[MIT](https://github.com/MathiasPaulenko/selenium-expect/blob/main/LICENSE)

---

## Links

- [Documentation](https://mathiaspaulenko.github.io/selenium-expect/)
- [Changelog](https://github.com/MathiasPaulenko/selenium-expect/blob/main/CHANGELOG.md)
- [Issues](https://github.com/MathiasPaulenko/selenium-expect/issues)
- [PyPI](https://pypi.org/project/selenium-expect/)
