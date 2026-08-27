# Cookie assertions

Cookie assertions are available via `expect(driver)` (inherited by `ExpectDriver`). They operate on `driver.get_cookies()` and related methods.

## Presence

### `to_have_cookie(name)`

Asserts that a cookie with `name` exists.

**Selenium API**: `driver.get_cookie(name) is not None`

**Parameters**:

- `name` (`str`): Cookie name.

**Example**:

```python
expect(driver).to_have_cookie("session_id")
```

**Negation**:

```python
expect(driver).not_.to_have_cookie("deleted_cookie")
```

---

### `to_have_no_cookies()`

Asserts that no cookies are set.

**Selenium API**: `driver.get_cookies() == []`

**Example**:

```python
driver.delete_all_cookies()
expect(driver).to_have_no_cookies()
```

## Value

### `to_have_cookie_value(name, value)`

Asserts that `driver.get_cookie(name)["value"]` equals `value`.

**Selenium API**: `driver.get_cookie(name)["value"]`

**Parameters**:

- `name` (`str`): Cookie name.
- `value` (`str`): Expected cookie value.

**Example**:

```python
expect(driver).to_have_cookie_value("session_id", "abc123")
```

---

### `to_have_cookie_value_contains(name, value)`

Asserts that `value` is a substring of the cookie's value.

**Selenium API**: `value in driver.get_cookie(name)["value"]`

**Parameters**:

- `name` (`str`): Cookie name.
- `value` (`str`): Expected substring.

**Example**:

```python
expect(driver).to_have_cookie_value_contains("session_id", "abc")
```

## Properties

### `to_have_cookie_domain(name, domain)`

Asserts that `driver.get_cookie(name)["domain"]` equals `domain`.

**Selenium API**: `driver.get_cookie(name)["domain"]`

**Parameters**:

- `name` (`str`): Cookie name.
- `domain` (`str`): Expected domain.

**Example**:

```python
expect(driver).to_have_cookie_domain("session_id", "example.com")
```

---

### `to_have_cookie_path(name, path)`

Asserts that `driver.get_cookie(name)["path"]` equals `path`.

**Selenium API**: `driver.get_cookie(name)["path"]`

**Parameters**:

- `name` (`str`): Cookie name.
- `path` (`str`): Expected path.

**Example**:

```python
expect(driver).to_have_cookie_path("session_id", "/")
```

---

### `to_have_cookie_http_only(name)`

Asserts that `driver.get_cookie(name)["httpOnly"]` is `True`.

**Selenium API**: `driver.get_cookie(name)["httpOnly"]`

**Parameters**:

- `name` (`str`): Cookie name.

**Example**:

```python
expect(driver).to_have_cookie_http_only("session_id")
```

---

### `to_have_cookie_secure(name)`

Asserts that `driver.get_cookie(name)["secure"]` is `True`.

**Selenium API**: `driver.get_cookie(name)["secure"]`

**Parameters**:

- `name` (`str`): Cookie name.

**Example**:

```python
expect(driver).to_have_cookie_secure("session_id")
```

---

### `to_have_cookie_same_site(name, same_site)`

Asserts that `driver.get_cookie(name)["sameSite"]` equals `same_site`.

**Selenium API**: `driver.get_cookie(name)["sameSite"]`

**Parameters**:

- `name` (`str`): Cookie name.
- `same_site` (`str`): Expected SameSite value (`"Strict"`, `"Lax"`, or `"None"`).

**Example**:

```python
expect(driver).to_have_cookie_same_site("session_id", "Strict")
```

## Count

### `to_have_cookie_count(count)`

Asserts that `len(driver.get_cookies())` equals `count`.

**Selenium API**: `len(driver.get_cookies())`

**Parameters**:

- `count` (`int`): Expected number of cookies.

**Example**:

```python
expect(driver).to_have_cookie_count(3)
```

---

### `to_have_cookie_count_greater_than(n)`

Asserts that `len(driver.get_cookies()) > n`.

**Selenium API**: `len(driver.get_cookies()) > n`

**Parameters**:

- `n` (`int`): Minimum exclusive count.

**Example**:

```python
expect(driver).to_have_cookie_count_greater_than(0)
```

## Expiry

### `to_have_cookie_expiry(name, expiry)`

Asserts that `driver.get_cookie(name)["expiry"]` equals `expiry`.

**Selenium API**: `driver.get_cookie(name)["expiry"]`

**Parameters**:

- `name` (`str`): Cookie name.
- `expiry` (`int`): Expected expiry timestamp (Unix epoch seconds).

**Example**:

```python
expect(driver).to_have_cookie_expiry("session_id", 1735689600)
```
