# Alert assertions

`expect(alert)` returns an `ExpectAlert` instance, which provides assertions for JavaScript `Alert` objects.

## Presence

### `to_be_present()`

Asserts that the alert is present (accessing `alert.text` does not raise).

**Selenium API**: `driver.switch_to.alert` (no exception)

**Example**:

```python
from selenium.webdriver.common.alert import Alert

alert = driver.switch_to.alert
expect(alert).to_be_present()
```

**Negation**:

```python
expect(alert).not_.to_be_present()
```

## Text

### `to_have_text(text)`

Asserts that `alert.text` equals `text`.

**Selenium API**: `alert.text`

**Parameters**:

- `text` (`str`): Expected alert text.

**Example**:

```python
expect(alert).to_have_text("Are you sure?")
```

---

### `to_have_text_contains(text)`

Asserts that `text` is a substring of `alert.text`.

**Selenium API**: `text in alert.text`

**Parameters**:

- `text` (`str`): Expected substring.

**Example**:

```python
expect(alert).to_have_text_contains("sure")
```

---

### `to_have_text_matches(pattern)`

Asserts that `re.search(pattern, alert.text)` finds a match.

**Selenium API**: `re.search(pattern, alert.text)`

**Parameters**:

- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(alert).to_have_text_matches(r"Are you .*\?")
```

## Tips and common patterns

### Handling confirmation dialogs

```python
from selenium.webdriver.common.by import By

# Trigger a confirmation dialog
driver.find_element(By.ID, "delete-button").click()

# Wait for the alert to appear
alert = driver.switch_to.alert
expect(alert).to_be_present(timeout=5)

# Verify the alert text
expect(alert).to_have_text("Are you sure you want to delete this item?")

# Accept the confirmation
alert.accept()

# Verify the alert is gone
expect(alert).not_.to_be_present(timeout=3)
```

### Handling prompt dialogs

```python
# Trigger a prompt dialog
driver.find_element(By.ID, "rename-button").click()

alert = driver.switch_to.alert
expect(alert).to_be_present()

# Verify the prompt message
expect(alert).to_have_text_contains("Enter new name")

# Provide input and accept
alert.send_keys("New Name")
alert.accept()
```

### Verifying alert text with patterns

```python
alert = driver.switch_to.alert
expect(alert).to_be_present()

# Exact match
expect(alert).to_have_text("Delete file 'report.pdf'?")

# Partial match — useful when the filename is dynamic
expect(alert).to_have_text_contains("Delete file")

# Regex match — extract dynamic content
expect(alert).to_have_text_matches(r"Delete file '(.+)'")
```

### Waiting for an alert to disappear

```python
# After accepting/dismissing, verify no alert is present
alert = driver.switch_to.alert
alert.accept()

# The alert should no longer be present
expect(alert).not_.to_be_present(timeout=5)
```
