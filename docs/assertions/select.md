# Select / Dropdown assertions

`expect(select_element)` returns an `ExpectSelect` instance when the target is a Selenium `Select` object. It provides assertions for value, selected options, and option count.

```python
from selenium.webdriver.support.ui import Select

select = Select(driver.find_element(By.TAG_NAME, "select"))
expect(select).to_have_value("apple")
```

## Value

### `to_have_value(value)`

Asserts that the first selected option's value equals `value`.

**Selenium API**: `select.first_selected_option.get_attribute("value")`

**Parameters**:

- `value` (`str`): Expected selected value.

**Example**:

```python
expect(select).to_have_value("apple")
```

**Negation**:

```python
expect(select).not_.to_have_value("banana")
```

---

### `to_have_first_selected_value(value)`

Asserts that the first selected option's value equals `value` (alias of `to_have_value`).

**Selenium API**: `select.first_selected_option.get_attribute("value")`

**Parameters**:

- `value` (`str`): Expected selected value.

**Example**:

```python
expect(select).to_have_first_selected_value("apple")
```

---

### `to_have_selected_text(text)`

Asserts that the first selected option's visible text equals `text`.

**Selenium API**: `select.first_selected_option.text`

**Parameters**:

- `text` (`str`): Expected selected text.

**Example**:

```python
expect(select).to_have_selected_text("Apple")
```

---

### `to_have_selected_values(values)`

Asserts that the list of all selected option values equals `values`.

**Selenium API**: `[opt.get_attribute("value") for opt in select.all_selected_options]`

**Parameters**:

- `values` (`list[str]`): Expected selected values in order.

**Example**:

```python
expect(select).to_have_selected_values(["apple", "banana"])
```

---

### `to_have_selected_texts(texts)`

Asserts that the list of all selected option texts equals `texts`.

**Selenium API**: `[opt.text for opt in select.all_selected_options]`

**Parameters**:

- `texts` (`list[str]`): Expected selected texts in order.

**Example**:

```python
expect(select).to_have_selected_texts(["Apple", "Banana"])
```

---

### `to_have_selected_count(count)`

Asserts that the number of selected options equals `count`.

**Selenium API**: `len(select.all_selected_options)`

**Parameters**:

- `count` (`int`): Expected number of selected options.

**Example**:

```python
expect(select).to_have_selected_count(2)
```

---

### `to_have_selected_index(index)`

Asserts that the first selected option is at `index`.

**Selenium API**: `select.options.index(first_selected_option)`

**Parameters**:

- `index` (`int`): Expected 0-based index.

**Example**:

```python
expect(select).to_have_selected_index(0)
```

---

### `to_have_no_selection()`

Asserts that no options are selected.

**Selenium API**: `len(select.all_selected_options) == 0`

**Example**:

```python
expect(select).to_have_no_selection()
```

## Options

### `to_have_option_count(count)`

Asserts that the total number of options equals `count`.

**Selenium API**: `len(select.options)`

**Parameters**:

- `count` (`int`): Expected number of options.

**Example**:

```python
expect(select).to_have_option_count(5)
```

---

### `to_have_option_count_greater_than(n)`

Asserts that the number of options is greater than `n`.

**Selenium API**: `len(select.options) > n`

**Parameters**:

- `n` (`int`): Minimum exclusive count.

**Example**:

```python
expect(select).to_have_option_count_greater_than(0)
```

---

### `to_have_option_at_index(index, value)`

Asserts that `select.options[index].get_attribute("value")` equals `value`.

**Selenium API**: `select.options[index].get_attribute("value")`

**Parameters**:

- `index` (`int`): Option index.
- `value` (`str`): Expected option value.

**Example**:

```python
expect(select).to_have_option_at_index(0, "apple")
```

---

### `to_have_option(value)`

Asserts that an option with value `value` exists in the select.

**Selenium API**: `any(opt.get_attribute("value") == value for opt in select.options)`

**Parameters**:

- `value` (`str`): Expected option value.

**Example**:

```python
expect(select).to_have_option("apple")
```

---

### `to_have_option_text(text)`

Asserts that an option with visible text `text` exists in the select.

**Selenium API**: `any(opt.text == text for opt in select.options)`

**Parameters**:

- `text` (`str`): Expected option text.

**Example**:

```python
expect(select).to_have_option_text("Apple")
```

## Multiple / Single

### `to_be_multiple()`

Asserts that the select is a multi-select (`select.is_multiple` is `True`).

**Selenium API**: `select.is_multiple`

**Example**:

```python
expect(select).to_be_multiple()
```

---

### `to_be_single_select()`

Asserts that the select is a single-select (`select.is_multiple` is `False`).

**Selenium API**: `not select.is_multiple`

**Example**:

```python
expect(select).to_be_single_select()
```

## Tips and common patterns

### Working with single-select dropdowns

```python
from selenium.webdriver.support.ui import Select

select = Select(driver.find_element(By.ID, "country"))

# Verify the selected value
expect(select).to_have_value("us")
expect(select).to_have_first_selected_value("us")

# Verify the selected text
expect(select).to_have_selected_text("United States")

# Verify the selected index
expect(select).to_have_selected_index(0)

# Verify it's a single-select
expect(select).to_be_single_select()

# Verify no selection
expect(select).to_have_no_selection()
```

### Working with multi-select dropdowns

```python
select = Select(driver.find_element(By.ID, "tags"))

# Verify it's a multi-select
expect(select).to_be_multiple()

# Verify multiple selected values
expect(select).to_have_selected_values("python", "selenium")

# Verify multiple selected texts
expect(select).to_have_selected_texts("Python", "Selenium")

# Verify the number of selected options
expect(select).to_have_selected_count(2)
```

### Verifying dropdown options

```python
select = Select(driver.find_element(By.ID, "color"))

# Verify total option count
expect(select).to_have_option_count(5)

# Verify at least 3 options
expect(select).to_have_option_count_greater_than(2)

# Verify a specific option exists
expect(select).to_have_option("red")
expect(select).to_have_option_text("Red")

# Verify option at a specific index
expect(select).to_have_option_at_index(0, "red")
expect(select).to_have_option_at_index(1, "blue")
```

### Negation

```python
# Select does NOT have value "old_value"
expect(select).not_.to_have_value("old_value")

# Select is NOT multiple
expect(select).not_.to_be_multiple()

# Select does NOT have 10 options
expect(select).not_.to_have_option_count(10)

# "red" is NOT an option
expect(select).not_.to_have_option("red")
```
