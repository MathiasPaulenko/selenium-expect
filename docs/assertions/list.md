# List assertions

`expect(elements)` where `elements` is a `list[WebElement]` returns an `ExpectList` instance, which provides assertions for count, text, values, and aggregate state.

## Count

### `to_have_count(count)`

Asserts that `len(elements)` equals `count`.

**Selenium API**: `len(elements)`

**Parameters**:

- `count` (`int`): Expected number of elements.

**Example**:

```python
items = driver.find_elements(By.CSS_SELECTOR, ".item")
expect(items).to_have_count(5)
```

**Negation**:

```python
expect(items).not_.to_have_count(0)
```

---

### `to_have_count_greater_than(n)`

Asserts that `len(elements) > n`.

**Selenium API**: `len(elements) > n`

**Parameters**:

- `n` (`int`): Minimum exclusive count.

**Example**:

```python
expect(items).to_have_count_greater_than(0)
```

---

### `to_have_count_less_than(n)`

Asserts that `len(elements) < n`.

**Selenium API**: `len(elements) < n`

**Parameters**:

- `n` (`int`): Maximum exclusive count.

**Example**:

```python
expect(items).to_have_count_less_than(10)
```

---

### `to_have_count_greater_than_or_equal(n)`

Asserts that `len(elements) >= n`.

**Selenium API**: `len(elements) >= n`

**Parameters**:

- `n` (`int`): Minimum inclusive count.

**Example**:

```python
expect(items).to_have_count_greater_than_or_equal(1)
```

---

### `to_have_count_less_than_or_equal(n)`

Asserts that `len(elements) <= n`.

**Selenium API**: `len(elements) <= n`

**Parameters**:

- `n` (`int`): Maximum inclusive count.

**Example**:

```python
expect(items).to_have_count_less_than_or_equal(10)
```

## Text

### `to_have_texts(texts)`

Asserts that the list of element texts equals `texts` (order-sensitive).

**Selenium API**: `[el.text for el in elements]`

**Parameters**:

- `texts` (`list[str]`): Expected texts in order.

**Example**:

```python
expect(items).to_have_texts(["Apple", "Banana", "Cherry"])
```

---

### `to_have_texts_contains(texts)`

Asserts that each expected text is found in the corresponding element's text.

**Selenium API**: `expected in el.text for each`

**Parameters**:

- `texts` (`list[str]`): Expected substrings in order.

**Example**:

```python
expect(items).to_have_texts_contains(["App", "Ban", "Cher"])
```

---

### `to_have_texts_contain(text)`

Asserts that at least one element's text contains `text`.

**Selenium API**: `any(text in el.text for el in elements)`

**Parameters**:

- `text` (`str`): Expected substring in at least one element.

**Example**:

```python
expect(items).to_have_texts_contain("Banana")
```

---

### `to_have_text_at(index, text)`

Asserts that `elements[index].text` equals `text`.

**Selenium API**: `elements[index].text`

**Parameters**:

- `index` (`int`): Element index.
- `text` (`str`): Expected text.

**Example**:

```python
expect(items).to_have_text_at(0, "Apple")
```

---

### `to_have_texts_match(patterns)`

Asserts that each element's text matches the corresponding regex pattern.

**Selenium API**: `re.search(pattern, el.text) for each`

**Parameters**:

- `patterns` (`list[str]`): Regex patterns in order.

**Example**:

```python
expect(items).to_have_texts_match([r"App\w+", r"Ban\w+", r"Cher\w+"])
```

## Values

### `to_have_values(values)`

Asserts that the list of element values equals `values` (order-sensitive).

**Selenium API**: `[el.get_attribute("value") for el in elements]`

**Parameters**:

- `values` (`list[str]`): Expected values in order.

**Example**:

```python
expect(inputs).to_have_values(["john", "john@example.com"])
```

---

### `to_have_values_contains(values)`

Asserts that each expected value is a substring of the corresponding element's value.

**Selenium API**: `expected in el.get_attribute("value") for each`

**Parameters**:

- `values` (`list[str]`): Expected substrings in order.

**Example**:

```python
expect(inputs).to_have_values_contains(["jo", "john@"])
```

---

### `to_have_value_at(index, value)`

Asserts that `elements[index].get_attribute("value")` equals `value`.

**Selenium API**: `elements[index].get_attribute("value")`

**Parameters**:

- `index` (`int`): Element index.
- `value` (`str`): Expected value.

**Example**:

```python
expect(inputs).to_have_value_at(0, "john")
```

## Aggregate state

### `to_have_all_visible()`

Asserts that every element in the list is displayed.

**Selenium API**: `all(el.is_displayed() for el in elements)`

**Example**:

```python
expect(items).to_have_all_visible()
```

---

### `to_have_any_visible()`

Asserts that at least one element in the list is displayed.

**Selenium API**: `any(el.is_displayed() for el in elements)`

**Example**:

```python
expect(items).to_have_any_visible()
```

---

### `to_have_all_enabled()`

Asserts that every element in the list is enabled.

**Selenium API**: `all(el.is_enabled() for el in elements)`

**Example**:

```python
expect(inputs).to_have_all_enabled()
```

---

### `to_have_all_selected()`

Asserts that every element in the list is selected.

**Selenium API**: `all(el.is_selected() for el in elements)`

**Example**:

```python
expect(checkboxes).to_have_all_selected()
```

## Tips and common patterns

### Waiting for a dynamic list to populate

```python
from selenium.webdriver.common.by import By

# Wait for search results to appear
results = driver.find_elements(By.CSS_SELECTOR, ".search-result")
expect(results).to_have_count(10, timeout=15)

# Or wait for at least one result
expect(results).to_be_not_empty(timeout=10)

# Wait for at least 5 results
expect(results).to_have_count_greater_than(4, timeout=15)
```

### Verifying table row texts

```python
# Get all rows in a table body
rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

# Verify exact ordered texts
expect(rows).to_have_texts(["Alice", "Bob", "Charlie"])

# Verify texts in any order (e.g., sorted by different columns)
expect(rows).to_have_texts_in_any_order("Bob", "Alice", "Charlie")

# Verify each row contains a substring
expect(rows).to_have_all_texts_contain("@")

# Verify no row contains an error
expect(rows).to_have_none_text_contain("Error")
```

### Working with form field lists

```python
# Get all input fields in a form
inputs = driver.find_elements(By.CSS_SELECTOR, "form input")

# Verify all are enabled
expect(inputs).to_have_all_enabled()

# Verify all are visible
expect(inputs).to_have_all_visible()

# Verify values match expected order
expect(inputs).to_have_values(["alice", "secret", ""])

# Verify value at a specific index
expect(inputs).to_have_value_at(0, "alice")

# Verify attribute at a specific index
expect(inputs).to_have_attribute_at(1, "type", "password")

# Verify all inputs have the same attribute value
expect(inputs).to_have_all_attribute("type", "text")

# Verify at least one input has a specific attribute value
expect(inputs).to_have_any_attribute("required", "true")
```

### Checking visibility of dynamic elements

```python
# Get all loading indicators
spinners = driver.find_elements(By.CLASS_NAME, "spinner")

# Wait for all spinners to be hidden
expect(spinners).to_have_none_visible(timeout=10)

# Or wait for at least one to be visible
expect(spinners).to_have_any_visible(timeout=5)

# Verify all are visible
expect(spinners).to_have_all_visible()
```

### Verifying specific elements by index

```python
items = driver.find_elements(By.CSS_SELECTOR, ".list-item")

# First item text
expect(items).to_have_first_text("Home")

# Last item text
expect(items).to_have_last_text("Contact")

# Text at index 2
expect(items).to_have_text_at(2, "About")

# Text at index 1 contains a substring
expect(items).to_have_nth_text_contains(1, "Products")

# Any item has exact text
expect(items).to_have_any_text("Services")
```

### Negation with list assertions

```python
# List does NOT have exactly 0 items
expect(items).not_.to_be_empty()

# List does NOT have 5 items
expect(items).not_.to_have_count(5)

# Not all items are visible
expect(items).not_.to_have_all_visible()

# No item contains "Error"
expect(items).not_.to_have_any_text_contain("Error")
```
