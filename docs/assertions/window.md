# Window assertions

Window assertions are available via `expect(driver)` (inherited by `ExpectDriver`). They operate on `driver.get_window_position()`, `driver.get_window_size()`, and `driver.get_window_rect()`.

## Position

### `to_have_position(x, y)`

Asserts that the window position matches `(x, y)`.

**Selenium API**: `driver.get_window_position()`

**Parameters**:

- `x` (`int`): Expected X coordinate.
- `y` (`int`): Expected Y coordinate.

**Example**:

```python
expect(driver).to_have_position(0, 0)
```

**Negation**:

```python
expect(driver).not_.to_have_position(100, 100)
```

## Size

### `to_have_size(width, height)`

Asserts that the window size matches `(width, height)`.

**Selenium API**: `driver.get_window_size()`

**Parameters**:

- `width` (`int`): Expected width in pixels.
- `height` (`int`): Expected height in pixels.

**Example**:

```python
expect(driver).to_have_size(1280, 800)
```

## Rect

### `to_have_rect(x, y, width, height)`

Asserts that the window rect matches all four values.

**Selenium API**: `driver.get_window_rect()`

**Parameters**:

- `x` (`int`): Expected X coordinate.
- `y` (`int`): Expected Y coordinate.
- `width` (`int`): Expected width.
- `height` (`int`): Expected height.

**Example**:

```python
expect(driver).to_have_rect(0, 0, 1280, 800)
```
