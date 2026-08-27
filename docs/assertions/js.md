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
