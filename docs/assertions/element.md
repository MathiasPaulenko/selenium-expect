# Element assertions

`expect(element)` returns an `ExpectElement` instance, which provides assertions for `WebElement` state, text, attributes, CSS, identity, position, accessibility, and shadow DOM.

## State

### `to_be_visible()`

Asserts that `element.is_displayed()` is `True`.

**Selenium API**: `element.is_displayed()`

**Example**:

```python
expect(element).to_be_visible()
```

**Negation**:

```python
expect(element).not_.to_be_visible()
```

---

### `to_be_hidden()`

Asserts that `element.is_displayed()` is `False`.

**Selenium API**: `not element.is_displayed()`

**Example**:

```python
expect(element).to_be_hidden()
```

---

### `to_be_enabled()`

Asserts that `element.is_enabled()` is `True`.

**Selenium API**: `element.is_enabled()`

**Example**:

```python
expect(element).to_be_enabled()
```

---

### `to_be_disabled()`

Asserts that `element.is_enabled()` is `False`.

**Selenium API**: `not element.is_enabled()`

**Example**:

```python
expect(element).to_be_disabled()
```

---

### `to_be_checked()`

Asserts that `element.is_selected()` is `True` (checkbox/radio).

**Selenium API**: `element.is_selected()`

**Example**:

```python
expect(checkbox).to_be_checked()
```

---

### `to_be_selected()`

Asserts that `element.is_selected()` is `True` (option/checkbox/radio).

**Selenium API**: `element.is_selected()`

**Example**:

```python
expect(option).to_be_selected()
```

---

### `to_be_present()`

Asserts that the element exists in the DOM (accessing `tag_name` does not raise).

**Selenium API**: `element.tag_name` (no exception)

**Example**:

```python
expect(element).to_be_present()
```

---

### `to_be_absent()`

Asserts that the element does not exist (accessing `tag_name` raises `StaleElementReferenceException` or `NoSuchElementException`).

**Selenium API**: `StaleElementReferenceException` / `NoSuchElementException`

**Example**:

```python
expect(element).to_be_absent()
```

---

### `to_be_clickable()`

Asserts that the element is both displayed and enabled.

**Selenium API**: `element.is_displayed() and element.is_enabled()`

**Example**:

```python
expect(button).to_be_clickable()
```

---

### `to_be_stale()`

Asserts that the element is stale (any access raises `StaleElementReferenceException`).

**Selenium API**: `StaleElementReferenceException` on access

**Example**:

```python
expect(element).to_be_stale()
```

---

### `to_be_unselected()`

Asserts that `element.is_selected()` is `False`.

**Selenium API**: `not element.is_selected()`

**Example**:

```python
expect(checkbox).to_be_unselected()
```

---

### `to_be_unchecked()`

Asserts that `element.is_selected()` is `False` (semantic alias for `not_.to_be_checked()`).

**Selenium API**: `not element.is_selected()`

**Example**:

```python
expect(checkbox).to_be_unchecked()
```

---

### `to_be_focused()`

Asserts that the element is the active element.

**Selenium API**: `element == driver.switch_to.active_element`

**Example**:

```python
expect(input_field).to_be_focused()
```

---

### `to_be_editable()`

Asserts that the element is editable (input/textarea, not readonly, not disabled).

**Selenium API**: `element.is_enabled() and not element.get_attribute("readonly")`

**Example**:

```python
expect(input_field).to_be_editable()
```

---

### `to_be_readonly()`

Asserts that the element has a `readonly` attribute.

**Selenium API**: `element.get_attribute("readonly") is not None`

**Example**:

```python
expect(input_field).to_be_readonly()
```

---

### `to_be_empty()`

Asserts that `element.text.strip()` is empty.

**Selenium API**: `element.text.strip() == ""`

**Example**:

```python
expect(element).to_be_empty()
```

## Text

### `to_have_text(text)`

Asserts that `element.text` equals `text`.

**Selenium API**: `element.text`

**Parameters**:

- `text` (`str`): Expected text content.

**Example**:

```python
expect(element).to_have_text("Hello, World!")
```

---

### `to_have_text_contains(text)`

Asserts that `text` is a substring of `element.text`.

**Selenium API**: `text in element.text`

**Parameters**:

- `text` (`str`): Expected substring.

**Example**:

```python
expect(element).to_have_text_contains("Hello")
```

---

### `to_have_text_matches(pattern)`

Asserts that `re.search(pattern, element.text)` finds a match.

**Selenium API**: `re.search(pattern, element.text)`

**Parameters**:

- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(element).to_have_text_matches(r"Hello, .*!")
```

---

### `to_have_text_empty()`

Asserts that `element.text` is `""`.

**Selenium API**: `element.text == ""`

**Example**:

```python
expect(element).to_have_text_empty()
```

---

### `to_have_text_not_empty()`

Asserts that `element.text` is not empty.

**Selenium API**: `element.text != ""`

**Example**:

```python
expect(element).to_have_text_not_empty()
```

---

### `to_have_text_starting_with(prefix)`

Asserts that `element.text` starts with `prefix`.

**Selenium API**: `element.text.startswith(prefix)`

**Parameters**:

- `prefix` (`str`): Expected prefix.

**Example**:

```python
expect(element).to_have_text_starting_with("Loading")
```

---

### `to_have_text_ending_with(suffix)`

Asserts that `element.text` ends with `suffix`.

**Selenium API**: `element.text.endswith(suffix)`

**Parameters**:

- `suffix` (`str`): Expected suffix.

**Example**:

```python
expect(element).to_have_text_ending_with("...")
```

---

### `to_have_text_in_list(*texts)`

Asserts that `element.text` is one of `*texts`.

**Selenium API**: `element.text in texts`

**Parameters**:

- `*texts` (`str`): Acceptable text values.

**Example**:

```python
expect(element).to_have_text_in_list("Active", "Pending", "Done")
```

## Value

### `to_have_value(value)`

Asserts that `element.get_attribute("value")` equals `value`.

**Selenium API**: `element.get_attribute("value")`

**Parameters**:

- `value` (`str`): Expected value.

**Example**:

```python
expect(input_field).to_have_value("john@example.com")
```

---

### `to_have_value_contains(value)`

Asserts that `value` is a substring of `element.get_attribute("value")`.

**Selenium API**: `value in element.get_attribute("value")`

**Parameters**:

- `value` (`str`): Expected substring.

**Example**:

```python
expect(input_field).to_have_value_contains("john")
```

---

### `to_have_value_matches(pattern)`

Asserts that `re.search(pattern, element.get_attribute("value"))` finds a match.

**Selenium API**: `re.search(pattern, element.get_attribute("value"))`

**Parameters**:

- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(input_field).to_have_value_matches(r"\w+@\w+\.\w+")
```

---

### `to_have_value_in_list(values)`

Asserts that `element.get_attribute("value")` is in `values`.

**Selenium API**: `element.get_attribute("value") in values`

**Parameters**:

- `values` (`list[str]`): Acceptable values.

**Example**:

```python
expect(select_el).to_have_value_in_list(["active", "pending"])
```

## Attributes

### `to_have_attribute(name, value)`

Asserts that `element.get_attribute(name)` equals `value`.

**Selenium API**: `element.get_attribute(name)`

**Parameters**:

- `name` (`str`): Attribute name.
- `value` (`str`): Expected attribute value.

**Example**:

```python
expect(element).to_have_attribute("data-testid", "submit-btn")
```

---

### `to_have_attribute_contains(name, value)`

Asserts that `value` is a substring of `element.get_attribute(name)`.

**Selenium API**: `value in element.get_attribute(name)`

**Parameters**:

- `name` (`str`): Attribute name.
- `value` (`str`): Expected substring.

**Example**:

```python
expect(element).to_have_attribute_contains("class", "active")
```

---

### `to_have_attribute_matches(name, pattern)`

Asserts that `re.search(pattern, element.get_attribute(name))` finds a match.

**Selenium API**: `re.search(pattern, element.get_attribute(name))`

**Parameters**:

- `name` (`str`): Attribute name.
- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(element).to_have_attribute_matches("href", r"https://.*")
```

---

### `to_have_attribute_empty(name)`

Asserts that `element.get_attribute(name)` is `""` or `None`.

**Selenium API**: `element.get_attribute(name) in ("", None)`

**Parameters**:

- `name` (`str`): Attribute name.

**Example**:

```python
expect(element).to_have_attribute_empty("data-value")
```

---

### `to_have_attribute_present(name)`

Asserts that `element.get_attribute(name)` is not `None`.

**Selenium API**: `element.get_attribute(name) is not None`

**Parameters**:

- `name` (`str`): Attribute name.

**Example**:

```python
expect(element).to_have_attribute_present("disabled")
```

---

### `to_have_attribute_absent(name)`

Asserts that `element.get_attribute(name)` is `None`.

**Selenium API**: `element.get_attribute(name) is None`

**Parameters**:

- `name` (`str`): Attribute name.

**Example**:

```python
expect(element).to_have_attribute_absent("disabled")
```

---

### `to_have_attribute_in_list(name, values)`

Asserts that `element.get_attribute(name)` is in `values`.

**Selenium API**: `element.get_attribute(name) in values`

**Parameters**:

- `name` (`str`): Attribute name.
- `values` (`list[str]`): Acceptable values.

**Example**:

```python
expect(element).to_have_attribute_in_list("status", ["active", "pending"])
```

---

### `to_have_dom_attribute(name, value)`

Asserts that `element.get_dom_attribute(name)` equals `value`.

**Selenium API**: `element.get_dom_attribute(name)`

**Parameters**:

- `name` (`str`): DOM attribute name.
- `value` (`str`): Expected value.

**Example**:

```python
expect(element).to_have_dom_attribute("class", "btn-primary")
```

---

### `to_have_dom_attribute_contains(name, value)`

Asserts that `value` is a substring of `element.get_dom_attribute(name)`.

**Selenium API**: `value in element.get_dom_attribute(name)`

**Parameters**:

- `name` (`str`): DOM attribute name.
- `value` (`str`): Expected substring.

**Example**:

```python
expect(element).to_have_dom_attribute_contains("class", "btn")
```

---

### `to_have_property(name, value)`

Asserts that `element.get_property(name)` equals `value`.

**Selenium API**: `element.get_property(name)`

**Parameters**:

- `name` (`str`): Property name.
- `value` (`Any`): Expected property value.

**Example**:

```python
expect(checkbox).to_have_property("checked", True)
```

---

### `to_have_property_contains(name, value)`

Asserts that `value` is a substring of `str(element.get_property(name))`.

**Selenium API**: `value in str(element.get_property(name))`

**Parameters**:

- `name` (`str`): Property name.
- `value` (`str`): Expected substring.

**Example**:

```python
expect(element).to_have_property_contains("className", "active")
```

## CSS

### `to_have_css_property(name, value)`

Asserts that `element.value_of_css_property(name)` equals `value`.

**Selenium API**: `element.value_of_css_property(name)`

**Parameters**:

- `name` (`str`): CSS property name.
- `value` (`str`): Expected CSS value.

**Example**:

```python
expect(element).to_have_css_property("color", "rgba(255, 0, 0, 1)")
```

---

### `to_have_css_property_contains(name, value)`

Asserts that `value` is a substring of `element.value_of_css_property(name)`.

**Selenium API**: `value in element.value_of_css_property(name)`

**Parameters**:

- `name` (`str`): CSS property name.
- `value` (`str`): Expected substring.

**Example**:

```python
expect(element).to_have_css_property_contains("color", "255")
```

---

### `to_have_css_property_matches(name, pattern)`

Asserts that `re.search(pattern, element.value_of_css_property(name))` finds a match.

**Selenium API**: `re.search(pattern, element.value_of_css_property(name))`

**Parameters**:

- `name` (`str`): CSS property name.
- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(element).to_have_css_property_matches("color", r"rgba\(255,.*\)")
```

## Identity

### `to_have_tag(tag)`

Asserts that `element.tag_name` equals `tag`.

**Selenium API**: `element.tag_name`

**Parameters**:

- `tag` (`str`): Expected tag name.

**Example**:

```python
expect(element).to_have_tag("button")
```

---

### `to_have_id(id)`

Asserts that `element.get_attribute("id")` equals `id`.

**Selenium API**: `element.get_attribute("id")`

**Parameters**:

- `id` (`str`): Expected element ID.

**Example**:

```python
expect(element).to_have_id("submit-btn")
```

---

### `to_have_class(class_name)`

Asserts that `class_name` is in the element's class list.

**Selenium API**: `class_name in element.get_attribute("class").split()`

**Parameters**:

- `class_name` (`str`): Expected class name.

**Example**:

```python
expect(element).to_have_class("active")
```

---

### `to_have_class_contains(class_name)`

Asserts that `class_name` is a substring of the `class` attribute.

**Selenium API**: `class_name in element.get_attribute("class")`

**Parameters**:

- `class_name` (`str`): Expected substring.

**Example**:

```python
expect(element).to_have_class_contains("btn")
```

---

### `to_contain_class(class_name)`

Asserts that `class_name` is in the element's class list (alias of `to_have_class`).

**Selenium API**: `class_name in element.get_attribute("class").split()`

**Parameters**:

- `class_name` (`str`): Expected class name.

**Example**:

```python
expect(element).to_contain_class("active")
```

---

### `to_have_class_matching(pattern)`

Asserts that any class in the element's class list matches `pattern`.

**Selenium API**: `re.search(pattern, class) for class in classes`

**Parameters**:

- `pattern` (`str`): Regular expression pattern.

**Example**:

```python
expect(element).to_have_class_matching(r"btn-\w+")
```

---

### `to_have_all_classes(*classes)`

Asserts that the element has all specified classes.

**Selenium API**: `set(classes).issubset(elem_classes)`

**Parameters**:

- `*classes` (`str`): All required class names.

**Example**:

```python
expect(element).to_have_all_classes("btn", "btn-primary", "active")
```

---

### `to_have_class_in_list(*classes)`

Asserts that the element has at least one of the specified classes.

**Selenium API**: `any(class in elem_classes for class in classes)`

**Parameters**:

- `*classes` (`str`): Acceptable class names.

**Example**:

```python
expect(element).to_have_class_in_list("active", "pending")
```

## Position / Dimensions

### `to_have_location(x, y)`

Asserts that `element.location` matches `{"x": x, "y": y}`.

**Selenium API**: `element.location`

**Parameters**:

- `x` (`int`): Expected X coordinate.
- `y` (`int`): Expected Y coordinate.

**Example**:

```python
expect(element).to_have_location(100, 200)
```

---

### `to_have_location_x(x)`

Asserts that `element.location["x"]` equals `x`.

**Selenium API**: `element.location["x"]`

**Parameters**:

- `x` (`int`): Expected X coordinate.

**Example**:

```python
expect(element).to_have_location_x(100)
```

---

### `to_have_location_y(y)`

Asserts that `element.location["y"]` equals `y`.

**Selenium API**: `element.location["y"]`

**Parameters**:

- `y` (`int`): Expected Y coordinate.

**Example**:

```python
expect(element).to_have_location_y(200)
```

---

### `to_have_size(width, height)`

Asserts that `element.size` matches `{"width": width, "height": height}`.

**Selenium API**: `element.size`

**Parameters**:

- `width` (`int`): Expected width.
- `height` (`int`): Expected height.

**Example**:

```python
expect(element).to_have_size(300, 50)
```

---

### `to_have_size_width(width)`

Asserts that `element.size["width"]` equals `width`.

**Selenium API**: `element.size["width"]`

**Parameters**:

- `width` (`int`): Expected width.

**Example**:

```python
expect(element).to_have_size_width(300)
```

---

### `to_have_size_height(height)`

Asserts that `element.size["height"]` equals `height`.

**Selenium API**: `element.size["height"]`

**Parameters**:

- `height` (`int`): Expected height.

**Example**:

```python
expect(element).to_have_size_height(50)
```

---

### `to_have_rect(x, y, width, height)`

Asserts that `element.rect` matches all four values.

**Selenium API**: `element.rect`

**Parameters**:

- `x` (`int`): Expected X coordinate.
- `y` (`int`): Expected Y coordinate.
- `width` (`int`): Expected width.
- `height` (`int`): Expected height.

**Example**:

```python
expect(element).to_have_rect(100, 200, 300, 50)
```

---

### `to_have_location_greater_than(x=None, y=None)`

Asserts that `element.location` x and/or y are greater than the given values.

**Selenium API**: `element.location > (x, y)`

**Parameters**:

- `x` (`int | None`): Minimum X (exclusive). At least one of `x`/`y` required.
- `y` (`int | None`): Minimum Y (exclusive).

**Example**:

```python
expect(element).to_have_location_greater_than(x=50)
```

---

### `to_have_location_less_than(x=None, y=None)`

Asserts that `element.location` x and/or y are less than the given values.

**Selenium API**: `element.location < (x, y)`

**Parameters**:

- `x` (`int | None`): Maximum X (exclusive). At least one of `x`/`y` required.
- `y` (`int | None`): Maximum Y (exclusive).

**Example**:

```python
expect(element).to_have_location_less_than(y=500)
```

---

### `to_have_size_greater_than(width=None, height=None)`

Asserts that `element.size` width and/or height are greater than the given values.

**Selenium API**: `element.size > (width, height)`

**Parameters**:

- `width` (`int | None`): Minimum width (exclusive). At least one required.
- `height` (`int | None`): Minimum height (exclusive).

**Example**:

```python
expect(element).to_have_size_greater_than(width=100)
```

---

### `to_have_size_less_than(width=None, height=None)`

Asserts that `element.size` width and/or height are less than the given values.

**Selenium API**: `element.size < (width, height)`

**Parameters**:

- `width` (`int | None`): Maximum width (exclusive). At least one required.
- `height` (`int | None`): Maximum height (exclusive).

**Example**:

```python
expect(element).to_have_size_less_than(height=200)
```

---

### `to_have_location_once_scrolled_into_view(x, y)`

Asserts that `element.location_once_scrolled_into_view` matches `{"x": x, "y": y}`.

**Selenium API**: `element.location` after scroll

**Parameters**:

- `x` (`int`): Expected X coordinate after scroll.
- `y` (`int`): Expected Y coordinate after scroll.

**Example**:

```python
expect(element).to_have_location_once_scrolled_into_view(0, 0)
```

## Accessibility (Selenium 4+)

### `to_have_aria_role(role)`

Asserts that `element.aria_role` equals `role`.

**Selenium API**: `element.aria_role`

**Parameters**:

- `role` (`str`): Expected ARIA role.

**Example**:

```python
expect(element).to_have_aria_role("button")
```

---

### `to_have_aria_role_contains(role)`

Asserts that `role` is a substring of `element.aria_role`.

**Selenium API**: `role in element.aria_role`

**Parameters**:

- `role` (`str`): Expected substring.

**Example**:

```python
expect(element).to_have_aria_role_contains("button")
```

---

### `to_have_aria_role_in_list(*roles)`

Asserts that `element.aria_role` is one of `*roles`.

**Selenium API**: `element.aria_role in roles`

**Parameters**:

- `*roles` (`str`): Acceptable ARIA roles.

**Example**:

```python
expect(element).to_have_aria_role_in_list("button", "link")
```

---

### `to_have_accessible_name(name)`

Asserts that `element.accessible_name` equals `name`.

**Selenium API**: `element.accessible_name`

**Parameters**:

- `name` (`str`): Expected accessible name.

**Example**:

```python
expect(element).to_have_accessible_name("Submit form")
```

---

### `to_have_accessible_name_contains(name)`

Asserts that `name` is a substring of `element.accessible_name`.

**Selenium API**: `name in element.accessible_name`

**Parameters**:

- `name` (`str`): Expected substring.

**Example**:

```python
expect(element).to_have_accessible_name_contains("Submit")
```

## Shadow DOM (element-level)

### `to_have_js_property(name, value)`

Asserts that a JavaScript property on the element equals `value`.

**Selenium API**: `element.get_property(name)` via JS

**Parameters**:

- `name` (`str`): JavaScript property name.
- `value` (`Any`): Expected value.

**Example**:

```python
expect(element).to_have_js_property("indeterminate", False)
```

---

### `to_have_shadow_root()`

Asserts that `element.shadow_root` is not `None`.

**Selenium API**: `element.shadow_root is not None`

**Example**:

```python
expect(element).to_have_shadow_root()
```

---

### `to_have_shadow_root_absent()`

Asserts that `element.shadow_root` is `None`.

**Selenium API**: `element.shadow_root is None`

**Example**:

```python
expect(element).to_have_shadow_root_absent()
```
