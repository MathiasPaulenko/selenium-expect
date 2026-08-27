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

## More examples

### Waiting for an API call to complete

```python
# Poll a JavaScript variable that's set when an API call finishes
expect.poll(
    lambda: driver.execute_script("return window.apiResponse?.status"),
    timeout=30,
    polling=0.5,
).to_equal("success")
```

### Waiting for a specific number of elements

```python
from selenium.webdriver.common.by import By

# Wait until at least 10 search results are loaded
expect.poll(
    lambda: len(driver.find_elements(By.CSS_SELECTOR, ".search-result")),
    timeout=15,
).to_be_greater_than(9)
```

### Waiting for a URL to match a pattern

```python
import re

# Wait for a redirect to complete
expect.poll(lambda: driver.current_url).to_match(r"https://app\.example\.com/dashboard")
```

### Waiting for a cookie to be set

```python
# Wait for a cookie to appear
expect.poll(
    lambda: driver.get_cookie("auth_token"),
    timeout=10,
).to_be_truthy()
```

### Waiting for page to be fully loaded

```python
# Wait for document.readyState to be 'complete'
expect.poll(
    lambda: driver.execute_script("return document.readyState"),
    timeout=30,
    polling=[0.1, 0.2, 0.5, 1.0],
).to_equal("complete")

# Also verify no pending AJAX requests (jQuery)
expect.poll(
    lambda: driver.execute_script("return jQuery.active"),
    timeout=10,
).to_equal(0)
```

### Negation with poll

```python
# Wait until a loading flag is falsy
expect.poll(
    lambda: driver.execute_script("return window.isLoading"),
    timeout=15,
).to_be_falsy()

# Wait until there are no error elements
expect.poll(
    lambda: len(driver.find_elements(By.CLASS_NAME, "error")),
    timeout=10,
).to_be_less_than(1)
```
