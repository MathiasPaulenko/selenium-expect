# expect.poll()

`expect.poll(fn)` wraps any zero-arg callable and provides Playwright-style assertion methods that retry until the function's return value satisfies the condition or the timeout expires.

## Usage

```python
from selenium_expect import expect

expect.poll(lambda: driver.execute_script("return document.readyState")).to_equal("complete")
```

## Available methods

### `to_equal(expected)`

Asserts `fn() == expected`.

```python
expect.poll(lambda: my_api.get_status()).to_equal("ready")
```

### `to_be_truthy()`

Asserts `bool(fn())` is `True`.

```python
expect.poll(lambda: driver.execute_script("return window.appReady")).to_be_truthy()
```

### `to_be_falsy()`

Asserts `bool(fn())` is `False`.

```python
expect.poll(lambda: driver.execute_script("return document.hidden")).to_be_falsy()
```

### `to_be_none()`

Asserts `fn()` is `None`.

```python
expect.poll(lambda: driver.execute_script("return window.pendingRequest")).to_be_none()
```

### `to_contain(expected)`

Asserts `expected in fn()`.

```python
expect.poll(lambda: driver.execute_script("return document.body.innerText")).to_contain("Welcome")
```

### `to_match(pattern)`

Asserts `re.search(pattern, str(fn()))` finds a match.

```python
expect.poll(lambda: driver.current_url).to_match(r"https://\w+\.example\.com")
```

### `to_be_greater_than(expected)`

Asserts `fn() > expected`.

```python
expect.poll(lambda: len(driver.find_elements(By.CSS_SELECTOR, ".item"))).to_be_greater_than(0)
```

### `to_be_less_than(expected)`

Asserts `fn() < expected`.

```python
expect.poll(lambda: driver.execute_script("return document.querySelectorAll('.error').length")).to_be_less_than(1)
```

### `to_be_in_list(expected)`

Asserts `fn() in expected`.

```python
expect.poll(lambda: my_api.get_status()).to_be_in_list(["ready", "idle"])
```

### `to_have_length(expected)`

Asserts `len(fn()) == expected`.

```python
expect.poll(lambda: driver.find_elements(By.CSS_SELECTOR, ".item")).to_have_length(5)
```

## Timeout and polling

```python
expect.poll(fn, timeout=10, polling=0.2).to_equal("done")
expect.poll(fn, polling=[0.1, 0.2, 0.5]).to_equal("done")
```

## Standalone `poll()`

You can also use the standalone `poll` function:

```python
from selenium_expect import poll

poll(lambda: driver.execute_script("return document.readyState"), timeout=10).to_equal("complete")
```
