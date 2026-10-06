# Iframe assertions

Iframe assertions are available via `expect(driver)` (inherited by `ExpectDriver`). They operate on `driver.find_elements(By.TAG_NAME, "iframe")` and frame switching.

## Availability

### `to_have_frame_available(frame_id)`

Asserts that switching to the given iframe succeeds. The previous frame context is restored afterwards.

**Selenium API**: `driver.switch_to.frame(frame_id)` (no exception)

**Parameters**:

- `frame_id` (`str | int`): frame name/id or 0-based index (anything `switch_to.frame` accepts).

**Example**:

```python
expect(driver).to_have_frame_available(0)
```

**Negation**:

```python
expect(driver).not_.to_have_frame_available(99)
```

## Count

### `to_have_frame_count(count)`

Asserts that the number of iframes on the page equals `count`.

**Selenium API**: `len(driver.find_elements(By.TAG_NAME, "iframe"))`

**Parameters**:

- `count` (`int`): Expected number of iframes.

**Example**:

```python
expect(driver).to_have_frame_count(2)
```

---

### `to_have_frame_count_greater_than(n)`

Asserts that the number of iframes is greater than `n`.

**Selenium API**: `len(driver.find_elements(By.TAG_NAME, "iframe")) > n`

**Parameters**:

- `n` (`int`): Minimum exclusive count.

**Example**:

```python
expect(driver).to_have_frame_count_greater_than(0)
```

## Content

### `to_have_frame_text(frame_id, text)`

Asserts that the page source of the given iframe contains `text`. The previous frame context is restored afterwards.

**Selenium API**: switch to frame, check `text in driver.page_source`, switch back

**Parameters**:

- `frame_id` (`str | int`): frame name/id or 0-based index.
- `text` (`str`): Expected substring of the frame's page source.

**Example**:

```python
expect(driver).to_have_frame_text(0, "Hello from iframe")
```

## Frame context

### `to_be_in_frame()`

Asserts that the driver is currently inside a frame (not in default content). Checks `window.frameElement` via `execute_script` — no context switching.

**Example**:

```python
driver.switch_to.frame(0)
expect(driver).to_be_in_frame()
```

---

### `to_be_in_default_content()`

Asserts that the driver is in the default content (not inside a frame). Checks `window.frameElement` via `execute_script` — no context switching.

**Example**:

```python
driver.switch_to.default_content()
expect(driver).to_be_in_default_content()
```

## Tips and common patterns

### Working with iframes

```python
from selenium.webdriver.common.by import By

# Verify an iframe is available on the page
expect(driver).to_have_frame_available("content-frame", timeout=10)

# Verify the number of iframes
expect(driver).to_have_frame_count(3)
expect(driver).to_have_frame_count_greater_than(0)

# Verify iframe text content
expect(driver).to_have_frame_text("content-frame", "Welcome")
```

### Switching to an iframe and back

```python
# Switch to an iframe
driver.switch_to.frame("content-frame")

# Verify we're in the iframe context
expect(driver).to_be_in_frame()

# Perform assertions inside the iframe
heading = driver.find_element(By.TAG_NAME, "h1")
expect(heading).to_have_text("Welcome")

# Switch back to the main document
driver.switch_to.default_content()

# Verify we're back in the default content
expect(driver).to_be_in_default_content()
```

### Negation

```python
# Iframe is NOT available
expect(driver).not_.to_have_frame_available("removed-frame")

# We are NOT in an iframe
expect(driver).not_.to_be_in_frame()

# There are NOT 5 iframes
expect(driver).not_.to_have_frame_count(5)
```
