# JavaScript / Browser state assertions

JavaScript and browser state assertions are available via `expect(driver)` (inherited by `ExpectDriver`). They use `driver.execute_script` to check JS state.

## JavaScript results

### `to_have_js_result(script, expected)`

Asserts that `driver.execute_script(script)` equals `expected`.

**Selenium API**: `driver.execute_script(script)`

**Parameters**:

- `script` (`str`): JavaScript to execute (must return a value).
- `expected` (`Any`): Expected return value.

**Example**:

```python
expect(driver).to_have_js_result("return document.readyState;", "complete")
```

**Negation**:

```python
expect(driver).not_.to_have_js_result("return document.hidden;", True)
```

---

### `to_have_js_result_contains(script, expected)`

Asserts that `expected` is found in the result of `driver.execute_script(script)`.

**Selenium API**: `expected in driver.execute_script(script)`

**Parameters**:

- `script` (`str`): JavaScript to execute.
- `expected` (`Any`): Expected contained value.

**Example**:

```python
expect(driver).to_have_js_result_contains(
    "return Array.from(document.querySelectorAll('p')).map(e => e.text);",
    "Hello",
)
```

---

### `to_have_async_js_result(script, expected)`

Asserts that `driver.execute_async_script(script)` equals `expected`.

**Selenium API**: `driver.execute_async_script(script)`

**Parameters**:

- `script` (`str`): Async JavaScript (must invoke the callback).
- `expected` (`Any`): Expected return value.

**Example**:

```python
expect(driver).to_have_async_js_result(
    "var callback = arguments[arguments.length - 1]; "
    "setTimeout(() => callback('done'), 500);",
    "done",
)
```

---

### `to_have_js_variable(name, expected)`

Asserts that a global JavaScript variable `window[name]` equals `expected`.

**Selenium API**: `driver.execute_script(f"return window[arguments[0]];", name)`

**Parameters**:

- `name` (`str`): Global variable name.
- `expected` (`Any`): Expected value.

**Example**:

```python
expect(driver).to_have_js_variable("appVersion", "2.0.1")
```

## localStorage

### `to_have_local_storage_item(key, value)`

Asserts that `localStorage.getItem(key)` equals `value`.

**Selenium API**: `driver.execute_script("return localStorage.getItem(arguments[0]);", key)`

**Parameters**:

- `key` (`str`): Storage key.
- `value` (`str`): Expected value.

**Example**:

```python
expect(driver).to_have_local_storage_item("theme", "dark")
```

---

### `to_have_local_storage_item_present(key)`

Asserts that `localStorage.getItem(key)` is not `None`.

**Selenium API**: `localStorage.getItem(key) is not None`

**Parameters**:

- `key` (`str`): Storage key.

**Example**:

```python
expect(driver).to_have_local_storage_item_present("theme")
```

---

### `to_have_local_storage_item_absent(key)`

Asserts that `localStorage.getItem(key)` is `None`.

**Selenium API**: `localStorage.getItem(key) is None`

**Parameters**:

- `key` (`str`): Storage key.

**Example**:

```python
expect(driver).to_have_local_storage_item_absent("deleted_key")
```

---

### `to_have_local_storage_length(length)`

Asserts that `localStorage.length` equals `length`.

**Selenium API**: `driver.execute_script("return localStorage.length;")`

**Parameters**:

- `length` (`int`): Expected number of items.

**Example**:

```python
expect(driver).to_have_local_storage_length(3)
```

## sessionStorage

### `to_have_session_storage_item(key, value)`

Asserts that `sessionStorage.getItem(key)` equals `value`.

**Selenium API**: `driver.execute_script("return sessionStorage.getItem(arguments[0]);", key)`

**Parameters**:

- `key` (`str`): Storage key.
- `value` (`str`): Expected value.

**Example**:

```python
expect(driver).to_have_session_storage_item("token", "abc123")
```

---

### `to_have_session_storage_item_present(key)`

Asserts that `sessionStorage.getItem(key)` is not `None`.

**Selenium API**: `sessionStorage.getItem(key) is not None`

**Parameters**:

- `key` (`str`): Storage key.

**Example**:

```python
expect(driver).to_have_session_storage_item_present("token")
```

---

### `to_have_session_storage_item_absent(key)`

Asserts that `sessionStorage.getItem(key)` is `None`.

**Selenium API**: `sessionStorage.getItem(key) is None`

**Parameters**:

- `key` (`str`): Storage key.

**Example**:

```python
expect(driver).to_have_session_storage_item_absent("expired_token")
```

---

### `to_have_session_storage_length(length)`

Asserts that `sessionStorage.length` equals `length`.

**Selenium API**: `driver.execute_script("return sessionStorage.length;")`

**Parameters**:

- `length` (`int`): Expected number of items.

**Example**:

```python
expect(driver).to_have_session_storage_length(2)
```

## Tips and common patterns

### Asserting on JavaScript execution results

```python
# Verify a JS expression returns a specific value
expect(driver).to_have_js_result("document.title", "Dashboard")

# Verify a JS expression returns a value containing a substring
expect(driver).to_have_js_result_contains("document.title", "Dash")

# Verify an async JS expression
expect(driver).to_have_async_js_result(
    "return await fetch('/api/status').then(r => r.json()).then(d => d.status)",
    "ok",
    timeout=10,
)

# Verify a JS variable value
expect(driver).to_have_js_variable("window.appVersion", "2.0.0")
```

### Working with localStorage

```python
# Verify a localStorage item exists
expect(driver).to_have_local_storage_item_present("authToken")

# Verify a localStorage item's value
expect(driver).to_have_local_storage_item("authToken", "abc123")

# Verify a localStorage item is absent
expect(driver).to_have_local_storage_item_absent("oldToken")

# Verify the number of localStorage items
expect(driver).to_have_local_storage_length(3)
```

### Working with sessionStorage

```python
# Verify a sessionStorage item exists
expect(driver).to_have_session_storage_item_present("tempData")

# Verify a sessionStorage item's value
expect(driver).to_have_session_storage_item("tempData", '{"page":1}')

# Verify a sessionStorage item is absent
expect(driver).to_have_session_storage_item_absent("clearedData")

# Verify the number of sessionStorage items
expect(driver).to_have_session_storage_length(2)
```

### Negation

```python
# JS result is NOT "loading"
expect(driver).not_.to_have_js_result("document.readyState", "loading")

# localStorage item is NOT present
expect(driver).not_.to_have_local_storage_item_present("oldToken")

# sessionStorage does NOT have 10 items
expect(driver).not_.to_have_session_storage_length(10)
```

### Real-world example — verifying SPA state

```python
# After a SPA navigates, verify the app state in localStorage
expect(driver).to_have_local_storage_item("currentRoute", "/dashboard")
expect(driver).to_have_local_storage_item_present("authToken")
expect(driver).to_have_js_variable("window.app.state", "loaded")
expect(driver).to_have_js_result("document.querySelector('#app').getAttribute('data-loaded')", "true")
```
