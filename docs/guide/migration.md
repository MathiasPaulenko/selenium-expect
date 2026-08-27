# Migration from WebDriverWait

This guide helps you migrate from `WebDriverWait` + `expected_conditions` to `selenium-expect`.

## Before / After

### Wait for element to be visible

**Before**:

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "submit")))
```

**After**:

```python
expect(driver, by=By.ID, value="submit").to_be_visible(timeout=10)
```

### Wait for title

**Before**:

```python
WebDriverWait(driver, 10).until(EC.title_contains("Dashboard"))
```

**After**:

```python
expect(driver).to_have_title_contains("Dashboard", timeout=10)
```

### Wait for element to have text

**Before**:

```python
element = driver.find_element(By.ID, "status")
WebDriverWait(driver, 10).until(lambda d: element.text == "Ready")
```

**After**:

```python
expect(element).to_have_text("Ready", timeout=10)
```

### Wait for element to be clickable

**Before**:

```python
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "submit")))
```

**After**:

```python
expect(driver, by=By.ID, value="submit").to_be_clickable(timeout=10)
```

### Wait for number of windows

**Before**:

```python
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
```

**After**:

```python
expect(driver).to_have_window_count(2, timeout=10)
```

## Key differences

| Feature | `WebDriverWait` | `selenium-expect` |
|---|---|---|
| Syntax | `until(condition)` | `expect(target).to_*(...)` |
| Negation | `until_not(condition)` | `.not_.to_*(...)` |
| Polling | Fixed interval | Fixed or backoff schedule |
| Error messages | Minimal | Descriptive multi-line |
| Custom conditions | Write a callable | `@extend` decorator |
| Composition | Manual | `to_satisfy_all/any/none` |
| Soft assertions | Not available | Built-in |
| Stale elements | Manual handling | Locator-based auto re-find |

## Migration tips

1. **Replace `until` with `to_*`**: Most `expected_conditions` have a direct `expect()` equivalent.
2. **Use locator-based expect for dynamic elements**: `expect(driver, by=..., value=...)` avoids `StaleElementReferenceException`.
3. **Set global timeout once**: `set_default_timeout(10)` replaces repeating `WebDriverWait(driver, 10)`.
4. **Use `.not_` for negation**: Cleaner than `until_not`.
5. **Leverage soft assertions**: Check multiple things and report all failures at once.
