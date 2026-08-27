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

## More migration examples

### Wait for element to contain text

**Before**:

```python
WebDriverWait(driver, 10).until(lambda d: "Welcome" in d.find_element(By.ID, "greeting").text)
```

**After**:

```python
expect(driver.find_element(By.ID, "greeting")).to_have_text_contains("Welcome", timeout=10)
```

### Wait for element to be selected

**Before**:

```python
WebDriverWait(driver, 10).until(EC.element_to_be_selected((By.ID, "checkbox")))
```

**After**:

```python
expect(driver.find_element(By.ID, "checkbox")).to_be_selected(timeout=10)
```

### Wait for presence of element (even if not visible)

**Before**:

```python
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "hidden-div")))
```

**After**:

```python
expect(driver, by=By.ID, value="hidden-div").to_be_present(timeout=10)
```

### Wait for staleness of element

**Before**:

```python
element = driver.find_element(By.ID, "old-element")
WebDriverWait(driver, 10).until(EC.staleness_of(element))
```

**After**:

```python
# Use locator-based expect with negation to wait for element to be gone
expect(driver, by=By.ID, value="old-element").not_.to_be_present(timeout=10)
```

### Wait for alert

**Before**:

```python
WebDriverWait(driver, 10).until(EC.alert_is_present())
```

**After**:

```python
alert = driver.switch_to.alert
expect(alert).to_be_present(timeout=10)
```

### Complex custom condition

**Before**:

```python
def element_has_class(driver, locator, class_name):
    element = driver.find_element(*locator)
    return class_name in element.get_attribute("class")

WebDriverWait(driver, 10).until(element_has_class, (By.ID, "btn"), "active")
```

**After**:

```python
# Direct assertion
expect(driver.find_element(By.ID, "btn")).to_have_class_contain("active", timeout=10)

# Or with a custom matcher
@extend("to_have_class")
def check_class(element, class_name):
    classes = element.get_attribute("class") or ""
    return (class_name in classes.split(), classes)

expect(driver.find_element(By.ID, "btn")).to_have_class("active", timeout=10)
```
