# Custom matchers

Custom matchers let you extend `expect()` with your own assertion methods that integrate with the retry loop and negation.

## `@extend` decorator

Register a custom matcher function under a name. The function receives the assertion's target as its first argument and must return a `(bool, Any)` tuple — the bool indicates pass/fail, and the Any is the actual value for error reporting.

```python
from selenium_expect import extend

@extend("to_be_in_viewport")
def check_in_viewport(element):
    driver = element.parent
    script = """
    var rect = arguments[0].getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= window.innerHeight &&
        rect.right <= window.innerWidth
    );
    """
    in_viewport = driver.execute_script(script, element)
    return (in_viewport, "in viewport" if in_viewport else "out of viewport")
```

### Usage

Once registered, the matcher is available on any `expect()` call:

```python
expect(element).to_be_in_viewport()
expect(element).not_.to_be_in_viewport()
expect(element).to_be_in_viewport(timeout=5, polling=0.2)
```

Custom matchers work with:

- `expect(element)` — `ExpectElement`
- `expect(driver)` — `ExpectDriver`
- `expect(driver, by=By.ID, value="foo")` — `LocatorExpect` (re-finds on each poll)
- `expect(items)` — `ExpectList`
- `expect(alert)` — `ExpectAlert`
- `expect(select)` — `ExpectSelect`
- `expect(shadow_root)` — `ExpectShadow`

## `merge_expects()`

Combine custom matchers from multiple modules into the registry:

```python
from selenium_expect import merge_expects

import my_project.matchers
import my_project.custom_assertions

merge_expects(my_project.matchers, my_project.custom_assertions)
```

You can also pass importable strings:

```python
merge_expects("my_project.matchers", "my_project.custom_assertions")
```

## Matcher signature

```python
def my_matcher(target: Any, *args, **kwargs) -> tuple[bool, Any]:
    ...
    return (passed, actual_value)
```

- `target`: The object passed to `expect()` (e.g. `WebElement`, `WebDriver`).
- `*args, **kwargs`: Any additional arguments from the call site (excluding `timeout` and `polling`, which are consumed by the retry loop).
- Return: `(bool, Any)` where `bool` is `True` if the condition passed.

## Example: custom text matcher

```python
from selenium_expect import extend

@extend("to_have_trimmed_text")
def check_trimmed_text(element, expected: str):
    actual = element.text.strip()
    return (actual == expected, actual)

# Usage
expect(element).to_have_trimmed_text("Hello, World!")
```

## More examples

### Custom matcher with arguments

```python
from selenium_expect import extend

@extend("to_have_css_color")
def check_css_color(element, color: str):
    """Assert element has a specific CSS color property."""
    actual = element.value_of_css_property("color")
    return (actual == color, actual)

# Usage
expect(element).to_have_css_color("rgba(255, 0, 0, 1)")
expect(element).not_.to_have_css_color("rgba(0, 0, 0, 1)")
```

### Custom matcher for driver

```python
from selenium_expect import extend

@extend("to_have_scroll_position")
def check_scroll_position(driver, position: int):
    """Assert the page is scrolled to a specific Y position."""
    actual = driver.execute_script("return window.scrollY")
    return (actual == position, actual)

# Usage
expect(driver).to_have_scroll_position(0)
expect(driver).not_.to_have_scroll_position(500)
```

### Custom matcher with timeout and polling

```python
@extend("to_have_data_loaded")
def check_data_loaded(element):
    """Assert element has data-loaded='true' attribute."""
    actual = element.get_attribute("data-loaded")
    return (actual == "true", actual)

# Custom timeout and polling work automatically
expect(element).to_have_data_loaded(timeout=15, polling=0.5)
```

### Organizing matchers in a module

```python
# my_project/matchers.py
from selenium_expect import extend

@extend("to_be_in_viewport")
def check_in_viewport(element):
    driver = element.parent
    script = """
    var rect = arguments[0].getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= window.innerHeight &&
        rect.right <= window.innerWidth
    );
    """
    in_viewport = driver.execute_script(script, element)
    return (in_viewport, "in viewport" if in_viewport else "out of viewport")

@extend("to_have_data_loaded")
def check_data_loaded(element):
    actual = element.get_attribute("data-loaded")
    return (actual == "true", actual)

@extend("to_have_no_console_errors")
def check_no_console_errors(driver):
    errors = driver.execute_script(
        "return window.__consoleErrors || []"
    )
    return (len(errors) == 0, errors)
```

```python
# my_project/test_something.py
from selenium_expect import expect, merge_expects
import my_project.matchers

# Register all matchers from the module
merge_expects(my_project.matchers)

# Use them
expect(element).to_be_in_viewport()
expect(element).to_have_data_loaded()
expect(driver).to_have_no_console_errors()
