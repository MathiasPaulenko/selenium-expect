# Driver / Page assertions

`expect(driver)` returns an `ExpectDriver` instance, which provides assertions for page title, URL, windows, browser capabilities, page source, and the active element.

It also inherits cookie, JavaScript, iframe, and window assertions — see [Cookie](cookie.md), [JavaScript / Browser state](js.md), [Iframe](iframe.md), and [Window](window.md) for those.

## Title

### `to_have_title(title)`

Asserts that the page title equals `title`.

**Selenium API**: `driver.title`

**Parameters**:

- `title` (`str`): Expected page title.

**Example**:

```python
expect(driver).to_have_title("Dashboard - My App")
```

With a custom timeout:

```python
expect(driver).to_have_title("Dashboard - My App", timeout=15)
```

**Negation**:

```python
expect(driver).not_.to_have_title("Loading...")
```

**Real-world example** — waiting for a SPA to finish loading:

```python
driver.get("https://app.example.com/dashboard")
# SPA frameworks update the title after JS loads
expect(driver).to_have_title("Dashboard | Example App", timeout=20)
```

---

### `to_have_title_contains(title)`

Asserts that `title` is a substring of `driver.title`.

**Selenium API**: `title in driver.title`

**Parameters**:

- `title` (`str`): Expected substring of the page title.

**Example**:

```python
expect(driver).to_have_title_contains("Dashboard")
```

---

### `to_have_title_matches(pattern)`

Asserts that `re.search(pattern, driver.title)` finds a match.

**Selenium API**: `re.search(pattern, driver.title)`

**Parameters**:

- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(driver).to_have_title_matches(r"Dashboard - .*")
```

## URL

### `to_have_url(url)`

Asserts that `driver.current_url` equals `url`.

**Selenium API**: `driver.current_url`

**Parameters**:

- `url` (`str`): Expected URL.

**Example**:

```python
expect(driver).to_have_url("https://example.com/dashboard")
```

---

### `to_have_url_contains(url)`

Asserts that `url` is a substring of `driver.current_url`.

**Selenium API**: `url in driver.current_url`

**Parameters**:

- `url` (`str`): Expected substring of the URL.

**Example**:

```python
expect(driver).to_have_url_contains("dashboard")
```

---

### `to_have_url_matches(pattern)`

Asserts that `re.search(pattern, driver.current_url)` finds a match.

**Selenium API**: `re.search(pattern, driver.current_url)`

**Parameters**:

- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(driver).to_have_url_matches(r"https://\w+\.example\.com")
```

---

### `to_have_url_changes(url)`

Asserts that `driver.current_url` is different from `url`.

**Selenium API**: `driver.current_url != url`

**Parameters**:

- `url` (`str`): The URL that should no longer be current.

**Example**:

```python
expect(driver).to_have_url_changes("https://example.com/login")
```

## Ready state

### `to_have_ready_state(state)`

Asserts that `document.readyState` equals `state`.

**Selenium API**: `driver.execute_script("return document.readyState")`

**Parameters**:

- `state` (`str`): Expected ready state (`"loading"`, `"interactive"`, or `"complete"`).

**Example**:

```python
expect(driver).to_have_ready_state("complete")
```

## Windows / tabs

### `to_have_window_count(count)`

Asserts that the number of open windows/tabs equals `count`.

**Selenium API**: `len(driver.window_handles)`

**Parameters**:

- `count` (`int`): Expected number of windows.

**Example**:

```python
expect(driver).to_have_window_count(2)
```

---

### `to_have_window_count_greater_than(n)`

Asserts that the number of windows is greater than `n`.

**Selenium API**: `len(driver.window_handles) > n`

**Parameters**:

- `n` (`int`): Minimum exclusive count.

**Example**:

```python
expect(driver).to_have_window_count_greater_than(1)
```

---

### `to_have_window_count_less_than(n)`

Asserts that the number of windows is less than `n`.

**Selenium API**: `len(driver.window_handles) < n`

**Parameters**:

- `n` (`int`): Maximum exclusive count.

**Example**:

```python
expect(driver).to_have_window_count_less_than(5)
```

---

### `to_have_window_handle(handle)`

Asserts that `driver.current_window_handle` equals `handle`.

**Selenium API**: `driver.current_window_handle`

**Parameters**:

- `handle` (`str`): Expected window handle.

**Example**:

```python
expect(driver).to_have_window_handle(original_handle)
```

---

### `to_have_new_window_opened(previous_handles)`

Asserts that a new window has opened since `previous_handles` was captured.

**Selenium API**: new handle not in `previous_handles`

**Parameters**:

- `previous_handles` (`list[str]`): Window handles captured before the action.

**Example**:

```python
before = driver.window_handles
driver.find_element(By.LINK_TEXT, "Open").click()
expect(driver).to_have_new_window_opened(before)
```

## Browser / capabilities

### `to_have_browser_name(name)`

Asserts that `driver.name` equals `name`.

**Selenium API**: `driver.name`

**Parameters**:

- `name` (`str`): Expected browser name (e.g. `"chrome"`, `"firefox"`).

**Example**:

```python
expect(driver).to_have_browser_name("chrome")
```

---

### `to_have_orientation(orientation)`

Asserts that the browser orientation equals `orientation`.

**Selenium API**: `driver.orientation`

**Parameters**:

- `orientation` (`str`): Expected orientation (`"PORTRAIT"` or `"LANDSCAPE"`).

**Example**:

```python
expect(driver).to_have_orientation("LANDSCAPE")
```

---

### `to_have_capability(key, value)`

Asserts that `driver.capabilities[key]` equals `value`.

**Selenium API**: `driver.capabilities[key]`

**Parameters**:

- `key` (`str`): Capability key.
- `value` (`Any`): Expected capability value.

**Example**:

```python
expect(driver).to_have_capability("browserVersion", "120.0")
```

---

### `to_have_capability_contains(key, value)`

Asserts that `value` is a substring of `str(driver.capabilities[key])`.

**Selenium API**: `value in str(driver.capabilities[key])`

**Parameters**:

- `key` (`str`): Capability key.
- `value` (`Any`): Expected substring.

**Example**:

```python
expect(driver).to_have_capability_contains("browserVersion", "120")
```

## Page source

### `to_have_page_source_contains(text)`

Asserts that `text` is found in `driver.page_source`.

**Selenium API**: `text in driver.page_source`

**Parameters**:

- `text` (`str`): Expected substring of the page source.

**Example**:

```python
expect(driver).to_have_page_source_contains("Welcome")
```

---

### `to_have_page_source_matches(pattern)`

Asserts that `re.search(pattern, driver.page_source)` finds a match.

**Selenium API**: `re.search(pattern, driver.page_source)`

**Parameters**:

- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(driver).to_have_page_source_matches(r"<title>Dashboard</title>")
```

---

### `to_have_page_source_not_contains(text)`

Asserts that `text` is not found in `driver.page_source`.

**Selenium API**: `text not in driver.page_source`

**Parameters**:

- `text` (`str`): Text that should not be present.

**Example**:

```python
expect(driver).to_have_page_source_not_contains("Error")
```

## Window position / size / rect

### `to_have_window_position(x, y)`

Asserts that the window position matches `(x, y)`.

**Selenium API**: `driver.get_window_position()`

**Parameters**:

- `x` (`int`): Expected X coordinate.
- `y` (`int`): Expected Y coordinate.

**Example**:

```python
expect(driver).to_have_window_position(0, 0)
```

---

### `to_have_window_size(width, height)`

Asserts that the window size matches `(width, height)`.

**Selenium API**: `driver.get_window_size()`

**Parameters**:

- `width` (`int`): Expected width in pixels.
- `height` (`int`): Expected height in pixels.

**Example**:

```python
expect(driver).to_have_window_size(1280, 800)
```

---

### `to_have_window_rect(x, y, width, height)`

Asserts that the window rect matches all four values.

**Selenium API**: `driver.get_window_rect()`

**Parameters**:

- `x` (`int`): Expected X coordinate.
- `y` (`int`): Expected Y coordinate.
- `width` (`int`): Expected width.
- `height` (`int`): Expected height.

**Example**:

```python
expect(driver).to_have_window_rect(0, 0, 1280, 800)
```

## Active element

### `to_have_active_element_tag(tag)`

Asserts that the active element's tag name equals `tag`.

**Selenium API**: `driver.switch_to.active_element.tag_name`

**Parameters**:

- `tag` (`str`): Expected tag name.

**Example**:

```python
expect(driver).to_have_active_element_tag("input")
```

---

### `to_have_active_element_id(id)`

Asserts that the active element's `id` attribute equals `id`.

**Selenium API**: `driver.switch_to.active_element.get_attribute("id")`

**Parameters**:

- `id` (`str`): Expected element ID.

**Example**:

```python
expect(driver).to_have_active_element_id("username")
```

---

### `to_have_active_element_class(class_name)`

Asserts that the active element has `class_name` in its class list.

**Selenium API**: `driver.switch_to.active_element.get_attribute("class")`

**Parameters**:

- `class_name` (`str`): Expected class name.

**Example**:

```python
expect(driver).to_have_active_element_class("focused")
```

## Tips and common patterns

### Waiting for page load

```python
# Wait for the page to finish loading
expect(driver).to_have_ready_state("complete", timeout=30)

# Then verify the title
expect(driver).to_have_title("Dashboard")
```

### Verifying a redirect

```python
# Navigate to a page that should redirect
driver.get("https://app.example.com/old-page")

# Wait for the URL to change
expect(driver).to_have_url("https://app.example.com/new-page", timeout=10)

# Or check that the URL has changed from the original
expect(driver).to_have_url_changes("https://app.example.com/old-page", timeout=10)
```

### Working with multiple windows/tabs

```python
# Store current handles before clicking a link that opens a new window
original_handles = driver.window_handles
driver.find_element(By.LINK_TEXT, "Open in new tab").click()

# Wait for the new window to appear
expect(driver).to_have_new_window_opened(original_handles, timeout=10)

# Switch to the new window
new_handles = [h for h in driver.window_handles if h not in original_handles]
driver.switch_to.window(new_handles[0])

# Assert on the new window
expect(driver).to_have_title("New Window Title")
```

### Chaining driver assertions

```python
# Chain multiple page-level checks
expect(driver).to_have_title("Dashboard").to_have_url_contains("/dashboard").to_have_ready_state("complete")
```

### Checking browser capabilities

```python
# Verify the browser supports headless mode
expect(driver).to_have_capability("browserName", "chrome")

# Check a specific capability value
expect(driver).to_have_capability("platformName", "linux")

# Check that a capability contains a value
expect(driver).to_have_capability_contains("browserVersion", "120")
```

### Verifying page source content

```python
# Check that specific text appears in the page source
expect(driver).to_have_page_source_contains("Copyright 2024")

# Use regex for more flexible matching
expect(driver).to_have_page_source_matches(r"User ID:\s*\d+")

# Verify text is NOT in the page source
expect(driver).to_have_page_source_not_contains("Error:")
```

### Active element assertions

```python
# After clicking a field, verify it's focused
driver.find_element(By.ID, "username").click()
expect(driver).to_have_active_element_id("username")
expect(driver).to_have_active_element_tag("input")

# After Tab navigation, verify the next field is focused
from selenium.webdriver.common.keys import Keys
driver.find_element(By.ID, "username").send_keys(Keys.TAB)
expect(driver).to_have_active_element_id("password")
```
