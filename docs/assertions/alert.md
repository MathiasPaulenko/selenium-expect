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
