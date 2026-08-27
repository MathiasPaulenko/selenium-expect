# Shadow DOM assertions

`expect(shadow_root)` returns an `ExpectShadow` instance when the target is a Selenium `ShadowRoot` object. It provides assertions for finding elements within a shadow root.

```python
host = driver.find_element(By.CSS_SELECTOR, "my-component")
shadow = host.shadow_root
expect(shadow).to_have_element(By.CSS_SELECTOR, "button")
```

## Elements

### `to_have_element(by, value)`

Asserts that `shadow_root.find_element(by, value)` does not raise `NoSuchElementException`.

**Selenium API**: `shadow_root.find_element(by, value)`

**Parameters**:

- `by` (`str`): Locator strategy (e.g. `By.CSS_SELECTOR`).
- `value` (`str`): Locator value.

**Example**:

```python
expect(shadow).to_have_element(By.CSS_SELECTOR, "button")
```

**Negation**:

```python
expect(shadow).not_.to_have_element(By.CSS_SELECTOR, ".hidden")
```

---

### `to_have_element_count(by, value, count)`

Asserts that `len(shadow_root.find_elements(by, value))` equals `count`.

**Selenium API**: `len(shadow_root.find_elements(by, value))`

**Parameters**:

- `by` (`str`): Locator strategy.
- `value` (`str`): Locator value.
- `count` (`int`): Expected number of elements.

**Example**:

```python
expect(shadow).to_have_element_count(By.CSS_SELECTOR, "li", 3)
```

---

### `to_have_element_text(by, value, text)`

Asserts that `shadow_root.find_element(by, value).text` equals `text`.

**Selenium API**: `shadow_root.find_element(by, value).text`

**Parameters**:

- `by` (`str`): Locator strategy.
- `value` (`str`): Locator value.
- `text` (`str`): Expected text.

**Example**:

```python
expect(shadow).to_have_element_text(By.CSS_SELECTOR, "span", "Hello")
```

---

### `to_have_element_attribute(by, value, attr, attr_value)`

Asserts that `shadow_root.find_element(by, value).get_attribute(attr)` equals `attr_value`.

**Selenium API**: `shadow_root.find_element(by, value).get_attribute(attr)`

**Parameters**:

- `by` (`str`): Locator strategy.
- `value` (`str`): Locator value.
- `attr` (`str`): Attribute name.
- `attr_value` (`str`): Expected attribute value.

**Example**:

```python
expect(shadow).to_have_element_attribute(By.CSS_SELECTOR, "button", "type", "submit")
```

---

### `to_have_element_visible(by, value)`

Asserts that `shadow_root.find_element(by, value).is_displayed()` is `True`.

**Selenium API**: `shadow_root.find_element(by, value).is_displayed()`

**Parameters**:

- `by` (`str`): Locator strategy.
- `value` (`str`): Locator value.

**Example**:

```python
expect(shadow).to_have_element_visible(By.CSS_SELECTOR, "button")
```

## Tips and common patterns

### Working with shadow DOM elements

```python
from selenium.webdriver.common.by import By

# Find the host element and get its shadow root
host = driver.find_element(By.CSS_SELECTOR, "my-widget")
shadow = host.shadow_root

# Verify the shadow root exists
expect(host).to_have_shadow_root()

# Verify elements inside the shadow DOM
expect(shadow).to_have_element(By.CSS_SELECTOR, "button")
expect(shadow).to_have_element_count(By.CSS_SELECTOR, "li", 5)
expect(shadow).to_have_element_text(By.CSS_SELECTOR, "span", "Hello")
expect(shadow).to_have_element_attribute(By.CSS_SELECTOR, "input", "type", "text")
expect(shadow).to_have_element_visible(By.CSS_SELECTOR, "button")
```

### Verifying shadow root absence

```python
# Verify an element does NOT have a shadow root
expect(element).to_have_shadow_root_absent()

# Or use negation
expect(element).not_.to_have_shadow_root()
```

### Negation with shadow DOM

```python
# Element is NOT in the shadow DOM
expect(shadow).not_.to_have_element(By.CSS_SELECTOR, ".hidden-element")

# Shadow DOM does NOT have 10 elements
expect(shadow).not_.to_have_element_count(By.CSS_SELECTOR, "li", 10)

# Element in shadow DOM is NOT visible
expect(shadow).not_.to_have_element_visible(By.CSS_SELECTOR, ".hidden")
```
