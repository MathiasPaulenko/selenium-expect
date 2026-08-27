# Iframe assertions

Iframe assertions are available via `expect(driver)` (inherited by `ExpectDriver`). They operate on `driver.find_elements(By.TAG_NAME, "iframe")` and frame switching.

## Availability

### `to_have_frame_available(index)`

Asserts that switching to the iframe at `index` succeeds.

**Selenium API**: `driver.switch_to.frame(index)` (no exception)

**Parameters**:

- `index` (`int`): 0-based iframe index.

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

### `to_have_frame_text(index, text)`

Asserts that the text content of the iframe at `index` equals `text`.

**Selenium API**: switch to frame, read `driver.page_source` or body text

**Parameters**:

- `index` (`int`): 0-based iframe index.
- `text` (`str`): Expected text content.

**Example**:

```python
expect(driver).to_have_frame_text(0, "Hello from iframe")
```

## Frame context

### `to_be_in_frame()`

Asserts that the driver is currently inside a frame (not in default content).

**Selenium API**: `driver.switch_to.default_content()` then check

**Example**:

```python
driver.switch_to.frame(0)
expect(driver).to_be_in_frame()
```

---

### `to_be_in_default_content()`

Asserts that the driver is in the default content (not inside a frame).

**Selenium API**: `driver.switch_to.default_content()`

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
expect(driver).to_have_frame_available(By.ID, "content-frame", timeout=10)

# Verify the number of iframes
expect(driver).to_have_frame_count(3)
expect(driver).to_have_frame_count_greater_than(0)

# Verify iframe text content
expect(driver).to_have_frame_text(By.ID, "content-frame", "Welcome")
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
expect(driver).not_.to_have_frame_available(By.ID, "removed-frame")

# We are NOT in an iframe
expect(driver).not_.to_be_in_frame()

# There are NOT 5 iframes
expect(driver).not_.to_have_frame_count(5)
```
